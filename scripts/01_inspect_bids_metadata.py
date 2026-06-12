#!/usr/bin/env python
"""
01_inspect_bids_metadata.py
===========================
Inspect the BIDS structure and metadata of the three OpenNeuro EEG mTBI
datasets and emit machine-readable summary tables for the feasibility report.

It reads from data/metadata_cache/<dsid>/ (produced by 00_download_or_load.py
in --mode metadata). If a full BIDS tree exists under data/raw/<dsid>/, that is
used to recompute the per-subject/session file inventory directly.

Outputs (CSV) -> outputs/metadata_summary_tables/
    01_dataset_overview.csv          one row per dataset (n, groups, tasks, ...)
    02_participants_<dsid>.csv       cleaned participants table per dataset
    03_group_by_dataset.csv          group counts per dataset
    04_session_availability.csv      per dataset: subjects x sessions present
    05_eeg_acquisition.csv           sampling rate, channels, reference, format
    06_clinical_variables.csv        inventory of clinical/outcome variables
    07_outcome_missingness.csv       NSI/Rivermead/BDI non-null counts per session
    08_cross_dataset_overlap.csv     shared Original_ID counts between datasets
    09_event_codes_<dsid>.csv        distinct event trigger codes per dataset

Nothing here preprocesses or loads EEG signals.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CACHE = PROJECT_ROOT / "data" / "metadata_cache"
RAW = PROJECT_ROOT / "data" / "raw"
OUT = PROJECT_ROOT / "outputs" / "metadata_summary_tables"

DATASETS = {
    "ds003522": "Three-Stim Auditory Oddball + Rest (acute & chronic TBI) [PRIMARY]",
    "ds005114": "DPX cognitive-control task (acute mild TBI)",
    "ds003523": "Visual Working Memory (acute TBI)",
}

# Outcome variables we care about for a recovery / persistent-symptom endpoint.
OUTCOME_VARS = ["NSIsoma", "NSIcog", "NSIemo", "RivermeadTotal", "BDItotal",
                "Anxiety", "Depression", "Fatigue", "PainRating"]
INJURY_VARS = ["GCS", "DaysSinceInjuryVisit1", "LOC", "DurationLOC_InMinutes",
               "MechanismOfInjury", "DazedDisoriented"]


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _read_filelist(dsid: str) -> list[str]:
    """Return the list of object keys for a dataset (from cache or live tree)."""
    raw_tree = RAW / dsid
    if raw_tree.is_dir():
        return [f"{dsid}/{p.relative_to(raw_tree).as_posix()}"
                for p in raw_tree.rglob("*") if p.is_file()]
    fl = CACHE / dsid / "_filelist.txt"
    if fl.exists():
        return [ln for ln in fl.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return []


def _participants(dsid: str) -> pd.DataFrame | None:
    f = CACHE / dsid / "participants.tsv"
    if not f.exists():
        f = RAW / dsid / "participants.tsv"
    if not f.exists():
        return None
    return pd.read_csv(f, sep="\t")


GROUP_LEVELS = {0: "mTBI", 1: "Control", 2: "Chronic TBI"}


# --------------------------------------------------------------------------- #
# Table builders
# --------------------------------------------------------------------------- #
def build_overview_and_participants() -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    rows = []
    parts: dict[str, pd.DataFrame] = {}
    for dsid, label in DATASETS.items():
        keys = _read_filelist(dsid)
        df = _participants(dsid)
        parts[dsid] = df

        subs = sorted({m.group(1) for k in keys
                       if (m := re.search(r"/(sub-[A-Za-z0-9]+)/", k))})
        sessions = sorted({m.group(1) for k in keys
                           if (m := re.search(r"(ses-[A-Za-z0-9]+)", k))})
        tasks = sorted({m.group(1) for k in keys
                        if (m := re.search(r"task-([A-Za-z0-9]+)", k))})
        exts = defaultdict(int)
        for k in keys:
            m = re.search(r"/sub-.*(\.[A-Za-z0-9]+)$", k)
            if m:
                exts[m.group(1)] += 1
        fmt = ", ".join(f"{e}({n})" for e, n in
                        sorted(exts.items(), key=lambda x: -x[1]))

        rows.append({
            "dataset": dsid,
            "description": label,
            "n_subjects_participants_tsv": 0 if df is None else len(df),
            "n_subjects_with_eeg": len(subs),
            "sessions": ", ".join(sessions),
            "n_sessions": len(sessions),
            "tasks": ", ".join(tasks),
            "groups": "" if df is None else ", ".join(
                f"{GROUP_LEVELS.get(g, g)}={c}"
                for g, c in df["Group"].value_counts().sort_index().items()),
            "eeg_file_formats": fmt,
        })
    return pd.DataFrame(rows), parts


def build_group_table(parts) -> pd.DataFrame:
    rows = []
    for dsid, df in parts.items():
        if df is None:
            continue
        for g, c in df["Group"].value_counts().sort_index().items():
            rows.append({"dataset": dsid, "group_code": g,
                         "group_label": GROUP_LEVELS.get(g, str(g)), "n": int(c)})
    return pd.DataFrame(rows)


def build_session_availability() -> pd.DataFrame:
    """Per dataset: how many subjects have EEG at each session (attrition)."""
    rows = []
    for dsid in DATASETS:
        keys = _read_filelist(dsid)
        # subject -> set(sessions with an *_eeg.set file)
        present: dict[str, set[str]] = defaultdict(set)
        for k in keys:
            if k.endswith("_eeg.set"):
                ms = re.search(r"/(sub-[A-Za-z0-9]+)/(ses-[A-Za-z0-9]+)/", k)
                if ms:
                    present[ms.group(1)].add(ms.group(2))
        all_ses = sorted({s for v in present.values() for s in v})
        per_ses = {s: sum(1 for v in present.values() if s in v) for s in all_ses}
        # session-count distribution
        ncount = defaultdict(int)
        for v in present.values():
            ncount[len(v)] += 1
        row = {"dataset": dsid, "n_subjects_with_eeg": len(present)}
        for s in all_ses:
            row[f"n_{s}"] = per_ses[s]
        for n in sorted(ncount):
            row[f"subjects_with_{n}_session(s)"] = ncount[n]
        rows.append(row)
    return pd.DataFrame(rows)


def build_eeg_acquisition() -> pd.DataFrame:
    rows = []
    for dsid in DATASETS:
        f = CACHE / dsid / "example_eeg.json"
        ch = CACHE / dsid / "example_channels.tsv"
        rec = {"dataset": dsid}
        if f.exists():
            meta = json.loads(f.read_text(encoding="utf-8"))
            for k in ("TaskName", "SamplingFrequency", "EEGChannelCount",
                      "EEGReference", "EEGGround", "PowerLineFrequency",
                      "ManufacturersModelName", "RecordingType", "RecordingDuration"):
                rec[k] = meta.get(k)
        if ch.exists():
            cdf = pd.read_csv(ch, sep="\t")
            rec["n_channels_in_example"] = len(cdf)
            rec["channel_types"] = ", ".join(sorted(cdf["type"].dropna().unique())) \
                if "type" in cdf.columns else ""
        rec["native_format"] = "EEGLAB .set/.fdt"
        rows.append(rec)
    return pd.DataFrame(rows)


def _load_bigagg(dsid: str):
    f = CACHE / dsid / "BigAgg_4BIDS.xlsx"
    if not f.exists():
        return None
    try:
        return pd.read_excel(f, sheet_name=None)  # all sheets
    except Exception as e:  # noqa: BLE001
        print(f"  (could not read {f.name}: {e}; install openpyxl)")
        return None


def build_clinical_inventory() -> pd.DataFrame:
    rows = []
    for dsid in DATASETS:
        sheets = _load_bigagg(dsid)
        if not sheets:
            continue
        for sheet, df in sheets.items():
            if sheet.lower() == "notes":
                continue
            for col in df.columns:
                rows.append({"dataset": dsid, "sheet": sheet, "variable": col,
                             "n_nonnull": int(df[col].notna().sum()),
                             "n_rows": len(df)})
    return pd.DataFrame(rows)


def build_outcome_missingness() -> pd.DataFrame:
    rows = []
    for dsid in DATASETS:
        sheets = _load_bigagg(dsid)
        if not sheets:
            continue
        for sheet in ("S1", "S2", "S3"):
            if sheet not in sheets:
                continue
            df = sheets[sheet].dropna(how="all")
            rec = {"dataset": dsid, "session_sheet": sheet, "n_rows": len(df)}
            for v in OUTCOME_VARS:
                rec[v] = int(df[v].notna().sum()) if v in df.columns else None
            rows.append(rec)
    return pd.DataFrame(rows)


def build_cross_dataset_overlap(parts) -> pd.DataFrame:
    import itertools
    sets = {d: set(df["Original_ID"]) for d, df in parts.items() if df is not None}
    rows = []
    for a, b in itertools.combinations(sets, 2):
        rows.append({"dataset_a": a, "dataset_b": b,
                     "n_a": len(sets[a]), "n_b": len(sets[b]),
                     "n_shared_Original_ID": len(sets[a] & sets[b])})
    if len(sets) == 3:
        inter = set.intersection(*sets.values())
        rows.append({"dataset_a": "ALL_THREE", "dataset_b": "",
                     "n_a": "", "n_b": "", "n_shared_Original_ID": len(inter)})
    return pd.DataFrame(rows)


def build_event_codes() -> dict[str, pd.DataFrame]:
    out = {}
    for dsid in DATASETS:
        f = CACHE / dsid / "example_events.tsv"
        if not f.exists():
            continue
        ev = pd.read_csv(f, sep="\t")
        val_col = "value" if "value" in ev.columns else ev.columns[-1]
        vc = ev[val_col].value_counts().reset_index()
        vc.columns = ["event_value", "count_in_example_run"]
        out[dsid] = vc
    return out


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not any((CACHE / d).exists() for d in DATASETS):
        sys.exit("No metadata found. Run scripts/00_download_or_load.py --mode metadata first.")

    print("Building summary tables ->", OUT)

    overview, parts = build_overview_and_participants()
    overview.to_csv(OUT / "01_dataset_overview.csv", index=False)
    print("\n=== Dataset overview ===")
    print(overview.to_string(index=False))

    for dsid, df in parts.items():
        if df is not None:
            df.to_csv(OUT / f"02_participants_{dsid}.csv", index=False)

    build_group_table(parts).to_csv(OUT / "03_group_by_dataset.csv", index=False)

    sess = build_session_availability()
    sess.to_csv(OUT / "04_session_availability.csv", index=False)
    print("\n=== Session availability (EEG .set files) ===")
    print(sess.to_string(index=False))

    acq = build_eeg_acquisition()
    acq.to_csv(OUT / "05_eeg_acquisition.csv", index=False)
    print("\n=== EEG acquisition ===")
    print(acq.to_string(index=False))

    clin = build_clinical_inventory()
    if not clin.empty:
        clin.to_csv(OUT / "06_clinical_variables.csv", index=False)
        print(f"\n=== Clinical variable inventory: {clin['variable'].nunique()} "
              f"distinct variables across {clin['dataset'].nunique()} datasets ===")

    miss = build_outcome_missingness()
    if not miss.empty:
        miss.to_csv(OUT / "07_outcome_missingness.csv", index=False)
        print("\n=== Outcome non-null counts per session sheet (attrition) ===")
        print(miss.to_string(index=False))

    overlap = build_cross_dataset_overlap(parts)
    overlap.to_csv(OUT / "08_cross_dataset_overlap.csv", index=False)
    print("\n=== Cross-dataset Original_ID overlap ===")
    print(overlap.to_string(index=False))

    for dsid, vc in build_event_codes().items():
        vc.to_csv(OUT / f"09_event_codes_{dsid}.csv", index=False)

    print("\nDone. Tables written to", OUT)


if __name__ == "__main__":
    main()
