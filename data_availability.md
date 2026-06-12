# Data Availability

This study used publicly available OpenNeuro datasets. Raw EEG and metadata are available from
OpenNeuro at:

| Dataset | Role | DOI |
|---|---|---|
| ds003522 | Discovery (acute mTBI; auditory oddball + rest) | [10.18112/openneuro.ds003522.v1.1.0](https://doi.org/10.18112/openneuro.ds003522.v1.1.0) |
| ds005114 | Designated replication (DPX) | [10.18112/openneuro.ds005114.v1.0.0](https://doi.org/10.18112/openneuro.ds005114.v1.0.0) |
| ds003523 | Designated replication (visual working memory) | [10.18112/openneuro.ds003523.v1.1.0](https://doi.org/10.18112/openneuro.ds003523.v1.1.0) |
| ds003490 | Paradigm reference (Parkinson's oddball + rest) | [10.18112/openneuro.ds003490.v1.1.0](https://doi.org/10.18112/openneuro.ds003490.v1.1.0) |

**No new human data were collected.** Raw EEG data and fetched dataset metadata are **not
redistributed** in this repository; they remain under their respective OpenNeuro terms (CC0).
Re-running the pipeline downloads the required Session-1 EEG directly from OpenNeuro (see
`reproducibility.md`).

**Derived materials** that *are* included in this repository: the participant crosswalk and
metadata summary tables (`outputs/metadata_summary_tables/`), the frozen cross-validation folds
(`outputs/splits/`), the extracted feature matrices and QC summaries (`outputs/features/`,
`outputs/qc/`), the model outputs (`outputs/analysis/`), and the figures (`outputs/figures/`). These
are small, derived from the public CC0 data, and identified only by the public OpenNeuro participant
labels and the scan identifier (URSI) already present in the public `participants.tsv`.

The original data were collected by the source investigators (J.F. Cavanagh, D. Quinn, and
colleagues) under their institutional approvals; this secondary analysis used only the deidentified
public releases.
