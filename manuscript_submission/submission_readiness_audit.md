# Submission Readiness Audit (Final)

**Audit date:** 2026-06-12
**Status:** Manuscript package finalized; public GitHub repository verified. Journal-specific
formatting is tracked separately in `journal_submission/`.

## 1. Unresolved-token count (target: all zero)

| Token | Count |
|---|---:|
| Author-verification marker | 0 |
| Reference-needed marker | 0 |
| To-do marker | 0 |
| Generic placeholder marker | 0 |
| Pending commit marker | 0 |
| Pending Zenodo marker | 0 |

All author, affiliation, email, ORCID, ethics, funding, conflicts, data/code-availability, and
reference markers have been resolved with verified values. Unverifiable facts were omitted rather
than invented.

## 2. Overclaiming scan (manuscript prose)

| Term | Result |
|---|---|
| proven | 0 |
| validated | Only calibrated uses: no validated threshold / not a validated prognostic tool |
| confirmed | 0 |
| diagnostic biomarker | 0 |
| predictive biomarker | 0 |
| failed replication | 0; wording is "replication was infeasible" |

Calibrated language ("no stable evidence", "inconclusive", "underpowered", "did not generalize",
"replication was infeasible") is used throughout.

## 3. Sample-size consistency (by role)

| N | Role |
|---:|---|
| 25 | Eligible discovery cohort (acute mTBI, S1 EEG + S3 NSI); resting-only model |
| 21 | Primary, secondary, transparency, and ERP-only models (ERP reliability gate) |
| 20 | Prespecified sensitivity (additionally drops one eyes-open-low subject) |
| 91 | ds005114 Session-1 recordings scanned for replication feasibility |

Each value is used only in its correct role; none is interchanged.

## 4. Git and archive integrity

| Item | Value |
|---|---|
| Repository (verified public remote) | https://github.com/blakepi/openneuro-tbi-eeg-biomarker-reanalysis |
| Current branch | `main` |
| Archived release commit | `ac84ad461197c20a7af7caeac7b293d6f1133d98` (`ac84ad461197c20a7af7caeac7b293d6f1133d98`) - CNP submission package |
| Verified public head before journal formatting | `953a06a` (`953a06aae8803c447ec29ac37bedbf8fbfb54856`) |
| Remote / public status | Public repository verified by GitHub API (`private: false`) |
| Release tag | `v1.0.0-cnp-submission` |
| Release status | GitHub tag pushed; DOI minted on Zenodo |
| Zenodo DOI status | `10.5281/zenodo.20682573` (https://doi.org/10.5281/zenodo.20682573) |
| Large raw EEG excluded | Yes - `.gitignore` excludes `data/`, `*.set/.fdt/.fif/.edf/.mat/.xlsx`, `.venv/` |
| Credentials staged | None identified |

## 5. Result integrity (no results changed)

| Artifact | MD5 (first 8) | Status |
|---|---|---|
| `outputs/splits/frozen_cv_folds.csv` | `453fede5` | unchanged |
| `outputs/analysis/model_coefficients.csv` | `5f3d418e` | unchanged |
| `outputs/analysis/cv_performance.csv` | `660825f0` | unchanged |
| `outputs/features/*` | - | unchanged |

No new statistical models were run during finalization. The locked statistical hierarchy and sample
sizes are unchanged.

## 6. Manuscript readiness

| Item | Status |
|---|---|
| Abstract word count | 288 words in original package; 223-word CNP abstract in `journal_submission/` |
| Figures present | 7 main + 4 supplementary (11 PNGs in `figures/`) |
| Tables present | 5 main (`tables/`) + 6 supplementary (`supplement/supplementary_tables.md`) |
| Supplement present | Methods, tables, figures, final locked plan, replication audit |
| References present | 26 entries in `references.bib` |
| Cover letter | Present |
| Title page | Present |
| Data availability | Present (four OpenNeuro DOIs; raw not redistributed) |
| Code availability | Present (verified GitHub URL + commits `953a06a`/`a995ac0`, MIT) |
| Ethics statement | Present (IRB-exempt; public deidentified data; no protocol number invented) |
| Conflicts statement | Present (none) |
| Funding statement | Present (none) |
| AI assistance disclosure | Present; AI is not an author |

## 7. Remaining issues

None internal to the scientific analysis package. Before portal upload, use the
`journal_submission/` audit for journal-specific formatting requirements.

## Number-to-source map (headline values)

| Reported value | Source |
|---|---|
| Primary n = 21; adjusted R2 = -0.19; R2 = 0.11; F p = 0.86 | `outputs/analysis/model_fit_summary.csv` |
| P3b standardized beta = +0.24, 95% CI -0.40 to 0.88; FDR p approximately 0.96 | `outputs/analysis/model_coefficients.csv` |
| OOF R2: baseline -0.40, primary -1.38, EN -0.06, full OLS -3.58, RF -0.29, XGB -0.36 | `outputs/analysis/cv_performance.csv` |
| Elastic Net all 10 coefficients = 0 | `outputs/analysis/elasticnet_coefficients.csv` |
| Resting-only n = 25; ERP-only n = 21 | `outputs/analysis/model_fit_summary.csv` |
| Outcome n = 25: mean 15.1, SD 15.7, median 9, range 0-51; skew 0.85 -> raw NSI | `outputs/analysis/ds003522_s1_analysis_table.csv`; `reports/phase4_results.md` |
| ds005114 0/91 rest, 0/91 oddball, 91/91 DPX; 0/8 features | `reports/phase5_replication_results.md`; `outputs/analysis/replication_feature_availability.csv` |
| ds003490 8/8 features but Parkinson's cohort | `outputs/analysis/replication_feature_availability.csv`; OpenNeuro ds003490 |
| 25/25 readable EEG; no feasibility-threatening QC failures | `reports/phase2_eeg_qc_report.md`; `outputs/qc/ds003522_s1_qc_summary.csv` |
| Dataset DOIs/versions | OpenNeuro `dataset_description.json` |
