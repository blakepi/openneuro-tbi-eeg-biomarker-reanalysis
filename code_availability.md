# Code Availability

Analysis code and derived manuscript materials are available at:
**https://github.com/blakepi/openneuro-tbi-eeg-biomarker-reanalysis**.

The verified public repository head before journal-specific formatting was commit **953a06a** (full
hash `953a06aae8803c447ec29ac37bedbf8fbfb54856`). The submitted scientific analysis package
corresponds to commit **a995ac0** (full hash `a995ac0edddf83fb2a381e253dc6e17f7053f230`), which
contains the complete analysis pipeline, frozen cross-validation folds, derived outputs, figures,
and manuscript package. Later commits update repository metadata and journal-specific formatting
only; they do not change analyses or results.

- **License:** MIT (code). Manuscript text and figures remain Copyright (c) 2026 Gregory Blake
  Pierpoint unless separately licensed.
- **Environment:** Python 3.14; MNE 1.12; MNE-BIDS; specparam 2.0; scikit-learn 1.9; statsmodels
  0.14; xgboost 3.2. Random seeds fixed at 42.
- **Raw data:** not redistributed; obtained from OpenNeuro (see `data_availability.md`).
- **Locked analysis plan:** included (`reports/final_locked_analysis_plan.md`), version-controlled so
  its pre-modeling status is verifiable in the commit history.

Zenodo DOI not yet created. Optional before submission.
