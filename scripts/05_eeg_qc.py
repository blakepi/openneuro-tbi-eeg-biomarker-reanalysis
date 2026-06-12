#!/usr/bin/env python
"""
05_eeg_qc.py
============
Phase 2, Task 3: minimal, read-only EEG quality control on Session-1 files.

This computes ONLY descriptive quality metrics needed to judge feasibility and to plan
Phase-3 preprocessing. It deliberately does NOT:
    * filter, re-reference, epoch, or run ICA,
    * compute spectral / ERP / aperiodic biomarker features,
    * look at the outcome in relation to any EEG quantity (the only outcome-adjacent
      reporting is whether QC *failure / missingness* differs by group, descriptively).

QC metrics per recording (continuous raw, as stored):
    readable                 file opens in MNE without error
    sfreq                    sampling frequency (Hz)
    n_channels               channel count (and EEG-type count)
    duration_s               recording length (s)
    n_bad_channels           channels marked bad in the file / channels.tsv 'status'
    amp_p2p_median_uV        median peak-to-peak amplitude across channels (gross range)
    amp_max_abs_uV           max abs amplitude (gross outlier indicator)
    pct_flat_channels        % channels with ~zero variance (flat)
    pct_zero_samples         % of samples exactly 0 across the data matrix
    pct_nan_samples          % of NaN samples

Input : data/raw/ds003522/sub-XXX/ses-01/eeg/*_eeg.set (+ .fdt), channels.tsv
        eligibility & folds from outputs/splits/frozen_cv_folds.csv
Output: outputs/qc/<dsid>_s1_qc_summary.csv  (one row per recording)
"""
from __future__ import annotations

import argparse
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW = PROJECT_ROOT / "data" / "raw"
MANIFEST_DIR = PROJECT_ROOT / "outputs" / "eeg_manifests"
QC_DIR = PROJECT_ROOT / "outputs" / "qc"
QC_DIR.mkdir(parents=True, exist_ok=True)

# QC thresholds (descriptive flags only -- NOT applied as exclusions here)
FLAT_VAR_UV2 = 1e-2        # channel variance below this (uV^2) treated as flat
FLAT_PCT_FAIL = 20.0       # >this % flat channels -> quality concern flag
AMP_EXTREME_UV = 5000.0    # max abs amplitude above this -> gross-artifact flag


def channels_tsv_bads(set_path: Path) -> tuple[int, int]:
    """Return (n_channels_in_tsv, n_bad) from the BIDS channels.tsv 'status' column."""
    tsv = Path(str(set_path).replace("_eeg.set", "_channels.tsv"))
    if not tsv.exists():
        return (0, 0)
    df = pd.read_csv(tsv, sep="\t")
    n = len(df)
    if "status" in df.columns:
        nbad = int((df["status"].astype(str).str.lower() == "bad").sum())
    else:
        nbad = 0
    return (n, nbad)


def qc_one(set_path: Path) -> dict:
    import mne
    row: dict = {"local_path": str(set_path.relative_to(PROJECT_ROOT))}
    n_tsv, n_bad_tsv = channels_tsv_bads(set_path)
    row["n_channels_tsv"] = n_tsv
    row["n_bad_channels_tsv"] = n_bad_tsv
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            raw = mne.io.read_raw_eeglab(set_path, preload=True, verbose="ERROR")
    except Exception as e:
        row["readable"] = False
        row["error"] = f"{type(e).__name__}: {e}"[:300]
        return row

    row["readable"] = True
    row["sfreq"] = float(raw.info["sfreq"])
    row["n_channels"] = len(raw.ch_names)
    row["n_eeg_channels"] = len(mne.pick_types(raw.info, eeg=True, meg=False))
    row["duration_s"] = round(raw.n_times / raw.info["sfreq"], 1)
    row["n_bad_channels_info"] = len(raw.info["bads"])

    data = raw.get_data()                       # (n_ch, n_times), volts
    data_uv = data * 1e6
    # gross amplitude
    p2p = np.ptp(data_uv, axis=1)
    row["amp_p2p_median_uV"] = round(float(np.median(p2p)), 1)
    row["amp_max_abs_uV"] = round(float(np.nanmax(np.abs(data_uv))), 1)
    # flat channels (near-zero variance)
    var = np.nanvar(data_uv, axis=1)
    n_flat = int((var < FLAT_VAR_UV2).sum())
    row["n_flat_channels"] = n_flat
    row["pct_flat_channels"] = round(100.0 * n_flat / data_uv.shape[0], 1)
    # zero / nan samples
    total = data_uv.size
    row["pct_zero_samples"] = round(100.0 * int((data == 0).sum()) / total, 3)
    row["pct_nan_samples"] = round(100.0 * int(np.isnan(data).sum()) / total, 3)

    # descriptive quality flags (not exclusions)
    flags = []
    if row["pct_flat_channels"] > FLAT_PCT_FAIL:
        flags.append("MANY_FLAT")
    if row["amp_max_abs_uV"] > AMP_EXTREME_UV:
        flags.append("EXTREME_AMP")
    if row["pct_nan_samples"] > 0:
        flags.append("HAS_NAN")
    row["quality_flags"] = ";".join(flags)
    return row


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="ds003522")
    args = ap.parse_args()
    dsid = args.dataset

    man = pd.read_csv(MANIFEST_DIR / f"{dsid}_s1_manifest.csv")
    sets = man[man["suffix"] == "eeg.set"].copy()

    rows = []
    print(f"QC on {len(sets)} Session-1 recordings ({dsid})\n")
    for _, m in sets.iterrows():
        set_path = PROJECT_ROOT / m["local_path"]
        meta = {"dataset": dsid, "bids_subject_id": m["bids_subject_id"],
                "subject_uid": m["subject_uid"], "Original_ID": m["Original_ID"],
                "fold": m["fold"], "task": m["task"]}
        if not set_path.exists():
            rows.append({**meta, "readable": False, "error": "LOCAL_FILE_MISSING",
                         "local_path": m["local_path"]})
            print(f"  {m['bids_subject_id']}: MISSING local file")
            continue
        r = qc_one(set_path)
        rows.append({**meta, **r})
        tag = "OK" if r.get("readable") else "UNREADABLE"
        extra = f" sf={r.get('sfreq')} nch={r.get('n_channels')} dur={r.get('duration_s')}s flags={r.get('quality_flags','')}"
        print(f"  {m['bids_subject_id']}: {tag}{extra if r.get('readable') else ' '+r.get('error','')}")

    qc = pd.DataFrame(rows)
    out = QC_DIR / f"{dsid}_s1_qc_summary.csv"
    qc.to_csv(out, index=False)
    print(f"\nQC summary -> {out}  ({len(qc)} recordings)")

    # high-level summary
    n = len(qc)
    n_read = int(qc.get("readable", pd.Series(dtype=bool)).fillna(False).sum())
    print(f"readable: {n_read}/{n}")
    if "sfreq" in qc:
        print("sfreq values:", qc["sfreq"].dropna().value_counts().to_dict())
        print("n_channels values:", qc["n_channels"].dropna().value_counts().to_dict())
        print(f"duration_s: median={qc['duration_s'].median()} "
              f"min={qc['duration_s'].min()} max={qc['duration_s'].max()}")
        flagged = qc[qc["quality_flags"].fillna("") != ""]
        print(f"recordings with quality flags: {len(flagged)}")
        if len(flagged):
            print(flagged[["bids_subject_id", "quality_flags"]].to_string(index=False))


if __name__ == "__main__":
    main()
