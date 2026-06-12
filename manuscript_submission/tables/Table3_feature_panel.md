## Table 3. Locked EEG feature panel

| # | Feature | Modality | State / task | Region | Definition (preregistered) | Primary | Secondary | Exploratory |
|---|---|---|---|---|---|:--:|:--:|:--:|
| 1 | Global aperiodic exponent | Resting | Eyes-closed | Global | specparam (fixed mode) 1/f exponent, 1–40 Hz fit | ✓ | ✓ | |
| 2 | Posterior IAF | Resting | Eyes-closed | Parietal–occipital | 7–13 Hz spectral peak frequency | ✓ | ✓ | |
| 3 | Frontal theta/alpha ratio | Resting | Eyes-closed | Frontal | θ(4–8 Hz)/α(8–12 Hz) absolute power | | ✓ | |
| 4 | Occipital relative alpha | Resting | Eyes-closed | Occipital | α power / total (1–45 Hz) power | | ✓ | |
| 5 | P3b amplitude | ERP | Oddball — Target | Parietal (Pz/CPz/POz) | mean amplitude 300–600 ms (peak = sensitivity) | ✓ | ✓ | |
| 6 | P3b latency | ERP | Oddball — Target | Parietal | peak latency 300–600 ms | | ✓ | |
| 7 | P3a amplitude | ERP | Oddball — Novel | Frontocentral (Fz/FCz/Cz) | mean amplitude 250–400 ms (peak = sensitivity) | | ✓ | |
| 8 | P3a latency | ERP | Oddball — Novel | Frontocentral | peak latency 250–400 ms | | ✓ | |
| 9 | Spectral entropy | Resting | Eyes-closed | Global | Shannon entropy of normalized PSD (1–45 Hz) | | | ✓ |

*Primary model = features 1, 2, 5 + age + sex (parsimonious, one biomarker per domain). Secondary
(Elastic Net) and transparency (full OLS) models = features 1–8 + age + sex. Feature 9 (spectral
entropy) is exploratory only. Eyes-closed is the primary resting condition; eyes-open versions are
sensitivity analyses. Source: `final_locked_analysis_plan.md`, `scripts/_eeg_common.py`,
`outputs/features/`.*
