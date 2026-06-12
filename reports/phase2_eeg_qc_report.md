# Phase 2 Report — Session-1 EEG: frozen splits, download, and quality control
### Primary dataset ds003522 (acute mild TBI, auditory oddball + embedded rest)

**Date:** 2026-06-11
**Scope guard honored:** no models trained, no biomarker (spectral/ERP/aperiodic) features
computed, no EEG–outcome association inspected. Only file reading and descriptive QC.
**Producing scripts:** `scripts/03_freeze_splits.py`, `scripts/04_download_s1_eeg.py`,
`scripts/05_eeg_qc.py`.
**Artifacts:** `outputs/splits/frozen_cv_folds.csv`, `outputs/eeg_manifests/ds003522_s1_manifest.csv`,
`outputs/qc/ds003522_s1_qc_summary.csv`.

---

## Executive answers to the Phase-2 questions

| Question | Answer |
|---|---|
| Eligible ds003522 S1 mTBI subjects with EEG? | **25 / 25** — every eligible subject has a complete Session-1 recording. |
| Which task files exist per subject/session? | One task only: **`task-ThreeStimAuditoryOddball`**, 8 BIDS files each (`.set`+`.fdt`, `channels.tsv`, `electrodes.tsv`, `coordsystem.json`, `*_eeg.json`, `events.tsv/json`). |
| Is **resting EEG** available as BIDS files? | **No separate `task-Rest` file.** Rest **is present as data**, embedded inside the oddball recording as event-marked **Eyes-Closed** and **Eyes-Open** blocks. Must be extracted by event markers in Phase 3. |
| Unreadable / missing files? | **None.** 200/200 files downloaded, all 25 `.set` open in MNE. |
| Usable N after QC? | **25 / 25.** No subject fails basic QC. |
| Quality problems threatening feasibility? | **None that threaten feasibility.** The only universal flag (EXTREME_AMP) is an artifact of raw, unfiltered, boundary-spliced EEGLAB data and is removed by standard preprocessing. |

---

## 1. Frozen leakage-safe splits (`scripts/03_freeze_splits.py`)

Folds are frozen **before** any EEG was read, with split unit = **`subject_uid` (URSI)** and a
fixed seed (42). Defined for all three eligible cohorts (acute mTBI with S1 EEG **and** an S3 NSI
outcome):

| Cohort | Dataset (task) | n | Folds | Stratified on S3-NSI tertiles | Fold sizes |
|---|---|---:|---:|---|---|
| **A (primary)** | ds003522 (oddball) | **25** | 5 | yes | 5/5/5/5/5 |
| B (replication) | ds005114 (DPX) | 34 | 5 | yes | 7/7/7/7/6 |
| C (replication) | ds003523 (WM) | 34 | 5 | yes | 7/7/7/7/6 |

Leakage cross-check: **0** subjects assigned to more than one fold within a cohort.
Provenance (seed, strategy, bin counts, fallback logic) is recorded in
`outputs/splits/split_provenance.json`. Because n is small, **leave-one-subject-out is flagged as
the recommended alternative** for the primary model; the 5-fold assignment is the default.

> **QC interaction (pre-declared):** a subject that later fails QC is **removed from its frozen
> fold in place** — folds are never reshuffled — preserving the leakage guarantee. In this run
> **no subject is removed** (25/25 pass), so cohort A remains 25.

---

## 2. Download manifest (`scripts/04_download_s1_eeg.py`)

Session-1 only. Later sessions were never fetched, so they cannot leak into an S1 predictor.

- Subjects: **25** eligible cohort-A subjects.
- Files: **200** (8 per subject), status = **DOWNLOADED for all 200**; 0 missing, 0 remote gaps.
- Volume: **3.53 GB** to `data/raw/ds003522/sub-*/ses-01/eeg/`.
- Task label on every file: `ThreeStimAuditoryOddball`.
- `.set` + `.fdt` present for **25/25** subjects (EEGLAB pair both required to read signal).

Full per-file detail (remote key, remote size, local size, size-match, status) is in
`outputs/eeg_manifests/ds003522_s1_manifest.csv`. The script supports `--dry-run` (HEAD-only
manifest, no download) and is resumable (skips files already present with matching byte size).

---

## 3. What is in a Session-1 recording (rest vs oddball)

Each subject has **one continuous recording (~15–28 min)** that contains **both** paradigms,
separated by event markers in `events.tsv`. Representative event composition:

| Event `trial_type` | Meaning | Count (example subject) |
|---|---|---:|
| `Eyes Closed: Every 1000 ms` | resting eyes-closed block (1-s pulse train) | 120 |
| `Eyes Open: Every 1000 ms` | resting eyes-open block (1-s pulse train) | 120 |
| `Standard Tone` | oddball frequent/standard | 184 |
| `Target Tone` | oddball target (P3b) | 38 |
| `Novel Tone` | oddball novel/distractor (P3a) | 38 |
| `STATUS` / `boundary` | recording status + EEGLAB splice point | 5 |

**Implications for Phase 3:**
- **Resting and task features are both obtainable** from the same file — the project's
  "spectral + aperiodic (rest)" and "task-evoked (oddball P3a/P3b)" feature families are all
  feasible from S1 data.
- Rest must be **segmented by the Eyes-Closed / Eyes-Open marker trains** (and their start/stop
  status codes), not assumed to be a separate file.
- A **`boundary` event** indicates a discontinuity (concatenation/cut). Preprocessing must be
  **boundary-aware**: do not filter, epoch, or compute spectra across a boundary.

---

## 4. Quality control results (`scripts/05_eeg_qc.py`)

Read-only descriptive QC on all 25 Session-1 recordings. **Uniform and clean:**

| Metric | Result across n=25 |
|---|---|
| Readable in MNE | **25 / 25** |
| Sampling frequency | **500 Hz** (all) |
| Channel count | **65 EEG** (all; consistent 10–20 montage: Fp1, Fz, F3, …) |
| Recording duration | median **1022 s** (≈17 min), range 920–1668 s |
| Flat channels | **0** in every subject |
| NaN samples | **0** in every subject |
| Zero samples | ≤ **0.001 %** (negligible) |
| Bad channels marked (`channels.tsv` / info) | **0** flagged by the dataset |
| Peak-to-peak amplitude (median across ch) | median **2430 µV**, range 742–5895 µV — high because data are **unfiltered (DC-coupled)** |
| Max abs amplitude | 0.26–2.9 V → triggers **EXTREME_AMP** in **all 25** |

**Interpretation of the universal EXTREME_AMP flag.** It fires for every subject because the
files are raw, **un-high-passed** EEGLAB exports with `boundary` splice transients and slow DC
drift. It is therefore **not a subject-level quality signal** and not a basis for exclusion. It is
fully expected to disappear after the Phase-3 high-pass filter and boundary-aware handling. The
genuinely discriminating QC metrics (flat channels, NaN, zero, bad-channel marks, readability)
are all clean.

**QC failure / missingness by group (descriptive).** The eligible cohort A is entirely acute
mTBI, so there is no within-cohort group contrast to compute, and **there were 0 QC failures** to
distribute across groups. The group-differential signal of interest is upstream — **attrition to
the S3 outcome** — quantified in Phase 1 (`attrition_by_session.csv`): mTBI fall from 44 (S1 EEG)
to 25 (S1 EEG + S3 outcome); controls from 27 to 21. Control EEG was deliberately **not**
downloaded here because the primary analysis is within-mTBI prediction; controls enter only later
as a reference/classification arm.

**Usable N after QC = 25 (cohort A).** This equals the eligible N; no attrition at the QC stage.

---

## 5. Feasibility verdict

**Feasible.** For the primary cohort:
- Complete, uniform, readable S1 EEG for all 25 eligible acute-mTBI subjects.
- Both resting and oddball signal present, enabling the full planned feature set (spectral,
  aperiodic 1/f, P3a/P3b).
- No corrupt files, no channel/montage heterogeneity, no missing data within recordings.

The binding constraint remains **sample size (n=25 with a 4-month outcome)**, not data quality —
exactly as flagged in the Phase-1 plan, which pre-specifies the S2 outcome (n≈34) and ds005114
(n≈34) as power-sensitivity / replication. Data quality does **not** add further attrition.

---

## 6. Recommended Phase-3 preprocessing decisions (carried forward, not yet executed)

1. **Boundary-aware pipeline.** Read `boundary`/`STATUS` events first; never filter, epoch, or
   estimate spectra across a `boundary`. Annotate splices as `BAD`.
2. **Filtering.** High-pass ~0.1–1 Hz (resolves the DC offsets behind EXTREME_AMP) + line-noise
   handling (notch/`zapline`); low-pass/anti-alias as needed. Fix exact cutoffs before features.
3. **Re-reference.** Decide and freeze (e.g., average reference after bad-channel handling);
   record the original reference from `*_eeg.json`.
4. **Segment by paradigm.** Extract resting Eyes-Closed and Eyes-Open blocks from the marker
   trains; epoch oddball around Standard/Target/Novel tones for P3a/P3b.
5. **Automated bad-channel + artifact handling.** The dataset marks 0 bad channels, so detection
   must be **derived** (variance/correlation/RANSAC) and ICA/ASR for ocular/muscle artifact —
   **all fit inside training folds only** (`frozen_cv_folds.csv`).
6. **Pre-register QC exclusion thresholds** (min clean epochs per condition, max interpolated
   channels) at the **start of Phase 3, before** any feature extraction; apply them in place
   within the frozen folds and log every drop in a CONSORT update.
7. **Replication parity.** Mirror the chosen pipeline on ds005114/ds003523 (different tasks: DPX,
   visual working memory) for cohorts B/C.

---

## 7. Artifacts produced in Phase 2

| File | Contents |
|---|---|
| `outputs/splits/frozen_cv_folds.csv` | 93 subject-fold rows (cohorts A/B/C), keyed on `subject_uid`, with S3 outcome + fold |
| `outputs/splits/split_provenance.json` | seed, fold strategy, stratification bins, fallback logic |
| `outputs/eeg_manifests/ds003522_s1_manifest.csv` | 200 file rows: remote key/size, local path/size, status |
| `outputs/qc/ds003522_s1_qc_summary.csv` | 25 recordings × QC metrics |
| `scripts/03_freeze_splits.py`, `04_download_s1_eeg.py`, `05_eeg_qc.py` | reproducible pipeline |

**Not done (by design):** no filtering/ICA/epoching, no spectral/ERP/aperiodic features, no
EEG–outcome association, no model training. Those begin in Phase 3 after QC-exclusion thresholds
are pre-registered.
