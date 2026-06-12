# Phase 0 Feasibility Report
### EEG markers of recovery after mild traumatic brain injury (OpenNeuro)

**Date:** 2026-06-11
**Author:** Research pipeline (Phase 0 — inspection only; no preprocessing, no modeling)
**Datasets:** OpenNeuro `ds003522` (primary), `ds005114`, `ds003523` (secondary)
**Provenance:** All numbers below are computed directly from metadata pulled from the public
`openneuro.org` S3 bucket (see `scripts/00_download_or_load.py`) and summarized by
`scripts/01_inspect_bids_metadata.py`. Source tables are in
`outputs/metadata_summary_tables/`.

---

## 0. Executive summary

A **feasible and publishable** primary study exists. The three datasets come from a **single
longitudinal mTBI cohort** (UNM Center for Brain Recovery and Repair, J.F. Cavanagh; collected
2016–2018) with:

- **64-channel EEG** at 3 timepoints spanning the acute-to-chronic recovery window
  (Session 1 = 3–14 days post-injury; Session 2 ≈ 2 months; Session 3 ≈ 4 months).
- **Validated persistent-symptom outcomes measured at every session** — the Neurobehavioral
  Symptom Inventory (NSI: somatic/cognitive/emotional) and the Rivermead Post-Concussion
  Symptoms Questionnaire — plus depression (BDI), pain, anxiety, fatigue, and a neuropsych
  battery. These live in supplementary spreadsheets keyed by `URSI`, **not** in
  `participants.tsv`.
- Three complementary tasks (auditory oddball, DPX cognitive control, visual working memory)
  for task-evoked features, plus resting EEG (in the primary dataset).

**Two cautions dominate the design:**

1. **The same people appear in all three datasets under different `sub-0XX` labels.** The only
   stable cross-dataset identity key is `Original_ID` / `URSI`. **70 individuals are shared
   across all three datasets**; 90 are shared between `ds003523` and `ds005114`. Any pooling,
   or any train/test split, must be done on `Original_ID` to avoid subject leakage.
2. **Attrition is heavy and almost certainly informative.** Per-session symptom outcomes drop
   from ~91 (S1) → 78 (S2) → 62 (S3). Dropout is plausibly related to recovery itself, so
   complete-case analysis will be biased.

A defensible **primary hypothesis** (see §7): *early (Session-1) EEG spectral + aperiodic +
task-evoked features predict persistent post-concussive symptom burden (NSI / Rivermead) at
~4 months in acute mTBI*, evaluated with subject-level, leakage-safe cross-validation.

---

## 1. How many subjects are available?

| Dataset | Task | `participants.tsv` | Subjects with EEG | Sessions present |
|---|---|---:|---:|---|
| **ds003522** (primary) | Three-Stim Auditory Oddball (+ Rest) | 96 | 96 | ses-01/02/03 |
| ds005114 | DPX cognitive control | 91 | 91 | ses-01/02/03 |
| ds003523 | Visual Working Memory | 91 | 91 | ses-01/02/03 |

Because of cross-dataset overlap (§8), the number of **unique individuals** across all three is
far smaller than 96 + 91 + 91 = 278. The acute mTBI + control cohort is essentially **one
group of ~118 people** (the `ds005114`/`ds003523` roster of 91, plus extra subjects unique to
`ds003522`, including the chronic-TBI arm).

*Source: `01_dataset_overview.csv`.*

---

## 2. What groups exist?

`Group` is coded in each `participants.tsv` (`participants.json` gives the levels):

| Group code | Label | ds003522 | ds005114 | ds003523 |
|---:|---|---:|---:|---:|
| 0 | mTBI (acute / sub-acute) | 44 | 57 | 57 |
| 1 | Control | 27 | 34 | 34 |
| 2 | Chronic TBI | 25 | — | — |

- **ds003522** is the only dataset with a **chronic TBI** arm (Group 2). Per the README, chronic
  subjects have **only one session by design**.
- `ds005114` and `ds003523` contain only acute mTBI vs. control.
- `sex` (0/1) and `age` (range 18–55, mean ≈ 30) are present in every `participants.tsv`.

*Source: `03_group_by_dataset.csv`, `02_participants_*.csv`.*

---

## 3. What sessions exist?

All three datasets use **`ses-01`, `ses-02`, `ses-03`**. Session timing (from the READMEs):

| Session | Timing | Notes |
|---|---|---|
| ses-01 | 3–14 days post-injury | only session with MRI (MRI not yet uploaded) |
| ses-02 | ~1.5–3 months after S1 | |
| ses-03 | ~3–5 months after S1 | |

**EEG availability per session (count of `*_eeg.set` files) — this is the attrition curve:**

| Dataset | ses-01 | ses-02 | ses-03 | 1 sess | 2 sess | 3 sess |
|---|---:|---:|---:|---:|---:|---:|
| ds003522 | 96 | 59 | 45 | 37 | 14 | 45 |
| ds005114 | 91 | 75 | 57 | 16 | 18 | 57 |
| ds003523 | 91 | 74 | 56 | 17 | 18 | 56 |

(In `ds003522`, the large "1 session" count reflects the 25 chronic-TBI subjects who were
single-session by design, plus genuine dropouts.)

*Source: `04_session_availability.csv`.*

---

## 4. What outcome variables are available?

**Not in `participants.tsv`.** The outcome/clinical variables live in
`code/BigAgg_4BIDS.xlsx` (sheets `S1`, `S2`, `S3` = one per session; a `Notes` sheet lists
exclusions), keyed by `URSI`. Note: the `BigAgg_4BIDS.xlsx` shipped with `ds003522` and with
`ds005114` are **byte-identical** — it is one shared master clinical table for the whole cohort.
72 distinct clinical variables were inventoried (`06_clinical_variables.csv`). The most useful:

**Persistent-symptom / recovery outcomes (measured at S1, S2, S3):**
- `NSIsoma`, `NSIcog`, `NSIemo` — Neurobehavioral Symptom Inventory subscales (the standard
  post-concussion symptom measure). **Primary outcome candidate.**
- `RivermeadTotal` — Rivermead Post-Concussion Symptoms Questionnaire. **Primary/confirmatory.**
- `BDItotal` (Beck Depression Inventory), `Anxiety`, `Depression`, `Fatigue`, `PainRating`,
  sleep and pain-interference items (PROMIS-style).
- Frontal Systems Behavior (FrSBe): apathy / disinhibition / executive (before vs. now).

**Injury-severity covariates (S1):** `GCS`, `DaysSinceInjuryVisit1`, `LOC`/`DurationLOC`,
`MechanismOfInjury`, `DazedDisoriented`, `HadCT`/`HadMRI`.

**Neuropsych battery (S1):** HVLT-R (verbal memory), Digit Span, Coding, TOPF (premorbid IQ),
TOMM (effort validity); S2/S3 add executive / working-memory / cognitive-control factor scores
(`Exec_Composite`, `WM_Fac`, `CogCtl_Fac`, …).

**Session intervals are recorded** (`DaysSinceInjuryVisit1`, `DaysSinceS1`, `DaysSinceS2`) so
elapsed time can be modeled explicitly rather than assumed.

> `ds003523` (Visual Working Memory) has **no clinical spreadsheet**; its behavioral data are
> per-subject/session `.mat` files under `code/WM Beh/`. Its README states the data were
> **never published** ("I have 1/3 of the paper done…") — an opportunity, but symptom outcomes
> for those subjects must be pulled from the shared `ds003522`/`ds005114` master table via `URSI`.

*Source: `06_clinical_variables.csv`, `07_outcome_missingness.csv`.*

---

## 5. Are longitudinal recovery outcomes available?

**Yes.** This is the dataset's biggest strength. NSI and Rivermead are recorded at all three
sessions, so both **persistent symptom burden at 4 months** and **recovery trajectory**
(change from S1) are directly available. Non-null outcome counts per session:

| Session sheet | NSI (soma/cog/emo) | Rivermead | BDI | rows |
|---|---:|---:|---:|---:|
| S1 | 91 | 90 | 91 | 93 |
| S2 | 78 | 77 | 78 | 93 |
| S3 | 62 | 60 | 62 | 93 |

So a longitudinal symptom outcome exists for ~60 subjects with complete 3-timepoint data, and
~78 with at least S1→S2. Combined with Session-1 EEG (available for ~91), this supports a
**predict-future-symptoms** design.

*Source: `07_outcome_missingness.csv`.*

---

## 6. What EEG file formats and tasks are present?

**Format:** identical across all three datasets — **EEGLAB `.set` + `.fdt`** (BIDS-EEG),
readable with `mne.io.read_raw_eeglab` / `mne-bids`.

**Acquisition (from `*_eeg.json`):**

| | ds003522 | ds005114 | ds003523 |
|---|---|---|---|
| Sampling rate | 500 Hz | 500 Hz | 500 Hz |
| EEG channels | 64 | 64 | 64 |
| Amplifier | BrainVision actiCHamp | same | same |
| Reference / Ground | CPz / AFz | CPz / AFz | CPz / AFz |
| Line frequency | 60 Hz | 60 Hz | 60 Hz |
| Extra channels | VEOG, EKG | VEOG, EKG | VEOG, EKG |

The harmonized 64-channel 10-20 montage across datasets makes cross-task feature extraction and
cross-dataset replication straightforward.

**Tasks:**

| Dataset | BIDS task label | Paradigm |
|---|---|---|
| ds003522 | `ThreeStimAuditoryOddball` | 3-stimulus auditory oddball (P3a/P3b); Rest also collected |
| ds005114 | `DPX` | Dot-Pattern Expectancy cognitive-control / proactive-reactive control |
| ds003523 | `VisualWorkingMemory` | visual WM with mind-wandering probes |

> **Caveat on "Rest":** the `ds003522` title advertises "and Rest," but the BIDS tree exposes
> **only** the `task-ThreeStimAuditoryOddball` files — there is no `task-Rest` directory. Resting
> EEG appears to be embedded/handled in the lab's MATLAB scripts (`STEP1_REST_JFC.m`) rather than
> released as a separate BIDS task. **Resting-state availability must be confirmed before relying
> on it** as a feature source.

*Source: `05_eeg_acquisition.csv`, `09_event_codes_*.csv`.*

---

## 7. What can support a publishable primary hypothesis?

**Recommended primary hypothesis (single dataset, leakage-safe):**

> In acute mild TBI (`ds003522`, Group 0), **Session-1 EEG features** — spectral power, the
> aperiodic (1/f) exponent and offset (FOOOF/`specparam`), and task-evoked oddball responses
> (P3a/P3b) — **predict persistent post-concussive symptom burden** (NSI total / Rivermead) at
> Session 3 (~4 months), over and above injury-severity and demographic covariates.

Why it is publishable and defensible:
- **Prospective framing** (early EEG → later outcome) avoids circularity and is clinically
  meaningful (triage / prognosis).
- **Established outcomes** (NSI, Rivermead) and **established EEG features** (aperiodic slope,
  P3) with prior TBI literature.
- **Built-in replication / generalization** across `ds005114` (DPX) and `ds003523` (WM) tasks —
  but only after deduplicating shared subjects (§8).

Supporting / secondary analyses the data can sustain:
- Group classification (mTBI vs. control vs. chronic) from resting/aperiodic features.
- Recovery-trajectory modeling (mixed-effects: NSI ~ time + EEG, with `DaysSinceS*` as time).
- Cross-task feature stability within subject.

**Power caveat:** with ~44 acute mTBI in `ds003522` and ~60 subjects having complete 3-timepoint
outcomes, this is a **modest-N** study. Frame as feature-prediction with nested CV and strict
multiple-comparison control; pre-register; avoid high-dimensional models without regularization.

---

## 8. Are subject IDs overlapping across datasets?

**Yes — substantially, and dangerously if ignored.** All three datasets are the same cohort.
The `participant_id` (`sub-0XX`) labels are **not** consistent across datasets (`ds003523` and
`ds005114` share one numbering; `ds003522` uses a different one). The stable identity keys are
**`Original_ID`** (recording ID, 3001–3120) and **`URSI`** (`M87…`).

| Pair | Shared `Original_ID` |
|---|---:|
| ds003522 ∩ ds005114 | 70 |
| ds003522 ∩ ds003523 | 70 |
| ds005114 ∩ ds003523 | 90 |
| **All three** | **70** |

**Implications (leakage-safe design rules):**
- Build a master crosswalk keyed on `Original_ID`/`URSI`; never join datasets on `sub-0XX`.
- Any pooled analysis must **deduplicate individuals** before train/test splitting, and split by
  `Original_ID` so no person spans train and test.
- Treat `ds005114`/`ds003523` as **different tasks on the same people**, not independent samples.

*Source: `08_cross_dataset_overlap.csv`.*

---

## 9. Are there missingness problems?

**Yes — three distinct kinds, all material:**

1. **Longitudinal attrition (informative).** Outcomes: S1 ≈ 91 → S2 ≈ 78 → S3 ≈ 62; EEG follows
   the same curve (§3). Dropout is plausibly related to recovery (recovered subjects leave;
   symptomatic ones may also leave), so it is **not missing-at-random** — complete-case analysis
   will bias prognosis estimates. Plan for sensitivity analyses / appropriate missing-data
   handling and report a CONSORT-style flow.

2. **Outcomes only defined for part of the sample.** Injury variables (`DaysSinceInjuryVisit1`,
   `GCS`, `LOC`) are populated for TBI subjects only (controls have no injury date — ~58/93
   non-null at S1, by design). NSI/Rivermead exist for both groups.

3. **Data-quality quirks to handle explicitly:**
   - `Original_ID` **3013 is duplicated** within each `participants.tsv` (`sub-027`/`sub-028` in
     ds003522; `sub-036`/`sub-037` in the others) with **two different `URSI`s**
     (`M87138342` vs `M87138432`) — looks like a transposition; treat carefully when crosswalking.
   - The `Notes` sheet lists **explicit exclusions** (e.g., pre-existing TBI, multiple prior TBIs,
     assessments discontinued, partial EEG) and "lost to follow-up" flags — apply these before
     analysis.
   - `channels.tsv` lists `type`/`units` as `n/a`; channel types must be inferred from names
     (EEG vs. VEOG/EKG) during preprocessing.
   - `ds003523` symptom data are not in a spreadsheet — must be obtained via the shared master
     table by `URSI`, and the dataset is unpublished.

*Source: `02_participants_*.csv`, `06_clinical_variables.csv`, `07_outcome_missingness.csv`,
the `Notes` sheet of `BigAgg_4BIDS.xlsx`.*

---

## 10. Recommendation & next steps (still no preprocessing/modeling)

**Go.** The primary dataset `ds003522` supports the prospective EEG→symptom hypothesis on its
own; the secondary datasets add task-evoked replication once subject overlap is handled.

Before Phase 1 (preprocessing):
1. **Build the `Original_ID`/`URSI` crosswalk** and a deduplicated master subject table, merging
   `participants.tsv` + the `BigAgg` clinical sheets. Resolve the 3013 duplicate.
2. **Confirm resting-state EEG** availability in `ds003522` (it is not exposed as a BIDS task).
3. **Lock the analysis plan / pre-register:** primary outcome (NSI total or Rivermead at S3),
   feature set, covariates, CV scheme (subject-level / leakage-safe), and missing-data strategy.
4. **Decide the split unit now** (`Original_ID`) so that all later code inherits a leakage-safe
   split.

---

### Appendix — generated artifacts
- `outputs/metadata_summary_tables/01_dataset_overview.csv`
- `…/03_group_by_dataset.csv`, `…/04_session_availability.csv`, `…/05_eeg_acquisition.csv`
- `…/06_clinical_variables.csv`, `…/07_outcome_missingness.csv`
- `…/08_cross_dataset_overlap.csv`, `…/09_event_codes_<dsid>.csv`
- `…/02_participants_<dsid>.csv`
- Raw metadata cache: `data/metadata_cache/<dsid>/`
