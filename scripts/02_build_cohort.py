#!/usr/bin/env python
"""
02_build_cohort.py
==================
Phase 1: build the deduplicated analytic cohort from the Phase 0 metadata cache.

Inputs (already fetched by scripts/00_download_or_load.py --mode metadata):
    data/metadata_cache/<dsid>/participants.tsv      BIDS roster + Original_ID + URSI
    data/metadata_cache/<dsid>/_filelist.txt         S3 key list (for EEG availability)
    data/metadata_cache/ds003522/BigAgg_4BIDS.xlsx   master clinical table (S1/S2/S3)

Identity keys
-------------
* Original_ID  : recording id (3001-3120 for the longitudinal acute/control cohort;
                 5-digit ids for the chronic-TBI arm). Equals BigAgg `SubID`.
* URSI         : scan-generated unique id (BIDS form 'M87dddddd'). The BigAgg `URSI`
                 column is the LAST 5 DIGITS of the BIDS URSI -> used to disambiguate
                 the duplicated Original_ID 3013 (two distinct URSIs).
* subject_uid  : canonical cross-dataset person key = full BIDS URSI. This is the unit
                 used for leakage-safe splitting and deduplication.

Outputs -> outputs/metadata_summary_tables/
    crosswalk_subject_ids.csv          one row per (dataset, BIDS subject)
    master_subject_session_table.csv   one row per (subject_uid, session) long format
    missingness_by_variable.csv        non-null / missing counts per key variable & session
    attrition_by_session.csv           CONSORT-style flow S1 -> S2 -> S3

No EEG is loaded; no model is trained.
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CACHE = PROJECT_ROOT / "data" / "metadata_cache"
OUT = PROJECT_ROOT / "outputs" / "metadata_summary_tables"
OUT.mkdir(parents=True, exist_ok=True)

DATASETS = ["ds003522", "ds005114", "ds003523"]
GROUP_LEVELS = {0: "mTBI", 1: "Control", 2: "Chronic TBI"}

# Strings used in BigAgg to denote missing / not-applicable.
MISSING_TOKENS = {"na", "n/a", "nr", "m", "nan", "", "none", "missing"}

OUTCOME_VARS = ["NSIsoma", "NSIcog", "NSIemo", "RivermeadTotal", "BDItotal"]
INJURY_VARS_S1 = ["GCS", "DaysSinceInjuryVisit1", "LOC", "DurationLOC_InMinutes"]


# --------------------------------------------------------------------------- #
def to_num(series: pd.Series) -> pd.Series:
    """Coerce a BigAgg column to float, mapping string missing-tokens to NaN."""
    def conv(x):
        if pd.isna(x):
            return np.nan
        if isinstance(x, str):
            if x.strip().lower() in MISSING_TOKENS:
                return np.nan
            # pull a leading number out of things like '1 minute'
            m = re.match(r"\s*(-?\d+(\.\d+)?)", x)
            return float(m.group(1)) if m else np.nan
        return float(x)
    return series.map(conv)


def ursi_short(ursi_full: str) -> int | float:
    """BIDS 'M87138432' -> 38432 (last 5 digits) to match BigAgg URSI column."""
    digits = re.sub(r"\D", "", str(ursi_full))
    return int(digits[-5:]) if len(digits) >= 5 else np.nan


# --------------------------------------------------------------------------- #
# 1. EEG availability per dataset: subject_id -> {sessions with *_eeg.set}
# --------------------------------------------------------------------------- #
def eeg_sessions_by_subject(dsid: str) -> dict[str, set[str]]:
    fl = CACHE / dsid / "_filelist.txt"
    present: dict[str, set[str]] = defaultdict(set)
    if not fl.exists():
        return present
    for k in fl.read_text(encoding="utf-8").splitlines():
        if k.endswith("_eeg.set"):
            m = re.search(r"/(sub-[A-Za-z0-9]+)/ses-([0-9]+)/", k)
            if m:
                present[m.group(1)].add(f"ses-{m.group(2)}")
    return present


# --------------------------------------------------------------------------- #
# 2. Crosswalk: one row per (dataset, BIDS subject)
# --------------------------------------------------------------------------- #
def build_crosswalk() -> pd.DataFrame:
    rows = []
    for dsid in DATASETS:
        parts = pd.read_csv(CACHE / dsid / "participants.tsv", sep="\t")
        eeg = eeg_sessions_by_subject(dsid)
        for _, r in parts.iterrows():
            sid = r["participant_id"]
            sess = sorted(eeg.get(sid, set()))
            rows.append({
                "dataset_id": dsid,
                "bids_subject_id": sid,
                "Original_ID": r["Original_ID"],
                "URSI": r["URSI"],
                "URSI_short": ursi_short(r["URSI"]),
                "subject_uid": r["URSI"],          # canonical person key
                "group_code": r["Group"],
                "group_label": GROUP_LEVELS.get(r["Group"], str(r["Group"])),
                "age": r["age"],
                "sex": r["sex"],
                "eeg_sessions": ";".join(sess),
                "n_eeg_sessions": len(sess),
            })
    cw = pd.DataFrame(rows)
    return cw


# --------------------------------------------------------------------------- #
# 3. Clinical table -> long (subject_uid via URSI_short, session)
# --------------------------------------------------------------------------- #
def load_clinical_long(cw: pd.DataFrame) -> pd.DataFrame:
    path = CACHE / "ds003522" / "BigAgg_4BIDS.xlsx"
    # map URSI_short -> subject_uid (full URSI). Built from crosswalk; unique.
    short2uid = (cw.dropna(subset=["URSI_short"])
                   .drop_duplicates("URSI_short")
                   .set_index("URSI_short")["subject_uid"].to_dict())
    long_rows = []
    for sheet, sess in [("S1", 1), ("S2", 2), ("S3", 3)]:
        df = pd.read_excel(path, sheet_name=sheet).dropna(how="all")
        rec = pd.DataFrame()
        rec["URSI_short"] = df["URSI"]
        rec["SubID"] = df["SubID"]
        rec["session"] = sess
        rec["control_flag"] = df.get("ControlEquals1")
        for v in OUTCOME_VARS:
            rec[v] = to_num(df[v]) if v in df.columns else np.nan
        rec["NSItotal"] = rec[["NSIsoma", "NSIcog", "NSIemo"]].sum(axis=1, min_count=3)
        for v in INJURY_VARS_S1:
            rec[v] = to_num(df[v]) if v in df.columns else np.nan
        for v in ("DaysSinceS1", "DaysSinceS2"):
            rec[v] = to_num(df[v]) if v in df.columns else np.nan
        rec["subject_uid"] = rec["URSI_short"].map(short2uid)
        long_rows.append(rec)
    return pd.concat(long_rows, ignore_index=True)


# --------------------------------------------------------------------------- #
# 4. Master subject x session table
# --------------------------------------------------------------------------- #
def build_master(cw: pd.DataFrame, clin: pd.DataFrame) -> pd.DataFrame:
    # subject-level identity (one row per subject_uid). Prefer ds003522 demographics,
    # fall back to any dataset. Group from ds003522 when present (has chronic arm).
    ident = (cw.sort_values("dataset_id")
               .drop_duplicates("subject_uid")
               .set_index("subject_uid")[["Original_ID", "group_code",
                                          "group_label", "age", "sex"]])

    # EEG availability flags per dataset per (subject_uid, session)
    eeg_flags = {}
    for dsid in DATASETS:
        sub = cw[cw.dataset_id == dsid]
        for _, r in sub.iterrows():
            for s in (r["eeg_sessions"].split(";") if r["eeg_sessions"] else []):
                sess = int(s.split("-")[1])
                eeg_flags[(r["subject_uid"], sess, dsid)] = True

    subjects = sorted(set(cw.subject_uid))
    rows = []
    clin_idx = clin.set_index(["subject_uid", "session"]).sort_index()
    # baseline (S1) injury vars per subject
    s1 = clin[clin.session == 1].set_index("subject_uid")
    for uid in subjects:
        for sess in (1, 2, 3):
            row = {"subject_uid": uid, "session": sess}
            if uid in ident.index:
                for c in ident.columns:
                    row[c] = ident.loc[uid, c]
            # eeg flags
            for dsid in DATASETS:
                row[f"eeg_{dsid}"] = eeg_flags.get((uid, sess, dsid), False)
            # session-varying clinical
            if (uid, sess) in clin_idx.index:
                cr = clin_idx.loc[(uid, sess)]
                if isinstance(cr, pd.DataFrame):   # safety: dup -> take first
                    cr = cr.iloc[0]
                for v in OUTCOME_VARS + ["NSItotal", "control_flag",
                                        "DaysSinceS1", "DaysSinceS2"]:
                    row[v] = cr.get(v)
                row["has_clinical"] = True
            else:
                row["has_clinical"] = False
            # baseline injury vars (carried, S1-defined)
            if uid in s1.index:
                for v in INJURY_VARS_S1:
                    row[f"{v}_S1"] = s1.loc[uid, v] if not isinstance(s1.loc[uid], pd.DataFrame) else s1.loc[uid, v].iloc[0]
            rows.append(row)
    master = pd.DataFrame(rows)
    return master


# --------------------------------------------------------------------------- #
# 5. Missingness by variable (per session, per cohort)
# --------------------------------------------------------------------------- #
def build_missingness(master: pd.DataFrame) -> pd.DataFrame:
    vars_session = ["NSItotal", "NSIsoma", "NSIcog", "NSIemo",
                    "RivermeadTotal", "BDItotal"]
    vars_baseline = ["GCS_S1", "DurationLOC_InMinutes_S1", "age", "sex", "group_code"]
    rows = []
    # denominator = subjects with EEG in the primary dataset (ds003522) for that session
    for sess in (1, 2, 3):
        sub = master[master.session == sess]
        # cohort definitions for denominators
        cohorts = {
            "ds003522_eeg": sub[sub.eeg_ds003522],
            "ds005114_eeg": sub[sub.eeg_ds005114],
            "ds003523_eeg": sub[sub.eeg_ds003523],
            "all_subjects": sub,
        }
        for cohort_name, cdf in cohorts.items():
            n = len(cdf)
            for v in vars_session:
                nn = int(cdf[v].notna().sum()) if v in cdf else 0
                rows.append({"cohort": cohort_name, "session": sess, "variable": v,
                             "n_in_cohort": n, "n_nonnull": nn, "n_missing": n - nn,
                             "pct_missing": round(100 * (n - nn) / n, 1) if n else np.nan})
            if sess == 1:  # baseline vars only meaningful at S1
                for v in vars_baseline:
                    nn = int(cdf[v].notna().sum()) if v in cdf else 0
                    rows.append({"cohort": cohort_name, "session": sess, "variable": v,
                                 "n_in_cohort": n, "n_nonnull": nn, "n_missing": n - nn,
                                 "pct_missing": round(100 * (n - nn) / n, 1) if n else np.nan})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# 6. CONSORT-style attrition S1 -> S3
# --------------------------------------------------------------------------- #
def build_attrition(master: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for dsid, flag in [("ds003522", "eeg_ds003522"),
                       ("ds005114", "eeg_ds005114"),
                       ("ds003523", "eeg_ds003523")]:
        for grp_label, grp_filter in [
            ("all", lambda d: d),
            ("mTBI", lambda d: d[d.group_code == 0]),
            ("Control", lambda d: d[d.group_code == 1]),
        ]:
            for sess in (1, 2, 3):
                sub = master[(master.session == sess) & (master[flag])]
                sub = grp_filter(sub)
                n_eeg = len(sub)
                n_nsi = int(sub["NSItotal"].notna().sum())
                n_both = int((sub[flag] & sub["NSItotal"].notna()).sum())
                rows.append({
                    "dataset": dsid, "group": grp_label, "session": sess,
                    "n_with_eeg": n_eeg,
                    "n_with_NSItotal": n_nsi,
                    "n_with_eeg_and_NSItotal": n_both,
                })
    att = pd.DataFrame(rows)
    return att


# --------------------------------------------------------------------------- #
def main() -> None:
    cw = build_crosswalk()
    cw.to_csv(OUT / "crosswalk_subject_ids.csv", index=False)
    print(f"crosswalk_subject_ids.csv: {len(cw)} rows "
          f"({cw.subject_uid.nunique()} unique subject_uid / URSI)")

    clin = load_clinical_long(cw)
    unmatched = clin[clin.subject_uid.isna()]
    if len(unmatched):
        print(f"  WARNING: {len(unmatched)} clinical rows had no URSI match "
              f"(SubIDs: {sorted(unmatched.SubID.dropna().unique().tolist())[:10]} ...)")

    master = build_master(cw, clin)
    master.to_csv(OUT / "master_subject_session_table.csv", index=False)
    print(f"master_subject_session_table.csv: {len(master)} rows "
          f"({master.subject_uid.nunique()} subjects x 3 sessions)")

    miss = build_missingness(master)
    miss.to_csv(OUT / "missingness_by_variable.csv", index=False)
    print(f"missingness_by_variable.csv: {len(miss)} rows")

    att = build_attrition(master)
    att.to_csv(OUT / "attrition_by_session.csv", index=False)
    print(f"attrition_by_session.csv: {len(att)} rows")

    # ---- console summary for the analysis plan ----
    print("\n=== Attrition (EEG & NSItotal) by dataset/group/session ===")
    show = att[att.group.isin(["mTBI", "Control"])]
    print(show.to_string(index=False))

    print("\n=== Outcome-prediction cohort sizes (S1 EEG AND S3 NSItotal) ===")
    for dsid, flag in [("ds003522", "eeg_ds003522"),
                       ("ds005114", "eeg_ds005114"),
                       ("ds003523", "eeg_ds003523")]:
        s1 = master[(master.session == 1) & (master[flag])]
        s3 = master[(master.session == 3)]
        s3_out = set(s3[s3["NSItotal"].notna()].subject_uid)
        s1_eeg = set(s1.subject_uid)
        usable = s1_eeg & s3_out
        mtbi = master[(master.subject_uid.isin(usable)) & (master.group_code == 0)].subject_uid.nunique()
        ctrl = master[(master.subject_uid.isin(usable)) & (master.group_code == 1)].subject_uid.nunique()
        print(f"  {dsid}: S1 EEG={len(s1_eeg)}, with S3 NSItotal={len(usable)} "
              f"(mTBI={mtbi}, Control={ctrl})")

    # all-three overlap usable cohort
    s1 = master[master.session == 1]
    all3 = set(s1[s1.eeg_ds003522 & s1.eeg_ds005114 & s1.eeg_ds003523].subject_uid)
    s3o = set(master[(master.session == 3) & master["NSItotal"].notna()].subject_uid)
    print(f"  ALL-THREE S1 EEG: {len(all3)}, with S3 NSItotal: {len(all3 & s3o)}")
    print("\nDone. Tables in", OUT)


if __name__ == "__main__":
    main()
