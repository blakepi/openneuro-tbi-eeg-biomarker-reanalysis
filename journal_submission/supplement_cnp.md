# Supplementary Material

Supplementary material for the Clinical Neurophysiology Practice submission.

---

## Supplementary Methods

## S.1 Software environment
Python 3.14.5; MNE-Python 1.12.1; specparam 2.0.0; scikit-learn 1.9.0; statsmodels 0.14.6; xgboost
3.2.0; numpy 2.4.6; pandas 3.0.3; matplotlib 3.10.9. All random seeds fixed at 42. Raw EEG was
fetched from the public OpenNeuro S3 mirror; raw files were retained unmodified and all derivatives
written to a separate processed tree.

## S.2 Identity resolution and the Original_ID 3013 collision
Each participant carries three keys: a BIDS `participant_id` (not stable across datasets), a recording
id `Original_ID` (= clinical-workbook `SubID`), and a scan-generated unique id `URSI`. We adopted
**`URSI` as the canonical `subject_uid`** because `Original_ID` 3013 maps to **two distinct URSIs**
(`M87138342` and `M87138432`, an apparent digit transposition), both labelled control. Keying on URSI
preserves both as separate records without merging potentially different people; only `M87138432` had
a clinical row, and the other was retained as EEG-only. Because both are controls, neither enters the
within-mTBI primary analysis. The clinical workbook stores `URSI` as the last five digits of the BIDS
URSI; the crosswalk records both forms (`outputs/metadata_summary_tables/crosswalk_subject_ids.csv`).
Three clinical-only subjects (recording ids 3008, 3022, 3120) had no EEG in any dataset and were
documented, not silently dropped.

## S.3 Outcome construction
Primary outcome = Session-3 NSI total = somatic + cognitive + emotional subscales; no precomputed total exists. Prespecified secondary outcomes were S3 Rivermead total, S1-to-S3 NSI change, and S1-to-S3 Rivermead change. Change scores were defined as Session 3 minus Session 1, so positive values indicate higher/worse symptom burden at Session 3 relative to Session 1. Clinical string missing-tokens ("na", "NR", "m") were mapped to missing. The transformation rule was prespecified on the **outcome distribution only**: |skewness| > 1.0 → analyse `log1p(NSI)`; observed skewness 0.85 → raw NSI retained. No binary "persistent symptoms" outcome was defined because no established threshold was available in the source documentation.

## S.4 Full preprocessing parameters (frozen; identical for all participants)
| Step | Setting |
|---|---|
| Input | EEGLAB `.set/.fdt`, 500 Hz, 65 channels (63 scalp + VEOG + EKG), online ref CPz |
| Channel typing | VEOG → EOG, EKG → ECG (excluded from referencing, montage, features) |
| Boundary handling | `boundary` → `BAD_boundary`; FIR filtering constrained within contiguous segments (segment-wise if any internal boundary; none present) |
| Notch | 60 Hz |
| Band-pass | 0.5–45 Hz, FIR (firwin) |
| Reference reconstruction | reinstate CPz (zero-filled) → standard 10–20 montage → average reference (64 EEG) |
| Bad channels | robust z of log-variance > 4, or flat; spherical-spline interpolation; reinstated reference exempt from the test |
| ERP branch | additional 40-Hz low-pass before epoching |

Bad-channel detection occurred after average rereferencing; 19/25 participants had no interpolated channels and 6/25 had 1-3 interpolated channels (CP1/CP2 or predominantly frontal-ocular/temporal sites). Per-participant logs: `data/processed/ds003522_s1/logs/`.

## S.5 Event-label handling and resting segmentation
Resting blocks were identified from `Eyes Closed/Open: Every 1000 ms` marker trains (a > 3 s gap began
a new block; block span = first to last marker + 1 s); two blocks of each condition per recording
(~120 s/condition). Oddball epochs used the curated `Standard/Target/Novel Tone` labels. One
participant (`sub-040`) lacked these curated labels — its tones were stored only as raw stimulus codes
(`S 8/9/10`) — and was excluded from ERP analyses; the non-standard code mapping was **not** inferred.

## S.6 Resting feature definitions
Welch PSD (2-s Hamming windows, 50% overlap, 1–45 Hz) on artifact-screened 2-s segments (rejection at
150 µV peak-to-peak), averaged within frontal/central/parietal/occipital/global regions. Bands: delta
1–4, theta 4–8, alpha 8–12, beta 13–30 Hz. Relative power normalized to 1–45 Hz total. Posterior IAF =
7–13 Hz peak of the mean parietal–occipital eyes-closed spectrum (undefined when no clear peak).
Aperiodic exponent/offset via specparam 2.0.0 using SpectralModel with fixed aperiodic mode, 1-40 Hz fit range, peak width limits 1-8 Hz, maximum six peaks, minimum peak height 0.0, and peak threshold 2.0. Aperiodic R2 was exported for each condition and region; no EC/EO aperiodic R2 fields were missing in the feature matrix, and no aperiodic spectra were excluded as unfit in the frozen outputs. Across exported EC/EO regional/global fits, R2 ranged from 0.7349 to 0.9984; 3/250 exported fits were below 0.90 and 1/250 was below 0.80. The primary EC global fit R2 ranged from 0.9202 to 0.9975 (mean 0.9863). No separate fit-error statistic or representative specparam model object/PSD plot was exported; Figure S5 therefore shows the exported fit-R2 distribution rather than a reconstructed model fit. Spectral entropy = Shannon entropy of the normalized 1-45 Hz PSD (exploratory).

## S.7 ERP feature definitions and reliability thresholds
Epochs −200 to +800 ms, baseline −200–0 ms, boundary-aware rejection, 150 µV peak-to-peak rejection on
EEG. P3b: target tones, parietal Pz/CPz/POz, 300–600 ms. P3a: novel tones, frontocentral Fz/FCz/Cz,
250–400 ms. N2 (200–350 ms) and a target-minus-standard difference wave were computed for context.
Each component required **≥ 15 retained Target and Novel epochs**; the resting reliability floor was
**≥ 40 s** of clean signal per condition (eyes-closed met for all 25; eyes-open for 22).

## S.8 Leakage-prevention implementation
Subject-level 5-fold cross-validation folds were stratified on Session-3 NSI tertiles (seed 42) and
**frozen before EEG processing** (`outputs/splits/frozen_cv_folds.csv`, MD5 `453fede5…`). All
standardization, imputation (sensitivity), and hyperparameter tuning were fit within training folds
via scikit-learn Pipelines; test folds saw no fitted parameter. Quality-control exclusions removed a
subject from its assigned fold only; folds were never regenerated. The outcome never informed
preprocessing or feature selection.

## S.9 Replication feasibility procedure
Session-1 `events.tsv` were scanned for eyes-closed/eyes-open rest markers and auditory-oddball
Target/Novel tones. ds005114 was scanned across all 91 recordings; ds003523 and ds003490 by sample. A
feature was deemed extractable only if its source paradigm was present
(`scripts/13_replication_feasibility.py`). No cross-paradigm feature substitution was performed.

---

## Supplementary Tables S1-S11

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

---

## Supplementary Figures S1-S5

Supplementary figures S1-S5 are provided with the submission figure files and were derived from frozen outputs. They are not used to promote exploratory analyses to confirmatory status.

## Figure S1. Primary-model partial effect diagnostics

**File:** `figures/FigureS1_partial_effects.png`

Partial/additional-variable diagnostic plots for the primary EEG predictors in the parsimonious model. These plots are included for transparency only. They should be interpreted alongside the coefficient forest plot and the leave-one-out instability diagnostics; they do not establish a stable predictor.

**Source:** `outputs/figures/fig_partial_effects.png`; model outputs in `outputs/analysis/model_coefficients.csv`.

## Figure S2. Elastic Net coefficient path

**File:** `figures/FigureS2_elasticnet_path.png`

Coefficient paths for the full-panel Elastic Net. The selected penalty shrank all ten predictors to zero, leaving an intercept-only/mean-predictor model.

**Source:** `outputs/figures/fig_elasticnet_path.png`; selected coefficients in `outputs/analysis/elasticnet_coefficients.csv`.

## Figure S3. Out-of-fold calibration

**File:** `figures/FigureS3_calibration.png`

Calibration of out-of-fold predictions against observed Session-3 NSI total. Predictions are compressed toward the cohort mean, consistent with the negative out-of-fold R2 values.

**Source:** `outputs/figures/fig_calibration.png`; predictions in `outputs/analysis/oof_predictions.csv`.

## Figure S4. Resting-versus-ERP contribution diagnostic

**File:** `figures/FigureS4_family_contribution.png`

Descriptive family-level contribution display for the full-panel analysis. This figure is exploratory/transparency material only and should not be read as evidence of a stable family-level biomarker.

**Source:** `outputs/figures/fig_family_contribution.png`; model outputs in `outputs/analysis/model_coefficients.csv`.

## Figure S5. specparam fit-quality distribution

**File:** `figures/FigureS5_specparam_fit_quality.png`

Histogram of exported EC/EO regional/global specparam fit R2 values. This is a QC visualization only; it is not a reconstructed representative model fit because PSD/model objects were not exported by the locked feature pipeline.

**Source:** `outputs/prereg_fidelity_revision_20260612_200455/specparam_qc/specparam_fit_r2_distribution.png`.

Supplementary figure image files are included in the submission figure package:
- FigureS1_partial_effects.png
- FigureS2_elasticnet_path.png
- FigureS3_calibration.png
- FigureS4_family_contribution.png
- FigureS5_specparam_fit_quality.png

---

## Final Locked Analysis Plan

### Early Resting-State and Task-Evoked EEG Biomarkers of Later Session-3 NSI Symptom Burden Following Mild Traumatic Brain Injury: A Leakage-Safe Longitudinal Reanalysis of a Public OpenNeuro Dataset

**Lock version:** 1.0 (Phase 3.6 final lock)
**Date locked:** 2026-06-11
**Lock declaration:** This document permanently fixes the analysis plan **before** any
feature–outcome association or predictive model has been computed. As of the lock date: the cohort
is final, identity leakage is resolved, subject-level cross-validation folds are frozen, EEG
preprocessing is complete, resting-state and ERP features are extracted, the feature files have
been verified to contain **no** outcome information, **no** outcome model has been fit, and **no**
EEG-feature/clinical-outcome association has been inspected. Any deviation after this date will be
reported as a transparent, dated amendment with justification.

**Canonical status:** This is the preregistration supplement of record. The working file
`reports/statistical_analysis_plan.md` (v1.1) is substantively identical; where any wording
differs, **this document governs.**

**Primary dataset:** OpenNeuro ds003522 (discovery). ds005114 and ds003523 are reserved for
**future** independent replication and are not analysed against the outcome here.

---

## 1. Final hypotheses

**Primary (H1).** Among adults with acute mTBI, a compact, biologically motivated panel of
Session-1 EEG features is associated with later Session-3 NSI symptom burden
(Session-3 NSI total), over and above age and sex.

The **primary confirmatory test** of H1 is a parsimonious linear model carrying one biomarker per
biological domain: the resting **global aperiodic exponent**, the resting **posterior IAF**, and
the task-evoked **P3b amplitude**, adjusted for age and sex (§7).

**Pre-registered directional expectations** (two-sided tests for inference; directions stated for
interpretation, literature in places mixed):

| Predictor | Expected direction vs. higher S3 NSI total |
|---|---|
| Global aperiodic exponent | lower (flatter) → higher symptoms |
| Posterior IAF | lower (alpha slowing) → higher symptoms |
| P3b amplitude | lower → higher symptoms |
| P3b latency | longer → higher symptoms |
| P3a amplitude | lower → higher symptoms |
| P3a latency | longer → higher symptoms |
| Frontal theta/alpha ratio | higher → higher symptoms |
| Occipital relative alpha | lower → higher symptoms |

**Secondary (H2–H4).** The panel is associated with S3 Rivermead total (H2), S1→S3 NSI change
(H3), and S1→S3 Rivermead change (H4).

**Exploratory (H5).** Spectral entropy adds incremental information; flexible learners capture
non-linearities beyond the linear panel.

---

## 2. Final cohort

- **Unit / split key:** `subject_uid` = full BIDS URSI (canonical person key; `Original_ID` is not
  used because value 3013 collides across two URSIs).
- **Primary analytic cohort:** acute-mTBI participants (ds003522 `Group == 0`) with a usable
  Session-1 EEG recording and a non-missing Session-3 NSI total — **n = 25**, frozen as cohort
  `A_ds003522` in `outputs/splits/frozen_cv_folds.csv`.
- **Effective N by modality:** resting (eyes-closed) **25**; ERP **21**; combined panel **20**.

---

## 3. Final inclusion / exclusion criteria

**Include:** acute mTBI; Session-1 EEG passing read QC; Session-3 NSI total present; unique
`subject_uid`.

**Exclude (accounted for in the CONSORT flow, Figure 1):**
- Chronic-TBI arm (`Group == 2`, n = 25) — single session, no longitudinal outcome.
- Controls (`Group == 1`) — not in within-mTBI prediction (reference/exploratory only; no control
  EEG processed here).
- `sub-040` — **ERP models only**; oddball tones stored as raw stimulus codes without curated
  `trial_type` labels (mapping not guessed). Retained for resting models.
- ERP reliability floor — < 15 retained Target **or** Novel epochs excludes from ERP models
  (`sub-020`, `sub-036`, `sub-058`); retained for resting models.
- Resting reliability floor — a resting condition with < 40 s clean signal is treated as missing
  for that condition (eyes-open only: `sub-020`, `sub-058`, `sub-068`).

**Absolute rule:** QC exclusions remove a subject from its **already-assigned fold in place**;
folds are never regenerated or rebalanced.

---

## 4. Final outcomes

| Tier | Outcome | Definition |
|---|---|---|
| **Primary** | **S3 NSI total** | `NSIsoma + NSIcog + NSIemo` at Session 3 (computed; continuous) |
| Secondary | S3 Rivermead total | `RivermeadTotal` at Session 3 |
| Secondary | NSI change | `NSItotal(S3) − NSItotal(S1)` |
| Secondary | Rivermead change | `RivermeadTotal(S3) − RivermeadTotal(S1)` |

**No binary "persistent symptoms" outcome** is defined: source documentation provides no validated
NSI/Rivermead threshold, and none is invented. The continuous NSI total remains primary in all
circumstances. Outcome transform: raw vs. `log1p(NSI)` decided from the **outcome distribution
only** (no predictor/feature–outcome information).

---

## 5. Final predictors (LOCKED panel)

Session-1 features, primary resting condition = **Eyes Closed (EC)**, primary ERP amplitude metric
= **mean-window amplitude** (peak amplitude = sensitivity metric).

**Primary resting-state feature family:**
1. Posterior IAF — `rest_EC_iaf_posterior_hz`
2. Global aperiodic exponent — `rest_EC_global_aper_exponent`
3. Frontal theta/alpha ratio — `rest_EC_frontal_theta_alpha_ratio`
4. Occipital relative alpha power — `rest_EC_occipital_alpha_rel`

**Primary ERP feature family:**
5. P3b amplitude — `erp_P3b_target_par_mean_uv` (sensitivity: `erp_P3b_target_par_peak_uv`)
6. P3b latency — `erp_P3b_target_par_lat_ms`
7. P3a amplitude — `erp_P3a_novel_fc_mean_uv` (sensitivity: `erp_P3a_novel_fc_peak_uv`)
8. P3a latency — `erp_P3a_novel_fc_lat_ms`

**Exploratory only:** Spectral entropy — `rest_EC_global_spec_entropy`.

**No additional EEG feature may enter the primary analyses.** Any other extracted feature is
exploratory and labelled as such.

**Covariates (fixed, no data-driven search):** age, sex. Sensitivity-only covariates: time since
injury, GCS / LOC duration, and S1 baseline symptom level (change models).

---

## 6. Final preprocessing decisions

**Primary pipeline (LOCKED, applied identically to all participants, outcome-blind):** MNE-Python
1.12; boundary-aware (`boundary`→`BAD_boundary`, segment-wise filtering guard); VEOG→EOG, EKG→ECG;
60-Hz notch; **band-pass 0.5–45 Hz**; reinstate CPz → standard 10–20 montage → **average
reference**; within-participant bad-channel detection (robust z of log-variance > 4) →
spherical-spline interpolation (reinstated reference exempt). ERP branch adds a **40-Hz low-pass**
before epoching.

Resting features: EC/EO blocks segmented from marker trains; 2-s segments rejected at 150 µV p2p;
Welch PSD (2-s windows, 50 % overlap, 1–45 Hz); bands δ1–4, θ4–8, α8–12, β13–30 Hz; specparam 2.0
aperiodic fit (fixed mode, 1–40 Hz); posterior IAF as the 7–13-Hz peak of the parietal–occipital
EC spectrum.

ERP features: epochs −200–800 ms, baseline −200–0 ms, boundary-aware, 150 µV p2p rejection; P3b
(target, Pz/CPz/POz, 300–600 ms), P3a (novel, Fz/FCz/Cz, 250–400 ms), N2 (200–350 ms);
mean-window and peak amplitude and peak latency; target-minus-standard parietal difference wave.

**Preprocessing robustness (sensitivity only):** the entire pipeline is **repeated with a 0.1-Hz
high-pass** (vs. the locked 0.5-Hz) and features re-extracted, to confirm stability of the slow
P3 components and the low-frequency spectral measures. This is documented strictly as a
**sensitivity analysis**; the 0.5–45-Hz pipeline remains primary, and the change is parameter-only
(no outcome involvement).

---

## 7. Final statistical hierarchy (LOCKED)

Four tiers; tier assignment is fixed and never upgraded on the basis of a result.

| Tier | Model | Specification | N |
|---|---|---|---|
| **Primary confirmatory** | Parsimonious linear regression | `S3_NSI_Total ~ Global_Aperiodic_Exponent + Posterior_IAF + P3b_Amplitude + Age + Sex` | 20 |
| **Secondary confirmatory** | Elastic Net | full locked panel (8 EEG) + Age + Sex; λ, α by nested CV on frozen folds | 20 |
| **Transparency (descriptive only)** | Full 10-term OLS | full locked panel (8 EEG) + Age + Sex, unpenalized — **flagged potentially overfit; NOT used for primary inferential claims** | 20 |
| **Exploratory** | Ridge, LASSO, Random Forest, XGBoost | full locked panel + covariates; nested CV on frozen folds | 20 |

**Reporting for every model:** standardized β coefficients, 95 % confidence intervals, p-values
(Benjamini–Hochberg FDR-controlled within the 8-predictor family), adjusted R², effect sizes
(partial R² / Cohen's f²), and VIF. Predictive performance: out-of-fold R²/MAE from the frozen
5-fold CV with bootstrap CIs; the headline contrast is **EEG panel vs. age+sex baseline**.
Supportive context: domain-specific resting (n = 25) and ERP (n = 21) linear models.

**Rationale for the parsimonious primary model:** the full 10-term specification (8 EEG + age +
sex) exceeds the events-per-variable supportable at n = 20; carrying one biomarker per biological
domain keeps the confirmatory model interpretable and adequately conditioned, while the Elastic Net
(secondary) and full OLS (transparency) preserve a full-panel view.

---

## 8. Leakage-prevention rules (ABSOLUTE)

1. **Folds immutable** — `frozen_cv_folds.csv` (5-fold, stratified on S3-NSI tertiles, seed 42)
   is never regenerated, reshuffled, or rebalanced.
2. **Split unit = `subject_uid` (URSI)** — no subject appears in more than one fold.
3. **Fold-internal fitting only** — standardization, imputation, dimensionality reduction, penalty
   (λ/α) selection, and the outcome-transform decision are fit on training data and applied to
   held-out data; never the reverse.
4. **Outcome never touches upstream steps** — preprocessing parameters and the locked feature
   panel were fixed without any outcome; feature selection is pre-registered, not data-driven.
5. **QC exclusions are fold-local** — a subject failing usability QC is removed from its assigned
   fold only.
6. **Auditability** — `crosswalk_subject_ids.csv` + frozen folds let a reviewer verify no person
   leaks across folds.

---

## 9. Missing-data strategy

- **Outcome never imputed.** Present for all 25 by eligibility.
- **Primary:** complete-case within each model's eligible N (resting 25, ERP 21, combined 20),
  reported via CONSORT flow.
- **Sensitivity:** MICE of **predictors only**, fit **within training folds**, pooled by Rubin's
  rules; compared to complete-case. Test-fold and outcome data never inform imputation.
- **Attrition check:** descriptive comparison of S1 characteristics (incl. EEG predictors) for S3
  completers vs. non-completers; if they differ, discuss bias and add an
  inverse-probability-of-attrition-weighted sensitivity model.

---

## 10. Sensitivity analyses (pre-specified)

1. Estimator: parsimonious OLS vs. Elastic Net vs. full OLS.
2. ERP metric: mean-window (primary) vs. peak amplitude/latency.
3. Resting condition: eyes-closed (primary) vs. eyes-open (n = 22).
4. Missing data: complete-case vs. MICE.
5. ERP reliability: with vs. without the 3 low-trial subjects; with vs. without an S-code recovery
   of `sub-040`.
6. Covariates: add time-since-injury and injury severity (GCS/LOC) where available.
7. Outcome timing: S2 NSI total (less attrition, larger N) as supportive replication.
8. Outcome transform: raw vs. `log1p` NSI.
9. **Preprocessing high-pass:** re-extract under 0.1-Hz high-pass (vs. locked 0.5-Hz) — §6.

All sensitivity analyses use the same frozen folds and leakage rules.

---

## 11. Exploratory analyses (after primary analyses only)

- **Exploratory penalized linear:** Ridge and LASSO over the full panel + covariates (compared to
  the secondary-confirmatory Elastic Net).
- **Spectral entropy** added to resting/combined models.
- **Flexible learners:** Random Forest and XGBoost, nested CV on frozen folds, interpreted with
  permutation importance / SHAP — clearly exploratory, not central to conclusions.
- **Secondary outcomes:** Rivermead total and S1→S3 change scores.
- **Region/band exploration** beyond the locked panel — FDR-controlled, hypothesis-generating.
- **Group comparisons** (mTBI vs. control vs. chronic) deferred to future work (requires
  processing control/chronic EEG).

---

## 12. Estimation philosophy

- **Effect sizes and confidence intervals are primary;** interpretation is anchored to estimates
  and their intervals, not to thresholds.
- **De-emphasize binary significance testing;** p-values (FDR-controlled) are one continuous piece
  of evidence. Non-significance is never read as evidence of no effect.
- **Standardized coefficients** are reported (predictors z-scored within folds) for cross-predictor
  comparison; raw-scale coefficients supplied for interpretability.
- **Predictive uncertainty is reported honestly:** out-of-fold R²/MAE with bootstrap CIs, expected
  to be wide at n ≈ 20; the headline is EEG-vs-(age+sex) improvement with its uncertainty.
- **ML performance metrics are supportive, not definitive;** no central conclusion rests on an ML
  accuracy figure.
- **Calibrated claims:** all findings are hypothesis-generating associations in a small discovery
  cohort requiring independent replication, not a validated prognostic tool.

---

## 13. Reproducibility

Python 3.14; MNE 1.12, specparam 2.0, scikit-learn 1.9, statsmodels, numpy, pandas; seeds fixed
(42). Frozen folds, feature files, per-subject preprocessing logs, and all scripts are version-
controlled and released with the manuscript. **No outcome model is run until this plan is locked
(it is, as of the lock date above).**

Post-analysis Phase 6 reproducibility audit: the frozen outputs were regenerated in
`outputs/reanalysis_audit_20260612_115010/` without overwriting originals; all 25 analytic
ds003522 Session-1 `.set/.fdt` pairs were data-readable with MNE; all 44 prespecified numeric checks
matched; and replication-feasibility conclusions were unchanged. The only non-exact artifact was the
expected non-scientific `--dry-run` download-manifest difference.

---

### Lock checklist (all true at lock date)
- [x] Cohort finalized (n = 25; modality N: rest 25 / ERP 21 / combined 20).
- [x] Identity leakage resolved (`subject_uid` = URSI; 3013 collision handled).
- [x] Frozen subject-level folds exist and are unchanged.
- [x] EEG preprocessing complete; features extracted.
- [x] Feature files verified to contain no outcome information.
- [x] No outcome modeling performed.
- [x] No feature–outcome association inspected.
- [x] Statistical hierarchy, predictors, preprocessing, and estimation philosophy locked.

---

## Replication Feasibility Audit

### Can the ds003522 discovery findings be replicated in ds005114?

**Date:** 2026-06-11
**Adherence statement:** The discovery analysis is **frozen and unmodified** (frozen-folds
checksum `453fede5`, feature files untouched). The locked statistical hierarchy, feature
definitions, and preprocessing were **not** changed. Cohorts were **not** combined. No exploratory
finding is promoted. The framework remains estimation-first; no causal claims are made.
Producing scripts: `13_replication_feasibility.py`, `14_replication_figures.py`.

**Headline:** The designated replication cohort **ds005114 is not feature-identical under the locked
definitions**, because it contains **neither the auditory-oddball paradigm nor any embedded resting
EEG**. **0 of the 8 locked predictors are extractable with their preregistered definitions.** A
feature-identical clinical replication model is therefore **not estimable** in ds005114 (nor in
ds003523) without redefining the locked features or changing the clinical estimand. The discovery
null thus remains **untested**, not refuted, in independent data.

---

## 1. Why replication is infeasible: paradigm and state mismatch

The locked panel draws on two paradigms that exist **only** in the discovery dataset:
- the four resting features (global aperiodic exponent, posterior IAF, frontal theta/alpha ratio,
  occipital relative alpha) require **eyes-closed resting EEG**;
- the four ERP features (P3b/P3a amplitude and latency) require the **three-stimulus auditory
  oddball** (Target/Novel tones).

We scanned Session-1 event markers across the shared-program datasets
(`replication_feature_availability.csv`). The result is unambiguous:

| Dataset | Paradigm | Eyes-closed rest | Auditory oddball | Locked features extractable | Post-concussive outcome |
|---|---|:--:|:--:|:--:|:--:|
| **ds003522** (discovery) | oddball + rest, mTBI | ✓ | ✓ | **8 / 8** | ✓ (NSI) |
| **ds005114** (designated replication) | **DPX** cognitive control, mTBI | ✗ | ✗ | **0 / 8** | ✓ (NSI) |
| **ds003523** (designated replication) | **visual working memory**, TBI | ✗ | ✗ | **0 / 8** | ✓ (NSI) |
| **ds003490** (paradigm match) | oddball + rest, **Parkinson's** | ✓ | ✓ | 8 / 8 | ✗ (no PCS) |

ds005114 was scanned across **all 91** Session-1 recordings: **0/91** contain an eyes-closed/
eyes-open rest marker and **0/91** contain an auditory-oddball tone; **91/91** contain DPX
cue/probe events. ds003523 shows the same pattern. (Figure: `fig_feature_availability_matrix.png`.)

**The core problem.** The shared-cohort OpenNeuro datasets were collected by running the **same
participants through different tasks**; only ds003522 paired the auditory oddball with rest. The
datasets that retain the clinical outcome (ds005114, ds003523) use incompatible paradigms, and the
one dataset that retains the paradigm (ds003490) is a Parkinson's cohort without a post-concussive
outcome. **No available dataset matches both the EEG paradigm/state and the clinical outcome of the
discovery analysis.**

---

## 2. What we deliberately did NOT do (and why)

Two "replications" were technically possible but scientifically invalid, and were **rejected on
principle**:

1. **Redefining the ERP features from DPX events** (e.g., treating the DPX probe-evoked P3 as
   "P3b"). The DPX probe P3 is a different component, evoked by a different stimulus class, under a
   different task demand. Substituting it would **modify the locked feature definition** — an
   explicit prohibition — and would not constitute replication of the oddball P3b/P3a.
2. **Computing "resting" spectra from DPX task EEG** (pre-trial baselines or the continuous
   record). Eyes-closed alpha-band features (IAF, occipital relative alpha) are strongly
   **state-dependent**; eyes-open active-task EEG is a fundamentally different state. Labeling such
   measures with the locked feature names would conflate brain states and again modify the
   preregistered definitions.

Declining these is itself the point: the discipline that makes a discovery analysis credible
(fixed definitions, no flexible substitution) is the same discipline that, honestly applied, says
**this replication cannot be run** with these data.

---

## 3. Discovery estimates and their replication status

Because no replication coefficient exists, we present the frozen discovery estimates alongside an
explicit "not estimable" replication status (`replication_effect_size_comparison.csv`;
Figure `fig_discovery_vs_replication_forest.png`). This is the effect-size comparison table the
protocol requested, populated honestly:

| Predictor | Discovery std. β (95% CI) | Discovery p (FDR) | Replication in ds005114 |
|---|---:|---:|---|
| Global aperiodic exponent | −0.02 (−0.83, 0.79) | 0.96 | **Not estimable** — no eyes-closed rest |
| Posterior IAF | −0.15 (−0.83, 0.52) | 0.96 | **Not estimable** — no eyes-closed rest |
| P3b amplitude | +0.24 (−0.40, 0.88) | 0.96 | **Not estimable** — no auditory oddball |

(The full eight-feature panel is identically not estimable; the three primary-model EEG terms are
shown for brevity.) Direction agreement, calibration transfer, and out-of-sample predictive
performance in replication are all **undefined**, because the predictors cannot be measured.

**Models requested in the protocol** (primary confirmatory, Elastic Net, resting-only, ERP-only)
were **not fit in ds005114**: each requires predictors that do not exist in that dataset. Fitting
them would require fabricated or redefined inputs and is therefore not reported.

---

## 4. The appropriate replication target (for future work)

A valid replication requires a dataset with **both** (a) the three-stimulus auditory oddball **and**
embedded eyes-closed/eyes-open rest, **and** (b) an acute-mTBI sample with a longitudinal
post-concussive symptom outcome (e.g., NSI/Rivermead). Among public data:
- **ds003490** satisfies (a) exactly (it is the same paradigm, named in the ds003522 descriptor)
  but fails (b) — it is a Parkinson's cohort. It is nonetheless suitable for a **feature-level
  pipeline check** (confirming the extraction pipeline yields physiologically plausible features in
  an independent sample), which we describe as possible future work, clearly distinct from an outcome
  replication.
- No surveyed dataset satisfies both. A prospective or retrospective mTBI cohort with the matched
  paradigm would be required.

---

## 5. Interpretation (estimation-first)

1. **The discovery null is neither supported nor refuted.** It remains the single available
   estimate, with wide intervals (§3), and is now shown to be **not yet independently testable**
   with matched data.
2. **This is a finding about the evidence base, not just this study.** Within a single
   well-organized research program, the public datasets do not necessarily support feature-identical EEG-biomarker replication because
   they deploy different paradigms and only one includes rest. The
   apparent availability of "three mTBI EEG datasets" overstates the replication resource: for any
   given feature panel, typically only one is usable.
3. **Implication for the discovery result.** A pre-registered, leakage-safe discovery analysis
   produced a null/inconclusive result that the field's existing public data **cannot currently
   challenge or corroborate**. Claims (positive or negative) about these EEG biomarkers should be
   held as provisional pending a matched-paradigm, adequately powered replication.

---

## 6. Limitations

- The feasibility assessment is based on **event-marker presence**; it is definitive for paradigm
  availability but does not, by itself, evaluate signal quality in ds005114 (moot, since the
  paradigms are absent).
- We did not attempt a cross-paradigm "construct" replication (e.g., DPX-evoked control ERPs vs.
  oddball ERPs); such an analysis would test a **different** hypothesis and is outside the locked
  plan.
- The conclusion is specific to the surveyed public datasets; other (non-public or future)
  mTBI oddball+rest cohorts may exist.

---

### Artifacts
`outputs/analysis/replication_feature_availability.csv`,
`outputs/analysis/replication_effect_size_comparison.csv`;
`outputs/figures/fig_discovery_vs_replication_forest.png`,
`outputs/figures/fig_feature_availability_matrix.png`.
