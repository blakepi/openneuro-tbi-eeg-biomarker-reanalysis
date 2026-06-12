# Leakage-Safe EEG Biomarker Analysis After Mild Traumatic Brain Injury

**A Preregistered OpenNeuro Reanalysis and Replication Feasibility Study**

[![License: MIT](https://img.shields.io/badge/Code%20License-MIT-blue.svg)](LICENSE)

## 1. Plain-language summary

After a concussion (mild traumatic brain injury, mTBI), some people have symptoms that last for
months. It would help doctors to know early who is at risk. Brain electrical activity (EEG) has been
proposed as an early "biomarker." This project tested, very carefully and using only public data,
whether early EEG features could predict who still had symptoms about four months later. The honest
answer here was **no stable signal** — the EEG measures did not reliably predict later symptoms in
this small group, and the result is best described as inconclusive rather than proof of no effect. We
then tried to repeat the analysis in related public datasets and found we **could not**, because
those datasets used different tasks and did not contain the same kind of EEG recordings. The study's
value is in showing how to do this kind of work rigorously and in documenting why "more public
datasets" does not automatically mean a finding can be checked.

## 2. Scientific summary

A preregistered, leakage-safe longitudinal reanalysis of OpenNeuro **ds003522** (acute mTBI; auditory
three-stimulus oddball with embedded eyes-closed/eyes-open rest) evaluated whether a biologically
motivated Session-1 EEG panel — posterior individual alpha frequency, global aperiodic exponent,
frontal theta/alpha ratio, occipital relative alpha, and P3b/P3a amplitude and latency — predicts the
Session-3 Neurobehavioral Symptom Inventory (NSI) total. Subjects were keyed on a stable identifier
(URSI) to prevent cross-dataset leakage; subject-level cross-validation folds were frozen and the
statistical hierarchy locked before any feature–outcome relationship was examined. In the primary
model (n = 21) no predictor's 95% CI excluded zero (largest standardized β = 0.24; adjusted
R² = −0.19); an Elastic Net shrank all coefficients to zero; and no model exceeded an age+sex baseline
out of fold. A planned replication in ds005114 was **infeasible** (0/91 Session-1 recordings contained
rest or oddball markers), as was replication in ds003523; the one paradigm-matched dataset (ds003490)
is a Parkinson's cohort without a post-concussive outcome. Findings are inconclusive and underpowered;
robust mTBI EEG biomarker claims require larger, paradigm-matched, outcome-linked cohorts.

## 3. Repository structure

```
EEG/
├── README.md                     # this file
├── LICENSE                       # MIT (code); manuscript text reserved
├── CITATION.cff                  # how to cite
├── requirements.txt              # pip dependencies
├── environment.yml               # conda environment
├── MANIFEST.md                   # what each file/folder is
├── reproducibility.md            # step-by-step reproduction
├── data_availability.md          # dataset DOIs; data not redistributed
├── code_availability.md          # repository + commit metadata
├── scripts/                      # 00–15: download, QC, splits, preprocessing, features, models, figures
├── reports/                      # phase 0–5 reports + locked analysis plan
├── outputs/
│   ├── metadata_summary_tables/  # cohort crosswalk, attrition, missingness (derived)
│   ├── splits/                   # frozen_cv_folds.csv (leakage-safe folds)
│   ├── features/                 # extracted feature matrices + QC (derived)
│   ├── qc/                       # EEG quality-control summary (derived)
│   ├── analysis/                 # model outputs (derived)
│   └── figures/                  # publication figures (PNG)
├── manuscript_submission/        # main manuscript, abstract, tables, figures, supplement, references.bib
└── data/                         # NOT committed: raw/processed EEG + fetched metadata (git-ignored)
```

## 4. How to reproduce

See `reproducibility.md` for full detail. In brief: set up the environment (§5), download the
Session-1 EEG for eligible subjects (`scripts/04_download_s1_eeg.py`), then run the numbered scripts
in order (preprocessing → feature extraction → frozen splits → models → figures). The frozen folds
and locked analysis plan must not be regenerated.

## 5. Environment setup

**Conda:**
```bash
conda env create -f environment.yml
conda activate eeg-mtbi
```

**pip (verified on Python 3.14):**
```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1   |   macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Key versions: MNE 1.12, MNE-BIDS, specparam 2.0, scikit-learn 1.9, statsmodels 0.14, xgboost 3.2.

## 6. Data acquisition

**The OpenNeuro datasets are not redistributed here.** Download them directly from OpenNeuro:

| Dataset | DOI |
|---|---|
| ds003522 (discovery) | 10.18112/openneuro.ds003522.v1.1.0 |
| ds005114 (replication) | 10.18112/openneuro.ds005114.v1.0.0 |
| ds003523 (replication) | 10.18112/openneuro.ds003523.v1.1.0 |
| ds003490 (paradigm reference) | 10.18112/openneuro.ds003490.v1.1.0 |

`scripts/00_download_or_load.py` (metadata) and `scripts/04_download_s1_eeg.py` (Session-1 EEG)
fetch what is needed over public HTTPS from the OpenNeuro S3 mirror. See `data_availability.md`.

## 7. Expected outputs

Derived tables in `outputs/` (cohort crosswalk, frozen folds, feature matrices, QC, model results)
and 11 figures in `outputs/figures/`. The headline result is a null/inconclusive primary model and an
infeasible replication; exact values are in `reports/phase4_results.md`,
`reports/phase5_replication_results.md`, and `manuscript_submission/`.

## 8. Manuscript

The full manuscript package is in `manuscript_submission/` (main manuscript, abstract, highlights,
cover letter, title page, Tables 1–5, Figures 1–7 + S1–S4, supplement, `references.bib`, reporting
checklist, submission-readiness audit, and target-journal recommendations).

## 9. Ethics statement

This study used publicly available, deidentified data from OpenNeuro and did not involve interaction
with human participants or access to identifiable private information. The project was considered
exempt from institutional review board review. The original data were collected by the source
investigators under their institutional approvals and are distributed under CC0.

## 10. AI assistance disclosure

AI-assisted coding and writing tools were used to support code generation, manuscript organization,
and editing. The author reviewed, verified, and takes full responsibility for all analyses,
interpretations, and manuscript content. AI tools are not authors.

## 11. Citation

Please cite the manuscript and the underlying OpenNeuro datasets (see `CITATION.cff` and
`manuscript_submission/references.bib`).

## 12. Code archive status

Public repository: https://github.com/blakepi/openneuro-tbi-eeg-biomarker-reanalysis.

Verified public head before journal-specific formatting: `953a06aae8803c447ec29ac37bedbf8fbfb54856`.
Zenodo DOI not yet created. Optional before submission.

## 13. License

Code is released under the MIT License (`LICENSE`). Manuscript text and figures remain Copyright (c)
2026 Gregory Blake Pierpoint unless separately licensed. Original OpenNeuro data remain under their
respective OpenNeuro/CC0 terms and are not redistributed here.

## 14. Contact

**Gregory Blake Pierpoint**
Macon and Joan Brock Virginia Health Sciences, Eastern Virginia Medical School at Old Dominion
University, Norfolk, Virginia, USA
Email: pierpogb@odu.edu · ORCID: https://orcid.org/0000-0001-8288-8549
