# Phase 3 Report — Boundary-aware preprocessing & Session-1 feature extraction
### Primary cohort ds003522 (acute mild TBI, n = 25)

**Date:** 2026-06-11
**Scope guard honored:** no models trained, **no feature–outcome association inspected**, no
preprocessing tuned on any outcome. Only Session-1 EEG was used. Raw files were never modified.
**Scripts:** `06_preprocess_ds003522_s1.py`, `07_extract_rest_features_ds003522.py`,
`08_extract_oddball_erp_features_ds003522.py`, `09_feature_qc_summary.py`, shared constants in
`_eeg_common.py`.
**Artifacts:** `data/processed/ds003522_s1/*_proc_raw.fif` (+ per-subject JSON logs),
`outputs/features/ds003522_s1_rest_features.csv`, `..._erp_features.csv`,
`..._feature_qc_summary.csv`, `..._subject_usability.csv`.

---

## 1. Exact preprocessing parameters (frozen, identical for all 25 subjects)

| Step | Setting | Notes |
|---|---|---|
| Input | EEGLAB `.set`/`.fdt`, 500 Hz, 65 channels | raw untouched; loaded with `mne.io.read_raw_eeglab` |
| Channel typing | `VEOG → eog`, `EKG → ecg` | excluded from montage, referencing, and EEG features |
| Line-noise notch | **60 Hz** | largely redundant under the 45-Hz low-pass; applied for safety |
| Band-pass | **0.5 – 45 Hz** (FIR, firwin) | high-pass removes the DC drift behind Phase-2 "EXTREME_AMP"; 45 Hz serves spectral analysis |
| ERP extra low-pass | **40 Hz** | applied only in the ERP branch (script 08), at epoch time |
| Online reference | **CPz** (from `*_eeg.json`) | re-added as a flat channel before re-referencing |
| Re-reference | **average** (64 EEG incl. reconstructed CPz) | CPz kept (legitimately 0 under its own reference) so the average is unbiased |
| Montage | **standard_1020** (by name) | all 10–10 labels matched |
| Bad channels | robust z of log-variance > **4** (within-subject), or flat | interpolated (spherical splines); the online reference is exempt from this test |
| Output | `*_proc_raw.fif` + JSON log per subject | one cleaned object per subject |

**High-pass / low-pass rationale.** A 0.5-Hz high-pass (rather than 0.1 Hz) was chosen because it
robustly removes the slow drift/boundary offsets seen in Phase 2 and stabilizes baselines; the
modest attenuation of the slow P3b is acceptable and is applied **uniformly** to every subject
(no outcome involved). Spectral analysis uses the broadband 0.5–45 Hz; the ERP branch adds a
40-Hz low-pass to suppress residual EMG/line activity in the averaged waveforms.

**Bad-channel outcome.** 0 bad channels for 19/25 subjects; 1–3 for the rest, almost all frontal
ocular sites (Fp1/Fp2/AF7/AF8) plus isolated CP/TP — consistent with eye-movement pickup, all
interpolated. (Per-subject lists in `data/processed/ds003522_s1/logs/*.json`.)

---

## 2. Boundary handling

Every recording carries exactly **one EEGLAB `boundary` event, at t = 0 s** (recording start) —
there are **no internal discontinuities** in any of the 25 subjects. The pipeline is nonetheless
genuinely boundary-aware:

- `boundary` events are converted to **`BAD_boundary` annotations**.
- The filter checks for any boundary with onset > 1 s; if found it **filters each contiguous
  segment independently** and re-concatenates (so the FIR filter never runs across a splice). In
  this dataset no subject triggered segment-wise filtering (logged as "single segment").
- Rest segmentation and ERP epoching both pass `reject_by_annotation=True`, so any segment/epoch
  overlapping a `BAD_boundary` is dropped. Because the only boundary is at t = 0, no rest block or
  tone epoch was lost to it here — but the safeguard is in force for the replication datasets.

Because no cropping occurred, the processed-FIF timeline is identical to the raw timeline, so the
`events.tsv` onsets map directly onto the cleaned data.

---

## 3. Resting-state segmentation results

Rest is embedded, not a separate file. Each recording contains **two Eyes-Closed and two
Eyes-Open blocks (~60 s each → ~120 s/condition)**, identified from the `Eyes Closed/Open: Every
1000 ms` marker trains (gap > 3 s starts a new block; block span = first→last marker + 1 s).
Within blocks the signal was cut into non-overlapping **2-s segments**; segments exceeding **150
µV peak-to-peak** on any EEG channel were rejected. PSD = Welch, 2-s windows, 50 % overlap.

**Usable rest after artifact rejection (n = 25):**

| Condition | Median usable | Range | Subjects ≥ 40 s |
|---|---:|---:|---:|
| Eyes Closed | **110 s** (55 of 60 segs) | 54–120 s | **25 / 25** |
| Eyes Open | 86 s | 24–118 s | **22 / 25** |

Eyes-Open loses more data (blinks/movement), as expected. Three subjects fall below the 40-s
reliability floor for **EO only** (sub-020 = 26 s, sub-058 = 24 s, sub-068 = 32 s); their
Eyes-Closed data are ample. Per-subject usable seconds are in
`ds003522_s1_rest_features.csv` (`rest_*_usable_s`) and `ds003522_s1_subject_usability.csv`.

---

## 4. Oddball ERP epoch counts

Epochs: **−200 to +800 ms**, baseline (−200, 0), boundary-aware, reject **150 µV** peak-to-peak
on EEG. Events come from the curated `trial_type` names (Standard/Target/Novel Tone).

- **24 / 25 subjects yield ERPs.** **sub-040 is excluded**: its tones are stored only as raw
  S-codes (`S 8/9/10`) without the named `trial_type` labels. Rather than guess the non-standard
  mapping (risking mislabeled conditions), sub-040 is flagged `NO_NAMED_TONE_EVENTS` — not
  silently dropped, and recoverable later via a documented S-code sensitivity analysis.

**Retained epochs (24 ERP subjects):**

| Condition | Marked | Median retained | Range retained |
|---|---:|---:|---:|
| Standard | 184 | 160 | 21–184 |
| Target | 38 | 31 | 11–38 |
| Novel | 38 | 32.5 | 9–37 |

Three subjects fall below the **15-trial** reliability floor for the rare tones (sub-020 = 12,
sub-058 = 11, sub-036 = 13 targets) → flagged `P3b_LOW_TRIALS`/`P3a_LOW_TRIALS`. Counts per
subject/condition are in `ds003522_s1_erp_features.csv` (`erp_n_*_kept` / `erp_n_*_rejected`).

**ERP sanity (descriptive, not outcome-related).** Target P3b at parietal sites: peak mean
**6.6 µV** (range 2.2–11.5), latency mean **464 ms** — a textbook parietal P3b. Target-minus-
Standard difference at parietal is positive in every subject (mean 3.7 µV). Novel P3a at
frontocentral sites: mean 2.8 µV. These confirm the paradigm and pipeline are working.

---

## 5. Retained usable N

| Modality | Usability criterion | Usable N |
|---|---|---:|
| **Eyes-Closed rest** | ≥ 40 s clean | **25 / 25** |
| Eyes-Open rest | ≥ 40 s clean | 22 / 25 |
| Rest (EC **and** EO) | both ≥ 40 s | 22 / 25 |
| **Oddball ERP** | named tones, ≥ 15 Target & Novel | **21 / 25** |
| Rest **and** ERP both usable | — | **20 / 25** |

No subject is lost to unreadable data or preprocessing failure; all attrition is from
artifact/trial-count thresholds. This is consistent with the Phase-1/2 expectation that **sample
size, not data quality, is the binding constraint**.

---

## 6. Feature dictionary

165 columns total across the two feature files (counts/QC fields included). All values are
physiologically plausible; feature missingness is ≤ 4 % for ERP components (sub-040) and 12 % for
the single EO-IAF feature (3 subjects without a clear eyes-open posterior alpha peak). Everything
else is 0 % missing.

### Resting features — `ds003522_s1_rest_features.csv`
Per **condition** {EC, EO} × **region** {frontal, central, parietal, occipital, global}:

| Feature stem | Definition | Example range (EC) |
|---|---|---|
| `{band}_abs` | absolute Welch band power (µV²), bands δ1–4, θ4–8, α8–12, β13–30 Hz | occipital α 1–220 |
| `{band}_rel` | band power / total (1–45 Hz) power | occipital α rel 0.10–0.84 |
| `theta_alpha_ratio` | θ / α absolute power | global 0.10–1.78 |
| `spec_entropy` | Shannon entropy of normalized PSD (1–45 Hz), 0–1 | global 0.63–0.88 |
| `aper_exponent` | specparam aperiodic exponent (1/f slope, 1–40 Hz fit) | global 0.78–1.57 |
| `aper_offset` | specparam aperiodic offset | global 0.40–1.55 |
| `aper_r2` | specparam model fit R² | global 0.92–1.00 (mean 0.99) |

Per **condition**: `iaf_posterior_hz` — individual alpha peak (7–13 Hz) from parietal+occipital
mean PSD (mean 10.0 Hz, range 8.5–12.5; NaN when no clear peak).
QC fields per condition: `usable_s`, `n_seg_kept`, `n_seg_total`, `n_blocks_used`.

### ERP features — `ds003522_s1_erp_features.csv`
Each component reports **peak amplitude (µV)**, **peak latency (ms)**, and **mean window
amplitude (µV)**:

| Feature stem | Component | Condition | ROI | Window |
|---|---|---|---|---|
| `erp_P3a_novel_fc_*` | P3a (positive) | Novel | Fz/FCz/Cz | 250–400 ms |
| `erp_P3b_target_par_*` | P3b (positive) | Target | Pz/CPz/POz | 300–600 ms |
| `erp_P3b_tMinusS_par_*` | P3b, Target−Standard diff | difference | Pz/CPz/POz | 300–600 ms |
| `erp_N2_target_fc_*` / `erp_N2_novel_fc_*` | N2 (negative) | Target / Novel | Fz/FCz/Cz | 200–350 ms |
| `erp_n_{cond}_kept` / `_rejected` / `_marked` | epoch counts | each | — | — |

---

## 7. Recommended locked feature set for Phase 4

To balance signal coverage against the small N (and the curse of dimensionality), Phase 4 should
**lock a compact, pre-registered feature set** and reduce within training folds only. Recommended
core (all already extracted, all from Session-1, no outcome seen):

**Resting (prefer Eyes-Closed; n = 25):**
1. `rest_EC_{region}_aper_exponent` and `rest_EC_global_aper_offset` — the project's aperiodic 1/f hypothesis; clean fits (R² ≈ 0.99).
2. `rest_EC_{region}_alpha_rel`, `rest_EC_occipital_alpha_rel`, and `rest_EC_iaf_posterior_hz` — alpha slowing is a canonical TBI marker.
3. `rest_EC_{region}_theta_rel` and `rest_EC_global_theta_alpha_ratio` — theta excess / θ-α ratio.
4. `rest_EC_global_spec_entropy` — broadband complexity.
   *(Eyes-Open versions are secondary; EO is usable for only 22/25.)*

**Task-evoked (n = 21):**
5. `erp_P3b_target_par_mean_uv` and `erp_P3b_target_par_lat_ms` — parietal P3b (target detection).
6. `erp_P3b_tMinusS_par_mean_uv` — reference-clean P3b difference wave.
7. `erp_P3a_novel_fc_mean_uv` — frontocentral novelty P3a.

**Regions:** keep frontal / central / parietal / occipital / global as specified; consider
collapsing to global + posterior for the rest 1/f and to the named ROIs for ERPs to limit feature
count.

**Usability gating for Phase 4 modeling:**
- Rest-only models: **n = 25** (EC) or 22 (EC+EO).
- ERP-only models: **n = 21** (≥ 15 rare-tone epochs; excludes sub-040, sub-020, sub-036, sub-058).
- Combined rest+ERP models: **n = 20**.
- All gating uses the frozen folds from Phase 2; subjects failing usability are removed **in place**
  from their fold (never reshuffled), preserving leakage safety.

> **Pre-registration reminder for Phase 4:** lock this feature list and the usability gates
> **before** looking at any feature–outcome relationship; fit all scaling / reduction / imputation
> **inside** training folds only; report the covariates-only baseline contrast as the headline.

---

## 8. What was explicitly NOT done
- No model trained, no hyperparameter tuned.
- No feature correlated, plotted, or tested against NSI/Rivermead or group.
- No preprocessing parameter chosen by looking at any outcome.
- sub-040 ERP recovery via raw S-codes was deliberately deferred (documented), not guessed.
