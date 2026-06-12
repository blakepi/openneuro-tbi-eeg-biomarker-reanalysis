#!/usr/bin/env python
"""
09_feature_qc_summary.py
========================
Phase 3, Task 4: summarize missingness and distributions of the extracted rest + ERP
features, and flag subjects / features with insufficient usable data.

STRICT scope: this script does NOT read NSI/Rivermead or any outcome, does NOT test
feature-outcome associations, and does NOT train models. It only describes the feature
matrix itself.

Usability thresholds (pre-registered, data-quality only):
    rest: a condition (EC/EO) is reliable only with >= 40 s usable signal
    erp : P3b needs >= 15 retained Target epochs; P3a needs >= 15 retained Novel epochs

Outputs:
    outputs/features/ds003522_s1_feature_qc_summary.csv   one row per feature: missing + distribution
    outputs/features/ds003522_s1_subject_usability.csv     one row per subject: usability flags
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from _eeg_common import FEAT_DIR

REST_MIN_USABLE_S = 40.0
ERP_MIN_TARGET = 15
ERP_MIN_NOVEL = 15


def feature_distribution(df: pd.DataFrame, kind: str) -> pd.DataFrame:
    rows = []
    n = len(df)
    for col in df.columns:
        if col == "subject":
            continue
        s = pd.to_numeric(df[col], errors="coerce")
        nn = int(s.notna().sum())
        rows.append({
            "feature": col, "kind": kind, "n_subjects": n, "n_nonnull": nn,
            "n_missing": n - nn, "pct_missing": round(100 * (n - nn) / n, 1),
            "mean": round(float(s.mean()), 4) if nn else np.nan,
            "sd": round(float(s.std()), 4) if nn > 1 else np.nan,
            "min": round(float(s.min()), 4) if nn else np.nan,
            "median": round(float(s.median()), 4) if nn else np.nan,
            "max": round(float(s.max()), 4) if nn else np.nan,
            "high_missing_flag": (n - nn) / n > 0.2,
        })
    return pd.DataFrame(rows)


def subject_usability(rest: pd.DataFrame, erp: pd.DataFrame) -> pd.DataFrame:
    rows = []
    erp_idx = erp.set_index("subject")
    for _, r in rest.iterrows():
        sub = r["subject"]
        ec_s = r.get("rest_EC_usable_s", np.nan)
        eo_s = r.get("rest_EO_usable_s", np.nan)
        e = erp_idx.loc[sub] if sub in erp_idx.index else None
        n_tgt = int(e["erp_n_target_kept"]) if e is not None and pd.notna(e.get("erp_n_target_kept")) else 0
        n_nov = int(e["erp_n_novel_kept"]) if e is not None and pd.notna(e.get("erp_n_novel_kept")) else 0
        erp_status = e["erp_status"] if e is not None else "MISSING"
        flags = []
        if not (ec_s >= REST_MIN_USABLE_S):
            flags.append("REST_EC_LOW")
        if not (eo_s >= REST_MIN_USABLE_S):
            flags.append("REST_EO_LOW")
        if erp_status != "OK":
            flags.append("ERP_NO_EVENTS")
        else:
            if n_tgt < ERP_MIN_TARGET:
                flags.append("P3b_LOW_TRIALS")
            if n_nov < ERP_MIN_NOVEL:
                flags.append("P3a_LOW_TRIALS")
        rows.append({
            "subject": sub,
            "rest_EC_usable_s": ec_s, "rest_EO_usable_s": eo_s,
            "erp_status": erp_status, "erp_target_kept": n_tgt, "erp_novel_kept": n_nov,
            "rest_usable": ec_s >= REST_MIN_USABLE_S and eo_s >= REST_MIN_USABLE_S,
            "erp_usable": erp_status == "OK" and n_tgt >= ERP_MIN_TARGET and n_nov >= ERP_MIN_NOVEL,
            "flags": ";".join(flags),
        })
    return pd.DataFrame(rows)


def main() -> None:
    rest = pd.read_csv(FEAT_DIR / "ds003522_s1_rest_features.csv")
    erp = pd.read_csv(FEAT_DIR / "ds003522_s1_erp_features.csv")

    feat_summary = pd.concat([feature_distribution(rest, "rest"),
                              feature_distribution(erp, "erp")], ignore_index=True)
    out1 = FEAT_DIR / "ds003522_s1_feature_qc_summary.csv"
    feat_summary.to_csv(out1, index=False)

    usability = subject_usability(rest, erp)
    out2 = FEAT_DIR / "ds003522_s1_subject_usability.csv"
    usability.to_csv(out2, index=False)

    # ---- console report ----
    print(f"Feature QC: {len(feat_summary)} features summarized -> {out1.name}")
    hi = feat_summary[feat_summary.high_missing_flag]
    print(f"  features with >20% missing: {len(hi)}")
    if len(hi):
        print("   ", hi.feature.tolist())

    print(f"\nSubject usability ({len(usability)} subjects) -> {out2.name}")
    print(f"  rest usable (EC&EO >= {REST_MIN_USABLE_S:.0f}s): "
          f"{int(usability.rest_usable.sum())}/{len(usability)}")
    print(f"  erp usable (>= {ERP_MIN_TARGET} target & novel): "
          f"{int(usability.erp_usable.sum())}/{len(usability)}")
    print(f"  both usable: {int((usability.rest_usable & usability.erp_usable).sum())}/{len(usability)}")
    flagged = usability[usability["flags"].fillna("") != ""]
    if len(flagged):
        print("\n  flagged subjects:")
        print(flagged[["subject", "rest_EC_usable_s", "rest_EO_usable_s",
                       "erp_target_kept", "flags"]].to_string(index=False))


if __name__ == "__main__":
    main()
