# MANIFEST

What each tracked file/folder in this repository is. Raw/processed EEG and fetched dataset metadata
under `data/` are **not** tracked (see `.gitignore`, `data_availability.md`).

## Top level
| Path | Description |
|---|---|
| `README.md` | Project overview, reproduction, citation, contact |
| `LICENSE` | MIT (code); manuscript text reserved |
| `CITATION.cff` | Citation metadata |
| `requirements.txt` / `environment.yml` | pip / conda environments |
| `MANIFEST.md` | This file |
| `reproducibility.md` | Step-by-step reproduction guide |
| `data_availability.md` | Dataset DOIs; data-not-redistributed statement |
| `code_availability.md` | Repository URL and submission commit metadata |
| `.gitignore` | Excludes EEG binaries, environments, secrets |

## scripts/ (run in numeric order)
| Script | Purpose |
|---|---|
| `00_download_or_load.py` | Fetch dataset metadata (and optionally full trees) |
| `01_inspect_bids_metadata.py` | Build metadata summary tables |
| `02_build_cohort.py` | Crosswalk, master subject/session table, missingness, attrition |
| `03_freeze_splits.py` | Frozen leakage-safe CV folds (seed 42) — do not regenerate |
| `04_download_s1_eeg.py` | Download Session-1 EEG for eligible subjects |
| `05_eeg_qc.py` | Read-only EEG quality control |
| `06_preprocess_ds003522_s1.py` | Boundary-aware preprocessing |
| `07_extract_rest_features_ds003522.py` | Resting spectral/aperiodic features |
| `08_extract_oddball_erp_features_ds003522.py` | P3b/P3a ERP features |
| `09_feature_qc_summary.py` | Feature distributions and usability flags |
| `_eeg_common.py` | Shared frozen constants (montage, regions, bands, windows) |
| `10_build_analysis_table.py` | Join features + outcome + covariates + folds |
| `11_fit_models.py` | Locked model hierarchy (primary, EN, supportive, transparency, exploratory) |
| `12_figures.py` | Model figures |
| `13_replication_feasibility.py` | Replication feature-availability scan |
| `14_replication_figures.py` | Replication figures |
| `15_schematic_figures.py` | Study-flow / recording-structure / pipeline schematics |

## reports/
Phase 0–5 reports, the statistical analysis plan, and the **final locked analysis plan**
(preregistration supplement). Manuscript drafts (introduction/methods/results/discussion).

## outputs/ (small, derived from public CC0 data)
| Folder | Contents |
|---|---|
| `metadata_summary_tables/` | crosswalk, master table, missingness, attrition |
| `splits/` | `frozen_cv_folds.csv`, `split_provenance.json` |
| `eeg_manifests/` | download manifest |
| `qc/` | EEG QC summary |
| `features/` | rest/ERP feature matrices, feature-QC, subject usability |
| `analysis/` | model coefficients, CV performance, diagnostics, replication tables |
| `figures/` | publication PNGs (11) |

## manuscript_submission/
`main_manuscript.md`, `abstract.md`, `highlights.md`, `cover_letter.md`, `title_page.md`,
`references.bib`, `reporting_checklist.md`, `submission_readiness_audit.md`,
`target_journal_recommendations.md`, plus `tables/` (1–5), `figures/` (1–7, S1–S4), and
`supplement/` (methods, tables S1–S6, figures, final locked plan, replication audit).
