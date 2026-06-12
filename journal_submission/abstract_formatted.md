# Structured Abstract

**Background.** Persistent post-concussive symptoms affect a clinically important minority after mild traumatic brain injury (mTBI), but early prognostication remains difficult. Resting-state and task-evoked EEG have been proposed as prognostic biomarkers, often in small samples vulnerable to leakage and overfitting.

**Objective.** To test whether early EEG features predict later symptom burden after acute mTBI in a preregistered, leakage-safe OpenNeuro reanalysis, and whether related public datasets permit feature-identical replication.

**Methods.** We reanalysed OpenNeuro ds003522, an acute mTBI dataset with auditory oddball EEG and embedded eyes-closed/eyes-open rest. Subjects were keyed by stable identifier; cross-validation folds and the statistical hierarchy were locked before outcome modeling. The feature panel included posterior individual alpha frequency, global aperiodic exponent, frontal theta/alpha ratio, occipital relative alpha, and P3b/P3a amplitude and latency. The primary outcome was Session-3 Neurobehavioral Symptom Inventory total.

**Results.** In the primary model (n = 21), no predictor's 95% CI excluded zero. The largest standardized association was P3b amplitude (beta = 0.24, 95% CI -0.40 to 0.88; adjusted R2 = -0.19), and all FDR-adjusted p values were approximately 0.96. Elastic Net shrank all 10 coefficients to zero; no model exceeded an age+sex baseline out of fold. Replication in ds005114 was infeasible because 0/91 recordings contained rest or oddball markers.

**Conclusions.** No stable evidence emerged that the tested EEG features predicted persistent post-concussive symptoms. Findings are inconclusive and underpowered; larger, paradigm-matched validation cohorts are needed.
