# Table S8. Prespecified sensitivity battery

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
