# Reporting Checklist

This checklist is tailored to a secondary analysis of public EEG data using a prespecified statistical hierarchy. It is not a substitute for a journal-specific checklist.

## Study Design And Reporting

| Item | Status | Location / note |
|---|---|---|
| Study design identified as retrospective secondary analysis | Complete | Main manuscript, Methods 2.1 |
| Public dataset source identified | Complete | Main manuscript, Methods 2.2; Data availability |
| No causal inference claimed | Complete | Methods 2.1; Discussion |
| Analysis plan locked before outcome modeling | Complete | Methods 2.1; Supplement final locked plan; version-controlled in the code repository with a commit-history timestamp |
| Primary outcome prespecified | Complete | Methods 2.4; Table 4 |
| Statistical hierarchy preserved | Complete | Methods 2.8; Table 4 |
| Exploratory models clearly marked | Complete | Methods 2.8; Results 3.5; Table 4 |
| Null/inconclusive results reported without positive biomarker framing | Complete | Abstract; Results; Discussion |

## Data, Cohort, And Identity Handling

| Item | Status | Location / note |
|---|---|---|
| Dataset identifiers reported | Complete | All four dataset DOIs/versions in Methods 2.2, Data availability, Table 5, and references [15,24,25,26] |
| Cohort construction described | Complete | Methods 2.3; Results 3.1; Table 2 |
| Chronic-TBI arm exclusion justified | Complete | Methods 2.3; Table 2 |
| Clinical-only subjects documented | Complete | Supplementary Methods S.2 |
| Stable subject key described | Complete | Methods 2.3; Supplementary Methods S.2 |
| Duplicate Original_ID 3013 handling described | Complete | Supplementary Methods S.2 |
| Missingness and attrition documented | Complete | Table 2; Supplementary Tables S3 |

## EEG Methods

| Item | Status | Location / note |
|---|---|---|
| Acquisition format and sampling rate reported | Complete | Methods 2.5 |
| Channel structure and online reference reported | Complete | Methods 2.5 |
| Recording sequence described | Complete | Methods 2.5; Figure 2 |
| Boundary handling described | Complete | Methods 2.6; Supplementary Methods S.4-S.5 |
| Preprocessing parameters reported | Complete | Methods 2.6; Supplementary Methods S.4 |
| Feature definitions reported | Complete | Methods 2.7; Table 3; Supplementary Methods S.6-S.7 |
| ERP reliability thresholds reported | Complete | Methods 2.7; Supplementary Methods S.7 |
| QC results reported | Complete | Results 3.1; Supplementary Tables S2 |

## Statistical And Machine-Learning Reporting

| Item | Status | Location / note |
|---|---|---|
| Primary model formula reported | Complete | Methods 2.8; Table 4 |
| Secondary Elastic Net model reported | Complete | Methods 2.8; Results 3.3; Table 4 |
| Full OLS labelled descriptive/overfit-prone | Complete | Results 3.4; Table 4; Supplementary Table S4 |
| Scaling/tuning confined to training folds | Complete | Methods 2.8; Supplementary Methods S.8 |
| Subject-level folds used | Complete | Methods 2.8; Supplementary Methods S.8 |
| Effect sizes and confidence intervals reported | Complete | Results 3.2; Table 4 |
| p-values not overemphasized | Complete | Results and Discussion language |
| Leave-one-out diagnostics reported | Complete | Results 3.2; Table 4 note |
| FDR handling reported | Complete | Methods 2.8; Results 3.2; Table 4 |
| Exploratory models not promoted | Complete | Results 3.5; Discussion |

## Replication Feasibility

| Item | Status | Location / note |
|---|---|---|
| ds005114 event inventory reported | Complete | Results 3.6; Table 5; Supplementary Table S6 |
| ds003523 feature availability reported | Complete | Results 3.6; Table 5 |
| ds003490 paradigm/outcome mismatch reported | Complete | Results 3.6; Table 5 |
| Replication-infeasible wording distinguished from replication-failure wording | Complete | Abstract; Results; Discussion |
| Cross-paradigm feature substitution rejected | Complete | Methods 2.9; Discussion |

## Administrative Items

| Item | Status | Location / note |
|---|---|---|
| Data availability statement | Complete | Main manuscript section 7 (all four dataset DOIs) |
| Code availability statement | Complete | Main manuscript section 8 (GitHub URL, MIT License) |
| Ethics statement | Complete | Main manuscript section 9 (IRB-exempt; public deidentified data) |
| Author contributions | Complete | Main manuscript section 10 (CRediT, single author) |
| Funding | Complete | Main manuscript section 11 (no funding received) |
| Conflicts of interest | Complete | Main manuscript section 12 (none declared) |
| Acknowledgments | Complete | Main manuscript section 13 |
| AI assistance disclosure | Complete | Main manuscript section 13 (acknowledgments) |
| References completed | Complete | 26 Vancouver-numbered references; `references.bib` provided; no placeholders |
