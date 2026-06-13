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



## Table S7. Prespecified secondary outcomes
| Outcome | n | Key EEG term | Std beta (95% CI) | p (FDR) | adj R2 | OOF R2 | Interpretation |
|---|---:|---|---:|---:|---:|---:|---|
| S3 Rivermead total | 19 | P3b Amplitude | 0.33 (-0.27 to 0.93) | 0.363 | 0.010 | -0.270 | No interval excluded zero. |
| S1-to-S3 NSI change | 21 | P3b Amplitude | 0.42 (-0.19 to 1.03) | 0.698 | -0.103 | -0.967 | No interval excluded zero. |
| S1-to-S3 Rivermead change | 19 | P3b Amplitude | 0.66 (0.21 to 1.11) | 0.035 | 0.450 | 0.248 | Secondary, hypothesis-generating association; change was defined as Session 3 minus Session 1, so positive values indicate higher/worse symptom burden at Session 3. Interpret cautiously and replicate. |

## Table S8. Prespecified sensitivity battery
| Sensitivity | Status | n | adj R2 | OOF R2 | Interpretation |
|---|---|---:|---:|---:|---|
| robust_HC3_primary | already_computed | 21 | -0.186 |  | HC3 p-values ranged from 0.643 to 0.967; inference remained null. |
| erp_metric_peak_primary | run | 21 | -0.195 | -1.596 | P3b peak amplitude replaced the mean-window P3b primary metric. |
| eyes_open_primary_combined | run | 17 | 0.174 | -0.719 | Eyes-open analogues replaced the eyes-closed resting predictors; EO >=40 s required. |
| mice_predictor_imputation_primary | run | 25 |  | -0.999 | Predictors only imputed; outcome was not imputed. Rubin-pooled coefficients and in-fold iterative-imputer OOF metrics reported. |
| erp_low_trial_subjects_included | run | 24 | -0.137 | -1.259 | Subjects with numeric ERP features but below locked trial-count reliability floor were included; sub-040 remained unavailable. |
| added_covariates_days_gcs_loc_duration | run | 18 | -0.707 | -15.248 | Added locked timing/severity covariates where available; LOC duration set to 0 when LOC=0 and duration structurally missing. |
| session2_nsi_timing_primary | run | 20 | -0.126 | -1.023 | Supportive outcome-timing sensitivity using S2 NSI total. |
| log1p_outcome_primary | run | 21 | -0.178 | -0.968 | Primary predictors refit on log1p(Session-3 NSI). |
| sub040_scode_recovery | not_run |  |  |  | Sub-040 events contain STATUS values S8/S9/S10/R12 rather than named target/novel/standard labels; exact recovery mapping was not operationalized in the locked feature pipeline. |
| highpass_0p1_reextract | not_run |  |  |  | No 0.1-Hz high-pass feature branch exists in frozen outputs; running it would require full raw reprocessing and a separate locked branch. Documented as an unexecuted registered sensitivity. |

## Table S9. S3 completers versus non-completers
| Baseline variable | Completers | Non-completers | SMD | descriptive p |
|---|---:|---:|---:|---:|
| Age | 28.08 (10.08) | 27.68 (9.70) | 0.04 | 0.896 |
| Sex (recorded female=1) | 0.28 | 0.42 | -0.30 |  |
| Session-1 NSI total | 21.04 (19.68) | 23.00 (19.08) | -0.10 | 0.741 |
| Session-1 Rivermead total | 21.32 (13.36) | 23.17 (13.48) | -0.14 | 0.659 |
| Days since injury at Session 1 | 9.64 (3.71) | 11.00 (3.21) | -0.39 | 0.201 |
| GCS | 14.95 (0.21) | 14.64 (0.74) | 0.64 | 0.149 |
| Loss of consciousness | 0.92 | 1.00 | -0.42 |  |

## Table S10. specparam fit quality
| Scope | n | min | median | mean | IQR | count <0.90 | count <0.80 |
|---|---:|---:|---:|---:|---:|---:|---:|
| rest_EC_frontal_aper_r2 | 25 | 0.930 | 0.994 | 0.986 | 0.014 | 0 | 0 |
| rest_EC_central_aper_r2 | 25 | 0.871 | 0.990 | 0.977 | 0.022 | 1 | 0 |
| rest_EC_parietal_aper_r2 | 25 | 0.965 | 0.992 | 0.990 | 0.008 | 0 | 0 |
| rest_EC_occipital_aper_r2 | 25 | 0.964 | 0.989 | 0.987 | 0.007 | 0 | 0 |
| rest_EC_global_aper_r2 | 25 | 0.920 | 0.994 | 0.986 | 0.008 | 0 | 0 |
| rest_EO_frontal_aper_r2 | 25 | 0.877 | 0.987 | 0.975 | 0.017 | 1 | 0 |
| rest_EO_central_aper_r2 | 25 | 0.735 | 0.988 | 0.973 | 0.010 | 1 | 1 |
| rest_EO_parietal_aper_r2 | 25 | 0.964 | 0.992 | 0.991 | 0.005 | 0 | 0 |
| rest_EO_occipital_aper_r2 | 25 | 0.956 | 0.990 | 0.988 | 0.005 | 0 | 0 |
| rest_EO_global_aper_r2 | 25 | 0.930 | 0.989 | 0.984 | 0.013 | 0 | 0 |

## Table S11. Locked-plan execution notes
| Issue | Resolution |
|---|---|
| n = 20 vs n = 21 | The primary eyes-closed/ERP model retained n = 21; the n = 20 analysis is the eyes-open-low sensitivity excluding sub-068. |
| 0.1-Hz high-pass sensitivity | No frozen 0.1-Hz branch existed; full raw reprocessing was not used to replace the locked 0.5-Hz pipeline. |
| sub-040 S-code recovery | Events were not named Target/Novel/Standard and the locked extractor did not operationalize a recovery mapping. |
| IPW attrition sensitivity | Descriptive attrition comparison was completed; no hard imbalance trigger was specified in the locked plan, so IPW was not invented post hoc. |
