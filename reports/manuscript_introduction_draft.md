# Introduction (manuscript draft)
### Early Resting-State and Task-Evoked EEG Biomarkers of Persistent Post-Concussive Symptoms Following mTBI

*Draft Introduction for peer review / pre-registration supplement. No results or feature–outcome
relationships are reported. Citation placeholders are marked [REF] for completion at submission.*

---

Mild traumatic brain injury (mTBI), or concussion, is among the most common neurological injuries
worldwide, with millions of cases presenting to emergency and primary-care settings each year
[REF]. Although mTBI is, by definition, "mild" at presentation, a clinically important minority of
patients do not follow the expected recovery trajectory: weeks to months after injury they
continue to report somatic, cognitive, and affective complaints — headache, dizziness, poor
concentration, irritability, sleep disturbance — collectively termed **persistent post-concussive
symptoms** [REF]. These persistent symptoms are a leading source of mTBI-related disability,
prolonged absence from work or sport, and healthcare utilization, yet at the acute stage they are
notoriously difficult to anticipate in the individual patient [REF].

The clinical challenge is fundamentally one of **prognosis**. Decisions about follow-up intensity,
return-to-activity timing, and early intervention would benefit enormously from an accurate, early
indicator of who is at risk for a protracted course. The prognostic tools currently available,
however, are limited. Structural neuroimaging (CT and conventional MRI) is, by the diagnostic
criteria for mTBI, typically unremarkable and correlates poorly with symptom persistence [REF].
Acute clinical descriptors — Glasgow Coma Scale, loss-of-consciousness duration, post-traumatic
amnesia — capture injury severity at the macroscopic level but explain little of the variance in
downstream symptom burden, and self-report symptom inventories obtained acutely are confounded by
transient peri-injury factors and by the very outcome they aim to predict [REF]. There is a clear
need for an **objective, physiologically grounded biomarker** of the disrupted neural function
that plausibly underlies prolonged recovery.

Electroencephalography (EEG) is an attractive candidate. It is inexpensive, portable, widely
available, and directly indexes the cortical neurophysiology — oscillatory dynamics, excitation/
inhibition balance, and the timing of information processing — that diffuse axonal injury and
neurometabolic dysregulation are thought to perturb in mTBI [REF]. Two largely separate EEG
literatures bear on this. **Resting-state** studies have linked mTBI to spectral changes such as
slowing of the posterior alpha rhythm, increased theta activity and theta/alpha ratios, and, more
recently, alterations in the **aperiodic (1/f) component** of the power spectrum that is
interpreted as a marker of cortical excitation/inhibition balance and neural noise [REF].
**Task-evoked** studies, particularly using the auditory oddball paradigm, have reported reduced
amplitude and prolonged latency of the **P3 family** of event-related potentials (ERPs) — the
parietal P3b indexing target evaluation and resource allocation, and the frontocentral P3a
indexing involuntary orienting to novelty — in concussed individuals [REF].

Despite this convergent evidence, three gaps limit the prognostic translation of EEG in mTBI.
First, resting-state and ERP biomarkers have almost always been studied **in isolation**, in
separate cohorts and separate analyses, even though they index complementary facets of neural
function and could carry additive prognostic information; few studies integrate both feature
classes within a single individual and a single predictive framework. Second, much of the
literature is **cross-sectional**, relating EEG to concurrent symptom status rather than using
genuinely early (acute) EEG to predict **later** outcomes, which is the prognostically relevant
question. Third — and increasingly recognized as a threat to the credibility of biomarker work —
many predictive analyses are vulnerable to **information leakage**: feature selection, scaling, or
participant overlap that allows knowledge of the outcome or the test set to contaminate model
fitting, inflating apparent performance and producing biomarkers that fail to replicate [REF].

Here we address these gaps with a deliberately conservative, **leakage-safe longitudinal
reanalysis** of a public OpenNeuro dataset (ds003522) in which acute-mTBI participants underwent
combined resting-state and auditory-oddball EEG within days of injury and were followed with
standardized symptom inventories over the subsequent months. We pre-specify a **compact,
biologically motivated panel** that integrates both feature classes — posterior individual alpha
frequency, the global aperiodic exponent, frontal theta/alpha ratio, and occipital relative alpha
power from rest, together with P3b and P3a amplitudes and latencies from the oddball — and relate
this acute EEG panel to persistent symptom burden (Session-3 Neurobehavioral Symptom Inventory
total) measured ~4 months later. Critically, the study is engineered against leakage from the
outset: subject-level cross-validation folds were frozen **before** any EEG was processed, the
canonical subject identifier was chosen to prevent the same individual from appearing in multiple
folds (a real risk given participant overlap across the related datasets), all feature scaling and
imputation are confined to training folds, and the feature files were verified to contain no
outcome information before any model was specified. The analysis plan favors **simple, explainable
statistical models** over algorithmic complexity, treats machine-learning methods as explicitly
exploratory, and was registered before any feature–outcome relationship was examined.

Our aim is not to deliver a finished clinical predictor — the discovery cohort is modest, and we
treat the work as hypothesis-generating, with two further datasets reserved for independent
replication. Rather, our contribution is to ask, with methodological rigor that the field has
often lacked, whether **early resting-state and task-evoked EEG features, considered together,
carry interpretable prognostic signal for persistent post-concussive symptoms**, and to provide a
fully pre-registered, reproducible, leakage-safe framework in which that question can be answered
and replicated.
