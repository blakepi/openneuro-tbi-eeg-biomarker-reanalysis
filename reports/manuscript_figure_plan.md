# Manuscript Figure Plan
### Early Resting-State and Task-Evoked EEG Biomarkers of Persistent Post-Concussive Symptoms Following mTBI

*Specification for the five planned display items. These are **schematic / methodological**
figures — none plots a feature against an outcome, and no Results are shown. Each entry gives the
purpose, panel layout, data source, draft caption, and rendering notes so the figures can be
produced reproducibly from the existing Phase 0–3 artifacts.*

**Global style:** colour-blind-safe palette; consistent family colours throughout —
**resting-state = teal**, **ERP/task = orange**, **clinical/outcome = grey**, **leakage-control
elements = dark slate**. Vector output (SVG/PDF), 8–9 pt sans-serif labels, single- or
double-column width per journal.

---

## Figure 1 — Study flow diagram (CONSORT-style)

**Purpose.** Show participant accounting from the full dataset to each effective analytic N, with
every exclusion and its reason — the transparency backbone of the manuscript.

**Layout.** Top-to-bottom flow with labelled boxes and side annotations:
1. OpenNeuro ds003522 enrolled (all groups; n in `participants.tsv`).
2. Split by group → acute mTBI / control / chronic TBI; annotate that controls and chronic TBI
   exit outcome modeling (chronic: no longitudinal outcome; controls: not in within-mTBI
   prediction).
3. Acute mTBI with Session-1 EEG → with non-missing Session-3 NSI total (**n = 25**, primary
   cohort).
4. Branch into the three effective analytic sets with exclusion reasons:
   - Resting (eyes-closed) usable: **n = 25**.
   - ERP usable: **n = 21** (− `sub-040` no curated tone labels; − `sub-020`, `sub-036`,
     `sub-058` < 15 rare-tone epochs).
   - Combined panel: **n = 20**.
5. Footer band: "Subject-level CV folds frozen *before* EEG processing; exclusions applied
   in-place within folds; folds never regenerated."

**Data source.** `outputs/metadata_summary_tables/attrition_by_session.csv`,
`crosswalk_subject_ids.csv`, `outputs/features/ds003522_s1_subject_usability.csv`.

**Draft caption.** *"Participant flow. From the acute-mTBI arm of ds003522, 25 participants had a
usable Session-1 EEG recording and a Session-3 NSI total. Modality-specific quality control
yielded 25 (resting), 21 (ERP), and 20 (combined-panel) analytic samples. Cross-validation folds
were frozen prior to EEG processing; quality-control exclusions were applied within each
participant's pre-assigned fold and folds were never regenerated."*

---

## Figure 2 — Structure of the continuous recording

**Purpose.** Make explicit that resting and task data are embedded in a single continuous file and
how they are segmented — central to understanding both the paradigm and the boundary-aware
extraction.

**Layout.** A horizontal time-axis "ribbon" (0 → ~end, minutes) for one representative recording,
with coloured blocks in acquisition order:

`Eyes Closed → Eyes Open → Oddball run 1 → Eyes Closed → Eyes Open → Oddball run 2`

- Resting blocks (teal) annotated with approximate duration (~60 s each; ~120 s/condition total).
- Oddball runs (orange) annotated with the interleaved Standard/Target/Novel stream (184/38/38
  tones total across runs).
- A small marker at t = 0 for the EEGLAB `boundary` (recording onset); callout: "single boundary
  at onset; no internal discontinuities — pipeline is boundary-aware regardless."
- Optional inset: the event-marker labels used for segmentation (`Eyes Closed/Open: Every
  1000 ms`, `Standard/Target/Novel Tone`).

**Data source.** A representative `events.tsv` (e.g. `sub-005`) — schematic, drawn to scale from
real onsets; no EEG signal or outcome shown.

**Draft caption.** *"Schematic of the single continuous recording. Eyes-closed and eyes-open
resting blocks bracket two runs of the three-stimulus auditory oddball. Resting and task segments
were identified from event markers; a single boundary event at recording onset was handled by a
boundary-aware pipeline."*

---

## Figure 3 — EEG preprocessing pipeline

**Purpose.** Communicate the fixed, outcome-blind preprocessing applied identically to all
participants.

**Layout.** Vertical flowchart, one box per step, with parameters annotated:
1. Raw EEGLAB `.set/.fdt` (500 Hz, 65 ch, online ref CPz) — "raw retained unmodified".
2. Channel typing (VEOG→EOG, EKG→ECG).
3. Boundary handling (`boundary` → `BAD_boundary`; segment-wise filtering guard).
4. Notch 60 Hz.
5. Band-pass 0.5–45 Hz (FIR) — side note: "+40 Hz low-pass on the ERP branch".
6. Re-add CPz → standard 10–20 montage → average reference.
7. Within-participant bad-channel detection (robust z > 4) → spherical-spline interpolation.
8. Cleaned FIF + per-participant log.

Right-margin vertical banner across all steps: **"No outcome information used at any step."**
Branch indicator after step 5 showing the split into the resting (0.5–45 Hz) and ERP
(+40 Hz LP) processing branches.

**Data source.** `scripts/06_preprocess_ds003522_s1.py`, `_eeg_common.py`, per-subject logs in
`data/processed/ds003522_s1/logs/`.

**Draft caption.** *"Preprocessing pipeline. A single fixed parameter set, selected without
reference to any outcome, was applied to every recording; raw files were never modified. The
pipeline was boundary-aware and branched into resting-state and ERP processing streams."*

---

## Figure 4 — Locked EEG feature families

**Purpose.** Present the compact, pre-registered predictor panel and its biological motivation,
grouped by family — the conceptual core of the study.

**Layout.** Two columns:
- **Resting-state (teal):** four small schematic icons —
  (1) posterior IAF (a spectrum with a 7–13 Hz alpha peak and a frequency marker);
  (2) global aperiodic exponent (log-log spectrum with a 1/f slope line; specparam fit);
  (3) frontal theta/alpha ratio (two shaded bands on a spectrum, with a frontal head inset);
  (4) occipital relative alpha (alpha band shaded relative to total, occipital head inset).
- **Task-evoked / ERP (orange):** schematic averaged waveforms —
  (5–6) parietal P3b with amplitude and latency markers (target);
  (7–8) frontocentral P3a with amplitude and latency markers (novel).
- A small "exploratory" chip for spectral entropy, visually set apart.
- Mini scalp maps indicating each feature's ROI (frontal / central / parietal / occipital /
  posterior).

**Important.** Waveforms/spectra are **idealized schematics** (textbook morphology), not group
averages from this cohort — to avoid any implicit feature–outcome display.

**Data source.** Predictor definitions from `_eeg_common.py` and the SAP locked-panel table.

**Draft caption.** *"Locked predictor panel. Four resting-state features (posterior individual
alpha frequency, global aperiodic exponent, frontal theta/alpha ratio, occipital relative alpha)
and four event-related potential features (P3b and P3a amplitude and latency) were pre-registered;
spectral entropy was retained as an exploratory feature. Waveforms and spectra are schematic."*

---

## Figure 5 — Planned statistical workflow

**Purpose.** Show the leakage-safe analysis architecture and the pre-specified model hierarchy
(primary → secondary → exploratory).

**Layout.** Left-to-right pipeline:
1. **Frozen folds** (5-fold, stratified on S3-NSI tertiles, split by `subject_uid`, seed 42) —
   icon of 25 subjects partitioned, with "frozen before EEG processing; never regenerated".
2. **Within-training-fold processing** box (standardize → impute [sensitivity] → fit), with a
   one-way arrow to held-out fold and a struck-through reverse arrow ("test data never inform
   fitting").
3. **Model hierarchy** stacked by tier:
   - *Primary (confirmatory):* parsimonious combined linear model (aperiodic exponent + posterior
     IAF + P3b amplitude + age + sex) and full-panel elastic net.
   - *Reported for transparency:* full 10-term OLS (flagged overfit-prone).
   - *Secondary (supportive):* ridge, LASSO; domain-specific resting/ERP models.
   - *Exploratory:* random forest, XGBoost; spectral entropy; secondary outcomes.
4. **Reporting outputs:** β + 95 % CI + FDR p-values + adjusted R² + effect sizes; out-of-fold
   R²/MAE vs. age+sex baseline.

Colour the confirmatory tier prominently; visually de-emphasize the exploratory tier.

**Data source.** SAP §8–§12; `outputs/splits/frozen_cv_folds.csv`,
`outputs/splits/split_provenance.json`.

**Draft caption.** *"Planned analysis workflow. Subject-level folds were frozen before EEG
processing; all scaling and imputation were fit within training folds only. A parsimonious linear
model and a full-panel elastic net are co-primary; ordinary least squares over the full panel is
reported for transparency; penalized and machine-learning models are supportive and exploratory,
respectively. No model was fit until the analysis plan was frozen."*

---

## Supplementary figures (optional)

- **S1 — Participant crosswalk / overlap:** how `subject_uid` (URSI) deduplicates participants
  across ds003522/ds005114/ds003523 and the `Original_ID` 3013 collision (motivates the leakage
  safeguard). Source: `crosswalk_subject_ids.csv`.
- **S2 — Per-participant data yield:** usable eyes-closed/eyes-open seconds and retained
  Standard/Target/Novel epoch counts (QC transparency, no outcome). Source:
  `ds003522_s1_subject_usability.csv`, `ds003522_s1_erp_features.csv`.
- **S3 — Missingness map:** feature × participant missingness grid. Source:
  `ds003522_s1_feature_qc_summary.csv`.

---

### Production notes
- Figures 1, 3, 5 are vector flowcharts (e.g. draw.io / matplotlib / TikZ).
- Figure 2 is a to-scale schematic from a real `events.tsv` (no signal).
- Figure 4 uses idealized morphologies; explicitly label as schematic in-figure to forestall
  misreading as cohort results.
- Every figure that could be mistaken for a result must carry the in-figure note "schematic" or
  "no outcome data shown".
