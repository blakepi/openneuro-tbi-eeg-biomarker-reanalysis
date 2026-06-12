# Discussion (manuscript draft)
### Early Resting-State and Task-Evoked EEG Biomarkers of Persistent Post-Concussive Symptoms Following mTBI

*Draft Discussion for peer review. Estimation-first; no causal claims; exploratory analyses are
not promoted. Citation placeholders marked [REF].*

---

In a pre-registered, leakage-safe longitudinal reanalysis of a public acute-mTBI cohort, a compact
panel of early resting-state and task-evoked EEG features was **not reliably associated with, and
did not predict out-of-sample, persistent post-concussive symptom burden at approximately four
months**. Standardized associations were small with confidence intervals spanning zero, coefficient
estimates were unstable to the removal of single participants, and every cross-validated model —
linear, penalized, and flexible — performed at or below a demographic baseline, with the penalized
full-panel model retaining no feature. We then asked whether these findings replicate in an
independent dataset and found that, with currently available public data, **the question cannot yet
be answered**: the designated replication cohorts do not contain the paradigms required to measure
the locked features. Below we interpret what these two results mean, separately and together.

## What replicated, and what could not be tested

In the strict sense the protocol intended — re-estimating the locked feature panel against the same
outcome in an independent sample — **nothing could be replicated, because nothing could be
measured.** The discovery features derive from an eyes-closed/eyes-open resting recording and a
three-stimulus auditory oddball. The two datasets reserved for replication (ds005114, a DPX
cognitive-control task; ds003523, a visual working-memory task) contain neither resting blocks nor
an auditory oddball, so none of the eight predictors is extractable with its preregistered
definition. The one public dataset that does share the paradigm (ds003490) is a Parkinson's-disease
cohort without a post-concussive outcome. Consequently the discovery null is **neither corroborated
nor refuted**; it stands as a single, wide-interval estimate that the existing public evidence base
cannot currently challenge.

We regard the decision **not** to force a replication as a result in its own right. It would have
been straightforward to relabel the DPX probe-evoked P3 as "P3b," or to compute "resting" spectra
from task EEG, and to report nominal replication coefficients. Both moves would have modified the
locked feature definitions — substituting a different ERP component evoked by a different stimulus
class, or conflating an eyes-closed state with an eyes-open active-task state — and would have
manufactured precisely the analytic flexibility that pre-registration exists to prevent. Declining
them keeps the inferential meaning of "replication" intact.

## Relation to prior EEG biomarker literature

Our discovery result sits against a backdrop of generally more optimistic reports linking mTBI to
resting alpha slowing, elevated theta/alpha ratios, altered aperiodic (1/f) activity, and reduced
or delayed P3 responses [REF]. Several features of the present study may explain the divergence.
First, much prior work is cross-sectional, relating EEG to **concurrent** symptom status, whereas
we used genuinely early EEG to predict a **later** outcome — a harder and more prognostically
relevant target. Second, the resting-state and ERP literatures have largely developed in
**separation**; integrating both feature classes for the same individuals, as here, removes the
opportunity to report whichever modality happens to look strongest. Third, and most importantly,
our analysis was **leakage-safe and pre-registered**: subject-level folds were frozen before
feature extraction, all scaling and selection were confined to training folds, and the feature
panel and statistical hierarchy were fixed before any feature–outcome relationship was examined.
Analytic pipelines without these safeguards can yield optimistic performance that does not
generalize [REF]. That a rigorously specified pipeline did not recover a large effect should
temper confidence in small, flexibly analysed positive reports.

We emphasize, in keeping with an estimation-first stance, that our result is **inconclusive rather
than a demonstration of absence**. With roughly 20 participants, confidence intervals reached
±0.8 standard deviations, and the data are simply uninformative about modest true associations. The
leave-one-out instability of every coefficient is the clearest internal signal that the cohort is
too small to estimate even a three-biomarker model dependably. None of this licenses the conclusion
that early EEG carries no prognostic information for post-concussive recovery; it licenses only the
conclusion that **this dataset cannot establish such information**, in either direction.

## Implications for EEG biomarker research

Two implications follow. The first concerns **paradigm fragmentation**. The existence of "three
mTBI EEG datasets" overstates the replication resource: because the same participants were run
through different tasks and only one session included rest, any specific feature panel is typically
measurable in only one dataset. Replication of EEG-biomarker findings therefore requires not just
another sample but a **paradigm- and state-matched** sample — a constraint that is easy to overlook
when datasets are described by population rather than by acquisition protocol. Biomarker programs
intending downstream replication should standardize the acquisition (including a dedicated resting
run) across cohorts from the outset.

The second concerns the **state-specificity of "resting" features**. Aperiodic and alpha-band
measures are routinely treated as portable traits, yet they depend materially on recording state;
an eyes-closed feature cannot be recovered from eyes-open task EEG without changing what is being
measured. Reports that compute "resting" spectral features from heterogeneous or task-embedded
segments should make the state explicit, because it is not interchangeable across studies.

## Implications for small-sample prediction studies

Our experience reinforces several now-familiar but still-underapplied lessons for prognostic
modeling in small neurophysiology samples [REF]. In-sample fit was actively misleading: the
resting-only model's R² of 0.31 collapsed to a negative out-of-fold R², and the unpenalized
full model overfit catastrophically (out-of-fold R² ≈ −3.6) — a vivid illustration of why
performance must be estimated out of fold and why an unpenalized model at this dimensionality is
uninterpretable. Penalization that shrank all coefficients to zero was not a failure of the method
but an honest verdict that, given the data, the mean is the best available predictor. And the
single most informative diagnostic was not any p-value but the **coefficient instability under
leave-one-out**, which exposed how little the point estimates could be trusted. We would encourage
small-sample biomarker studies to pre-register, to report effect sizes with intervals rather than
dichotomized significance, to estimate performance strictly out of fold against a covariate
baseline, and to treat replication feasibility — not merely replication results — as a design
question answered before data are promised.

## Limitations

The dominant limitation is **sample size**: with about 20–25 acute-mTBI participants carried to the
four-month outcome, the discovery study is powered only for large effects and yields unstable
estimates. The cohort is single-site and single-device; outcomes are self-report symptom
inventories subject to their own measurement error; resting EEG was extracted from blocks embedded
within the task recording rather than a standalone run; and attrition from the acute to the chronic
assessment may select on recovery, which the complete-case analysis does not model. The replication
assessment establishes paradigm availability but, by construction, cannot evaluate an outcome
association that the data cannot support. Finally, our conclusions concern the surveyed public
datasets; other mTBI cohorts with matched acquisition may exist and would be the natural venue for
the replication this study could not perform.

## Conclusion

Early resting-state and task-evoked EEG features, analysed together within a pre-registered,
leakage-safe longitudinal framework, did not reliably predict persistent post-concussive symptom
burden in this small acute-mTBI discovery cohort, and the result could not be tested in independent
public data because no available dataset matches both the EEG paradigm and the clinical outcome. We
interpret these findings as inconclusive rather than negative, and as a caution: credible EEG
prognostic biomarkers for mTBI will require larger, pre-registered, paradigm-matched, and
replication-ready cohorts. The value of the present work lies less in any single estimate than in
demonstrating an analysis pipeline rigorous enough that its null is informative and its replication
requirements are explicit.
