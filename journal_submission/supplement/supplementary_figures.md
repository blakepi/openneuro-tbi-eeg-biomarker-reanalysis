# Supplementary Figures

Supplementary figures are copied into `manuscript_submission/figures/` with the main figure files. They are derived from frozen outputs and are not used to promote exploratory analyses to confirmatory status.

## Figure S1. Primary-model partial effect diagnostics

**File:** `manuscript_submission/figures/FigureS1_partial_effects.png`

Partial/additional-variable diagnostic plots for the primary EEG predictors in the parsimonious model. These plots are included for transparency only. They should be interpreted alongside the coefficient forest plot and the leave-one-out instability diagnostics; they do not establish a stable predictor.

**Source:** `outputs/figures/fig_partial_effects.png`; model outputs in `outputs/analysis/model_coefficients.csv`.

## Figure S2. Elastic Net coefficient path

**File:** `manuscript_submission/figures/FigureS2_elasticnet_path.png`

Coefficient paths for the full-panel Elastic Net. The selected penalty shrank all ten predictors to zero, leaving an intercept-only/mean-predictor model.

**Source:** `outputs/figures/fig_elasticnet_path.png`; selected coefficients in `outputs/analysis/elasticnet_coefficients.csv`.

## Figure S3. Out-of-fold calibration

**File:** `manuscript_submission/figures/FigureS3_calibration.png`

Calibration of out-of-fold predictions against observed Session-3 NSI total. Predictions are compressed toward the cohort mean, consistent with the negative out-of-fold R2 values.

**Source:** `outputs/figures/fig_calibration.png`; predictions in `outputs/analysis/oof_predictions.csv`.

## Figure S4. Resting-versus-ERP contribution diagnostic

**File:** `manuscript_submission/figures/FigureS4_family_contribution.png`

Descriptive family-level contribution display for the full-panel analysis. This figure is exploratory/transparency material only and should not be read as evidence of a stable family-level biomarker.

**Source:** `outputs/figures/fig_family_contribution.png`; model outputs in `outputs/analysis/model_coefficients.csv`.

## Notes For Production

- Confirm journal requirements for supplementary figure resolution, file type, and separate legend files.
- These figures are diagnostic supports. The main inferential displays remain the primary coefficient forest plot, mean-predictor behavior plot, and replication feasibility matrix.
- No supplementary figure changes the locked statistical hierarchy.

