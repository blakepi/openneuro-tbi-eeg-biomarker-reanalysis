#!/usr/bin/env python
"""
04_download_s1_eeg.py
=====================
Phase 2, Task 2: download / locate ONLY Session-1 EEG for eligible subjects.

Scope guard: this script touches Session-1 EEG only. Later sessions are never fetched,
so they cannot leak into a Session-1 predictor pipeline. Eligible subjects come from the
frozen folds (scripts/03_freeze_splits.py), i.e. acute mTBI with S1 EEG and an S3 outcome.

Modes
-----
--dry-run   metadata only: HEAD every remote file, write the manifest with remote sizes,
            download nothing.
(default)   stream the EEG files to data/raw/<dsid>/...; skip files already present with a
            matching byte size (resumable); verify downloaded size against the remote size.

Files fetched per subject (Session-1 'eeg' folder): the EEGLAB pair (.set + .fdt) needed
to read the signal, plus BIDS sidecars (channels.tsv, electrodes.tsv, *_eeg.json,
events.tsv/json, coordsystem.json). The authoritative remote file list is the cached S3
key listing (data/metadata_cache/<dsid>/_filelist.txt) produced in Phase 0.

Output: outputs/eeg_manifests/<dsid>_s1_manifest.csv  (one row per expected file)
"""
from __future__ import annotations

import argparse
import re
import shutil
import urllib.request
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CACHE = PROJECT_ROOT / "data" / "metadata_cache"
TABLES = PROJECT_ROOT / "outputs" / "metadata_summary_tables"
SPLITS = PROJECT_ROOT / "outputs" / "splits"
RAW = PROJECT_ROOT / "data" / "raw"
MANIFEST_DIR = PROJECT_ROOT / "outputs" / "eeg_manifests"
MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

S3_ROOT = "https://s3.amazonaws.com/openneuro.org"
SESSION = "ses-01"
COHORT_FOR_DATASET = {"ds003522": "A_ds003522",
                      "ds005114": "B_ds005114",
                      "ds003523": "C_ds003523"}


def remote_size(key: str) -> int | None:
    req = urllib.request.Request(f"{S3_ROOT}/{key}", method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return int(r.headers.get("Content-Length", 0))
    except Exception:
        return None


def download(key: str, dest: Path) -> int | None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    try:
        with urllib.request.urlopen(f"{S3_ROOT}/{key}", timeout=120) as r, open(tmp, "wb") as fh:
            shutil.copyfileobj(r, fh, length=1 << 20)
        tmp.replace(dest)
        return dest.stat().st_size
    except Exception:
        if tmp.exists():
            tmp.unlink()
        return None


def parse_task(filename: str) -> str:
    m = re.search(r"task-([A-Za-z0-9]+)", filename)
    return m.group(1) if m else ""


def parse_suffix(filename: str) -> str:
    # e.g. sub-001_ses-01_task-..._eeg.set -> 'eeg.set'
    parts = filename.split("_")
    return parts[-1] if parts else filename


def eligible_subjects(dsid: str) -> pd.DataFrame:
    folds = pd.read_csv(SPLITS / "frozen_cv_folds.csv")
    cohort = COHORT_FOR_DATASET[dsid]
    elig = folds[folds.cohort_id == cohort][["subject_uid", "Original_ID", "fold"]].copy()
    cw = pd.read_csv(TABLES / "crosswalk_subject_ids.csv")
    cw = cw[cw.dataset_id == dsid][["subject_uid", "bids_subject_id"]]
    return elig.merge(cw, on="subject_uid", how="left")


def remote_s1_eeg_keys(dsid: str, bids_subject_id: str) -> list[str]:
    fl = (CACHE / dsid / "_filelist.txt").read_text(encoding="utf-8").splitlines()
    pat = f"{dsid}/{bids_subject_id}/{SESSION}/eeg/"
    return [k for k in fl if k.startswith(pat)]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="ds003522", choices=list(COHORT_FOR_DATASET))
    ap.add_argument("--dry-run", action="store_true",
                    help="metadata only: HEAD remote files, download nothing")
    ap.add_argument("--limit", type=int, default=None, help="limit number of subjects (debug)")
    args = ap.parse_args()
    dsid = args.dataset

    subs = eligible_subjects(dsid)
    if args.limit:
        subs = subs.head(args.limit)
    print(f"{dsid}: {len(subs)} eligible S1 mTBI subjects "
          f"({'DRY-RUN' if args.dry_run else 'DOWNLOAD'} mode)\n")

    rows = []
    for _, s in subs.iterrows():
        sid = s["bids_subject_id"]
        if pd.isna(sid):
            rows.append({"dataset": dsid, "subject_uid": s["subject_uid"],
                         "bids_subject_id": None, "status": "NO_BIDS_SUBJECT", "session": SESSION})
            continue
        keys = remote_s1_eeg_keys(dsid, sid)
        if not keys:
            rows.append({"dataset": dsid, "subject_uid": s["subject_uid"], "bids_subject_id": sid,
                         "Original_ID": s["Original_ID"], "fold": s["fold"],
                         "session": SESSION, "status": "NO_REMOTE_S1_EEG"})
            continue
        for key in keys:
            fname = key.split("/")[-1]
            dest = RAW / key
            rsize = remote_size(key)
            row = {
                "dataset": dsid, "subject_uid": s["subject_uid"], "bids_subject_id": sid,
                "Original_ID": s["Original_ID"], "fold": s["fold"], "session": SESSION,
                "task": parse_task(fname), "suffix": parse_suffix(fname),
                "remote_key": key, "remote_size_bytes": rsize,
                "local_path": str(dest.relative_to(PROJECT_ROOT)),
            }
            if args.dry_run:
                row["downloaded"] = False
                row["local_size_bytes"] = dest.stat().st_size if dest.exists() else None
                row["status"] = "REMOTE_OK" if rsize else "REMOTE_MISSING"
            else:
                if dest.exists() and rsize and dest.stat().st_size == rsize:
                    lsize = dest.stat().st_size
                    row["status"] = "ALREADY_PRESENT"
                else:
                    lsize = download(key, dest)
                    row["status"] = "DOWNLOADED" if lsize else "DOWNLOAD_FAILED"
                row["downloaded"] = row["status"] in ("DOWNLOADED", "ALREADY_PRESENT")
                row["local_size_bytes"] = lsize
                row["size_match"] = (lsize == rsize) if (lsize and rsize) else None
            rows.append(row)
        print(f"  {sid}: {len(keys)} files  task={parse_task(keys[0].split('/')[-1])}")

    man = pd.DataFrame(rows)
    out = MANIFEST_DIR / f"{dsid}_s1_manifest.csv"
    man.to_csv(out, index=False)

    # summary
    print(f"\nManifest -> {out}  ({len(man)} file rows)")
    if "status" in man:
        print("status counts:", man["status"].value_counts().to_dict())
    core = man[man["suffix"].isin(["eeg.set", "eeg.fdt"])] if "suffix" in man else man
    subj_with_setfdt = core.groupby("bids_subject_id")["suffix"].nunique()
    n_complete = int((subj_with_setfdt >= 2).sum())
    print(f"subjects with both .set and .fdt present remotely: {n_complete}/{subs['bids_subject_id'].notna().sum()}")
    if not args.dry_run and "remote_size_bytes" in man:
        got = man[man.get("downloaded") == True]["local_size_bytes"].dropna().sum()
        print(f"downloaded volume: {got/1e9:.2f} GB")


if __name__ == "__main__":
    main()
