# Phase 5 Results — Independent Replication Assessment
### Can the ds003522 discovery findings be replicated in ds005114?

**Date:** 2026-06-11
**Adherence statement:** The discovery analysis is **frozen and unmodified** (frozen-folds
checksum `453fede5`, feature files untouched). The locked statistical hierarchy, feature
definitions, and preprocessing were **not** changed. Cohorts were **not** combined. No exploratory
finding is promoted. The framework remains estimation-first; no causal claims are made.
Producing scripts: `13_replication_feasibility.py`, `14_replication_figures.py`.

> **Headline:** The designated replication cohort **ds005114 cannot replicate the discovery
> analysis**, because it contains **neither the auditory-oddball paradigm nor any embedded resting
> EEG**. **0 of the 8 locked predictors are extractable with their preregistered definitions.** A
> feature-identical outcome replication is therefore **not possible** in ds005114 (nor in
> ds003523), and we decline to manufacture one by redefining features — doing so would violate the
> locked definitions and reintroduce exactly the analytic flexibility this project is designed to
> exclude. The discovery null thus remains **untested**, not refuted, in independent data.

---

## 1. Why replication is infeasible: paradigm and state mismatch

The locked panel draws on two paradigms that exist **only** in the discovery dataset:
- the four resting features (global aperiodic exponent, posterior IAF, frontal theta/alpha ratio,
  occipital relative alpha) require **eyes-closed resting EEG**;
- the four ERP features (P3b/P3a amplitude and latency) require the **three-stimulus auditory
  oddball** (Target/Novel tones).

We scanned Session-1 event markers across the shared-program datasets
(`replication_feature_availability.csv`). The result is unambiguous:

| Dataset | Paradigm | Eyes-closed rest | Auditory oddball | Locked features extractable | Post-concussive outcome |
|---|---|:--:|:--:|:--:|:--:|
| **ds003522** (discovery) | oddball + rest, mTBI | ✓ | ✓ | **8 / 8** | ✓ (NSI) |
| **ds005114** (designated replication) | **DPX** cognitive control, mTBI | ✗ | ✗ | **0 / 8** | ✓ (NSI) |
| **ds003523** (designated replication) | **visual working memory**, TBI | ✗ | ✗ | **0 / 8** | ✓ (NSI) |
| **ds003490** (paradigm match) | oddball + rest, **Parkinson's** | ✓ | ✓ | 8 / 8 | ✗ (no PCS) |

ds005114 was scanned across **all 91** Session-1 recordings: **0/91** contain an eyes-closed/
eyes-open rest marker and **0/91** contain an auditory-oddball tone; **91/91** contain DPX
cue/probe events. ds003523 shows the same pattern. (Figure: `fig_feature_availability_matrix.png`.)

**The core problem.** The shared-cohort OpenNeuro datasets were collected by running the **same
participants through different tasks**; only ds003522 paired the auditory oddball with rest. The
datasets that retain the clinical outcome (ds005114, ds003523) use incompatible paradigms, and the
one dataset that retains the paradigm (ds003490) is a Parkinson's cohort without a post-concussive
outcome. **No available dataset matches both the EEG paradigm/state and the clinical outcome of the
discovery analysis.**

---

## 2. What we deliberately did NOT do (and why)

Two "replications" were technically possible but scientifically invalid, and were **rejected on
principle**:

1. **Redefining the ERP features from DPX events** (e.g., treating the DPX probe-evoked P3 as
   "P3b"). The DPX probe P3 is a different component, evoked by a different stimulus class, under a
   different task demand. Substituting it would **modify the locked feature definition** — an
   explicit prohibition — and would not constitute replication of the oddball P3b/P3a.
2. **Computing "resting" spectra from DPX task EEG** (pre-trial baselines or the continuous
   record). Eyes-closed alpha-band features (IAF, occipital relative alpha) are strongly
   **state-dependent**; eyes-open active-task EEG is a fundamentally different state. Labeling such
   measures with the locked feature names would conflate brain states and again modify the
   preregistered definitions.

Declining these is itself the point: the discipline that makes a discovery analysis credible
(fixed definitions, no flexible substitution) is the same discipline that, honestly applied, says
**this replication cannot be run** with these data.

---

## 3. Discovery estimates and their replication status

Because no replication coefficient exists, we present the frozen discovery estimates alongside an
explicit "not estimable" replication status (`replication_effect_size_comparison.csv`;
Figure `fig_discovery_vs_replication_forest.png`). This is the effect-size comparison table the
protocol requested, populated honestly:

| Predictor | Discovery std. β (95% CI) | Discovery p (FDR) | Replication in ds005114 |
|---|---:|---:|---|
| Global aperiodic exponent | −0.02 (−0.83, 0.79) | 0.96 | **Not estimable** — no eyes-closed rest |
| Posterior IAF | −0.15 (−0.83, 0.52) | 0.96 | **Not estimable** — no eyes-closed rest |
| P3b amplitude | +0.24 (−0.40, 0.88) | 0.96 | **Not estimable** — no auditory oddball |

(The full eight-feature panel is identically not estimable; the three primary-model EEG terms are
shown for brevity.) Direction agreement, calibration transfer, and out-of-sample predictive
performance in replication are all **undefined**, because the predictors cannot be measured.

**Models requested in the protocol** (primary confirmatory, Elastic Net, resting-only, ERP-only)
were **not fit in ds005114**: each requires predictors that do not exist in that dataset. Fitting
them would require fabricated or redefined inputs and is therefore not reported.

---

## 4. The appropriate replication target (for future work)

A valid replication requires a dataset with **both** (a) the three-stimulus auditory oddball **and**
embedded eyes-closed/eyes-open rest, **and** (b) an acute-mTBI sample with a longitudinal
post-concussive symptom outcome (e.g., NSI/Rivermead). Among public data:
- **ds003490** satisfies (a) exactly (it is the same paradigm, named in the ds003522 descriptor)
  but fails (b) — it is a Parkinson's cohort. It is nonetheless suitable for a **feature-level
  pipeline check** (confirming the extraction pipeline yields physiologically plausible features in
  an independent sample), which we flag as optional future work, clearly distinct from an outcome
  replication.
- No surveyed dataset satisfies both. A prospective or retrospective mTBI cohort with the matched
  paradigm would be required.

---

## 5. Interpretation (estimation-first)

1. **The discovery null is neither supported nor refuted.** It remains the single available
   estimate, with wide intervals (§3), and is now shown to be **not yet independently testable**
   with matched data.
2. **This is a finding about the evidence base, not just this study.** Within a single
   well-organized research program, the public datasets cannot replicate one another's
   EEG-biomarker analyses because they deploy different paradigms and only one includes rest. The
   apparent availability of "three mTBI EEG datasets" overstates the replication resource: for any
   given feature panel, typically only one is usable.
3. **Implication for the discovery result.** A pre-registered, leakage-safe discovery analysis
   produced a null/inconclusive result that the field's existing public data **cannot currently
   challenge or corroborate**. Claims (positive or negative) about these EEG biomarkers should be
   held as provisional pending a matched-paradigm, adequately powered replication.

---

## 6. Limitations

- The feasibility assessment is based on **event-marker presence**; it is definitive for paradigm
  availability but does not, by itself, evaluate signal quality in ds005114 (moot, since the
  paradigms are absent).
- We did not attempt a cross-paradigm "construct" replication (e.g., DPX-evoked control ERPs vs.
  oddball ERPs); such an analysis would test a **different** hypothesis and is outside the locked
  plan.
- The conclusion is specific to the surveyed public datasets; other (non-public or future)
  mTBI oddball+rest cohorts may exist.

---

### Artifacts
`outputs/analysis/replication_feature_availability.csv`,
`outputs/analysis/replication_effect_size_comparison.csv`;
`outputs/figures/fig_discovery_vs_replication_forest.png`,
`outputs/figures/fig_feature_availability_matrix.png`.
