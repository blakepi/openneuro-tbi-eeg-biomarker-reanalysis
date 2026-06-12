#!/usr/bin/env python
"""
03_freeze_splits.py
===================
Phase 2, Task 1: freeze leakage-safe, subject-level cross-validation folds.

Splits are defined NOW, before any EEG is read or any feature is computed, so that
the entire downstream pipeline (preprocessing, feature extraction, scaling, model fit)
can be refit strictly inside training folds. The fold assignment is the contract that
guarantees no `subject_uid` (URSI) ever appears in both train and test.

Eligible cohorts (each = acute mTBI with Session-1 EEG AND a Session-3 NSI outcome):
    A. ds003522 (auditory oddball)   -- PRIMARY
    B. ds005114 (DPX)                -- replication
    C. ds003523 (visual working mem) -- replication

Notes
-----
* Split unit = `subject_uid` (URSI), never `Original_ID` (which collides; see Phase 1).
* Deterministic: fixed RANDOM_SEED.
* Stratification by Session-3 NSI-total quantile bins when each bin has >= n_splits
  members; otherwise we fall back to unstratified KFold and record the reason in
  outputs/splits/split_provenance.json.
* QC has NOT run yet. Subjects that later fail EEG QC (Task 3) are removed from their
  frozen fold in place -- folds are NOT reshuffled -- preserving leakage safety.

Output: outputs/splits/frozen_cv_folds.csv  (+ split_provenance.json)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, StratifiedKFold

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TABLES = PROJECT_ROOT / "outputs" / "metadata_summary_tables"
OUT = PROJECT_ROOT / "outputs" / "splits"
OUT.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
N_SPLITS = 5
N_STRAT_BINS = 3            # tertiles of the S3 NSI outcome
PRIMARY_OUTCOME = "NSItotal"   # at Session 3

COHORTS = {
    "A_ds003522": "eeg_ds003522",
    "B_ds005114": "eeg_ds005114",
    "C_ds003523": "eeg_ds003523",
}


def eligible_subjects(master: pd.DataFrame, eeg_flag: str) -> pd.DataFrame:
    """Acute mTBI (group 0) with S1 EEG in the given dataset AND a non-null S3 NSI total."""
    s1 = master[(master.session == 1) & (master.group_code == 0) & (master[eeg_flag])]
    s3 = master[(master.session == 3)][["subject_uid", PRIMARY_OUTCOME]].rename(
        columns={PRIMARY_OUTCOME: "outcome_S3_NSItotal"})
    elig = s1.merge(s3, on="subject_uid", how="left")
    elig = elig[elig["outcome_S3_NSItotal"].notna()].copy()
    return elig[["subject_uid", "Original_ID", "group_code",
                 "outcome_S3_NSItotal"]].reset_index(drop=True)


def make_folds(elig: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Assign each subject a fold index; stratify on outcome bins when feasible."""
    n = len(elig)
    prov = {"n_subjects": n, "n_splits": N_SPLITS, "seed": RANDOM_SEED}
    y = elig["outcome_S3_NSItotal"].to_numpy()

    # try stratified by quantile bins
    bins = pd.qcut(elig["outcome_S3_NSItotal"], q=N_STRAT_BINS,
                   labels=False, duplicates="drop")
    bin_counts = pd.Series(bins).value_counts()
    can_stratify = (n >= N_SPLITS * 2) and (bin_counts.min() >= N_SPLITS) and (bins.nunique() >= 2)

    fold = np.full(n, -1, dtype=int)
    if can_stratify:
        skf = StratifiedKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_SEED)
        for f, (_, test_idx) in enumerate(skf.split(np.zeros(n), bins)):
            fold[test_idx] = f
        prov["stratified"] = True
        prov["strategy"] = f"StratifiedKFold on {N_STRAT_BINS}-quantile bins of S3 NSI total"
        prov["bin_counts"] = {int(k): int(v) for k, v in bin_counts.items()}
    else:
        kf = KFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_SEED)
        for f, (_, test_idx) in enumerate(kf.split(np.zeros(n))):
            fold[test_idx] = f
        prov["stratified"] = False
        prov["strategy"] = "KFold (unstratified)"
        prov["fallback_reason"] = (
            f"min outcome-bin count ({int(bin_counts.min())}) < n_splits ({N_SPLITS}) "
            f"or n ({n}) too small for stratified {N_SPLITS}-fold")

    out = elig.copy()
    out["outcome_bin"] = bins.to_numpy()
    out["fold"] = fold
    prov["loso_recommended"] = bool(n < 40)   # advise leave-one-subject-out for small N
    return out, prov


def main() -> None:
    master = pd.read_csv(TABLES / "master_subject_session_table.csv")
    all_rows = []
    provenance = {"random_seed": RANDOM_SEED, "n_splits": N_SPLITS,
                  "split_unit": "subject_uid (URSI)", "cohorts": {}}
    print("Freezing leakage-safe folds (split unit = subject_uid / URSI)\n")
    for cohort_id, eeg_flag in COHORTS.items():
        elig = eligible_subjects(master, eeg_flag)
        folded, prov = make_folds(elig)
        folded.insert(0, "cohort_id", cohort_id)
        folded.insert(1, "dataset_id", eeg_flag.replace("eeg_", ""))
        all_rows.append(folded)
        provenance["cohorts"][cohort_id] = prov
        strat = "stratified" if prov["stratified"] else "UNSTRATIFIED (" + prov.get("fallback_reason", "") + ")"
        print(f"  {cohort_id}: n={prov['n_subjects']}  {N_SPLITS}-fold  [{strat}]")
        fold_sizes = folded["fold"].value_counts().sort_index().to_dict()
        print(f"      fold sizes: {fold_sizes}")

    frozen = pd.concat(all_rows, ignore_index=True)
    frozen.to_csv(OUT / "frozen_cv_folds.csv", index=False)
    with open(OUT / "split_provenance.json", "w") as fh:
        json.dump(provenance, fh, indent=2)

    print(f"\nWrote {OUT / 'frozen_cv_folds.csv'} ({len(frozen)} subject-fold rows)")
    print(f"Wrote {OUT / 'split_provenance.json'}")
    # leakage cross-check: no subject_uid in >1 fold within a cohort
    dup = (frozen.groupby(["cohort_id", "subject_uid"])["fold"].nunique() > 1).sum()
    print(f"Leakage check: subjects assigned to >1 fold within a cohort = {dup} (must be 0)")


if __name__ == "__main__":
    main()
