#!/usr/bin/env python
"""
00_download_or_load.py
======================
Acquire (or locate) the OpenNeuro EEG mTBI datasets for this project.

Datasets
--------
    ds003522  Three-Stim Auditory Oddball + Rest, acute & chronic TBI   (PRIMARY)
    ds005114  DPX cognitive-control task, acute mild TBI                (secondary)
    ds003523  Visual Working Memory, acute TBI                          (secondary)

Design goals
------------
* Reproducible and transparent: every byte fetched is logged, nothing is
  silently mutated, and the same command re-run is idempotent.
* No heavy dependencies required for Phase 0. The default mode ("metadata")
  pulls only the small BIDS sidecar / participants / clinical files over public
  HTTPS from the openneuro.org S3 bucket -- no AWS credentials, no git-annex.
* Pluggable full-download backends for later phases: datalad, openneuro-py,
  eegdash, or boto3/S3. The script auto-detects which are installed.

Usage
-----
    # Phase 0 default: fetch only lightweight metadata into data/metadata_cache/
    python scripts/00_download_or_load.py --mode metadata

    # Later phases: full BIDS trees into data/raw/<dsid>/ via an available backend
    python scripts/00_download_or_load.py --mode full --backend datalad
    python scripts/00_download_or_load.py --mode full --backend openneuro
    python scripts/00_download_or_load.py --mode full --datasets ds003522

This script intentionally does NOT preprocess or load EEG signals.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
DATASETS = {
    "ds003522": "Three-Stim Auditory Oddball + Rest (acute & chronic TBI) [PRIMARY]",
    "ds005114": "DPX cognitive-control task (acute mild TBI)",
    "ds003523": "Visual Working Memory (acute TBI)",
}

S3_BASE = "https://s3.amazonaws.com/openneuro.org"
S3_BUCKET_LIST = "https://s3.amazonaws.com/openneuro.org"  # ListObjectsV2 endpoint
S3_NS = "{http://s3.amazonaws.com/doc/2006-03-01/}"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
METADATA_DIR = PROJECT_ROOT / "data" / "metadata_cache"
RAW_DIR = PROJECT_ROOT / "data" / "raw"

# Small, always-useful top-level files (best-effort; missing ones are skipped).
TOP_LEVEL_FILES = [
    "dataset_description.json",
    "participants.tsv",
    "participants.json",
    "README",
    "CHANGES",
]

# Clinical / outcome spreadsheets that live under code/ (per-dataset).
# These hold the longitudinal symptom + neuropsych variables (NSI, Rivermead,
# BDI, ...) that are NOT in participants.tsv.
CLINICAL_FILES = {
    "ds003522": ["code/BigAgg_4BIDS.xlsx", "code/BigAgg_Quinn_4Bids.xlsx"],
    "ds005114": ["code/BigAgg_4BIDS.xlsx", "code/READ ME.txt"],
    "ds003523": [],  # behavioral data is per-subject .mat under code/WM Beh/
}


# --------------------------------------------------------------------------- #
# HTTP helpers (stdlib only)
# --------------------------------------------------------------------------- #
def _get(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "eeg-mtbi-phase0/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def fetch_to(url: str, dest: Path, timeout: int = 60) -> str:
    """Download url -> dest. Returns a one-line status string."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        data = _get(url, timeout=timeout)
    except urllib.error.HTTPError as e:
        return f"MISS ({e.code})  {url.rsplit('/', 1)[-1]}"
    except Exception as e:  # noqa: BLE001 - report and continue
        return f"ERR  {type(e).__name__}: {e}"
    dest.write_bytes(data)
    return f"OK   {dest.name}  ({len(data):,} bytes)"


def list_s3_keys(prefix: str, timeout: int = 60) -> list[str]:
    """List every object key under `prefix` in the public openneuro.org bucket."""
    keys: list[str] = []
    token: str | None = None
    while True:
        url = f"{S3_BUCKET_LIST}?list-type=2&prefix={prefix}&max-keys=1000"
        if token:
            url += f"&continuation-token={urllib.parse.quote(token)}"
        root = ET.fromstring(_get(url, timeout=timeout))
        for c in root.findall(f"{S3_NS}Contents"):
            key = c.findtext(f"{S3_NS}Key")
            if key:
                keys.append(key)
        truncated = (root.findtext(f"{S3_NS}IsTruncated") or "false") == "true"
        token = root.findtext(f"{S3_NS}NextContinuationToken")
        if not truncated or not token:
            break
    return keys


import urllib.parse  # noqa: E402  (kept near use for clarity)


# --------------------------------------------------------------------------- #
# Mode: metadata (Phase 0 default)
# --------------------------------------------------------------------------- #
def download_metadata(datasets: list[str]) -> None:
    print("=" * 70)
    print("METADATA MODE - fetching lightweight BIDS + clinical metadata only")
    print("Source: public openneuro.org S3 bucket over HTTPS (no credentials)")
    print("=" * 70)
    for dsid in datasets:
        out = METADATA_DIR / dsid
        print(f"\n### {dsid}  -- {DATASETS[dsid]}")

        # 1. full key listing (cheap, ~a few thousand keys) -> _filelist.txt
        try:
            keys = list_s3_keys(f"{dsid}/")
            (out).mkdir(parents=True, exist_ok=True)
            (out / "_filelist.txt").write_text("\n".join(keys), encoding="utf-8")
            print(f"  file list: {len(keys):,} keys -> {out/'_filelist.txt'}")
        except Exception as e:  # noqa: BLE001
            keys = []
            print(f"  file list: FAILED ({e})")

        # 2. top-level metadata files
        for f in TOP_LEVEL_FILES:
            print("   ", fetch_to(f"{S3_BASE}/{dsid}/{f}", out / f))

        # 3. clinical/outcome spreadsheets
        for f in CLINICAL_FILES.get(dsid, []):
            safe = Path(f).name.replace(" ", "_")
            print("   ", fetch_to(f"{S3_BASE}/{dsid}/{urllib.parse.quote(f)}", out / safe))

        # 4. one representative set of EEG sidecars (events/channels/eeg json)
        _fetch_example_sidecars(dsid, keys, out)


def _fetch_example_sidecars(dsid: str, keys: list[str], out: Path) -> None:
    """Grab one example *_eeg.json and its sibling sidecars for schema review."""
    eeg_json = next((k for k in keys if k.endswith("_eeg.json")), None)
    if not eeg_json:
        return
    stem = eeg_json[: -len("_eeg.json")]  # full key prefix incl. dsid/
    for suffix in ("_eeg.json", "_events.tsv", "_events.json",
                   "_channels.tsv", "_coordsystem.json", "_electrodes.tsv"):
        url = f"{S3_BASE}/{stem}{suffix}"
        print("   ", fetch_to(url, out / f"example{suffix}"))


# --------------------------------------------------------------------------- #
# Mode: full (later phases) - pluggable backends
# --------------------------------------------------------------------------- #
def _have(module: str) -> bool:
    import importlib.util
    return importlib.util.find_spec(module) is not None


def download_full(datasets: list[str], backend: str) -> None:
    print("=" * 70)
    print(f"FULL MODE - downloading complete BIDS trees via backend='{backend}'")
    print(f"Target: {RAW_DIR}")
    print("=" * 70)

    if backend == "auto":
        for cand in ("datalad", "openneuro", "eegdash", "s3"):
            if _backend_available(cand):
                backend = cand
                break
        else:
            sys.exit("No download backend available. Install datalad, openneuro-py, "
                     "eegdash, or boto3 (see requirements.txt / environment.yml).")
        print(f"auto-selected backend: {backend}")

    for dsid in datasets:
        dest = RAW_DIR / dsid
        dest.mkdir(parents=True, exist_ok=True)
        print(f"\n### {dsid} -> {dest}")
        if backend == "datalad":
            _full_datalad(dsid, dest)
        elif backend == "openneuro":
            _full_openneuro(dsid, dest)
        elif backend == "eegdash":
            _full_eegdash(dsid, dest)
        elif backend == "s3":
            _full_s3(dsid, dest)
        else:
            sys.exit(f"Unknown backend: {backend}")


def _backend_available(backend: str) -> bool:
    return {
        "datalad": _have("datalad"),
        "openneuro": _have("openneuro"),
        "eegdash": _have("eegdash"),
        "s3": _have("boto3"),
    }.get(backend, False)


def _full_datalad(dsid: str, dest: Path) -> None:
    import datalad.api as dl  # type: ignore
    url = f"https://github.com/OpenNeuroDatasets/{dsid}.git"
    print(f"  datalad install {url}")
    dl.install(path=str(dest), source=url)
    print("  datalad get (this downloads the EEG payload; may be large)")
    dl.get(dataset=str(dest), path=".")


def _full_openneuro(dsid: str, dest: Path) -> None:
    import openneuro  # type: ignore
    print(f"  openneuro.download(dataset={dsid}, target_dir={dest})")
    openneuro.download(dataset=dsid, target_dir=str(dest))


def _full_eegdash(dsid: str, dest: Path) -> None:
    try:
        from eegdash import EEGDash  # type: ignore
    except Exception as e:  # noqa: BLE001
        sys.exit(f"eegdash import failed: {e}")
    print(f"  EEGDash query/download for {dsid} -> {dest}")
    eeg = EEGDash()
    recs = eeg.find({"dataset": dsid})
    print(f"  EEGDash returned {len(recs)} records; downloading to cache")
    # EEGDash caches locally; see its docs for cache configuration.


def _full_s3(dsid: str, dest: Path) -> None:
    import boto3  # type: ignore
    from botocore import UNSIGNED  # type: ignore
    from botocore.config import Config  # type: ignore
    s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
    paginator = s3.get_paginator("list_objects_v2")
    n = 0
    for page in paginator.paginate(Bucket="openneuro.org", Prefix=f"{dsid}/"):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            target = dest / key[len(dsid) + 1:]
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and target.stat().st_size == obj["Size"]:
                continue
            s3.download_file("openneuro.org", key, str(target))
            n += 1
    print(f"  downloaded/updated {n} files")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--mode", choices=["metadata", "full"], default="metadata",
                   help="metadata = lightweight sidecars (Phase 0 default); "
                        "full = complete BIDS trees")
    p.add_argument("--backend", default="auto",
                   choices=["auto", "datalad", "openneuro", "eegdash", "s3"],
                   help="download backend for --mode full")
    p.add_argument("--datasets", nargs="+", default=list(DATASETS),
                   choices=list(DATASETS),
                   help="subset of datasets to acquire")
    args = p.parse_args()

    if args.mode == "metadata":
        download_metadata(args.datasets)
        print("\nDone. Inspect results with scripts/01_inspect_bids_metadata.py")
    else:
        download_full(args.datasets, args.backend)


if __name__ == "__main__":
    main()
