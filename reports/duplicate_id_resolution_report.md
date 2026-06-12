# Duplicate ID Resolution Report
### Original_ID 3013 and clinical-only records — transparent handling

**Date:** 2026-06-11
**Scope:** Identity reconciliation for the Phase 1 master subject/session table.
**Principle:** No record is silently dropped. Every ambiguity is documented, and the
canonical identity key is chosen so that ambiguities are *represented*, not erased.

---

## 1. Identity keys and why `Original_ID` is not the primary key

| Key | Form | Role |
|---|---|---|
| `Original_ID` (= BigAgg `SubID`) | integer (3001–3120; chronic arm uses 5-digit ids) | recording id; join key to the clinical spreadsheet |
| `URSI` | `M87dddddd` (BIDS) / last-5 digits in BigAgg | scan-generated **unique** subject id |
| **`subject_uid`** (chosen canonical key) | **full BIDS `URSI`** | leakage-safe split unit; deduplication unit |

`Original_ID` is **not unique** — value **3013 is shared by two different `URSI`s** (see §2).
`URSI` is unique by construction, so `subject_uid = URSI` is used as the canonical person key
throughout the master table and for all train/test splitting.

The BigAgg clinical spreadsheet stores `URSI` as the **last 5 digits** of the BIDS `URSI`
(e.g. BIDS `M87184858` → BigAgg `84858`). The crosswalk records both forms (`URSI`,
`URSI_short`) so the clinical join is explicit and reversible.

---

## 2. The `Original_ID 3013` collision

`participants.tsv` (in all three datasets) lists **two rows** with `Original_ID = 3013`, under
**two different URSIs that differ by a digit transposition** (`...342` ↔ `...432`):

| dataset | BIDS subject | Original_ID | URSI | URSI_short | group | EEG present |
|---|---|---:|---|---:|---|---|
| ds003522 | sub-027 | 3013 | **M87138342** | 38342 | Control | ds003522/05114/03523 |
| ds003522 | sub-028 | 3013 | **M87138432** | 38432 | Control | ds003522/05114/03523 |
| ds005114 | sub-036 | 3013 | M87138342 | 38342 | Control | (same) |
| ds005114 | sub-037 | 3013 | M87138432 | 38432 | Control | (same) |
| ds003523 | sub-036 | 3013 | M87138342 | 38342 | Control | (same) |
| ds003523 | sub-037 | 3013 | M87138432 | 38432 | Control | (same) |

**Clinical (BigAgg) coverage:** the BigAgg table contains **only `URSI 38432`** (→ `M87138432`),
with `NSItotal = 0` at Session 1. `URSI 38342` (→ `M87138342`) has **no clinical row**.

### Interpretation
- Both records are labeled **Control**, and both have EEG in all three datasets.
- The two URSIs differ only by a transposition (`138342` vs `138432`). This is consistent with
  *either* (a) one person entered twice with one URSI mistyped, *or* (b) two distinct controls
  erroneously assigned the same `Original_ID`. **The available metadata cannot disambiguate
  these two possibilities.**

### Resolution (no data dropped)
1. **Key on `URSI`, not `Original_ID`.** Under `subject_uid = URSI`, the two records are retained
   as **two distinct subjects** (`M87138342`, `M87138432`). This is the conservative choice: it
   never merges what might be two people.
2. **Clinical data attaches only where the URSI matches.** `M87138432` receives the BigAgg row
   (`NSItotal=0`); `M87138342` is flagged `has_clinical = False`. No clinical value is copied,
   imputed, or guessed across the two URSIs.
3. **Effect on cohorts:** both are **controls**, so neither enters the within-mTBI primary
   analysis regardless. For any control-reference / classification analysis they are treated as
   two records; `M87138342` (no outcome) is excluded by the *same* "must have outcome" rule
   applied to every subject — **not** by a special-case deletion.
4. **Flag preserved in outputs.** Both rows are visible in
   `crosswalk_subject_ids.csv` and `master_subject_session_table.csv` with their distinct
   `subject_uid`, so any downstream user can apply a different policy if desired.

> **Recommended note for the manuscript / pre-registration:** report `Original_ID 3013` as a
> known data-entry anomaly; analyses key on URSI; a sensitivity check that drops both 3013
> records changes no primary (mTBI) result because both are controls.

---

## 3. Clinical-only records (in BigAgg, no EEG anywhere)

Three `SubID`s appear in the BigAgg clinical sheets but have **no EEG `.set` file in any of the
three datasets**, so they cannot enter an EEG analytic cohort:

| BigAgg SubID | Status |
|---:|---|
| 3008 | clinical row is essentially empty (all-NaN outcomes) at S1; no EEG |
| 3022 | clinical-only; no EEG in ds003522/ds005114/ds003523 |
| 3120 | clinical-only; no EEG in ds003522/ds005114/ds003523 |

**Handling:** these produce the 9 "unmatched clinical rows" warning (3 subjects × 3 session
sheets) in `02_build_cohort.py`. They are **excluded from the EEG cohort by definition** (no EEG)
and are reported here rather than dropped silently. They could be reinstated if EEG for these
subjects is located in a dataset not yet downloaded.

---

## 4. Cohort-size accounting (reconciliation)

| Quantity | Count |
|---|---:|
| Crosswalk rows (dataset × BIDS subject) | 278 |
| **Unique `subject_uid` (URSI) across all datasets** | **116** |
| BigAgg clinical subjects with no EEG (excluded) | 3 |
| `Original_ID` collisions | 1 (value 3013 → 2 URSIs) |

The 116 unique subjects comprise the longitudinal acute-mTBI + control cohort plus the
ds003522-only chronic-TBI arm (25 subjects, who have single-session EEG but **no** BigAgg
clinical/outcome data — see the analysis plan).

*Generated from `outputs/metadata_summary_tables/crosswalk_subject_ids.csv` and
`master_subject_session_table.csv` by `scripts/02_build_cohort.py`.*
