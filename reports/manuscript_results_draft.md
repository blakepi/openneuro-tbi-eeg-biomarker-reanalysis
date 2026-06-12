# Results (manuscript draft)
### Early Resting-State and Task-Evoked EEG Biomarkers of Persistent Post-Concussive Symptoms Following mTBI

*Draft Results for peer review. Prose emphasizes effect sizes, confidence intervals, and
uncertainty; significance is not overstated and no causal language is used. All analyses were
pre-registered and executed without modification of the locked statistical hierarchy.*

---

## 3.1 Sample and outcome

Of the 25 acute-mTBI participants with a usable Session-1 recording and a Session-3 outcome, the
locked usability criteria yielded analytic samples of 25 for resting-only models and 21 for all
models incorporating the event-related potential (ERP) panel (four participants were excluded from
ERP analyses: one whose oddball tones lacked curated event labels and three with fewer than 15
retained rare-tone epochs). Session-3 Neurobehavioral Symptom Inventory (NSI) total scores were
right-skewed but below the pre-specified transformation threshold (skewness = 0.85), and were
therefore analysed on the raw scale (mean 15.1, SD 15.7, median 9, range 0–51).

## 3.2 Primary confirmatory analysis

The pre-registered parsimonious model — Session-3 NSI total regressed on the global aperiodic
exponent, posterior individual alpha frequency, P3b amplitude, age, and sex (n = 21) — did not
account for variance in persistent symptom burden beyond chance (R² = 0.11, adjusted R² = −0.19,
omnibus F-test p = 0.86). No predictor showed a confidence interval excluding zero. The largest
standardized association was for P3b amplitude (standardized β = 0.24, 95% CI −0.40 to 0.88,
p = 0.43), followed by posterior individual alpha frequency (β = −0.15, 95% CI −0.83 to 0.52) and
the global aperiodic exponent (β = −0.02, 95% CI −0.83 to 0.79); age and sex were likewise
uninformative. After Benjamini–Hochberg correction all p-values were 0.96, and
heteroscedasticity-consistent (HC3) inference was materially identical (p = 0.64–0.97). In
estimation terms, the data are uninformative as to the sign or magnitude of any hypothesized
association: every interval spans both negligible and moderate effects in both directions.

Residual diagnostics were unremarkable (Shapiro–Wilk p = 0.09; Breusch–Pagan p = 0.50;
Durbin–Watson = 1.86), but the model was sensitive to individual observations: three of 21
participants exceeded the Cook's-distance threshold (4/n = 0.19), including one clear outlier
(externally studentized residual = 3.6). In a leave-one-subject-out refit, no predictor retained a
stable sign — every coefficient reversed direction depending on which single participant was
omitted — indicating that the cohort is too small to estimate even this five-term model with
stability.

## 3.3 Secondary confirmatory analysis

An Elastic Net over the full eight-feature panel plus age and sex, with all scaling and
hyperparameter selection confined to training folds, selected a penalty
(α = 43.2, mixing parameter = 0.10) that shrank all ten coefficients to zero; the retained model
was the intercept alone (14.6, the cohort mean). Out-of-fold performance was at or below that of a
mean-only predictor (R² = −0.06, 95% CI −0.50 to −0.02; mean absolute error 13.3 NSI points), and
predicted values were compressed to a near-constant line across the full observed range
(Figure 5). Thus the regularized full-panel analysis converged on the same conclusion as the
primary model: no feature improved out-of-sample prediction.

## 3.4 Supportive and transparency analyses

Domain-specific models reproduced this pattern. The resting-only model (n = 25) showed the largest
in-sample fit (R² = 0.31) but a near-zero adjusted R² (0.08), a non-significant omnibus test
(p = 0.29), and negative out-of-fold R² (−0.59); the ERP-only model (n = 21) was similarly
uninformative (adjusted R² = −0.12; out-of-fold R² = −1.13). The full ten-term ordinary-least-
squares model, reported solely for transparency, illustrated the expected overfitting of an
unpenalized model at this sample size: despite an in-sample R² of 0.39 it had a negative adjusted
R² (−0.22), a design condition number exceeding 22,000, and the poorest generalization of any
model (out-of-fold R² = −3.58). It is descriptive only and was not used for inference.

## 3.5 Exploratory analyses

Exploratory penalized (ridge, LASSO) and flexible (random forest, gradient boosting) learners,
each cross-validated on the frozen folds, all produced negative out-of-fold R² (range −0.06 to
−0.36); the least-poor models were those that regularized most strongly toward the mean, and the
flexible learners recovered no non-linear structure. Adding spectral entropy did not alter any
result. No exploratory analysis is central to the conclusions.

## 3.6 Sensitivity analyses

Conclusions were unchanged across pre-specified sensitivity analyses, including the n = 20 variant
that additionally excluded the single participant with limited eyes-open data (adjusted R² =
−0.21), robust HC3 inference, and the comparison of penalized with unpenalized estimators (all
penalized models converged on the mean predictor).

---

**Summary.** Across the primary parsimonious model, a full-panel Elastic Net, domain-specific
supportive models, and a range of exploratory learners, early resting-state and task-evoked EEG
features were not reliably associated with, and did not predict out-of-sample, persistent
post-concussive symptom burden at approximately four months. Effect sizes were small with
confidence intervals spanning zero, coefficient estimates were unstable to individual
observations, and every cross-validated model performed at or below a demographic baseline. These
findings are most appropriately interpreted as inconclusive given the modest sample size rather
than as positive evidence of absence; they do not exclude modest true associations that a larger,
independently replicated cohort could resolve.
