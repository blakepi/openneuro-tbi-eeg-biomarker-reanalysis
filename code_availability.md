# Code Availability

Analysis code and derived manuscript materials are available at the GitHub repository:
**https://github.com/gblakepierpoint/openneuro-tbi-eeg-biomarker-reanalysis**

The submitted version corresponds to commit **a995ac0** (full hash
`a995ac0edddf83fb2a381e253dc6e17f7053f230`), which contains the complete analysis pipeline, frozen
cross-validation folds, derived outputs, figures, and the manuscript package. Subsequent commits add
repository/availability metadata only.

- **License:** MIT (code). Manuscript text and figures remain Copyright (c) 2026 Gregory Blake
  Pierpoint unless separately licensed.
- **Environment:** Python 3.14; MNE 1.12; MNE-BIDS; specparam 2.0; scikit-learn 1.9; statsmodels
  0.14; xgboost 3.2. Random seeds fixed at 42.
- **Raw data:** not redistributed; obtained from OpenNeuro (see `data_availability.md`).
- **Locked analysis plan:** included (`reports/final_locked_analysis_plan.md`), version-controlled so
  its pre-modeling status is verifiable in the commit history.

> Note on publication status: at the time of writing, the local repository and commit above were
> created in the project working directory. Pushing to the public GitHub URL requires the author's
> authenticated GitHub account (`gh auth login` or an authenticated `git push`); see
> `manuscript_submission/submission_readiness_audit.md` for the exact publish commands. Verify the
> repository is public and the commit is present before citing this statement in a submission.
