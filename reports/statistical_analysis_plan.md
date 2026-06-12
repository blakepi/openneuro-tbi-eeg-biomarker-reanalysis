# Statistical Analysis Plan (SAP)
### Early Resting-State and Task-Evoked EEG Biomarkers of Persistent Post-Concussive Symptoms Following Mild Traumatic Brain Injury: A Leakage-Safe Longitudinal Reanalysis of a Public OpenNeuro Dataset

**Version:** 1.1 — **LOCKED** (Phase 3.6 final lock; supersedes v1.0)
**Date:** 2026-06-11
**Status:** Pre-specified and **permanently locked before** any feature–outcome relationship has
been examined. The companion `reports/final_locked_analysis_plan.md` is the canonical
preregistration supplement; this file is the working SAP and is identical in substance. The
predictor files (`outputs/features/ds003522_s1_rest_features.csv`,
`..._erp_features.csv`) have been verified to contain no outcome information, and the
cross-validation folds (`outputs/splits/frozen_cv_folds.csv`) were frozen in Phase 2 prior to EEG
processing. This document is intended for inclusion in a pre-registration supplement.

**Primary dataset:** OpenNeuro ds003522 (discovery). ds005114 and ds003523 are reserved for
**future** replication and are not analysed against the outcome here.

---

## 1. Background and objective

The objective is **not** to maximize predictive accuracy. It is to identify **clinically
interpretable, biologically motivated** early EEG biomarkers associated with persistent
post-concussive symptom burden after acute mild traumatic brain injury (mTBI). Analyses
prioritize simple, explainable models, pre-registration, and leakage-safe design over algorithmic
complexity. Machine-learning models are explicitly secondary/exploratory.

---

## 2. Hypotheses

**Primary hypothesis (H1).** Among adults with acute mTBI, a compact panel of Session-1 EEG
features — combining resting-state spectral/aperiodic measures and auditory-oddball event-related
potentials (ERPs) — is associated with persistent symptom burden at ~4 months (Session-3
Neurobehavioral Symptom Inventory [NSI] total), over and above age and sex.

**Pre-registered directional sub-hypotheses** (two-sided tests used for confirmatory inference;
directions stated for interpretation and are motivated by prior literature, which is in places
mixed):

| Predictor | Expected direction of association with higher S3 NSI total |
|---|---|
| Posterior individual alpha frequency (IAF) | lower IAF → higher symptoms (alpha slowing) |
| Global aperiodic exponent | lower (flatter) exponent → higher symptoms (E/I balance / neural noise) |
| Frontal theta/alpha ratio | higher ratio → higher symptoms (theta excess) |
| Occipital relative alpha power | lower relative alpha → higher symptoms |
| P3b amplitude (target, parietal) | lower amplitude → higher symptoms (reduced resource allocation) |
| P3b latency | longer latency → higher symptoms (slowed processing) |
| P3a amplitude (novel, frontocentral) | lower amplitude → higher symptoms (reduced novelty orienting) |
| P3a latency | longer latency → higher symptoms |

**Secondary hypotheses.** The panel is associated with (H2) S3 Rivermead total, (H3) S1→S3 NSI
change, and (H4) S1→S3 Rivermead change.

**Exploratory hypothesis (H5).** Spectral entropy adds incremental information; flexible learners
(random forest, gradient boosting) capture non-linearities not represented by the linear panel.

---

## 3. Cohort definition

**Unit of analysis / split unit:** `subject_uid` = full BIDS URSI (the canonical person key
established in Phase 1; `Original_ID` is **not** used because value 3013 collides across two
URSIs).

**Primary analytic cohort.** Acute mTBI participants (ds003522 `Group == 0`) with (a) a usable
Session-1 EEG recording and (b) a non-missing Session-3 NSI total. This cohort and its frozen
5-fold assignment were fixed in Phase 2: **n = 25** (cohort `A_ds003522` in
`frozen_cv_folds.csv`).

**Effective N by feature modality** (from Phase-3 usability QC,
`outputs/features/ds003522_s1_subject_usability.csv`):

| Model uses | Usable N |
|---|---:|
| Resting features only (Eyes-Closed) | **25** |
| ERP features only | **21** |
| Resting **and** ERP (combined panel) | **20** |

---

## 4. Inclusion / exclusion criteria

**Include:** acute mTBI; Session-1 EEG passing Phase-2 read QC; Session-3 NSI total present;
identity resolvable to a unique `subject_uid`.

**Exclude (with transparent accounting in the CONSORT flow):**
- Chronic-TBI arm (`Group == 2`, n = 25): single-session EEG only, **no longitudinal clinical
  outcomes** — ineligible for outcome prediction.
- Controls (`Group == 1`): not part of within-mTBI prediction; retained only for descriptive
  reference and exploratory group analyses (no control EEG is processed in this manuscript).
- `sub-040`: excluded from **ERP** models only — its oddball tones are stored as raw stimulus
  codes (`S 8/9/10`) without curated `trial_type` labels; the mapping is not recovered by
  guessing (a documented S-code sensitivity analysis is deferred). `sub-040` is retained for
  resting models.
- ERP reliability floor: subjects with < 15 retained Target **or** Novel epochs are excluded from
  ERP models (`sub-020`, `sub-036`, `sub-058`) but retained for resting models.
- Resting reliability floor: a resting condition with < 40 s of clean signal is treated as
  missing for that condition (affects Eyes-Open only: `sub-020`, `sub-058`, `sub-068`).

**Absolute rule:** QC-driven exclusions remove a subject **from its already-assigned fold in
place**. Folds are **never** regenerated or rebalanced.

---

## 5. Outcomes

| Tier | Outcome | Definition | Source |
|---|---|---|---|
| **Primary** | **S3 NSI total** | `NSIsoma + NSIcog + NSIemo` at Session 3 (computed; no precomputed total exists) | BigAgg S3 sheet |
| Secondary | S3 Rivermead total | `RivermeadTotal` at Session 3 | BigAgg S3 |
| Secondary | NSI change | `NSItotal(S3) − NSItotal(S1)` | BigAgg S1, S3 |
| Secondary | Rivermead change | `RivermeadTotal(S3) − RivermeadTotal(S1)` | BigAgg S1, S3 |

The NSI total is treated as a **continuous** outcome (right-skewed; see §8 for transformation
rule). **No binary "persistent symptoms" outcome is defined**: source documentation
(README, `participants.json`, BigAgg `Notes`) contains no validated NSI/Rivermead threshold, and
none is invented. Should a binary endpoint ever be required it must be externally validated,
pre-registered, and reported as externally anchored; the continuous outcome remains primary.

---

## 6. Predictors (locked panel)

All predictors are Session-1, extracted in Phase 3, and map to fixed columns. Eyes-Closed (EC) is
the primary resting condition (full N = 25; Eyes-Open is a sensitivity condition).

| # | Predictor | Feature column | Family |
|---|---|---|---|
| 1 | Posterior IAF | `rest_EC_iaf_posterior_hz` | resting spectral |
| 2 | Global aperiodic exponent | `rest_EC_global_aper_exponent` | resting aperiodic |
| 3 | Frontal theta/alpha ratio | `rest_EC_frontal_theta_alpha_ratio` | resting spectral |
| 4 | Occipital relative alpha | `rest_EC_occipital_alpha_rel` | resting spectral |
| 5 | P3b amplitude | `erp_P3b_target_par_mean_uv` (mean-window; peak is a sensitivity measure) | ERP |
| 6 | P3b latency | `erp_P3b_target_par_lat_ms` | ERP |
| 7 | P3a amplitude | `erp_P3a_novel_fc_mean_uv` | ERP |
| 8 | P3a latency | `erp_P3a_novel_fc_lat_ms` | ERP |
| 9 | Spectral entropy (**exploratory only**) | `rest_EC_global_spec_entropy` | resting (exploratory) |

No additional EEG features enter confirmatory analyses. Any other extracted feature is
exploratory and labelled as such.

---

## 7. Covariates

Pre-specified, fixed (no data-driven covariate search): **age** and **sex**. Continuous
covariates and predictors are standardized (z-scored) **within training folds only**.

Pre-specified covariate sensitivity set (Session-1, mTBI-defined, partially missing): time since
injury (`DaysSinceInjuryVisit1`), injury severity (`GCS`, `DurationLOC_InMinutes`), and baseline
symptom level (S1 NSI total) for change models. These are added only in sensitivity analyses
(§11), never as part of the locked primary specification.

---

## 8. Statistical methods

### 8.1 The events-per-variable (EPV) problem — pre-registered simplification rule
The base specification names **8 EEG predictors + 2 covariates = 10 terms** against **n ≈ 20–25**.
This is far below the ~10–15 observations per term needed for stable ordinary least squares (OLS)
inference, so the brief's clause "*if sample size or multicollinearity requires simplification,
reduce model complexity*" **is triggered**. The simplification is pre-registered here (not chosen
post hoc):

1. **Primary confirmatory estimator = penalized linear regression (elastic net)** over the full
   10-term panel, with the penalty selected by nested cross-validation on the frozen folds
   (inner loop for λ/α, outer loop for performance). This admits all locked predictors while
   controlling variance, and is the honest primary model at this N.
2. **Full OLS on all 10 terms is reported for transparency** (coefficients, 95% CIs, p-values,
   adjusted R²) but is explicitly flagged as overfit-prone and **not** the basis for confirmatory
   claims.
3. **Pre-specified reduced OLS models** (interpretable, adequately powered) are reported as the
   confirmatory linear models, one per biological domain plus a parsimonious combined model:
   - *Resting model:* `S3_NSI ~ IAF + aperiodic_exponent + frontal_theta_alpha + occipital_rel_alpha + age + sex` (n = 25).
   - *ERP model:* `S3_NSI ~ P3b_amp + P3b_lat + P3a_amp + P3a_lat + age + sex` (n = 21).
   - *Parsimonious combined model:* the single strongest a priori biomarker from each family
     (pre-registered choice: **aperiodic exponent**, **posterior IAF**, **P3b amplitude**) + age
     + sex (n = 20) — ≈ 5 terms, within EPV tolerance.

### 8.1b LOCKED statistical hierarchy (Phase 3.6)

The estimator hierarchy is frozen as four tiers. Tier assignment is fixed; a model's tier is
never upgraded on the basis of its result.

| Tier | Model | Specification | N | Role |
|---|---|---|---|---|
| **Primary confirmatory** | **Parsimonious linear regression** | `S3_NSI_Total ~ Global_Aperiodic_Exponent + Posterior_IAF + P3b_Amplitude + Age + Sex` | 20 | the single headline inferential model |
| **Secondary confirmatory** | **Elastic Net** | full locked panel (8 EEG) + Age + Sex; λ and α by nested CV on frozen folds | 20 | supportive confirmation across the full panel |
| **Transparency** | **Full 10-term OLS** | full locked panel (8 EEG) + Age + Sex, unpenalized | 20 | **descriptive only; potentially overfit; NOT used for primary inferential claims** |
| **Exploratory** | Ridge, LASSO, Random Forest, XGBoost | full locked panel + covariates; nested CV on frozen folds | 20 | hypothesis-generating; not central to conclusions |

The **parsimonious linear model is the sole primary confirmatory analysis.** It carries one
biologically motivated biomarker from each family — the resting **aperiodic exponent** (1/f /
E-I balance), the resting **posterior IAF** (alpha slowing), and the task-evoked **P3b amplitude**
(target-evaluation resource allocation) — at ~5 terms, within the events-per-variable tolerance
for n = 20. The Elastic Net over the full panel is the **secondary confirmatory** analysis; the
full unpenalized OLS is reported **for transparency only** and is explicitly flagged as
descriptive and potentially overfit. Ridge, LASSO, Random Forest, and XGBoost are **exploratory**
(§12). Divergence between the primary and secondary confirmatory models is interpreted, not
resolved by post hoc selection.

Domain-specific linear models (resting-only, n = 25; ERP-only, n = 21) are reported as supportive
context for the primary model but do not displace it.

### 8.2 Estimation and reporting
- Outcome distribution checked; if right-skew is material, fit on `log1p(NSI)` or use a
  Gaussian GLM with appropriate link, pre-specified by the skew of the **outcome only** (no
  predictor or feature–outcome information used to choose the transform).
- For every model report: standardized **β coefficients**, **95 % confidence intervals**,
  **p-values**, **adjusted R²**, and **effect sizes** (partial R² / Cohen's f² per predictor;
  model-level f²). Coefficient p-values within the 8-predictor family are **FDR-controlled**
  (Benjamini–Hochberg).
- **Multicollinearity:** variance inflation factors (VIF) reported; |VIF| > 5 triggers the
  pre-specified domain reduction in §8.1 rather than ad hoc dropping.
- **Predictive performance** (secondary to inference): out-of-fold R² and MAE from the frozen
  5-fold CV, with bootstrap CIs. The headline performance contrast is **EEG panel vs.
  covariates-only (age + sex) baseline** — i.e., does EEG add information beyond demographics.

### 8.3 Secondary confirmatory penalized analysis
**Elastic Net** over the full locked panel (8 EEG features) + age + sex, with λ and the
L1/L2 mixing parameter α selected by nested cross-validation on the frozen folds (inner loop for
hyperparameters, outer loop for performance). Report selected coefficients, selection stability
(frequency across outer folds), and out-of-fold performance. This is the single secondary
confirmatory model; ridge and LASSO are demoted to exploratory (§12).

### 8.4 Estimation philosophy

This study is **estimation-first, not significance-first**. The inferential goal is to characterize
the magnitude, direction, and uncertainty of each biomarker–symptom association, not to declare
binary "hits."

- **Effect sizes and confidence intervals are primary.** Every reported association leads with a
  point estimate and its 95 % confidence (compatibility) interval; interpretation is anchored to
  the estimate and the interval's range of plausible values, not to a threshold.
- **De-emphasize dichotomous significance testing.** p-values are reported (FDR-controlled within
  the predictor family) but treated as one continuous piece of evidence among several. We avoid
  "significant/non-significant" language as the basis for conclusions and never infer absence of
  effect from a non-significant p-value alone.
- **Standardized coefficients.** Predictors and continuous covariates are z-scored within training
  folds, so standardized β coefficients are reported to compare relative association strength
  across the panel; raw-scale coefficients are provided in the supplement for interpretability.
- **Predictive uncertainty is reported honestly.** Out-of-fold R²/MAE carry bootstrap confidence
  intervals; given n ≈ 20 these are expected to be wide and are presented as such. The headline
  contrast is whether the EEG panel improves on an age + sex baseline, with the uncertainty of
  that improvement made explicit.
- **ML metrics are supportive, not definitive.** Performance from penalized and flexible learners
  contextualizes the linear findings; it does not override the interpretable primary model, and no
  central conclusion rests on an ML accuracy figure.
- **Calibrated claims.** Conclusions are framed as hypothesis-generating associations in a small
  discovery cohort requiring independent replication, never as a validated prognostic tool.

---

## 9. Missing-data strategy

- **Outcome:** present for all 25 by eligibility (complete). S2/S3 attrition is handled by cohort
  definition, not imputation of the outcome (the outcome is **never** imputed).
- **Predictors:** ERP features missing for `sub-040` (no events) and unreliable for 3 low-trial
  subjects; Eyes-Open features missing for 3 subjects. Covariates (age, sex) complete.
- **Primary approach:** **complete-case** within each model's eligible N (resting n = 25, ERP
  n = 21, combined n = 20), reported transparently with a CONSORT flow.
- **Sensitivity:** multiple imputation by chained equations (MICE) of **predictors only**, fit
  **within training folds**, pooled by Rubin's rules; compared to complete-case. The outcome and
  test-fold data never inform imputation.
- **Attrition check:** compare Session-1 characteristics (age, sex, baseline NSI, injury
  severity, and the EEG predictors) of S3 completers vs. non-completers descriptively; if they
  differ, discuss potential bias and, as a further sensitivity analysis, fit an
  inverse-probability-of-attrition-weighted model.

---

## 10. Leakage-prevention strategy (absolute)

1. **Folds are immutable.** `outputs/splits/frozen_cv_folds.csv` (seed 42, stratified on S3-NSI
   tertiles) is never regenerated, reshuffled, or rebalanced.
2. **Split unit = `subject_uid` (URSI).** No subject appears in more than one fold; the overlap
   with ds005114/ds003523 is irrelevant here because those datasets are not analysed against the
   outcome in this manuscript.
3. **All fold-dependent fitting is internal to training folds:** standardization, imputation,
   any dimensionality reduction, penalty (λ/α) selection, and the transform decision pipeline are
   fit on training data and applied to held-out data — never the reverse.
4. **Outcome never touches upstream steps.** Preprocessing parameters (Phase 3) and the locked
   feature panel (this SAP) were both fixed without reference to any outcome; feature selection is
   pre-registered, not data-driven.
5. **QC exclusions are fold-local:** a subject failing usability QC is removed from its assigned
   fold only; the remaining fold structure is untouched.
6. **Auditability:** `crosswalk_subject_ids.csv` and the frozen folds allow a reviewer to verify
   that no person leaks across folds.

---

## 11. Sensitivity analyses (pre-specified)

1. **Estimator:** parsimonious primary OLS vs. secondary-confirmatory full-panel Elastic Net vs.
   transparency full OLS (§8.1b); Ridge/LASSO are compared as exploratory (§12).
2. **ERP measurement:** mean-window vs. peak P3b/P3a amplitude and latency.
3. **Resting condition:** Eyes-Closed (primary) vs. Eyes-Open (n = 22).
4. **Missing data:** complete-case vs. MICE (§9).
5. **ERP reliability:** with vs. without the 3 low-trial subjects; with vs. without an S-code
   recovery of `sub-040`.
6. **Covariate set:** add time-since-injury and injury severity (GCS/LOC) where available.
7. **Outcome timing:** S2 NSI total (less attrition, larger N) as a supportive replication of the
   primary S1→outcome association.
8. **Outcome transform:** raw vs. `log1p` NSI.
9. **High-pass robustness:** re-extract under a 0.1-Hz high-pass (vs. the locked 0.5-Hz) to
   confirm slow-ERP stability — requires re-running Phase 3 with a documented parameter change and
   is reported as a robustness check, not a respecification.

All sensitivity analyses use the same frozen folds and leakage rules.

---

## 12. Exploratory analyses (after primary analyses only)

- **Exploratory penalized linear:** **Ridge** and **LASSO** over the full locked panel +
  covariates, nested CV on frozen folds; reported alongside the secondary-confirmatory Elastic Net
  for comparison of regularization behaviour. Exploratory, not confirmatory.
- **Spectral entropy** (predictor 9) added to the resting/combined models.
- **Flexible learners:** random forest and gradient boosting (XGBoost) over the locked panel,
  nested CV on frozen folds, interpreted with permutation importance / SHAP. **Clearly labelled
  exploratory; not part of central conclusions.**
- **Secondary outcomes:** Rivermead total and S1→S3 change scores (H2–H4).
- **Per-region / per-band exploration** beyond the locked panel — hypothesis-generating, FDR-
  controlled, explicitly exploratory.
- **Group-level descriptive comparison** (mTBI vs. control vs. chronic) deferred to future work
  (requires processing control/chronic EEG).

---

## 13. Reproducibility and software

Python 3.14; MNE 1.12, specparam 2.0, scikit-learn 1.9, statsmodels (for OLS inference), pandas,
numpy. Random seeds fixed (42). All scripts, frozen folds, feature files, and per-subject
preprocessing logs are version-controlled. Analysis code for this SAP will be released with the
manuscript. **No outcome model is run until this SAP is frozen.**

---

## 14. Limitations acknowledged a priori
- **Small discovery N** (20–25): this is a hypothesis-generating discovery study, not a validated
  prognostic tool. Confidence intervals, not point estimates, carry the inference; out-of-sample
  replication in ds005114/ds003523 is essential future work.
- Single site, single device; outcomes are self-report symptom inventories.
- Resting EEG was extracted from blocks embedded within the task recording (not a standalone
  resting run); Eyes-Open data are noisier.
- Findings are associations, not causal or clinically deployable predictions.
