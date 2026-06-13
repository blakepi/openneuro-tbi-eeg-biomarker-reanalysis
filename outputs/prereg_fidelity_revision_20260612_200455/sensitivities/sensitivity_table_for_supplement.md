# Supplementary Table: Prespecified Sensitivity Battery

| Sensitivity | Status | n | Adjusted R2 | OOF R2 | Conclusion changed | Notes |
|---|---|---:|---:|---:|---|---|
| robust_HC3_primary | already_computed | 21 | -0.186 |  | False | HC3 p-values ranged from 0.643 to 0.967; inference remained null. |
| estimator_primary_parsimonious | already_computed | 21 | -0.186 | -1.382 | False | Frozen Phase 6 output; retained as estimator sensitivity context. |
| estimator_transparency_full_OLS | already_computed | 21 | -0.220 | -3.576 | False | Frozen Phase 6 output; retained as estimator sensitivity context. |
| estimator_secondary_elasticnet | already_computed | 21 |  | -0.055 | False | Frozen Phase 6 output; retained as estimator sensitivity context. |
| erp_metric_peak_primary | run | 21 | -0.195 | -1.596 | False | P3b peak amplitude replaced the mean-window P3b primary metric. |
| eyes_open_primary_combined | run | 17 | 0.174 | -0.719 | False | Eyes-open analogues replaced the eyes-closed resting predictors; EO >=40 s required. |
| mice_predictor_imputation_primary | run | 25 |  | -0.999 | False | Predictors only imputed; outcome was not imputed. Rubin-pooled coefficients and in-fold iterative-imputer OOF metrics reported. |
| erp_low_trial_subjects_included | run | 24 | -0.137 | -1.259 | False | Subjects with numeric ERP features but below locked trial-count reliability floor were included; sub-040 remained unavailable. |
| sub040_scode_recovery | not_run |  |  |  | False | Sub-040 events contain STATUS values S8/S9/S10/R12 rather than named target/novel/standard labels; exact recovery mapping was not operationalized in the locked feature pipeline. |
| added_covariates_days_gcs_loc_duration | run | 18 | -0.707 | -15.248 | False | Added locked timing/severity covariates where available; LOC duration set to 0 when LOC=0 and duration structurally missing. |
| session2_nsi_timing_primary | run | 20 | -0.126 | -1.023 | False | Supportive outcome-timing sensitivity using S2 NSI total. |
| log1p_outcome_primary | run | 21 | -0.178 | -0.968 | False | Primary predictors refit on log1p(Session-3 NSI). |
| highpass_0p1_reextract | not_run |  |  |  | False | No 0.1-Hz high-pass feature branch exists in frozen outputs; running it would require full raw reprocessing and a separate locked branch. Documented as an unexecuted registered sensitivity. |
