# Phase 1 Analysis Plan
### Prospective prediction of persistent post-concussive symptoms from early EEG

**Date:** 2026-06-11
**Status:** Pre-modeling analysis plan. **No EEG has been preprocessed; no model has been
trained.** This document is intended to be frozen (pre-registered) before any signal processing.
**Inputs:** `outputs/metadata_summary_tables/` (built by `scripts/02_build_cohort.py` from the
Phase 0 metadata cache and `BigAgg_4BIDS.xlsx`).
**Companion:** `reports/duplicate_id_resolution_report.md` (identity handling).

---

## 1. Final cohort recommendation

**Primary analytic cohort: `ds003522` acute mTBI subjects (Group 0)** with Session-1 EEG and a
Session-3 symptom outcome.

Rationale:
- `ds003522` is the project's primary dataset and the only one with the **auditory oddball
  (P3a/P3b)** paradigm and **resting EEG**, giving the richest task-evoked + spectral/aperiodic
  feature set for the published hypothesis.
- It carries the full longitudinal clinical battery (NSI, Rivermead, BDI) at S1/S2/S3.

**The N tradeoff is explicit and pre-registered (it does not change the primary choice but
governs interpretation and the replication plan).** Counts of mTBI subjects with Session-1 EEG
and an NSI total at each follow-up:

| Dataset (task) | S1 EEG (mTBI) | + S1 NSI | + S2 NSI | + S3 NSI |
|---|---:|---:|---:|---:|
| **ds003522** (oddball) — **primary** | 44 | 44 | 34 | **25** |
| ds005114 (DPX) — replication | 57 | 57 | 45 | **34** |
| ds003523 (WM) — replication | 57 | 57 | 45 | **34** |
| all-three overlap (multi-task) | 47* | — | — | **~25** |

\*47 = subjects with S1 EEG in all three datasets (any group); ~25 are mTBI. *Source:
`attrition_by_session.csv`, `02_build_cohort.py` console summary.*

Because the primary mTBI cohort is small (**n ≈ 25** with a 4-month outcome), the **Session-2
outcome (n ≈ 34) is pre-specified as the primary-power sensitivity analysis**, and **`ds005114`
(n ≈ 34 at S3) is pre-specified as the confirmatory replication cohort**. The four candidate
cohorts requested in the brief are retained and defined below; A is primary, B is the
replication, C and D are exploratory.

### The four candidate cohorts

| | Cohort | Definition | Unique subjects (mTBI / Control) | Primary use |
|---|---|---|---|---|
| **A** | ds003522-only | EEG in ds003522 | 44 / 27 (+25 chronic) | **PRIMARY** prospective prediction |
| **B** | ds005114-only | EEG in ds005114 | 57 / 34 | pre-registered **replication** |
| **C** | ds003523-only | EEG in ds003523 | 57 / 34 | exploratory replication (WM; unpublished data) |
| **D** | all-dataset overlap | EEG in all three (key on URSI) | ~25 mTBI / ~22 control of 47 | exploratory **multi-task** feature fusion |

> **Chronic-TBI arm (ds003522 Group 2, n = 25):** has single-session EEG but **no BigAgg
> clinical/outcome data**. It is **excluded from all outcome-prediction analyses** and reserved
> only for a secondary group-classification analysis (mTBI vs control vs chronic).

---

## 2. Primary hypothesis

> **H1 (primary).** Among adults with acute mild TBI, **Session-1 EEG features** — resting and
> oddball-evoked spectral power, the aperiodic (1/f) exponent and offset, and the P3a/P3b
> event-related responses — **predict persistent post-concussive symptom burden at ~4 months
> (Session-3 NSI total)**, over and above age, sex, baseline symptom level, time since injury,
> and injury severity.

Directional expectation: greater early disruption (e.g. flatter aperiodic slope / altered P3)
is associated with **higher** persistent symptom burden / slower recovery.

Secondary hypotheses: (H2) the same features predict Session-3 Rivermead total; (H3) features
predict **symptom change** (recovery slope) S1→S3; (H4 exploratory) resting aperiodic features
discriminate mTBI / control / chronic groups.

---

## 3. Inclusion / exclusion criteria

**Include** a subject in the primary cohort if all hold:
1. Group = acute **mTBI** (`group_code == 0`).
2. A usable **Session-1 EEG** recording exists in `ds003522`
   (`eeg_ds003522 == True`, session 1).
3. A non-missing **primary outcome** (Session-3 NSI total) exists.
4. Canonical identity resolvable to a unique `subject_uid` (URSI).

**Exclude:**
- Chronic TBI (Group 2) — no longitudinal outcomes (group-classification only).
- Controls — not part of the within-mTBI prediction; retained as a **reference group** for
  descriptive contrast and for H4 classification only.
- Subjects flagged in the BigAgg `Notes` sheet for analysis-invalidating reasons
  (pre-existing/multiple prior TBI, assessment discontinued, effort-validity failure on TOMM,
  partial/again-unusable EEG). These flags are applied **after** EEG QC in Phase 2 and logged.
- Clinical-only subjects with no EEG (`SubID` 3008, 3022, 3120) — by definition.
- `Original_ID 3013`: both URSIs are controls; handled per the duplicate report (kept, keyed on
  URSI, no effect on the mTBI primary analysis).

**EEG quality control (Phase 2, pre-specified now):** minimum retained clean epochs per
condition, maximum interpolated channels, and amplitude/variance thresholds will be fixed before
feature extraction; subjects failing QC are dropped and counted in the CONSORT flow.

---

## 4. Outcomes

| Tier | Outcome | Definition | Session | N (mTBI) |
|---|---|---|---|---:|
| **Primary** | **NSI total** | `NSIsoma + NSIcog + NSIemo` (computed; no precomputed total exists). Continuous. | S3 | ~25 (ds003522) |
| Secondary | Rivermead total | `RivermeadTotal`, continuous | S3 | ~24 |
| Sensitivity | NSI change | `NSItotal(S3) − NSItotal(S1)` (recovery slope; ≤0 = improvement) | S1→S3 | ~25 |
| Power-sensitivity | NSI total | same as primary but at **S2** (less attrition) | S2 | ~34 |

**Outcome scale check (mTBI):** NSI total S1 mean 24.9 (SD 19.8, median 20, range 0–70); S3 mean
16.6 (SD 17.9, median 10) — symptoms decline over recovery as expected. Controls S1 mean 7.8
(median 3), confirming group separation. NSI total is right-skewed → model on a transformed scale
or with a distribution that admits skew/overdispersion (§7).

### Binary "persistent symptoms" outcome — **deferred, not invented**
The dataset documentation (README, `participants.json`, BigAgg `Notes` sheet) provides **no
validated NSI/Rivermead cutoff** for "persistent post-concussive symptoms." Per the Phase 1
brief, **no threshold is invented here.** A binary outcome is therefore **not part of this plan.**
If a binary endpoint becomes necessary, it must be (a) drawn from an external validated source,
(b) pre-registered before modeling, and (c) reported as externally-anchored — and even then the
continuous NSI total remains primary. This decision is logged so it cannot be retro-fitted.

---

## 5. Covariates

Baseline (Session-1) adjustment set for the primary model:
- **Demographics:** `age`, `sex`.
- **Baseline symptom level:** Session-1 NSI total (anchors the prediction to *change*, not level).
- **Time:** `DaysSinceInjuryVisit1` (S1 timing) and `DaysSinceS2` (S1→S3 interval) — model
  elapsed time explicitly rather than assuming fixed spacing.
- **Injury severity (where available):** `GCS`, `DurationLOC_InMinutes` / `LOC`. These are
  **mTBI-only and partly missing** (controls have none); see §6.

Covariates are pre-specified and fixed; no data-driven covariate selection on the outcome.
Continuous covariates centered; collinearity checked (VIF) before fitting.

---

## 6. Missing-data plan

Missingness is **substantial and almost certainly informative** (attrition tracks recovery).
Quantified in `missingness_by_variable.csv` and `attrition_by_session.csv`.

**Patterns:**
- **Longitudinal attrition (outcome MAR/MNAR):** NSI present for mTBI: S1 = 44 → S2 = 34 → S3 =
  25 (ds003522). The primary analysis is **complete-case on the S3 outcome**, with the
  consequence stated openly.
- **Injury-severity covariates partly missing** within mTBI (`GCS`, `LOC` recorded as `NR`/`na`
  for some), and undefined for controls by design.
- **String missing-tokens** (`na`, `NR`, `m`) are mapped to `NaN` during table construction
  (`scripts/02_build_cohort.py`).

**Plan:**
1. **Primary:** complete-case for the outcome (S3 NSI total present). Report N transparently in a
   CONSORT diagram (§8).
2. **Covariate missingness:** multiple imputation (MICE) of **baseline covariates only** (never
   the outcome, never EEG features post-hoc), pooled by Rubin's rules; sensitivity vs.
   complete-case.
3. **Informative-dropout sensitivity:** compare S1 characteristics (baseline NSI, severity,
   demographics, EEG features) of **completers vs. non-completers** at S3; if they differ,
   report and discuss bias direction. Optionally fit an inverse-probability-of-attrition
   weighted model as a sensitivity analysis.
4. **Power-sensitivity at S2** (n≈34) as a pre-specified, less-attrited replication of the
   primary effect.
5. The **mixed-effects trajectory model (§7)** uses all available timepoints under MAR, partially
   recovering subjects lost only at S3.

---

## 7. Proposed statistical models

All models are specified now and frozen. **Modeling is not run in Phase 1.**

**M1 — Primary (cross-validated prediction).**
`NSItotal_S3 ~ EEG_S1_features + age + sex + NSItotal_S1 + days_since_injury (+ severity)`.
- Estimator: penalized regression (elastic net) or a small random forest, chosen *a priori*;
  EEG feature block dimensionality reduced by *a priori* regions/bands (no outcome-guided
  selection).
- Validation: **subject-level, leakage-safe nested cross-validation**, split unit = `subject_uid`
  (URSI). Given n≈25, use **repeated stratified k-fold / leave-one-subject-out** with the full
  preprocessing+feature pipeline refit inside each fold.
- Metrics: out-of-fold R² / MAE for continuous NSI; report with bootstrap CIs.
- Inference benchmark: compare EEG model vs. a **covariates-only baseline** (does EEG add signal
  beyond demographics + baseline symptoms?). This contrast, not raw R², is the headline.

**M2 — Secondary.** Same design with `RivermeadTotal_S3`.

**M3 — Sensitivity (change score).** Outcome = `NSItotal_S3 − NSItotal_S1`.

**M4 — Longitudinal trajectory (uses all timepoints, MAR-robust).**
Linear mixed model: `NSItotal ~ time + EEG_S1_features*time + age + sex + (time | subject_uid)`,
time encoded by `DaysSince*`. Tests whether early EEG predicts **recovery slope**.

**M5 — Secondary group classification (exploratory, includes chronic arm).**
Resting/aperiodic features → mTBI vs control vs chronic, subject-level CV, split on `subject_uid`.

**Replication (pre-registered):** rerun M1/M2 on **Cohort B (ds005114, n≈34)** with the
analogous DPX-evoked + resting features; consistency of sign/magnitude is the replication
criterion. **Cohort D** (multi-task overlap) is exploratory feature-fusion only.

**Multiple comparisons:** primary outcome + single primary model is the confirmatory test; all
else is explicitly secondary/exploratory and FDR-controlled within family. Pre-register before
Phase 2.

---

## 8. Leakage-prevention plan

This is the load-bearing design constraint and is enforced mechanically, not by discipline:

1. **Canonical subject key = `URSI` (`subject_uid`).** All splits, all dedup, all joins use it.
   `Original_ID` is **never** used as a split/merge key (it collides — value 3013).
2. **Same people span datasets.** 70 subjects appear in all three datasets; 90 in
   ds005114∩ds003523. Therefore:
   - Cohorts B/C/D are **not independent samples** of A — any pooled or transfer analysis
     deduplicates on `subject_uid` first, and **no subject_uid is ever in both train and test**.
   - Treat ds005114/ds003523 as *different tasks on the same people*, not new subjects.
3. **Split before you look.** The train/test (CV) fold assignment is generated from
   `subject_uid` **before** any EEG preprocessing or feature extraction, and the entire pipeline
   (filtering, ICA, feature scaling, imputation, feature selection, model fit) is refit **inside**
   each training fold only. Test folds see no fitted parameter.
4. **No outcome-aware feature selection** outside CV folds; no normalization using test-set
   statistics; no imputation of the outcome.
5. **Temporal direction enforced:** predictors are strictly Session-1; outcomes strictly later
   sessions. No same-session circularity.
6. **Identity audit shipped:** `crosswalk_subject_ids.csv` lets a reviewer verify that no person
   leaks across folds or datasets.

---

## 9. Deliverables produced in Phase 1

| File | Contents |
|---|---|
| `outputs/metadata_summary_tables/crosswalk_subject_ids.csv` | dataset × BIDS subject ↔ Original_ID/URSI/subject_uid, group, EEG sessions |
| `outputs/metadata_summary_tables/master_subject_session_table.csv` | one row per (subject_uid, session): identity, EEG flags per dataset, NSI/Rivermead/BDI, baseline injury vars |
| `outputs/metadata_summary_tables/missingness_by_variable.csv` | non-null/missing counts & % per variable, session, and cohort |
| `outputs/metadata_summary_tables/attrition_by_session.csv` | CONSORT-style EEG & outcome counts by dataset/group/session |
| `reports/phase1_analysis_plan.md` | this document |
| `reports/duplicate_id_resolution_report.md` | identity reconciliation |

### CONSORT-style attrition (primary cohort, ds003522 mTBI)

| Stage | n |
|---|---:|
| Acute mTBI with Session-1 EEG | 44 |
| … with Session-1 NSI outcome | 44 |
| … retained with Session-2 NSI | 34 |
| … retained with Session-3 NSI (**primary analysis set**) | **25** |

(Control reference arm: 27 with S1 EEG → 21 with S3 NSI. Full breakdown incl. ds005114/ds003523
in `attrition_by_session.csv`.)

---

## 10. What is explicitly NOT done yet
- No EEG loaded, filtered, or epoched; no features computed.
- No models fit; no hyperparameters tuned; no outcome inspected beyond aggregate descriptives.
- No binary symptom threshold defined (none is documented in the dataset).
- Final QC-based exclusions and the frozen CV fold assignment are produced at the **start of
  Phase 2**, before any feature extraction.
