# Supplementary Methods

## S.1 Software environment
Python 3.14.5; MNE-Python 1.12.1; specparam 2.0.0; scikit-learn 1.9.0; statsmodels 0.14.6; xgboost
3.2.0; numpy 2.4.6; pandas 3.0.3; matplotlib 3.10.9. All random seeds fixed at 42. Raw EEG was
fetched from the public OpenNeuro S3 mirror; raw files were retained unmodified and all derivatives
written to a separate processed tree.

## S.2 Identity resolution and the Original_ID 3013 collision
Each participant carries three keys: a BIDS `participant_id` (not stable across datasets), a recording
id `Original_ID` (= clinical-workbook `SubID`), and a scan-generated unique id `URSI`. We adopted
**`URSI` as the canonical `subject_uid`** because `Original_ID` 3013 maps to **two distinct URSIs**
(`M87138342` and `M87138432`, an apparent digit transposition), both labelled control. Keying on URSI
preserves both as separate records without merging potentially different people; only `M87138432` had
a clinical row, and the other was retained as EEG-only. Because both are controls, neither enters the
within-mTBI primary analysis. The clinical workbook stores `URSI` as the last five digits of the BIDS
URSI; the crosswalk records both forms (`outputs/metadata_summary_tables/crosswalk_subject_ids.csv`).
Three clinical-only subjects (recording ids 3008, 3022, 3120) had no EEG in any dataset and were
documented, not silently dropped.

## S.3 Outcome construction
Primary outcome = Session-3 NSI total = somatic + cognitive + emotional subscales (no precomputed
total exists). Clinical string missing-tokens ("na", "NR", "m") were mapped to missing. The
transformation rule was prespecified on the **outcome distribution only**: |skewness| > 1.0 → analyse
`log1p(NSI)`; observed skewness 0.85 → raw NSI retained. No binary "persistent symptoms" outcome was
defined (no established threshold in the source documentation).

## S.4 Full preprocessing parameters (frozen; identical for all participants)
| Step | Setting |
|---|---|
| Input | EEGLAB `.set/.fdt`, 500 Hz, 65 channels (63 scalp + VEOG + EKG), online ref CPz |
| Channel typing | VEOG → EOG, EKG → ECG (excluded from referencing, montage, features) |
| Boundary handling | `boundary` → `BAD_boundary`; FIR filtering constrained within contiguous segments (segment-wise if any internal boundary; none present) |
| Notch | 60 Hz |
| Band-pass | 0.5–45 Hz, FIR (firwin) |
| Reference reconstruction | reinstate CPz (zero-filled) → standard 10–20 montage → average reference (64 EEG) |
| Bad channels | robust z of log-variance > 4, or flat; spherical-spline interpolation; reinstated reference exempt from the test |
| ERP branch | additional 40-Hz low-pass before epoching |

Bad-channel counts: 0 for 19/25 participants, 1–3 (predominantly frontal-ocular sites) for the rest;
all interpolated. Per-participant logs: `data/processed/ds003522_s1/logs/`.

## S.5 Event-label handling and resting segmentation
Resting blocks were identified from `Eyes Closed/Open: Every 1000 ms` marker trains (a > 3 s gap began
a new block; block span = first to last marker + 1 s); two blocks of each condition per recording
(~120 s/condition). Oddball epochs used the curated `Standard/Target/Novel Tone` labels. One
participant (`sub-040`) lacked these curated labels — its tones were stored only as raw stimulus codes
(`S 8/9/10`) — and was excluded from ERP analyses; the non-standard code mapping was **not** inferred.

## S.6 Resting feature definitions
Welch PSD (2-s Hamming windows, 50% overlap, 1–45 Hz) on artifact-screened 2-s segments (rejection at
150 µV peak-to-peak), averaged within frontal/central/parietal/occipital/global regions. Bands: delta
1–4, theta 4–8, alpha 8–12, beta 13–30 Hz. Relative power normalized to 1–45 Hz total. Posterior IAF =
7–13 Hz peak of the mean parietal–occipital eyes-closed spectrum (undefined when no clear peak).
Aperiodic exponent/offset via specparam (fixed mode, 1–40 Hz fit). Spectral entropy = Shannon entropy
of the normalized 1–45 Hz PSD (exploratory).

## S.7 ERP feature definitions and reliability thresholds
Epochs −200 to +800 ms, baseline −200–0 ms, boundary-aware rejection, 150 µV peak-to-peak rejection on
EEG. P3b: target tones, parietal Pz/CPz/POz, 300–600 ms. P3a: novel tones, frontocentral Fz/FCz/Cz,
250–400 ms. N2 (200–350 ms) and a target-minus-standard difference wave were computed for context.
Each component required **≥ 15 retained Target and Novel epochs**; the resting reliability floor was
**≥ 40 s** of clean signal per condition (eyes-closed met for all 25; eyes-open for 22).

## S.8 Leakage-prevention implementation
Subject-level 5-fold cross-validation folds were stratified on Session-3 NSI tertiles (seed 42) and
**frozen before EEG processing** (`outputs/splits/frozen_cv_folds.csv`, MD5 `453fede5…`). All
standardization, imputation (sensitivity), and hyperparameter tuning were fit within training folds
via scikit-learn Pipelines; test folds saw no fitted parameter. Quality-control exclusions removed a
subject from its assigned fold only; folds were never regenerated. The outcome never informed
preprocessing or feature selection.

## S.9 Replication feasibility procedure
Session-1 `events.tsv` were scanned for eyes-closed/eyes-open rest markers and auditory-oddball
Target/Novel tones. ds005114 was scanned across all 91 recordings; ds003523 and ds003490 by sample. A
feature was deemed extractable only if its source paradigm was present
(`scripts/13_replication_feasibility.py`). No cross-paradigm feature substitution was performed.
