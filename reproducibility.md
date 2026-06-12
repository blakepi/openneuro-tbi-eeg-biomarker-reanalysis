# Reproducibility

This pipeline is deterministic (all seeds fixed at 42) and leakage-safe by construction. The frozen
cross-validation folds (`outputs/splits/frozen_cv_folds.csv`) and the locked analysis plan
(`reports/final_locked_analysis_plan.md`) must **not** be regenerated.

## Environment
```bash
# conda
conda env create -f environment.yml && conda activate eeg-mtbi
# or pip (Python 3.14 verified)
python -m venv .venv && source .venv/bin/activate   # PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Verified versions: MNE 1.12.1, MNE-BIDS 0.19, specparam 2.0.0, scikit-learn 1.9.0,
statsmodels 0.14.6, xgboost 3.2.0, numpy 2.4.6, pandas 3.0.3.

## Step-by-step
1. **Metadata + cohort** — `python scripts/00_download_or_load.py --mode metadata`,
   then `01_inspect_bids_metadata.py` and `02_build_cohort.py`
   → `outputs/metadata_summary_tables/`.
2. **Freeze folds** — `python scripts/03_freeze_splits.py` → `outputs/splits/frozen_cv_folds.csv`
   (already provided; do not re-run to "improve" splits).
3. **Download Session-1 EEG** — `python scripts/04_download_s1_eeg.py --dataset ds003522`
   (downloads ~3.5 GB to `data/raw/`, not committed). `--dry-run` produces the manifest only.
4. **QC** — `python scripts/05_eeg_qc.py --dataset ds003522` → `outputs/qc/`.
5. **Preprocess** — `python scripts/06_preprocess_ds003522_s1.py` → `data/processed/` (not committed).
6. **Features** — `07_extract_rest_features_ds003522.py`, `08_extract_oddball_erp_features_ds003522.py`,
   `09_feature_qc_summary.py` → `outputs/features/`.
7. **Analysis table + models** — `10_build_analysis_table.py`, then `11_fit_models.py`
   → `outputs/analysis/`. (This is the only step that reads the outcome; it runs *after* the plan is
   locked.)
8. **Figures** — `12_figures.py`, `14_replication_figures.py`, `15_schematic_figures.py`
   → `outputs/figures/`.
9. **Replication feasibility** — `13_replication_feasibility.py`
   → `outputs/analysis/replication_feature_availability.csv`.

## Integrity anchors (do not change)
| Artifact | MD5 (first 8) |
|---|---|
| `outputs/splits/frozen_cv_folds.csv` | `453fede5` |
| `outputs/analysis/model_coefficients.csv` | `5f3d418e` |
| `outputs/analysis/cv_performance.csv` | `660825f0` |

If any of these change, the discovery analysis has been altered and results are no longer the locked,
preregistered ones.

## Leakage rules (enforced in code)
- Split unit = `subject_uid` (URSI); no subject in more than one fold.
- Scaling, imputation, dimensionality reduction, and hyperparameter tuning fit **within training
  folds only** (scikit-learn Pipelines).
- The outcome never informs preprocessing or feature selection.
- QC exclusions remove a subject from its assigned fold only; folds are never reshuffled.
