## Table 1. Dataset and cohort overview

| Dataset | Role | Paradigm | Embedded rest | Groups | Sessions | EEG (n with `_eeg.set`, S1) | Outcome (NSI/Rivermead) |
|---|---|---|:--:|---|:--:|---:|:--:|
| **ds003522** | **Discovery** | Three-stimulus auditory oddball + rest | Yes (EC/EO) | acute mTBI / control / chronic TBI | 3 | 96 | Yes |
| ds005114 | Designated replication | DPX cognitive control | No | acute mTBI / control | 3 | 91 | Yes |
| ds003523 | Designated replication | Visual working memory | No | acute TBI / control | 3 | 91 | Yes (via shared workbook) |
| ds003490 | Paradigm reference | Three-stimulus auditory oddball + rest | Yes (EC/EO) | **Parkinson's disease** (25 PD / 25 control) | 2 | not analysed (paradigm reference) | **No (no post-concussive outcome)** |

*All datasets: 500-Hz BrainVision EEG, EEGLAB `.set/.fdt`, online reference CPz, 60-Hz line. The
discovery and replication datasets derive from one longitudinal UNM cohort (Cavanagh et al.,
2016–2018); the same individuals recur across the three TBI datasets and were deduplicated on a
stable unique identifier (URSI). ds003490 is a separate Parkinson's-disease cohort (50 participants,
25 PD / 25 control, 2 sessions) used only to assess feature extractability, not analysed for outcome.
EC = eyes-closed; EO = eyes-open. Source: `outputs/metadata_summary_tables/`,
`outputs/analysis/replication_feature_availability.csv`, OpenNeuro dataset records [15,24,25,26].*
