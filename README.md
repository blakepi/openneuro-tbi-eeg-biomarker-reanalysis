# Leakage-Safe EEG Biomarker Analysis After Mild Traumatic Brain Injury: An Internally Locked OpenNeuro Reanalysis and Replication Feasibility Study

This repository contains the analysis code, frozen analysis plan, derived outputs, and manuscript materials for:

**Leakage-Safe EEG Biomarker Analysis After Mild Traumatic Brain Injury: An Internally Locked OpenNeuro Reanalysis and Replication Feasibility Study**

## Reviewer quick start

This repository is intended to let reviewers inspect the analysis decisions, frozen folds, derived outputs, and replication-feasibility audit without redistributing raw EEG data.

- Final CNP submission package: `journal_submission/cnp_submission_final_20260613/`
- Manuscript source package: `journal_submission/` and `manuscript_submission/`
- Locked analysis plan: `reports/statistical_analysis_plan.md` and `journal_submission/supplement_cnp.docx`
- Frozen subject-level folds: `outputs/splits/frozen_cv_folds.csv`
- Main model coefficients: `outputs/analysis/model_coefficients.csv`
- Out-of-fold performance: `outputs/analysis/cv_performance.csv`
- Elastic Net coefficients: `outputs/analysis/elasticnet_coefficients.csv`
- Replication feasibility: `outputs/analysis/replication_feature_availability.csv`
- Figures: `outputs/figures/`, `journal_submission/figures/`, and the submission figure files
- Derived feature tables: `outputs/features/`

Raw EEG data are publicly available from OpenNeuro and are not redistributed here.

## Main findings

In the primary model (n = 21), no predictor's 95% confidence interval excluded zero. The Elastic Net retained no EEG feature for the primary NSI outcome. All EEG-feature models had negative out-of-fold R-squared. The least-poor penalized models performed less poorly than the age+sex baseline only by shrinking to, or near, a mean/intercept predictor rather than by retaining a reproducible EEG-feature signal.

A prespecified secondary P3b association with S1-to-S3 Rivermead change was treated as hypothesis-generating and does not alter the primary NSI conclusion.

Feature-identical clinical replication was not estimable in the surveyed related public datasets because no available dataset matched both the EEG paradigm/state and the post-concussive clinical outcome structure required by the locked feature definitions.

## Release/package state

The final reviewer-facing CNP submission package is released as GitHub tag `v1.0.1-cnp-submission-final` and archived on Zenodo at https://doi.org/10.5281/zenodo.20682573 (DOI: `10.5281/zenodo.20682573`).

The frozen analyses and derived outputs were not changed by the final reviewer-facing manuscript/repository packaging pass.

## Citation and DOI

Please cite the archived Zenodo record for the reviewer-facing release: https://doi.org/10.5281/zenodo.20682573 (DOI: `10.5281/zenodo.20682573`). The GitHub source repository remains available at https://github.com/blakepi/openneuro-tbi-eeg-biomarker-reanalysis.

## Repository structure

```text
scripts/                      analysis pipeline
reports/                      locked plan and phase reports
outputs/                      derived outputs committed for review
journal_submission/           CNP-ready manuscript package
manuscript_submission/        manuscript source package
data/                         raw/processed EEG, git-ignored and not redistributed
```

## Reproducibility

See `reproducibility.md` for the step-by-step computational workflow. The final polish pass did not rerun the scientific analysis.

## License

Code is released under the MIT License (`LICENSE`). Manuscript text and figures remain Copyright (c) 2026 Gregory Blake Pierpoint unless separately licensed. Original OpenNeuro data remain under their respective OpenNeuro/CC0 terms and are not redistributed here.

## Contact

Gregory Blake Pierpoint, Macon and Joan Brock Virginia Health Sciences, Eastern Virginia Medical School at Old Dominion University, Norfolk, Virginia, USA. Email: pierpogb@odu.edu. ORCID: https://orcid.org/0000-0001-8288-8549
