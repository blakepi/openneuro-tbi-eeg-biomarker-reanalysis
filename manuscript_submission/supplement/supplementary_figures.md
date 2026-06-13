# Supplementary Figures

Supplementary figures S1-S5 are provided with the submission figure files and were derived from frozen outputs. They are not used to promote exploratory analyses to confirmatory status.

## Figure S1. Primary-model partial effect diagnostics

**File:** `figures/FigureS1_partial_effects.png`

Partial/additional-variable diagnostic plots for the primary EEG predictors in the parsimonious model. These plots are included for transparency only. They should be interpreted alongside the coefficient forest plot and the leave-one-out instability diagnostics; they do not establish a stable predictor.

**Source:** `outputs/figures/fig_partial_effects.png`; model outputs in `outputs/analysis/model_coefficients.csv`.

## Figure S2. Elastic Net coefficient path

**File:** `figures/FigureS2_elasticnet_path.png`

Coefficient paths for the full-panel Elastic Net. The selected penalty shrank all ten predictors to zero, leaving an intercept-only/mean-predictor model.

**Source:** `outputs/figures/fig_elasticnet_path.png`; selected coefficients in `outputs/analysis/elasticnet_coefficients.csv`.

## Figure S3. Out-of-fold calibration

**File:** `figures/FigureS3_calibration.png`

Calibration of out-of-fold predictions against observed Session-3 NSI total. Predictions are compressed toward the cohort mean, consistent with the negative out-of-fold R2 values.

**Source:** `outputs/figures/fig_calibration.png`; predictions in `outputs/analysis/oof_predictions.csv`.

## Figure S4. Resting-versus-ERP contribution diagnostic

**File:** `figures/FigureS4_family_contribution.png`

Descriptive family-level contribution display for the full-panel analysis. This figure is exploratory/transparency material only and should not be read as evidence of a stable family-level biomarker.

**Source:** `outputs/figures/fig_family_contribution.png`; model outputs in `outputs/analysis/model_coefficients.csv`.

## Figure S5. specparam fit-quality distribution

**File:** `figures/FigureS5_specparam_fit_quality.png`

Histogram of exported EC/EO regional/global specparam fit R2 values. This is a QC visualization only; it is not a reconstructed representative model fit because PSD/model objects were not exported by the locked feature pipeline.

**Source:** `outputs/prereg_fidelity_revision_20260612_200455/specparam_qc/specparam_fit_r2_distribution.png`; fit-quality summaries in `outputs/prereg_fidelity_revision_20260612_200455/specparam_qc/`.
