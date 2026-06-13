# Response-To-Reviewers Skeleton

## Opening

Thank you for the careful preregistration-fidelity review. We agree that the prior package underreported several locked secondary, sensitivity, attrition, and execution-note elements. We completed a targeted preregistration-fidelity revision without changing the locked estimand, feature definitions, subject identity rules, frozen folds, or primary conclusions.

## Major Issues

**M1. Registered secondary outcomes.** We agree. The registered secondary outcomes are now reported in Supplementary Table S7 and summarized in Results section 3.5. The added outcomes are S3 Rivermead total, S1-to-S3 NSI change, and S1-to-S3 Rivermead change. The S1-to-S3 Rivermead-change P3b association is explicitly labeled secondary and hypothesis-generating, was not externally replicated, and is not promoted to the primary conclusion.

**M2. Prespecified sensitivity battery.** We agree. The sensitivity battery is now inventoried and reported in Supplementary Table S8, with omissions documented in Table S11 and `outputs/prereg_fidelity_revision_20260612_200455/sensitivities/sensitivity_omissions_or_infeasibility.md`. HC3 inference, peak ERP metric, eyes-open features, predictor-only MICE, ERP threshold, added covariates, Session-2 timing, and log1p outcome checks did not alter the primary interpretation. The 0.1-Hz high-pass and sub-040 S-code recovery branches were not run because they were not represented in frozen features or operationalized event mappings.

**M3. Attrition/completer check.** We agree. The S3 completer versus non-completer comparison is now reported in Supplementary Table S9 and cited in Methods/Limitations. The public Group-0 Session-1 EEG universe was n = 44, with 25 S3 NSI completers and 19 non-completers. IPW was not implemented because the locked plan did not specify an operational imbalance trigger; this is documented rather than invented post hoc.

**M4. Locked-plan N = 20 versus primary n = 21.** We agree this needed transparent reconciliation. Methods and Supplementary Table S11 now explain that the locked-plan combined-panel N = 20 reflected the eyes-open-low sensitivity excluding sub-068, whereas the primary model used eyes-closed rest plus reliable ERP and retained sub-068, yielding n = 21. The n = 20 eyes-open/low-data sensitivity remains reported with unchanged conclusions.

**M5. Estimation versus prediction and OOF R2 framing.** We agree. The Methods and Discussion now frame OOF R2/MAE as leakage-safety transparency metrics, not stable model-ranking estimates at n = 21. The overstrong `generalizable prediction` and `no model exceeded baseline` framing was removed from the final rendered package.

## Minor Issues

**m1. Acute versus sub-acute terminology.** Revised. The discovery cohort is described as sub-acute/early post-injury mTBI where scientifically appropriate, with the source title/dataset terminology handled neutrally.

**m2. n = 44 versus source-publication n = 38.** Clarified. Table 2 and the supplement state that the public BIDS metadata contain 44 Group-0 participants with Session-1 EEG and that the exact reason for a smaller source-publication analytic subset was not verifiable locally.

**m3. Alpha-window caveat.** Revised. The Methods/Limitations now state that the locked 7-13 Hz posterior IAF window cannot detect dominant posterior slowing below 7 Hz.

**m4. specparam fit quality.** Revised. Supplementary Table S10 and Figure S5 summarize exported specparam fit R2 values. No representative model fit plot was regenerated because PSD/model objects were not exported by the locked pipeline.

**m5. Ocular correction/ICA.** Revised. Methods and Limitations now state that VEOG/EKG were typed non-EEG and excluded from features/reference, and that no ICA/SSP/EOG-regression branch was added after outcome modeling because it would add post hoc analytic flexibility.

**m6. Bad-channel after average reference.** Revised. Methods/Supplement now report that 19/25 participants had no interpolated channels and 6/25 had 1-3 interpolated channels, with bad-channel detection after average rereferencing noted as a limitation.

**m7. Self-audit framing.** Revised. Code availability now states that Phase 6 establishes internal computational reproducibility under the local environment, not independent external validation or independent code review.

**m8. Formatting artifacts.** Rechecked. Current DOCX text exports were scanned for Markdown leftovers and stale phrases; no hits remained. Visual QA PDFs/PNGs/contact sheets are saved under `visual_qa/`.

**m9. Article type.** Revised. Title page and cover letter now use `Research Paper`, matching the portal language.

## Results And Conclusions

The primary scientific results did not change: primary n = 21, R2 = 0.11, adjusted R2 = -0.19, omnibus F p = 0.86, P3b standardized beta = 0.24 with 95% CI -0.40 to 0.88, Elastic Net alpha = 43.2, mixing parameter = 0.10, zero selected coefficients, and OOF R2 approximately -0.06. The revisions add preregistered completeness reporting and QC transparency rather than changing the primary result.
