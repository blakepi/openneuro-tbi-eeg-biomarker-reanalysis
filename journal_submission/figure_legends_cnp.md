# Figure Legends

**Figure 1. Study design and cohort flow.** Participant accounting from OpenNeuro ds003522 to each effective analytic sample. The chronic-TBI arm (no longitudinal outcome) and controls (not part of within-mTBI prediction) exit outcome modeling. Modality-specific quality control yields 25 (resting), 21 (ERP), and 21 (combined-panel) analytic samples. Subject-level cross-validation folds were frozen before EEG processing; exclusions were applied within each participant's pre-assigned fold and folds were never regenerated.

**Figure 2. Structure of the ds003522 continuous Session-1 recording.** A single continuous recording (~15-28 min) contained eyes-closed and eyes-open resting blocks bracketing two auditory-oddball runs. Resting and task segments were identified from event markers; a single boundary event at recording onset (no internal discontinuities) was handled by a boundary-aware pipeline. Resting blocks provided spectral/aperiodic features; oddball runs provided P3b (target) and P3a (novel) ERPs.

**Figure 3. EEG preprocessing and feature-extraction pipeline.** A single fixed parameter set, selected without reference to any outcome, was applied to every recording; raw files were never modified. The boundary-aware pipeline branched into resting-state (0.5-45 Hz) and ERP (+40-Hz low-pass) streams. Schematic; no outcome data shown.

**Figure 4. Primary-model coefficient forest plot.** Standardized beta coefficients (points) with 95% confidence intervals (bars) for the primary parsimonious model (n = 21); resting features in teal, ERP in orange, covariates in grey, with a colour legend and predictor labels identifying each feature family. All intervals span zero (dashed line).

**Figure 5. Out-of-fold predicted versus observed NSI (Elastic Net).** Out-of-fold predictions versus observed Session-3 NSI total. Predictions collapse toward the cohort mean (dotted line) across the full observed range (0-51), consistent with the penalized model retaining no feature (R2_oof = -0.06). The dashed line is identity.

**Figure 6. Dataset x feature availability matrix.** Extractability of each locked feature, with its preregistered definition, by dataset (green = extractable). ds005114 and ds003523 lack eyes-closed rest and the auditory oddball (0/8); ds003490 supports all eight features but is a Parkinson's cohort without a post-concussive outcome.

**Figure 7. Discovery estimates with replication status.** Frozen discovery standardized beta coefficients (95% CI) for the primary-model EEG predictors, annotated to indicate that replication in ds005114 is not estimable because the source paradigms are absent.

**Supplementary figures S1-S5.** S1, partial (added-variable) plots for the primary EEG predictors; S2, Elastic Net coefficient path; S3, out-of-fold calibration; S4, resting-versus-ERP standardized contribution from the full-panel (descriptive) model; S5, specparam fit-quality distribution.
