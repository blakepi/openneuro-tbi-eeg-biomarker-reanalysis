# Code Availability

Analysis code and derived manuscript materials (download, identity resolution, preprocessing, feature extraction, frozen cross-validation folds, models, figures, and manuscript-supporting materials) are available in the public GitHub repository: https://github.com/blakepi/openneuro-tbi-eeg-biomarker-reanalysis.

The reviewer-facing submission package is prepared for GitHub release `v1.0.0-cnp-submission`; the exact archived commit is the commit targeted by that release tag. Raw EEG data are publicly available from OpenNeuro and are not redistributed in the code repository. The repository is released under the MIT License; the locked analysis plan and machine-readable bibliography files are included. A Zenodo DOI will be added if minted before final journal upload.

A post-analysis reproducibility audit regenerated the frozen analysis outputs into `outputs/reanalysis_audit_20260612_115010/` without overwriting the original outputs; all 25 analytic ds003522 Session-1 `.set/.fdt` pairs were verified as data-readable with MNE, all 44 prespecified numeric checks matched the frozen outputs, and the only non-exact artifact was a non-scientific `--dry-run` download-manifest difference.

- **License:** MIT (code). Manuscript text and figures remain Copyright (c) 2026 Gregory Blake Pierpoint unless separately licensed.
- **Environment:** Python 3.14; MNE 1.12; MNE-BIDS; specparam 2.0; scikit-learn 1.9; statsmodels 0.14; xgboost 3.2. Random seeds fixed at 42.
- **Raw data:** not redistributed; obtained from OpenNeuro (see `data_availability.md`).
- **Locked analysis plan:** included (`reports/final_locked_analysis_plan.md`), version-controlled so its pre-modeling status is verifiable in the commit history.
