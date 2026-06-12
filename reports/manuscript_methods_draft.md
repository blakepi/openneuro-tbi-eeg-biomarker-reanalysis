# Methods (manuscript draft)
### Early Resting-State and Task-Evoked EEG Biomarkers of Persistent Post-Concussive Symptoms Following mTBI

*Draft Methods for peer review / pre-registration supplement. Values describe data structure,
acquisition, and procedures only; no feature–outcome relationships are reported. Statements are
drawn from the dataset's BIDS sidecars, the original data descriptor (Cavanagh & Quinn,
OpenNeuro ds003522), and the project's Phase 0–3 pipeline.*

---

## 2.1 Dataset

We performed a leakage-safe longitudinal reanalysis of the publicly available OpenNeuro dataset
**ds003522** ("EEG: Three-Stim Auditory Oddball and Rest in Acute and Chronic TBI"; License CC0;
BIDS-formatted). The dataset was collected at the Center for Brain Recovery and Repair, University
of New Mexico Health Sciences Center (data collected 2016–2018) and comprises EEG recorded during
a single continuous session that combined resting-state and three-stimulus auditory-oddball
paradigms. Data were obtained directly from the OpenNeuro Amazon S3 mirror; raw files were
retained unmodified and all derivatives were written to a separate processed tree.

Two related OpenNeuro datasets acquired in the same research program and partially overlapping
participant pool — **ds005114** (DPX cognitive-control task) and **ds003523** (visual working
memory) — are reserved for future independent replication and are **not** analysed against the
outcome in the present manuscript. Because the three datasets share participants, all analyses use
a canonical subject identifier (see §2.2) to guarantee that no individual contributes to more than
one cross-validation fold.

## 2.2 Participants, identity resolution, and outcomes

The dataset includes three groups coded in `participants.tsv`: acute mild TBI (Group 0), controls
(Group 1), and chronic TBI (Group 2). The present analysis concerns the **acute mTBI** group.
For control and acute-mTBI participants, Session 1 was recorded 3–14 days post-injury, Session 2
at ~1.5–3 months, and Session 3 at ~3–5 months; the chronic-TBI group contributed a single
session and no longitudinal clinical follow-up.

**Identity resolution.** Each participant is identified by three keys: a BIDS `participant_id`, a
recording id (`Original_ID`, equal to the clinical-spreadsheet `SubID`), and a scan-generated
unique identifier (`URSI`). Because one `Original_ID` (3013) maps to two distinct `URSI`s, we
adopted **`URSI` as the canonical subject key (`subject_uid`)** for all merging and
cross-validation splitting. Clinical outcomes were drawn from the dataset's aggregated clinical
workbook (`BigAgg_4BIDS.xlsx`), joined to EEG by `Original_ID`/`URSI`; string missing-tokens
("na", "NR", "m") were mapped to missing.

**Outcomes.** The primary outcome was the **Session-3 Neurobehavioral Symptom Inventory (NSI)
total**, computed as the sum of the somatic, cognitive, and emotional subscales (no precomputed
total exists in the source). Secondary outcomes were the Session-3 Rivermead Post-Concussion
Symptoms Questionnaire total and Session-1→Session-3 change scores for both instruments. No binary
"persistent symptoms" outcome was defined, as the source documentation provides no validated
clinical threshold.

**Analytic cohort.** Eligible participants were acute-mTBI cases with a usable Session-1 EEG
recording and a non-missing Session-3 NSI total (**n = 25**). The chronic-TBI group (no
longitudinal outcome) and controls (not part of within-mTBI prediction) were excluded from outcome
modeling. Cohort construction, the participant crosswalk, and a CONSORT-style attrition table were
fixed in advance and are reported in the Supplement.

## 2.3 EEG acquisition

Continuous EEG was recorded at **500 Hz** from **63 scalp electrodes** arranged in the
international 10–10 system, plus a vertical electro-oculogram (VEOG) and an electrocardiogram
(EKG) channel (65 channels total), with an online reference at **CPz** and a power-line frequency
of **60 Hz** (per the BIDS `*_eeg.json` and `channels.tsv` sidecars). Each recording (~15–28 min)
contained, in sequence, an eyes-closed rest block, an eyes-open rest block, a run of the
three-stimulus auditory oddball, and a second cycle of eyes-closed/eyes-open rest and oddball.
Resting and task segments were demarcated by event markers in `events.tsv`
(`Eyes Closed: Every 1000 ms`, `Eyes Open: Every 1000 ms`, and `Standard`/`Target`/`Novel Tone`),
yielding ~120 s of eyes-closed and ~120 s of eyes-open rest and, per recording, 184 standard, 38
target, and 38 novel tones.

## 2.4 EEG preprocessing

All preprocessing was performed in MNE-Python (v1.12) with a single fixed parameter set applied
identically to every participant and chosen **without reference to any outcome**; raw files were
never altered. The pipeline was **boundary-aware**: EEGLAB `boundary` events were converted to
`BAD_boundary` annotations, and the FIR filter was configured to operate within contiguous
segments so that it never spanned a recording discontinuity (in this dataset a single boundary
occurred at recording onset in every file, with no internal discontinuities).

For each recording we (i) typed the non-scalp channels (VEOG as EOG, EKG as ECG) so they were
excluded from referencing, montage, and feature computation; (ii) applied a 60-Hz notch filter;
(iii) band-pass filtered the data 0.5–45 Hz (FIR, Hamming window); (iv) reinstated the online
reference channel CPz, assigned a standard 10–20 montage, and re-referenced to the average of the
64 EEG channels; and (v) performed within-participant bad-channel detection (robust z-score of
log-variance > 4, or flat channels), interpolating flagged channels by spherical splines (the
reinstated reference channel was exempt from this test). Bad-channel detection used only each
participant's own Session-1 data and therefore introduced no cross-subject or outcome leakage.
A high-pass cutoff of 0.5 Hz was selected to remove the slow drift and boundary-related offsets
observed at quality control; for the ERP analysis branch an additional 40-Hz low-pass was applied
prior to epoching. Cleaned recordings were written as FIF files with per-participant processing
logs.

## 2.5 Resting-state feature extraction

Resting analyses used the **eyes-closed** condition as primary (eyes-open as a sensitivity
condition). Eyes-closed and eyes-open blocks were defined from their marker trains (a gap > 3 s
delimited separate blocks; block span = first to last marker + 1 s) and screened for
discontinuities. Within each block the signal was divided into non-overlapping 2-s segments;
segments exceeding 150 µV peak-to-peak on any EEG channel were rejected. Power spectral density
(PSD) was estimated by Welch's method (2-s Hamming windows, 50 % overlap, 1–45 Hz) on the retained
segments and averaged across channels within four scalp regions (frontal, central, parietal,
occipital) and globally.

From the regional/global spectra we computed absolute and relative band power for delta (1–4 Hz),
theta (4–8 Hz), alpha (8–12 Hz), and beta (13–30 Hz); the theta/alpha ratio; Shannon spectral
entropy of the normalized 1–45-Hz spectrum; and the **aperiodic (1/f) exponent and offset** using
spectral parameterization (specparam v2.0; fixed aperiodic mode; 1–40-Hz fit). The **posterior
individual alpha frequency (IAF)** was defined as the spectral peak within 7–13 Hz of the mean
parietal–occipital eyes-closed spectrum (undefined when no clear peak was present). Usable signal
duration per condition was recorded for quality control. The locked confirmatory resting panel
comprised posterior IAF, global aperiodic exponent, frontal theta/alpha ratio, and occipital
relative alpha power; spectral entropy was retained as an exploratory feature.

## 2.6 ERP feature extraction

ERP analyses used the auditory-oddball events labelled in `events.tsv`. Epochs spanning −200 to
+800 ms relative to tone onset were extracted from the 40-Hz-low-passed data, baseline-corrected
to the −200–0 ms interval, and screened with `reject_by_annotation` (so no epoch crossed a
boundary) and a 150-µV peak-to-peak rejection threshold on EEG channels. Condition averages were
formed per participant. We quantified, from pre-registered regions and time windows: the **P3b**
(target tones, parietal Pz/CPz/POz, 300–600 ms), the **P3a** (novel tones, frontocentral
Fz/FCz/Cz, 250–400 ms), and the **N2** (200–350 ms, frontocentral); for each component we
extracted mean-window amplitude, peak amplitude, and peak latency, and additionally computed a
target-minus-standard difference wave at parietal sites. Retained and rejected epoch counts were
logged per condition. The locked confirmatory ERP panel comprised P3b amplitude, P3b latency, P3a
amplitude, and P3a latency (mean-window amplitude primary; peak as a sensitivity measure).

## 2.7 Quality control

Quality control was performed at three stages and never used outcome information. (1) **Read QC**
(Phase 2): all 25 recordings were readable with a uniform 500-Hz sampling rate and 65-channel
montage; no flat, NaN, or zero-filled channels and no dataset-marked bad channels were present.
(2) **Preprocessing QC**: 0–3 channels per participant were interpolated (predominantly frontal
ocular sites). (3) **Feature QC** (Phase 3): a resting condition was deemed reliable with ≥ 40 s of
clean signal (eyes-closed: 25/25; eyes-open: 22/25), and an ERP component reliable with ≥ 15
retained rare-tone epochs. One participant (`sub-040`) lacked curated tone labels — its tones were
stored only as raw stimulus codes — and was excluded from ERP analyses without attempting to infer
the non-standard code mapping; three further participants fell below the ERP epoch-count floor.
Effective sample sizes were therefore 25 (resting), 21 (ERP), and 20 (combined panel). All
exclusions were applied within each participant's pre-assigned cross-validation fold; folds were
never regenerated.

## 2.8 Statistical analysis

Analyses followed a pre-registered Statistical Analysis Plan finalized **before** any
feature–outcome relationship was examined; feature files were verified to contain no outcome
information, and subject-level cross-validation folds (5-fold, stratified on Session-3 NSI
tertiles, seed 42, split by `subject_uid`) were frozen prior to EEG processing. The primary
question was whether the compact Session-1 EEG panel is associated with Session-3 NSI total beyond
age and sex.

Because the full specification (8 EEG predictors + age + sex) exceeds the events-per-variable
supportable at n ≈ 20–25, the SAP pre-specified a simplification: a **parsimonious combined linear
model** carrying the single strongest a priori biomarker from each family (aperiodic exponent,
posterior IAF, P3b amplitude) plus age and sex served as the primary confirmatory linear model,
and **elastic-net penalized regression** over the full panel served as the primary penalized
model; the full ordinary-least-squares model was reported for transparency but not used for
confirmatory inference. Domain-specific resting (n = 25) and ERP (n = 21) models were also
pre-specified. Predictors and continuous covariates were standardized within training folds only;
imputation (sensitivity analyses), penalty selection, and any normalization were likewise fit
within training folds, never using held-out or outcome data. For each model we report standardized
β coefficients, 95 % confidence intervals, p-values (Benjamini–Hochberg FDR-controlled within the
predictor family), adjusted R², partial-R²/Cohen's f² effect sizes, and variance inflation
factors; out-of-fold R² and MAE quantify predictive performance, benchmarked against an
age-plus-sex baseline. Ridge and LASSO regressions were supportive analyses; random forest and
gradient boosting were exploratory. All analyses used Python 3.14 with MNE 1.12, specparam 2.0,
scikit-learn 1.9, statsmodels, numpy, and pandas, with fixed random seeds; code and frozen folds
are released with the manuscript.
