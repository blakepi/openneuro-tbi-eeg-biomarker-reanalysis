#!/usr/bin/env python
"""
07_extract_rest_features_ds003522.py
====================================
Phase 3, Task 2: extract pre-registered resting-state spectral features from the
Eyes-Closed (EC) and Eyes-Open (EO) blocks embedded in each Session-1 recording.

Segmentation
------------
Rest is NOT a separate file. It is marked by 1-Hz pulse trains labelled
"Eyes Closed: Every 1000 ms" / "Eyes Open: Every 1000 ms" in events.tsv (two blocks of
each per recording, ~60 s each -> ~120 s/condition). A block = a contiguous run of that
label (gap > 3 s starts a new block). Block span = [first marker, last marker + 1 s].
Blocks overlapping a BAD_boundary annotation are skipped (boundary-aware).

Within each block the continuous signal is cut into non-overlapping 2-s segments;
segments with peak-to-peak > 150 uV on any EEG channel are rejected. PSD (Welch, 2-s
windows) is computed on the retained data per channel, then aggregated to regions.

Features (per condition EC/EO, per region frontal/central/parietal/occipital/global):
    absolute + relative band power (delta/theta/alpha/beta), theta/alpha ratio,
    spectral entropy, aperiodic exponent/offset/r2 (specparam, 1-40 Hz fit).
Plus per condition: individual alpha peak frequency (posterior).
Plus QC: usable seconds, segments kept/total, n blocks per condition.

NO outcome is read; thresholds are fixed a priori (no outcome-driven tuning).
Output: outputs/features/ds003522_s1_rest_features.csv
"""
from __future__ import annotations

import warnings
from pathlib import Path

import numpy as np
import pandas as pd

from _eeg_common import (BANDS, FEAT_DIR, IAF_BAND, PROC_DIR, RAW_DIR, REGIONS,
                         REST_GAP_S, REST_LABELS, REST_REJECT_UV, REST_SEG_S,
                         TOTAL_BAND, WELCH_OVERLAP, WELCH_WIN_S, region_of)

warnings.simplefilter("ignore")


def rest_blocks(events: pd.DataFrame, label: str) -> list[tuple[float, float]]:
    e = events[events.trial_type == label].sort_values("onset")
    if e.empty:
        return []
    onsets = e.onset.to_numpy()
    splits = np.where(np.diff(onsets) > REST_GAP_S)[0]
    groups = np.split(np.arange(len(onsets)), splits + 1)
    return [(float(onsets[g[0]]), float(onsets[g[-1]] + 1.0)) for g in groups]


def bad_spans(raw) -> list[tuple[float, float]]:
    out = []
    for o, d, dur in zip(raw.annotations.onset, raw.annotations.description,
                         raw.annotations.duration):
        if str(d).startswith("BAD"):
            out.append((float(o), float(o + max(dur, 0.0))))
    return out


def overlaps_bad(a: float, b: float, spans) -> bool:
    return any(not (b <= s or a >= e) for s, e in spans)


def collect_clean_segments(raw, blocks, eeg_names) -> tuple[np.ndarray | None, dict]:
    """Return (data [n_ch, n_samp] of concatenated clean 2-s segments, qc dict)."""
    sf = raw.info["sfreq"]
    seg_n = int(REST_SEG_S * sf)
    spans = bad_spans(raw)
    picks = [raw.ch_names.index(c) for c in eeg_names]
    kept, n_total, n_kept = [], 0, 0
    used_blocks = 0
    for (a, b) in blocks:
        if overlaps_bad(a, b, spans):
            continue
        used_blocks += 1
        seg = raw.copy().crop(tmin=max(a, 0), tmax=min(b, raw.times[-1]), include_tmax=False)
        d = seg.get_data(picks=picks)        # volts
        nseg = d.shape[1] // seg_n
        for k in range(nseg):
            n_total += 1
            chunk = d[:, k * seg_n:(k + 1) * seg_n]
            p2p = np.ptp(chunk * 1e6, axis=1)         # uV
            if np.max(p2p) <= REST_REJECT_UV:
                kept.append(chunk)
                n_kept += 1
    qc = {"n_blocks_used": used_blocks, "n_seg_total": n_total, "n_seg_kept": n_kept,
          "usable_s": round(n_kept * REST_SEG_S, 1)}
    if not kept:
        return None, qc
    return np.concatenate(kept, axis=1), qc


def welch_psd(data: np.ndarray, sf: float):
    from mne.time_frequency import psd_array_welch
    n_per = int(WELCH_WIN_S * sf)
    n_ov = int(n_per * WELCH_OVERLAP)
    psd, freqs = psd_array_welch(data, sf, fmin=1.0, fmax=45.0, n_fft=n_per,
                                 n_per_seg=n_per, n_overlap=n_ov, verbose="ERROR")
    return psd * 1e12, freqs        # V^2/Hz -> uV^2/Hz


def band_power(psd_1d, freqs, lo, hi):
    m = (freqs >= lo) & (freqs <= hi)
    return float(np.trapezoid(psd_1d[m], freqs[m]))


def spectral_entropy(psd_1d, freqs):
    m = (freqs >= TOTAL_BAND[0]) & (freqs <= TOTAL_BAND[1])
    p = psd_1d[m]
    p = p / (p.sum() + 1e-30)
    return float(-np.sum(p * np.log(p + 1e-30)) / np.log(len(p)))


def aperiodic(psd_1d, freqs):
    try:
        from specparam import SpectralModel
        sm = SpectralModel(peak_width_limits=(1, 8), max_n_peaks=6,
                           aperiodic_mode="fixed", verbose=False)
        sm.fit(freqs, psd_1d, [1, 40])
        offset, exponent = sm.get_params("aperiodic")
        r2 = float(sm.results.get_metrics("gof"))
        return float(offset), float(exponent), r2
    except Exception:
        return np.nan, np.nan, np.nan


def iaf_posterior(psd_by_ch, freqs, eeg_names):
    post = REGIONS["parietal"] + REGIONS["occipital"]
    idx = [i for i, c in enumerate(eeg_names) if c in post]
    if not idx:
        return np.nan
    mean_psd = psd_by_ch[idx].mean(axis=0)
    m = (freqs >= IAF_BAND[0]) & (freqs <= IAF_BAND[1])
    fb, pb = freqs[m], mean_psd[m]
    if len(pb) < 3:
        return np.nan
    k = int(np.argmax(pb))
    if k == 0 or k == len(pb) - 1:       # peak at edge -> not a clear alpha peak
        return np.nan
    return round(float(fb[k]), 2)


def region_indices(eeg_names):
    ridx = {r: [i for i, c in enumerate(eeg_names) if region_of(c) == r]
            for r in REGIONS}
    ridx["global"] = list(range(len(eeg_names)))
    return ridx


def features_for_condition(raw, blocks, eeg_names, cond) -> dict:
    feat = {}
    data, qc = collect_clean_segments(raw, blocks, eeg_names)
    for k, v in qc.items():
        feat[f"rest_{cond}_{k}"] = v
    if data is None or data.shape[1] < int(WELCH_WIN_S * raw.info["sfreq"]):
        return feat                      # insufficient clean data -> features stay absent
    psd, freqs = welch_psd(data, raw.info["sfreq"])
    ridx = region_indices(eeg_names)
    feat[f"rest_{cond}_iaf_posterior_hz"] = iaf_posterior(psd, freqs, eeg_names)
    for region, idx in ridx.items():
        rpsd = psd[idx].mean(axis=0)
        total = band_power(rpsd, freqs, *TOTAL_BAND)
        powers = {}
        for band, (lo, hi) in BANDS.items():
            ap = band_power(rpsd, freqs, lo, hi)
            powers[band] = ap
            feat[f"rest_{cond}_{region}_{band}_abs"] = round(ap, 4)
            feat[f"rest_{cond}_{region}_{band}_rel"] = round(ap / (total + 1e-30), 5)
        feat[f"rest_{cond}_{region}_theta_alpha_ratio"] = round(
            powers["theta"] / (powers["alpha"] + 1e-30), 4)
        feat[f"rest_{cond}_{region}_spec_entropy"] = round(
            spectral_entropy(rpsd, freqs), 4)
        off, exp, r2 = aperiodic(rpsd, freqs)
        feat[f"rest_{cond}_{region}_aper_offset"] = round(off, 4) if off == off else np.nan
        feat[f"rest_{cond}_{region}_aper_exponent"] = round(exp, 4) if exp == exp else np.nan
        feat[f"rest_{cond}_{region}_aper_r2"] = round(r2, 4) if r2 == r2 else np.nan
    return feat


def main() -> None:
    import mne
    FEAT_DIR.mkdir(parents=True, exist_ok=True)
    fifs = sorted(PROC_DIR.glob("sub-*_ses-01_proc_raw.fif"))
    rows = []
    print(f"Rest features for {len(fifs)} subjects\n")
    for fif in fifs:
        sub = fif.name.split("_")[0]
        raw = mne.io.read_raw_fif(fif, preload=True, verbose="ERROR")
        eeg_names = [raw.ch_names[i] for i in mne.pick_types(raw.info, eeg=True)]
        ev_path = next((RAW_DIR / sub / "ses-01" / "eeg").glob("*_events.tsv"))
        events = pd.read_csv(ev_path, sep="\t")
        row = {"subject": sub}
        for cond, label in (("EC", REST_LABELS["eyes_closed"]),
                            ("EO", REST_LABELS["eyes_open"])):
            blocks = rest_blocks(events, label)
            row.update(features_for_condition(raw, blocks, eeg_names, cond))
        rows.append(row)
        print(f"  {sub}: EC usable={row.get('rest_EC_usable_s')}s "
              f"({row.get('rest_EC_n_seg_kept')}/{row.get('rest_EC_n_seg_total')} seg), "
              f"EO usable={row.get('rest_EO_usable_s')}s "
              f"({row.get('rest_EO_n_seg_kept')}/{row.get('rest_EO_n_seg_total')} seg), "
              f"IAF_EC={row.get('rest_EC_iaf_posterior_hz')}")
    df = pd.DataFrame(rows)
    out = FEAT_DIR / "ds003522_s1_rest_features.csv"
    df.to_csv(out, index=False)
    print(f"\nWrote {out}  ({df.shape[0]} subjects x {df.shape[1]-1} features)")


if __name__ == "__main__":
    main()
