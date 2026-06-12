#!/usr/bin/env python
"""
08_extract_oddball_erp_features_ds003522.py
===========================================
Phase 3, Task 3: extract pre-registered auditory-oddball ERP features from Session-1.

Events are taken from the BIDS-curated `trial_type` labels (Standard / Target / Novel
Tone). Epochs are built boundary-aware (`reject_by_annotation=True` skips BAD_boundary),
baseline-corrected, and gross-artifact epochs (peak-to-peak > 150 uV on EEG) are dropped.
An extra 40-Hz low-pass is applied for the ERP branch.

Pre-registered components (windows fixed a priori in _eeg_common.py; no outcome used):
    P3a : Novel tones, frontocentral (Fz/FCz/Cz), 250-400 ms  -> peak(+) amp, latency, mean
    P3b : Target tones, parietal (Pz/CPz/POz), 300-600 ms     -> peak(+) amp, latency, mean
    N2  : Target & Novel, frontocentral, 200-350 ms           -> peak(-) amp, latency, mean
    Target-minus-Standard difference wave at parietal (clean P3b)
Plus retained / rejected epoch counts per condition.

Subjects whose recording lacks the named tone labels (e.g. sub-040, tones stored only as
raw S-codes) yield NaN ERP features and are flagged -- not silently dropped, and not
recovered by guessing the non-standard code mapping.

Output: outputs/features/ds003522_s1_erp_features.csv
"""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd

from _eeg_common import (ERP_BASELINE, ERP_CONDITIONS, ERP_PICKS, ERP_REJECT_UV,
                         ERP_TMAX, ERP_TMIN, ERP_WINDOWS, FEAT_DIR, LP_ERP_HZ,
                         PROC_DIR, RAW_DIR)

warnings.simplefilter("ignore")


def build_events(events_tsv: pd.DataFrame, sfreq: float):
    """MNE events array + id dict from trial_type onsets (no cropping -> sample=onset*sf)."""
    ev_id, rows = {}, []
    for i, (cond, label) in enumerate(ERP_CONDITIONS.items(), start=1):
        ev_id[cond] = i
        sub = events_tsv[events_tsv.trial_type == label]
        for onset in sub.onset.to_numpy():
            rows.append([int(round(onset * sfreq)), 0, i])
    if not rows:
        return np.empty((0, 3), int), ev_id
    arr = np.array(sorted(rows, key=lambda r: r[0]), dtype=int)
    return arr, ev_id


def roi_wave(evoked, picks):
    avail = [p for p in picks if p in evoked.ch_names]
    if not avail:
        return None, None
    data = evoked.get_data(picks=avail).mean(axis=0) * 1e6   # uV
    return data, evoked.times


def measure(wave, times, window, polarity):
    if wave is None:
        return np.nan, np.nan, np.nan
    m = (times >= window[0]) & (times <= window[1])
    seg, tt = wave[m], times[m]
    mean_amp = float(np.mean(seg))
    k = int(np.argmax(seg)) if polarity == "pos" else int(np.argmin(seg))
    return round(float(seg[k]), 3), round(float(tt[k] * 1000), 1), round(mean_amp, 3)


def erp_for_subject(fif, events_tsv) -> dict:
    import mne
    sub = fif.name.split("_")[0]
    raw = mne.io.read_raw_fif(fif, preload=True, verbose="ERROR")
    raw.filter(None, LP_ERP_HZ, picks="eeg", fir_design="firwin", verbose="ERROR")
    events, ev_id = build_events(events_tsv, raw.info["sfreq"])
    row = {"subject": sub}

    present = {c: int((events[:, 2] == i).sum()) for c, i in ev_id.items()}
    row.update({f"erp_n_{c}_marked": n for c, n in present.items()})
    if sum(present.values()) == 0 or present.get("target", 0) == 0:
        row["erp_status"] = "NO_NAMED_TONE_EVENTS"
        return row

    epochs = mne.Epochs(raw, events, ev_id, tmin=ERP_TMIN, tmax=ERP_TMAX,
                        baseline=ERP_BASELINE, picks="eeg",
                        reject={"eeg": ERP_REJECT_UV * 1e-6},
                        reject_by_annotation=True, preload=True, verbose="ERROR")
    for c in ev_id:
        n_ok = len(epochs[c]) if c in epochs.event_id else 0
        row[f"erp_n_{c}_kept"] = n_ok
        row[f"erp_n_{c}_rejected"] = present[c] - n_ok
    row["erp_status"] = "OK"

    ev = {c: (epochs[c].average() if (c in epochs.event_id and len(epochs[c]) > 0) else None)
          for c in ev_id}

    # P3a (Novel, frontocentral)
    if ev["novel"] is not None:
        w, t = roi_wave(ev["novel"], ERP_PICKS["P3a"])
        a, lat, mn = measure(w, t, ERP_WINDOWS["P3a"], "pos")
        row.update({"erp_P3a_novel_fc_peak_uv": a, "erp_P3a_novel_fc_lat_ms": lat,
                    "erp_P3a_novel_fc_mean_uv": mn})
        w, t = roi_wave(ev["novel"], ERP_PICKS["N2"])
        a, lat, mn = measure(w, t, ERP_WINDOWS["N2"], "neg")
        row.update({"erp_N2_novel_fc_peak_uv": a, "erp_N2_novel_fc_lat_ms": lat,
                    "erp_N2_novel_fc_mean_uv": mn})
    # P3b (Target, parietal) + N2 (Target, frontocentral)
    if ev["target"] is not None:
        w, t = roi_wave(ev["target"], ERP_PICKS["P3b"])
        a, lat, mn = measure(w, t, ERP_WINDOWS["P3b"], "pos")
        row.update({"erp_P3b_target_par_peak_uv": a, "erp_P3b_target_par_lat_ms": lat,
                    "erp_P3b_target_par_mean_uv": mn})
        w, t = roi_wave(ev["target"], ERP_PICKS["N2"])
        a, lat, mn = measure(w, t, ERP_WINDOWS["N2"], "neg")
        row.update({"erp_N2_target_fc_peak_uv": a, "erp_N2_target_fc_lat_ms": lat,
                    "erp_N2_target_fc_mean_uv": mn})
    # Target-minus-Standard difference wave at parietal (clean P3b)
    if ev["target"] is not None and ev["standard"] is not None:
        wt, t = roi_wave(ev["target"], ERP_PICKS["P3b"])
        ws, _ = roi_wave(ev["standard"], ERP_PICKS["P3b"])
        if wt is not None and ws is not None:
            a, lat, mn = measure(wt - ws, t, ERP_WINDOWS["P3b"], "pos")
            row.update({"erp_P3b_tMinusS_par_peak_uv": a, "erp_P3b_tMinusS_par_lat_ms": lat,
                        "erp_P3b_tMinusS_par_mean_uv": mn})
    return row


def main() -> None:
    FEAT_DIR.mkdir(parents=True, exist_ok=True)
    fifs = sorted(PROC_DIR.glob("sub-*_ses-01_proc_raw.fif"))
    rows = []
    print(f"ERP features for {len(fifs)} subjects\n")
    for fif in fifs:
        sub = fif.name.split("_")[0]
        ev_path = next((RAW_DIR / sub / "ses-01" / "eeg").glob("*_events.tsv"))
        events_tsv = pd.read_csv(ev_path, sep="\t")
        row = erp_for_subject(fif, events_tsv)
        rows.append(row)
        if row.get("erp_status") == "OK":
            print(f"  {sub}: OK  kept S/T/N = "
                  f"{row.get('erp_n_standard_kept')}/{row.get('erp_n_target_kept')}/"
                  f"{row.get('erp_n_novel_kept')}  "
                  f"P3b={row.get('erp_P3b_target_par_mean_uv')}uV "
                  f"P3a={row.get('erp_P3a_novel_fc_mean_uv')}uV")
        else:
            print(f"  {sub}: {row.get('erp_status')} (excluded from ERP)")
    df = pd.DataFrame(rows)
    out = FEAT_DIR / "ds003522_s1_erp_features.csv"
    df.to_csv(out, index=False)
    n_ok = int((df.get("erp_status") == "OK").sum())
    print(f"\nWrote {out}  ({df.shape[0]} subjects, {n_ok} with usable ERPs, "
          f"{df.shape[1]-1} columns)")


if __name__ == "__main__":
    main()
