# Abstract

**Background.** Persistent post-concussive symptoms affect a clinically important minority after
mild traumatic brain injury (mTBI), yet acute prognostication is difficult. Resting-state and
task-evoked EEG have been proposed as prognostic biomarkers, but the supporting literature often
uses small samples and pipelines vulnerable to leakage and overfitting.

**Objective.** To test, in a preregistered, leakage-safe framework, whether early EEG features
predict later symptom burden after acute mTBI in a public dataset, and whether the analysis can be
replicated in related public datasets.

**Methods.** We reanalysed OpenNeuro ds003522 (acute mTBI; auditory three-stimulus oddball with
embedded eyes-closed/eyes-open rest). Subjects were keyed on a stable identifier (URSI) to prevent
leakage; subject-level cross-validation folds were frozen before EEG processing; a biologically
motivated panel (posterior individual alpha frequency, global aperiodic exponent, frontal
theta/alpha ratio, occipital relative alpha, P3b/P3a amplitude and latency) was extracted with
boundary-aware preprocessing. The primary outcome was the Session-3 Neurobehavioral Symptom
Inventory (NSI) total. The statistical hierarchy was locked before outcome modeling.

**Results.** In the primary model (n = 21), no predictor's 95% confidence interval excluded zero
(largest standardized β = 0.24, 95% CI −0.40 to 0.88; adjusted R² = −0.19), and coefficients were
unstable under leave-one-out. The Elastic Net shrank all coefficients to zero; every model produced
negative out-of-fold R² and none exceeded an age+sex baseline. Replication in ds005114 was
infeasible (0/91 recordings contained rest or oddball markers; 0/8 features extractable); ds003523
likewise; the one paradigm-matched dataset (ds003490) is a Parkinson's cohort without a
post-concussive outcome.

**Conclusions.** No stable evidence emerged that the tested EEG features predict persistent
post-concussive symptoms; the result is inconclusive and underpowered, not a demonstration of
absence. Feature-identical public-dataset replication was infeasible owing to EEG paradigm
fragmentation; robust mTBI biomarker claims will require larger, longitudinal, paradigm-matched,
outcome-linked cohorts.

*(~290 words)*
