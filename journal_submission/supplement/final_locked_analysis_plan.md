# FINAL LOCKED ANALYSIS PLAN — Preregistration Supplement
### Early Resting-State and Task-Evoked EEG Biomarkers of Persistent Post-Concussive Symptoms Following Mild Traumatic Brain Injury: A Leakage-Safe Longitudinal Reanalysis of a Public OpenNeuro Dataset

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
Session-1 EEG features is associated with persistent post-concussive symptom burden at ~4 months
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

**Optional exploratory:** Spectral entropy — `rest_EC_global_spec_entropy`.

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
