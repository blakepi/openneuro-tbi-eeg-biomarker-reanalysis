#!/usr/bin/env python
"""
10_build_analysis_table.py
==========================
Phase 4: assemble the modeling table by joining, for the first time, the locked EEG
predictors to the Session-3 outcome and covariates, keyed on subject_uid, with the
frozen fold labels attached. This is the first step in which the outcome is read; it is
permitted now that the analysis plan is locked.

Locked panel (no additions / removals):
    rest (EC):  Global_Aperiodic_Exponent, Posterior_IAF,
                Frontal_Theta_Alpha_Ratio, Occipital_Relative_Alpha
    ERP:        P3b_Amplitude (mean-window), P3b_Latency,
                P3a_Amplitude (mean-window), P3a_Latency
    exploratory: Spectral_Entropy
    covariates: Age, Sex
    sensitivity ERP metric: P3b_Amplitude_peak, P3a_Amplitude_peak

Outcome: S3 NSI total (from master_subject_session_table.csv, session 3, NSItotal).

Output: outputs/analysis/ds003522_s1_analysis_table.csv
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
TAB = ROOT / "outputs" / "metadata_summary_tables"
FEAT = ROOT / "outputs" / "features"
SPLITS = ROOT / "outputs" / "splits"
OUT = ROOT / "outputs" / "analysis"
OUT.mkdir(parents=True, exist_ok=True)

# locked feature column -> analysis name
REST_MAP = {
    "rest_EC_global_aper_exponent": "Global_Aperiodic_Exponent",
    "rest_EC_iaf_posterior_hz": "Posterior_IAF",
    "rest_EC_frontal_theta_alpha_ratio": "Frontal_Theta_Alpha_Ratio",
    "rest_EC_occipital_alpha_rel": "Occipital_Relative_Alpha",
    "rest_EC_global_spec_entropy": "Spectral_Entropy",
}
ERP_MAP = {
    "erp_P3b_target_par_mean_uv": "P3b_Amplitude",
    "erp_P3b_target_par_lat_ms": "P3b_Latency",
    "erp_P3a_novel_fc_mean_uv": "P3a_Amplitude",
    "erp_P3a_novel_fc_lat_ms": "P3a_Latency",
    "erp_P3b_target_par_peak_uv": "P3b_Amplitude_peak",
    "erp_P3a_novel_fc_peak_uv": "P3a_Amplitude_peak",
}


def main() -> None:
    folds = pd.read_csv(SPLITS / "frozen_cv_folds.csv")
    folds = folds[folds.cohort_id == "A_ds003522"][
        ["subject_uid", "Original_ID", "fold", "outcome_S3_NSItotal"]].copy()

    master = pd.read_csv(TAB / "master_subject_session_table.csv")
    s1 = master[master.session == 1][["subject_uid", "age", "sex"]].drop_duplicates("subject_uid")

    rest = pd.read_csv(FEAT / "ds003522_s1_rest_features.csv")
    erp = pd.read_csv(FEAT / "ds003522_s1_erp_features.csv")
    cw = pd.read_csv(TAB / "crosswalk_subject_ids.csv")
    cw = cw[cw.dataset_id == "ds003522"][["subject_uid", "bids_subject_id"]].drop_duplicates("subject_uid")

    # rest/erp are keyed by BIDS subject; map to subject_uid via crosswalk
    rest = rest.merge(cw, left_on="subject", right_on="bids_subject_id", how="left")
    erp = erp.merge(cw, left_on="subject", right_on="bids_subject_id", how="left")
    rest_sel = rest[["subject_uid"] + list(REST_MAP)].rename(columns=REST_MAP)
    erp_sel = erp[["subject_uid"] + list(ERP_MAP)].rename(columns=ERP_MAP)

    df = (folds.merge(s1, on="subject_uid", how="left")
                .merge(rest_sel, on="subject_uid", how="left")
                .merge(erp_sel, on="subject_uid", how="left"))
    df = df.rename(columns={"outcome_S3_NSItotal": "S3_NSI_Total"})
    df["Sex"] = df["sex"].astype("Int64")     # 0/1 as recorded
    df = df.rename(columns={"age": "Age"})

    # ---- locked usability gates (apply §3 exclusion criteria to the LOCKED predictors) ----
    # The locked resting predictors are eyes-closed only, so the eyes-OPEN reliability floor does
    # NOT gate any locked model; EC is >=40 s for all 25. The ERP floor (>=15 Target & Novel
    # epochs, named-tone events present) gates all ERP-containing models.
    use = pd.read_csv(FEAT / "ds003522_s1_subject_usability.csv")[
        ["subject", "rest_EC_usable_s", "rest_EO_usable_s", "erp_usable"]]
    use = use.merge(cw, left_on="subject", right_on="bids_subject_id", how="left")
    df = df.merge(use[["subject_uid", "rest_EC_usable_s", "rest_EO_usable_s", "erp_usable"]],
                  on="subject_uid", how="left")
    df["ec_rest_reliable"] = df["rest_EC_usable_s"] >= 40.0       # all True here
    df["erp_reliable"] = df["erp_usable"].fillna(False).astype(bool)

    # ---- pre-specified outcome-transform rule (OUTCOME distribution only) ----
    y = df["S3_NSI_Total"].dropna().to_numpy()
    skew = float(stats.skew(y))
    use_log = abs(skew) > 1.0
    df["S3_NSI_Total_log1p"] = np.log1p(df["S3_NSI_Total"])
    df["primary_outcome_is_log"] = use_log

    cols = (["subject_uid", "Original_ID", "fold", "S3_NSI_Total", "S3_NSI_Total_log1p",
             "primary_outcome_is_log", "Age", "Sex"]
            + list(REST_MAP.values()) + list(ERP_MAP.values())
            + ["rest_EC_usable_s", "rest_EO_usable_s", "ec_rest_reliable", "erp_reliable"])
    df = df[cols]
    df.to_csv(OUT / "ds003522_s1_analysis_table.csv", index=False)

    # ---- console summary (outcome + availability only; NO feature-outcome stats) ----
    print(f"Analysis table -> {OUT/'ds003522_s1_analysis_table.csv'}  shape={df.shape}")
    print(f"\nOutcome S3_NSI_Total (n={len(y)}): mean={y.mean():.1f} sd={y.std(ddof=1):.1f} "
          f"median={np.median(y):.0f} range={y.min():.0f}-{y.max():.0f}")
    print(f"skewness={skew:.2f} -> primary outcome scale = "
          f"{'log1p(NSI)' if use_log else 'raw NSI'} (rule: |skew|>1 -> log1p)")
    print("\nPredictor availability (non-null counts):")
    for c in list(REST_MAP.values()) + list(ERP_MAP.values()) + ["Age", "Sex"]:
        print(f"  {c:30s} {int(df[c].notna().sum())}/{len(df)}")

    # complete-case N per locked model
    prim = ["Global_Aperiodic_Exponent", "Posterior_IAF", "P3b_Amplitude", "Age", "Sex"]
    panel = ["Global_Aperiodic_Exponent", "Posterior_IAF", "Frontal_Theta_Alpha_Ratio",
             "Occipital_Relative_Alpha", "P3b_Amplitude", "P3b_Latency",
             "P3a_Amplitude", "P3a_Latency", "Age", "Sex"]
    rest_m = ["Global_Aperiodic_Exponent", "Posterior_IAF", "Frontal_Theta_Alpha_Ratio",
              "Occipital_Relative_Alpha", "Age", "Sex"]
    erp_m = ["P3b_Amplitude", "P3b_Latency", "P3a_Amplitude", "P3a_Latency", "Age", "Sex"]
    print("\nLocked-model N (complete-case AND §3 usability gates applied):")
    for name, cset, needs_erp in [
            ("primary (parsimonious)", prim, True),
            ("secondary/transparency (full panel)", panel, True),
            ("supportive resting-only", rest_m, False),
            ("supportive ERP-only", erp_m, True)]:
        mask = df[cset + ["S3_NSI_Total"]].notna().all(axis=1) & df["ec_rest_reliable"]
        if needs_erp:
            mask = mask & df["erp_reliable"]
        print(f"  {name:38s} n={int(mask.sum())}")
    print("\nERP-reliable subjects:", int(df.erp_reliable.sum()),
          "| ERP-unreliable excluded:",
          df.loc[~df.erp_reliable, "Original_ID"].tolist())
    print("fold sizes (full cohort A):", df.fold.value_counts().sort_index().to_dict())


if __name__ == "__main__":
    main()
