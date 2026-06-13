# Phase 4 Results — Pre-registered confirmatory analysis
### Early EEG biomarkers and persistent post-concussive symptoms (ds003522, sub-acute/early post-injury mTBI)

**Date:** 2026-06-11
**Adherence statement:** Every model below was executed exactly as fixed in
`reports/final_locked_analysis_plan.md`. No predictor was added or removed; exploratory models
remained exploratory; the frozen folds were used unchanged (subjects failing the locked
§3 usability gates were dropped from their assigned fold only). The outcome scale was set by the
pre-specified rule (outcome skewness = 0.85 < 1.0 → **raw NSI**, no transform). Producing scripts:
`10_build_analysis_table.py`, `11_fit_models.py`, `12_figures.py`. Result tables in
`outputs/analysis/`; figures in `outputs/figures/`.

> **Headline (stated up front, in estimation terms):** In this small sub-acute/early post-injury mTBI discovery cohort,
> the pre-registered Session-1 EEG panel showed **no reliable association with, and no
> out-of-sample predictive value for, Session-3 NSI total beyond age and sex.** All standardized
> effect sizes were small with 95% confidence intervals spanning zero; penalized and
> cross-validated analyses converged on the mean (intercept-only) predictor. We interpret this as
> **inconclusive/null**, not as evidence of absence, given the wide intervals and small N.

---

## 0. Sample accounting (locked gates applied)

| Model | N | Notes |
|---|---:|---|
| Primary (parsimonious) | **21** | sub-acute/early post-injury mTBI with EC rest + reliable P3b; excludes sub-040 (no tone labels) + 3 low-trial ERP subjects |
| Secondary Elastic Net / Transparency OLS (full panel) | 21 | same gating |
| Supportive resting-only | 25 | EC rest reliable for all 25 |
| Supportive ERP-only | 21 | ERP reliability gate |
| Sensitivity (drop EO-low subject) | 20 | reconciliation with plan's summary N |

**Reconciliation note (transparent, not a plan change).** The locked plan's *summary* combined-N
of 20 assumed both eyes-closed **and** eyes-open resting reliability. The locked resting
predictors are **eyes-closed only**, so the eyes-open floor does not gate the confirmatory model;
applying the operative §3 exclusion criteria yields **n = 21**. The n = 20 variant (additionally
dropping the one eyes-open-low subject) is reported as a pre-specified sensitivity analysis and is
substantively identical (below).

Outcome S3 NSI total (n = 25): mean 15.1, SD 15.7, median 9, range 0–51.

---

## 1. Primary confirmatory analysis

**Model:** `S3_NSI_Total ~ Global_Aperiodic_Exponent + Posterior_IAF + P3b_Amplitude + Age + Sex`
(OLS, n = 21). Model-level: R² = 0.11, **adjusted R² = −0.19**, F-test p = 0.86 — the model is
**not distinguishable from an intercept-only fit**.

| Predictor | β (raw) | 95% CI | Std. β | Std. 95% CI | p | p (FDR) |
|---|---:|---:|---:|---:|---:|---:|
| Global aperiodic exponent | −1.42 | [−64.3, 61.5] | −0.02 | [−0.83, 0.79] | 0.962 | 0.962 |
| Posterior IAF | −2.58 | [−13.9, 8.8] | −0.15 | [−0.83, 0.52] | 0.635 | 0.962 |
| **P3b amplitude** | 2.07 | [−3.4, 7.5] | **0.24** | [−0.40, 0.88] | 0.433 | 0.962 |
| Age | −0.06 | [−1.24, 1.13] | −0.04 | [−0.83, 0.75] | 0.916 | 0.962 |
| Sex | −4.85 | [−25.6, 15.9] | −0.13 | [−0.71, 0.44] | 0.626 | 0.962 |

**Interpretation (estimation-first).** The largest point estimate is **P3b amplitude
(standardized β = +0.24)**, but its 95% CI (−0.40 to 0.88) comfortably includes zero and both
directions of clinically meaningful effect; it is therefore uninformative as to sign or magnitude.
All other standardized effects are |β| ≤ 0.15 with intervals spanning zero. After FDR control
every p-value is 0.96. The data neither support nor exclude modest associations of the
hypothesized directions; they are simply **uninformative at this N**.

**Robust inference.** Heteroscedasticity-consistent (HC3) p-values are materially identical
(0.64–0.97), so the null is not an artifact of variance assumptions.

### 1.1 Residual diagnostics
Residuals are approximately normal (Shapiro–Wilk p = 0.094) and homoscedastic (Breusch–Pagan
p = 0.50); Durbin–Watson = 1.86. The design condition number is 749 (moderate collinearity, mainly
the aperiodic-exponent scale). **Three of 21 participants exceed the Cook's-distance threshold
(4/n = 0.19)**; one (subject `M87123864`) is a clear outlier (externally studentized residual
= 3.6, observed NSI far above its prediction). With n = 21, single observations are influential —
consistent with the coefficient instability below.

### 1.2 Leave-one-subject-out influence
Refitting the primary model 21 times, each dropping one subject, **no predictor's coefficient is
sign-stable**: every standardized/raw coefficient changes sign depending on which single
participant is removed (e.g. P3b amplitude ranges −0.71 to +5.72 in raw units; posterior IAF
−5.16 to +1.75). This is the expected signature of fitting 5 terms to 21 noisy observations and is
the strongest internal evidence that the point estimates carry no stable signal.

---

## 2. Secondary confirmatory analysis — Elastic Net (full panel)

Elastic Net over the full 8-feature panel + age + sex (nested CV on frozen folds; scaling and
imputation fit within training folds only). The cross-validated penalty was
**α = 43.2, l1_ratio = 0.10**, which **shrank all 10 coefficients to exactly zero** — the selected
model is the **intercept only (14.6, the sample mean)**. Out-of-fold performance:
**R²_oof = −0.055** (95% bootstrap CI −0.50 to −0.017), MAE = 13.3. The penalized model's verdict
is unambiguous: given the data, no feature improves out-of-sample prediction over the mean.

Calibration (Fig. fig_calibration) and predicted-vs-observed (Fig. fig_predicted_vs_observed) show
predictions compressed to a near-flat line at the cohort mean across the full 0–51 observed range.

---

## 3. Supportive analyses

| Model | N | R² | adj R² | F p | R²_oof (95% CI) |
|---|---:|---:|---:|---:|---:|
| Resting-only OLS | 25 | 0.31 | 0.08 | 0.29 | −0.59 (−2.07, −0.08) |
| ERP-only OLS | 21 | 0.22 | −0.12 | 0.69 | −1.13 (−2.83, −0.38) |

The resting-only model shows the largest in-sample R² (0.31) but a near-zero adjusted R² (0.08), a
non-significant omnibus test (p = 0.29), and **negative out-of-fold R² (−0.59)** — i.e. the
in-sample fit does not generalize. These analyses are **supportive context only** and are **not**
reinterpreted as primary.

---

## 4. Transparency analysis — full 10-term OLS

**Descriptive only; potentially overfit; not used for inference.** In-sample R² = 0.39 but
**adjusted R² = −0.22**, design condition number ≈ 22,400 (severe multicollinearity), and
**R²_oof = −3.58** (MAE = 27.5) — the worst generalization of any model. This is included exactly
as the locked plan intends: to make the overfitting of the unpenalized full model visible rather
than to support any claim.

---

## 5. Exploratory analyses

Out-of-fold performance (frozen folds; all exploratory, not central to conclusions):

| Model | R²_oof (95% CI) | MAE |
|---|---:|---:|
| Baseline (age + sex) | −0.40 (−1.36, −0.13) | 15.7 |
| Ridge (full panel) | −0.14 (−0.61, −0.03) | 13.6 |
| LASSO (full panel) | −0.055 (−0.50, −0.02) | 13.3 |
| Random Forest | −0.29 (−1.14, −0.06) | 14.9 |
| XGBoost | −0.36 (−1.36, 0.09) | 14.7 |

Every model — linear, penalized, and flexible — produces **negative out-of-fold R²**. The
best-performing models (LASSO, Elastic Net, Ridge) are precisely those that regularize toward the
mean; the flexible learners do not recover any non-linear structure. No exploratory result alters
the primary conclusion.

---

## 6. Sensitivity analyses

| Sensitivity | Result | Conclusion |
|---|---|---|
| Drop eyes-open-low subject (n = 20) | primary adj R² = −0.21 | unchanged |
| HC3 robust SEs (primary) | p = 0.64–0.97 | unchanged |
| Penalized vs OLS | EN/Ridge/LASSO all → mean predictor | unchanged |
| Resting vs ERP families | both null individually (§3) | unchanged |
| Flexible learners | negative R²_oof (§5) | unchanged |

Pre-specified sensitivities not run here because they cannot rescue a null and/or require
re-running upstream phases (0.1-Hz high-pass re-extraction; MICE imputation; S2-outcome timing;
peak vs mean ERP metric) are deferred to a documented robustness appendix; none is expected to
change a result in which every estimator converges on the mean.

---

## 7. Interpretation

1. **The pre-registered EEG panel did not predict persistent post-concussive symptom burden** at
   ~4 months in this sub-acute/early post-injury mTBI sample. Standardized effects are small (|β| ≤ 0.24) with intervals
   spanning zero; out-of-sample R² is negative for every model; the penalized model retains no
   feature.
2. **This is an inconclusive/null result, not proof of no effect.** With n ≈ 21 and confidence
   intervals as wide as ±0.8 SD, the study cannot exclude modest true associations. The
   leave-one-out instability shows the cohort is too small to estimate an 8-feature (even
   3-biomarker) model with any stability.
3. **Value of the result.** Because the analysis was pre-registered, leakage-safe, and
   estimation-focused, this null is informative: it stands in contrast to the more optimistic
   resting-EEG and P3 literature and is consistent with the possibility that some prior positive
   prognostic claims were inflated by small samples, flexible analytic choices, or information
   leakage. A rigorously specified pipeline here did **not** reproduce a large effect.
4. **No causal interpretation** is made; these are observational associations (or their absence).

---

## 8. Limitations

- **Sample size (n ≈ 21)** is the dominant limitation; the study is powered only to detect large
  effects, and coefficient estimates are unstable to single observations.
- **Single site/device; self-report outcomes;** resting EEG extracted from blocks embedded in the
  task recording; eyes-open data noisier.
- **Attrition** from Session 1 to Session 3 (and ERP trial-count losses) reduces N and may select
  on recovery; the complete-case primary analysis does not model informative dropout (a
  pre-specified IPAW sensitivity is deferred).
- **Generalization untested:** ds005114 and ds003523 remain reserved for independent replication;
  the present conclusion is confined to this discovery cohort.
- Findings should be read as **hypothesis-generating**: a larger, multi-site, pre-registered
  replication is required before any prognostic claim — positive or negative — can be considered
  established.

---

### Result artifacts
`outputs/analysis/`: `model_coefficients.csv`, `model_fit_summary.csv`, `cv_performance.csv`,
`elasticnet_coefficients.csv`, `loo_influence.csv`, `loo_coefficient_stability.csv`,
`oof_predictions.csv`, `diagnostics.json`.
`outputs/figures/`: coefficient forest, partial-effect, Elastic-Net path, calibration,
predicted-vs-observed, resting-vs-ERP contribution.
