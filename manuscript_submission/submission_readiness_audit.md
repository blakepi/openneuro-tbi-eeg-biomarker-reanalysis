# Submission Readiness Audit

**Audit date:** 2026-06-11

## Executive Status

**Status:** scientifically coherent draft package, not yet submission-ready.

The manuscript package is assembled and internally consistent with the locked project outputs on the main numerical results. Remaining blockers are mostly author-side administrative and reference-completion tasks: author list, affiliations, institutional ethics/exemption language, repository/DOI/license, dataset DOI/version verification for all datasets, journal formatting, and completion of literature citations.

## Required Files

| Required item | Status |
|---|---|
| `main_manuscript.md` | Present |
| `abstract.md` | Present |
| `highlights.md` | Present |
| `cover_letter.md` | Present |
| `title_page.md` | Present |
| `tables/` with Tables 1-5 | Present |
| `figures/` with main and supplementary figures | Present |
| `supplement/supplementary_methods.md` | Present |
| `supplement/supplementary_tables.md` | Present |
| `supplement/supplementary_figures.md` | Present |
| `supplement/final_locked_analysis_plan.md` | Present |
| `supplement/replication_feasibility_audit.md` | Present |
| `reporting_checklist.md` | Present |
| `target_journal_recommendations.md` | Present |

## Number-To-Source Map

| Reported value | Source |
|---|---|
| Primary model n = 21 | `outputs/analysis/model_fit_summary.csv`; `reports/phase4_results.md` |
| Primary adjusted R2 = -0.19 | `outputs/analysis/model_fit_summary.csv` (`-0.18617089677691068`) |
| Primary R2 = 0.11 | `outputs/analysis/model_fit_summary.csv` (`0.11037182741731688`) |
| Primary F p = 0.86 | `outputs/analysis/model_fit_summary.csv` (`0.8598594557840847`) |
| P3b standardized beta = +0.24 | `outputs/analysis/model_coefficients.csv` (`0.24032313552218196`) |
| P3b standardized 95% CI = -0.40 to 0.88 | `outputs/analysis/model_coefficients.csv` |
| Primary all FDR p values approximately 0.96 | `outputs/analysis/model_coefficients.csv` (`0.9623210557200663`) |
| Baseline age+sex OOF R2 = -0.40 | `outputs/analysis/cv_performance.csv` |
| Primary OOF R2 = -1.38 | `outputs/analysis/cv_performance.csv` |
| Elastic Net OOF R2 = -0.06 | `outputs/analysis/cv_performance.csv` |
| Full OLS OOF R2 = -3.58 | `outputs/analysis/cv_performance.csv` |
| Random Forest / XGBoost OOF R2 = -0.29 / -0.36 | `outputs/analysis/cv_performance.csv` |
| Elastic Net all 10 coefficients zero | `outputs/analysis/elasticnet_coefficients.csv` |
| Resting-only n = 25; ERP-only n = 21 | `outputs/analysis/model_fit_summary.csv`; `reports/phase4_results.md` |
| ds005114 all 91 S1 recordings DPX, 0/91 rest, 0/91 oddball | `reports/phase5_replication_results.md`; `outputs/analysis/replication_feature_availability.csv` for feature-level extractability |
| ds003523 0/8 locked features extractable | `outputs/analysis/replication_feature_availability.csv`; `reports/phase5_replication_results.md` |
| ds003490 8/8 features extractable but wrong clinical population/outcome | `outputs/analysis/replication_feature_availability.csv`; `reports/phase5_replication_results.md` |
| 25/25 readable EEG and no feasibility-threatening QC failures | `reports/phase2_eeg_qc_report.md`; `outputs/qc/ds003522_s1_qc_summary.csv` |
| Raw NSI retained because skewness = 0.85 | `reports/phase4_results.md` |

## Consistency Checks

| Check | Status | Notes |
|---|---|---|
| Sample-size consistency | Pass with caveat | Primary n = 21; resting-only n = 25; sensitivity n = 20; ds005114 scan n = 91. These are distinct and should remain labelled. |
| Locked statistical hierarchy preserved | Pass | Primary OLS, secondary Elastic Net, full OLS transparency, exploratory learners only. |
| Null result language | Pass | Manuscript uses "no stable evidence", "inconclusive", "underpowered", and "replication infeasible." |
| Replication infeasible vs replication-failure wording | Pass | No replication-failure framing. |
| No new models run for manuscript assembly | Pass | Manuscript assembly used existing outputs and reports only. |
| Discovery analysis files and frozen folds preserved | Pass | No edits were made to `outputs/analysis/`, `outputs/features/`, or `outputs/splits/`. |
| Figures present | Pass | Main Figures 1-7 and Supplementary Figures S1-S4 are present in `manuscript_submission/figures/`. |
| Tables present | Pass | Tables 1-5 present; Supplementary Tables S1-S6 included in `supplementary_tables.md`. |
| References completed | Not ready | Multiple `[REFERENCE NEEDED]` placeholders remain. |
| Administrative statements completed | Not ready | Author list, funding, conflicts, ethics/exemption, repository URL/DOI, and license require author verification. |

## Automated Text Checks

Initial search terms requested by the assembly prompt:

| Term | Result | Interpretation |
|---|---:|---|
| `proven` | 0 | Pass |
| `diagnostic biomarker` | 0 | Pass |
| replication-failure phrase | 0 | Pass |
| `predictive biomarker` | 0 after wording edit | Pass |
| `confirmed` | 0 after wording edit | Pass |
| `validated` | 2 contextual hits in copied locked analysis plan | Not used to claim biomarker validation; one states no validated symptom threshold, one states the cohort is not a validated prognostic tool. |

Sample-size checks should be interpreted by role: `n = 21` is the primary/ERP-gated model sample, `n = 25` is the resting-only eligible discovery cohort, `n = 20` is the eyes-open sensitivity subset, and `n = 91` is the full ds005114 Session-1 scan.

## Figure File Check

| Figure | File | Status |
|---|---|---|
| Figure 1 | `figures/Figure_1_study_flow.png` | Present |
| Figure 2 | `figures/Figure_2_recording_structure.png` | Present |
| Figure 3 | `figures/Figure_3_preprocessing_pipeline.png` | Present |
| Figure 4 | `figures/Figure_4_primary_coefficient_forest.png` | Present |
| Figure 5 | `figures/Figure_5_predicted_vs_observed.png` | Present |
| Figure 6 | `figures/Figure_6_feature_availability_matrix.png` | Present |
| Figure 7 | `figures/Figure_7_discovery_vs_replication.png` | Present |
| Figure S1 | `figures/FigureS1_partial_effects.png` | Present |
| Figure S2 | `figures/FigureS2_elasticnet_path.png` | Present |
| Figure S3 | `figures/FigureS3_calibration.png` | Present |
| Figure S4 | `figures/FigureS4_family_contribution.png` | Present |

## Placeholders Requiring Author Review

The package intentionally contains placeholders rather than invented details. Main unresolved classes:

- `[AUTHOR VERIFY: author list and affiliations]`
- `[AUTHOR VERIFY: corresponding author details and email]`
- `[AUTHOR VERIFY: ORCID iDs]`
- `[AUTHOR VERIFY: public preregistration / repository / DOI]`
- `[AUTHOR VERIFY: code license]`
- `[AUTHOR VERIFY: ds005114, ds003523, ds003490 DOI/version]`
- `[AUTHOR VERIFY: institutional IRB review/exemption and original ethics citation]`
- `[AUTHOR VERIFY: CRediT author contributions]`
- `[AUTHOR VERIFY: funding statement]`
- `[AUTHOR VERIFY: conflicts of interest]`
- `[AUTHOR VERIFY: journal-specific highlight length and formatting]`
- `[REFERENCE NEEDED: ...]` literature placeholders throughout the Introduction, Methods, Discussion, and References.

Final automated placeholder scan found 100 placeholder hits across the manuscript package
(58 `[AUTHOR VERIFY]` + 42 `[REFERENCE NEEDED]`). These are intentional unresolved author/reference
items, not inferred facts.

**Post-assembly reconciliation (independently verified):** (i) the standalone `abstract.md` was
trimmed to ~288 words to meet the 250–300-word target and match the in-manuscript abstract;
(ii) Results cross-references in `reporting_checklist.md` were aligned to the main-manuscript
numbering (Elastic Net = 3.3, transparency = 3.4, replication = 3.6); (iii) frozen folds and
discovery outputs were re-checksummed and are byte-identical (`frozen_cv_folds.csv` = 453fede5…,
`model_coefficients.csv` = 5f3d418e…, `cv_performance.csv` = 660825f0…); (iv) overclaiming-word
scan of the manuscript prose returned no hits outside this audit's own search-term table.

## Version-Control Check

`git status --short` was attempted in `C:\Research\EEG`, but the `git` executable is not available on PATH in this environment. No model scripts were run during manuscript assembly, and source outputs under `outputs/analysis/`, `outputs/features/`, and `outputs/splits/` were not edited.

## Readiness Recommendation

Before submission:

1. Complete the references with verified citations and no fabricated bibliographic metadata.
2. Verify every OpenNeuro dataset DOI/version.
3. Add author names, affiliations, ORCID identifiers, contributions, funding, conflicts, acknowledgments, and ethics/exemption language.
4. Decide target journal and adapt formatting, word count, highlights, figure files, table format, and data/code availability statements.
5. Confirm repository release plan, license, and archival DOI.
6. Rerun the automated checks in this audit after administrative edits.
