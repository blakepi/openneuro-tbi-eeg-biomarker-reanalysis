# Supplementary Tables

## Table S1. Full feature dictionary
The complete extracted feature set (resting features per condition [EC/EO] × region
[frontal/central/parietal/occipital/global] × band [delta/theta/alpha/beta], plus theta/alpha ratio,
spectral entropy, aperiodic exponent/offset/R², posterior IAF; and ERP P3b/P3a/N2 and
target-minus-standard mean/peak amplitude and latency with epoch counts) is provided as machine-
readable files:
- `outputs/features/ds003522_s1_rest_features.csv` (140 resting features)
- `outputs/features/ds003522_s1_erp_features.csv` (ERP features + epoch counts)
- `outputs/features/ds003522_s1_feature_qc_summary.csv` (per-feature distributions and missingness)

The eight locked confirmatory features and one exploratory feature are listed in main-text Table 3.

## Table S2. Quality-control summary (ds003522 Session-1, n = 25)
| Metric | Result |
|---|---|
| Readable in MNE | 25 / 25 |
| Sampling frequency | 500 Hz (all) |
| EEG channels | 64 after CPz reinstatement (65 recorded incl. VEOG, EKG) |
| Recording duration | median ~1022 s (range ~920–1668 s) |
| Flat / NaN / zero-filled channels | 0 |
| Dataset-marked bad channels | 0 |
| Interpolated channels per participant | 0 (19/25), 1–3 (6/25), mostly frontal-ocular |
| Eyes-closed usable ≥ 40 s | 25 / 25 |
| Eyes-open usable ≥ 40 s | 22 / 25 |
| ERP usable (≥ 15 Target & Novel epochs, tone labels) | 21 / 25 |

*Source: `outputs/qc/ds003522_s1_qc_summary.csv`, `outputs/features/ds003522_s1_subject_usability.csv`.*

## Table S3. Missingness and attrition
| Item | Value |
|---|---|
| Cohort symptom outcomes (whole UNM cohort) | ~91 (S1) → ~78 (S2) → ~62 (S3) |
| Discovery cohort outcome (S3 NSI) | complete by eligibility (n = 25) |
| Predictor missingness — resting (EC) | 0 |
| Predictor missingness — ERP | `sub-040` (no tone labels); 3 below epoch floor |
| Eyes-open posterior IAF missing | 3 (no clear EO alpha peak) |
| Covariates (age, sex) | complete |
| Excluded flagged participants | sub-020, sub-036, sub-040, sub-058 (ERP); sub-068 (EO-low only) |

*Source: `outputs/metadata_summary_tables/missingness_by_variable.csv`,
`outputs/metadata_summary_tables/attrition_by_session.csv`,
`outputs/features/ds003522_s1_subject_usability.csv`.*

## Table S4. Transparency model — full 10-term OLS (descriptive; potentially overfit)
`S3_NSI_Total ~ all 8 locked features + Age + Sex` (n = 21; in-sample R² = 0.39, adjusted R² = −0.22;
design condition number ≈ 22,000; out-of-fold R² = −3.58). **Not used for inference.**

| Predictor | β (raw) | Std. β | 95% CI (std.) | p | p (FDR) |
|---|---:|---:|---:|---:|---:|
| Global aperiodic exponent | −16.11 | −0.21 | −1.17 to 0.76 | 0.64 | 0.80 |
| Posterior IAF | −4.23 | −0.25 | −1.34 to 0.83 | 0.62 | 0.80 |
| Frontal theta/alpha ratio | −26.33 | −1.02 | −2.39 to 0.35 | 0.13 | 0.80 |
| Occipital relative alpha | −68.59 | −0.86 | −2.20 to 0.48 | 0.18 | 0.80 |
| P3b amplitude | 0.57 | 0.07 | −0.70 to 0.83 | 0.85 | 0.85 |
| P3b latency | 0.02 | 0.11 | −0.55 to 0.77 | 0.72 | 0.80 |
| P3a amplitude | −3.41 | −0.46 | −1.33 to 0.41 | 0.27 | 0.80 |
| P3a latency | −0.06 | −0.17 | −0.94 to 0.60 | 0.64 | 0.80 |
| Age | −0.59 | −0.39 | −1.57 to 0.78 | 0.47 | 0.80 |
| Sex | 12.71 | 0.35 | −0.49 to 1.19 | 0.37 | 0.80 |

*All intervals span zero; no FDR p < 0.80. Estimates are unstable (severe multicollinearity) and are
shown only to make the overfitting of the unpenalized full model explicit. Source:
`outputs/analysis/model_coefficients.csv`.*

## Table S5. Exploratory and supportive model performance
See main-text Table 4B (all models, out-of-fold R²/MAE). Exploratory penalized (ridge, LASSO) and
flexible (random forest, XGBoost) learners all produced negative out-of-fold R² (−0.06 to −0.36).
Source: `outputs/analysis/cv_performance.csv`.

## Table S6. Replication event-label inventory
| Dataset | Session-1 recordings scanned | Rest markers present | Oddball tones present | Task markers |
|---|---:|:--:|:--:|---|
| ds003522 (discovery) | 12 (of 25; full set verified) | Yes (12/12) | Yes (12/12) | Standard/Target/Novel Tone, Eyes Closed/Open |
| ds005114 | **91 (all)** | **No (0/91)** | **No (0/91)** | DPX: CueA/CueB, Probe_aX/aY/bY, Responses (91/91) |
| ds003523 | 12 sample | No (0/12) | No (0/12) | Visual working-memory events |
| ds003490 | sample | Yes | Yes | Standard/Target/Novel Tone, Eyes Closed/Open (Parkinson's cohort) |

*Source: `outputs/analysis/replication_feature_availability.csv`; full ds005114 scan in
`scripts/13_replication_feasibility.py` console log and `reports/phase5_replication_results.md`.*
