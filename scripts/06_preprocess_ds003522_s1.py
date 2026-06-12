#!/usr/bin/env python
"""
06_preprocess_ds003522_s1.py
============================
Phase 3, Task 1: boundary-aware, standardized preprocessing of ds003522 Session-1 EEG
for the 25 eligible mTBI subjects. Raw files in data/raw/ are NEVER modified; cleaned
data are written as new FIF files in data/processed/ds003522_s1/.

Pipeline (parameters frozen in scripts/_eeg_common.py; identical for every subject;
no outcome is consulted):
    1. read raw EEGLAB (.set/.fdt); preload
    2. type non-EEG channels (VEOG -> eog, EKG -> ecg)
    3. boundary handling: EEGLAB 'boundary' events -> 'BAD_boundary' annotations;
       detect any *internal* boundary (onset > 1 s) and filter each contiguous
       segment independently so the filter never runs across a discontinuity
    4. notch at line frequency (60 Hz; mostly redundant under the 45 Hz low-pass)
    5. band-pass 0.5-45 Hz (broadband; serves spectral analysis)
    6. re-add the online reference CPz, set standard_1020 montage, average reference
    7. within-subject bad-channel detection (robust z of log-variance) + interpolation
       -- uses only this subject's S1 data, so it is leakage-safe
    8. save *_proc_raw.fif + a per-subject JSON log

This script does NOT epoch, extract features, or look at outcomes.
"""
from __future__ import annotations

import json
import warnings
from datetime import datetime, timezone

import numpy as np

from _eeg_common import (BAD_CHAN_Z, HP_HZ, LINE_FREQ, LP_BROADBAND_HZ, LOG_DIR,
                         MONTAGE, NON_EEG, ONLINE_REF, PROC_DIR, RAW_DIR, REFERENCE)


def find_set_files() -> list:
    return sorted(RAW_DIR.glob("sub-*/ses-01/eeg/*_task-ThreeStimAuditoryOddball_eeg.set"))


def boundary_onsets(raw) -> list[float]:
    return [float(o) for o, d in zip(raw.annotations.onset, raw.annotations.description)
            if "boundary" in str(d).lower()]


def filter_boundary_aware(raw, log: dict):
    """Band-pass + notch. If an internal boundary exists, filter each segment separately."""
    import mne
    onsets = sorted(boundary_onsets(raw))
    internal = [o for o in onsets if o > 1.0]
    log["boundary_onsets_s"] = [round(o, 2) for o in onsets]
    log["internal_boundaries"] = [round(o, 2) for o in internal]
    picks = mne.pick_types(raw.info, eeg=True, eog=True, ecg=True)

    def _filt(r):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            r.notch_filter(LINE_FREQ, picks=picks, verbose="ERROR")
            r.filter(HP_HZ, LP_BROADBAND_HZ, picks=picks,
                     fir_design="firwin", verbose="ERROR")
        return r

    if not internal:
        log["filter_strategy"] = "single segment (only boundary at recording start)"
        return _filt(raw)

    # split at internal boundaries, filter each crop, then concatenate
    log["filter_strategy"] = f"segment-wise across {len(internal)} internal boundary(ies)"
    edges = [0.0] + internal + [raw.times[-1] + 1.0 / raw.info["sfreq"]]
    segs = []
    for a, b in zip(edges[:-1], edges[1:]):
        seg = raw.copy().crop(tmin=a, tmax=min(b, raw.times[-1]), include_tmax=False)
        segs.append(_filt(seg))
    out = segs[0]
    if len(segs) > 1:
        out.append(segs[1:])
    return out


def detect_bad_channels(raw, log: dict) -> list[str]:
    """Robust within-subject bad-channel flag. The just re-added online reference
    (CPz, legitimately all-zeros under its own reference) is excluded so it is not
    mistaken for a flat/bad channel; it must remain in the average-reference set."""
    import mne
    eeg = mne.pick_types(raw.info, eeg=True)
    names = [raw.ch_names[i] for i in eeg]
    keep = [i for i, nm in enumerate(names) if nm != ONLINE_REF]
    data = raw.get_data(picks=[eeg[i] for i in keep])
    var = np.var(data, axis=1)
    logv = np.log(var + 1e-30)
    med, mad = np.median(logv), np.median(np.abs(logv - np.median(logv))) + 1e-30
    z = 0.6745 * (logv - med) / mad
    kept_names = [names[i] for i in keep]
    bads = [kept_names[j] for j in range(len(kept_names))
            if abs(z[j]) > BAD_CHAN_Z or var[j] < 1e-20]
    log["bad_channels"] = bads
    log["n_bad_channels"] = len(bads)
    return bads


def preprocess_one(set_path) -> dict:
    import mne
    sub = set_path.name.split("_")[0]
    log = {"subject": sub, "raw_file": str(set_path.relative_to(set_path.parents[4])),
           "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "params": {"hp_hz": HP_HZ, "lp_hz": LP_BROADBAND_HZ, "notch_hz": LINE_FREQ,
                      "montage": MONTAGE, "reference": REFERENCE,
                      "bad_chan_z": BAD_CHAN_Z}}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        raw = mne.io.read_raw_eeglab(set_path, preload=True, verbose="ERROR")
    log["sfreq"] = raw.info["sfreq"]
    log["n_channels_raw"] = len(raw.ch_names)
    log["duration_s"] = round(raw.n_times / raw.info["sfreq"], 1)

    # 2. channel types
    type_map = {ch: t for ch, t in NON_EEG.items() if ch in raw.ch_names}
    if type_map:
        raw.set_channel_types(type_map)
    log["non_eeg_channels"] = type_map

    # 3-4-5. boundary-aware filtering (+ notch)
    raw = filter_boundary_aware(raw, log)
    # rename boundary annotations so epoching/segmentation treats them as BAD
    if len(raw.annotations):
        newdesc = ["BAD_boundary" if "boundary" in str(d).lower() else d
                   for d in raw.annotations.description]
        raw.annotations.description = np.array(newdesc)

    # 6. re-add online reference, montage, average reference
    if ONLINE_REF not in raw.ch_names:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            raw = mne.add_reference_channels(raw, ONLINE_REF)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        raw.set_montage(MONTAGE, match_case=False, on_missing="warn", verbose="ERROR")
    log["n_eeg_channels"] = len(mne.pick_types(raw.info, eeg=True))

    # 7. within-subject bad-channel detection -> average reference (bads excluded
    #    from the average by MNE) -> interpolate the flagged channels
    bads = detect_bad_channels(raw, log)
    raw.info["bads"] = bads
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        raw.set_eeg_reference(REFERENCE, projection=False, verbose="ERROR")
        if bads:
            raw.interpolate_bads(reset_bads=True, verbose="ERROR")

    # 8. save
    PROC_DIR.mkdir(parents=True, exist_ok=True)
    out = PROC_DIR / f"{sub}_ses-01_proc_raw.fif"
    raw.save(out, overwrite=True, verbose="ERROR")
    log["processed_file"] = str(out.relative_to(PROC_DIR.parents[2]))
    log["status"] = "OK"
    return log


def main() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    files = find_set_files()
    print(f"Preprocessing {len(files)} Session-1 recordings -> {PROC_DIR}\n")
    logs = []
    for f in files:
        try:
            log = preprocess_one(f)
            print(f"  {log['subject']}: OK  bads={log['n_bad_channels']} "
                  f"{log['bad_channels'] if log['bad_channels'] else ''}  "
                  f"filt={log['filter_strategy']}")
        except Exception as e:
            log = {"subject": f.name.split("_")[0], "status": "FAILED",
                   "error": f"{type(e).__name__}: {e}"[:300]}
            print(f"  {log['subject']}: FAILED {log['error']}")
        with open(LOG_DIR / f"{log['subject']}_preproc_log.json", "w") as fh:
            json.dump(log, fh, indent=2)
        logs.append(log)

    ok = [l for l in logs if l.get("status") == "OK"]
    with open(LOG_DIR / "_preproc_summary.json", "w") as fh:
        json.dump(logs, fh, indent=2)
    print(f"\nDone: {len(ok)}/{len(files)} preprocessed. Logs in {LOG_DIR}")
    if ok:
        nb = [l["n_bad_channels"] for l in ok]
        print(f"bad channels per subject: min={min(nb)} median={int(np.median(nb))} max={max(nb)}")
        anyint = [l['subject'] for l in ok if l.get('internal_boundaries')]
        print(f"subjects with internal boundaries (segment-wise filtered): {anyint or 'none'}")


if __name__ == "__main__":
    main()
