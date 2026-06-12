## Table 4. Model results

### 4A. Primary confirmatory model — coefficients
`S3_NSI_Total ~ Global_Aperiodic_Exponent + Posterior_IAF + P3b_Amplitude + Age + Sex` (OLS, n = 21;
R² = 0.11, adjusted R² = −0.19, omnibus F p = 0.86; raw NSI scale)

| Predictor | β (raw) | Std. β | 95% CI (std.) | p | p (FDR) |
|---|---:|---:|---:|---:|---:|
| Global aperiodic exponent | −1.42 | −0.02 | −0.83 to 0.79 | 0.96 | 0.96 |
| Posterior IAF | −2.58 | −0.15 | −0.83 to 0.52 | 0.64 | 0.96 |
| P3b amplitude | 2.07 | 0.24 | −0.40 to 0.88 | 0.43 | 0.96 |
| Age | −0.06 | −0.04 | −0.83 to 0.75 | 0.92 | 0.96 |
| Sex | −4.85 | −0.13 | −0.71 to 0.44 | 0.63 | 0.96 |

*No 95% CI excludes zero. Heteroscedasticity-consistent (HC3) p-values: 0.64–0.97. Leave-one-subject-
out: no predictor sign-stable. Source: `outputs/analysis/model_coefficients.csv`,
`outputs/analysis/loo_coefficient_stability.csv`, `outputs/analysis/diagnostics.json`.*

### 4B. Out-of-fold performance (frozen folds)

| Model | Tier | n | Out-of-fold R² (95% CI) | MAE | adj. R² (in-sample) |
|---|---|---:|---:|---:|---:|
| Baseline (age + sex) | reference | 21 | −0.40 (−1.36, −0.13) | 15.7 | — |
| **Primary parsimonious** | **primary confirmatory** | 21 | **−1.38 (−2.85, −0.89)** | 19.2 | −0.19 |
| **Elastic Net (full panel)** | **secondary confirmatory** | 21 | **−0.06 (−0.50, −0.02)** | 13.3 | — (0/10 coef ≠ 0) |
| Full 10-term OLS | transparency (descriptive) | 21 | −3.58 (−9.82, −1.81) | 27.5 | −0.22 |
| Resting-only OLS | supportive | 25 | −0.59 (−2.07, −0.08) | 16.7 | 0.08 |
| ERP-only OLS | supportive | 21 | −1.13 (−2.83, −0.38) | 17.1 | −0.12 |
| Ridge | exploratory | 21 | −0.14 (−0.61, −0.03) | 13.6 | — |
| LASSO | exploratory | 21 | −0.06 (−0.50, −0.02) | 13.3 | — |
| Random Forest | exploratory | 21 | −0.29 (−1.14, −0.06) | 14.9 | — |
| XGBoost | exploratory | 21 | −0.36 (−1.36, 0.09) | 14.7 | — |

*All EEG models have negative out-of-fold R²; none exceeds the age+sex baseline. The Elastic Net
selected α = 43.2, mixing parameter = 0.10, and shrank all 10 coefficients to zero (intercept =
14.6, the cohort mean). Source: `outputs/analysis/cv_performance.csv`,
`outputs/analysis/elasticnet_coefficients.csv`, `outputs/analysis/model_fit_summary.csv`.*
