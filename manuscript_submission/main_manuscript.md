# Leakage-Safe EEG Biomarker Analysis After Mild Traumatic Brain Injury: An Internally Locked OpenNeuro Reanalysis and Replication Feasibility Study

**Running title:** Leakage-safe EEG biomarkers after mTBI

**Author:** Gregory Blake Pierpoint

**Affiliation:** Macon and Joan Brock Virginia Health Sciences, Eastern Virginia Medical School at
Old Dominion University, Norfolk, Virginia, USA

**Correspondence:** pierpogb@odu.edu · ORCID 0000-0001-8288-8549

---

## Abstract

**Background.** Persistent post-concussive symptoms affect a clinically important minority after mild traumatic brain injury (mTBI), but early prognostication remains difficult. Resting-state and task-evoked EEG have been proposed as prognostic biomarkers, often in leakage-prone small samples.

**Objective.** To estimate whether early EEG features were associated with later Session-3 NSI symptom burden after sub-acute/early post-injury mTBI in a preregistered, leakage-safe OpenNeuro reanalysis, and whether related public datasets permit feature-identical replication.

**Methods.** We reanalysed OpenNeuro ds003522, a sub-acute/early post-injury mTBI dataset with auditory oddball EEG and embedded eyes-closed/eyes-open rest. Subjects were keyed by stable identifier; cross-validation folds and the statistical hierarchy were locked before outcome modeling. The feature panel included posterior alpha frequency, global aperiodic exponent, theta/alpha ratio, relative alpha, and P3b/P3a amplitude and latency. The primary outcome was continuous Session-3 Neurobehavioral Symptom Inventory (NSI) total.

**Results.** In the primary model (n = 21), no predictor's 95% CI excluded zero. The largest standardized primary association was P3b amplitude (beta = 0.24, 95% CI -0.40 to 0.88; adjusted R2 = -0.19). Elastic Net retained no feature. A prespecified secondary Rivermead-change P3b association (n = 19; beta = 0.66, FDR p = 0.035) was hypothesis-generating and did not alter the primary NSI conclusion. Sensitivities did not alter the primary interpretation. Feature-identical clinical replication was not estimable in related public datasets.

**Conclusions.** No stable primary EEG predictive signal was recoverable from the locked features in these data. Findings remain inconclusive and underpowered; larger, paradigm-matched validation cohorts are needed.

**Keywords:** mild traumatic brain injury; electroencephalography; post-concussive symptoms; event-related potentials; reproducibility; data leakage; OpenNeuro

---

## 1. Introduction

Mild traumatic brain injury (mTBI), or concussion, is among the most common neurological
presentations worldwide [1]. Although most patients
recover within weeks, a clinically important minority develop **persistent post-concussive
symptoms** — headache, dizziness, cognitive difficulty, irritability, and sleep disturbance that
endure for months — and these account for a large share of mTBI-related disability and healthcare
use [2,3]. Identifying, at the acute
stage, which patients are at risk for a protracted course would inform follow-up intensity,
return-to-activity decisions, and early intervention.

Current prognostic tools are limited. Conventional CT and MRI are, by the diagnostic criteria for
mTBI, typically unremarkable and correlate poorly with symptom persistence [2], and acute clinical
descriptors (Glasgow Coma Scale, loss-of-consciousness duration) explain little outcome variance
[2]. This motivates the search for objective indicators associated with prolonged recovery.

Electroencephalography (EEG) is an attractive candidate: it is inexpensive, portable, and provides temporally precise measures of cortical population dynamics, information-processing timing, and spectral structure that have been proposed to relate to excitation/inhibition-linked physiology [4]. Two largely separate
literatures bear on mTBI. **Resting-state** studies report alpha-rhythm slowing, increased theta
and theta/alpha ratios, and — more recently — alterations in the **aperiodic (1/f)** component of
the spectrum proposed to reflect excitation/inhibition-linked spectral structure and neural noise [5,6,7].
**Task-evoked** studies, especially with the auditory oddball, report reduced amplitude and
prolonged latency of the **P3 family** of event-related potentials (ERPs), with the parietal P3b
indexing target evaluation and the frontocentral P3a indexing novelty orienting [8].

Despite this convergent evidence, the small-sample EEG biomarker literature carries well-documented
risks: **analytic flexibility** (many defensible feature, region, and model choices), **subject
leakage** (the same individuals, or test-set information, influencing model fitting), **insufficient
external validation**, and **overfit machine learning** that does not generalize [9,10,11]. Public,
standardized datasets (e.g., OpenNeuro/BIDS) offer a path toward more reproducible biomarker
research [12,13,14], but it remains unclear
whether a leakage-safe, preregistered EEG feature panel produces stable symptom-prediction signal
in such data, and whether related public datasets can actually support feature-identical
replication.

We therefore conducted a preregistered, leakage-safe longitudinal reanalysis of OpenNeuro ds003522,
in which sub-acute/early post-injury mTBI participants underwent combined resting and auditory-oddball EEG within days of
injury and were followed with standardized symptom inventories. We (i) prespecified a compact
biologically motivated feature panel integrating resting-state and ERP measures; (ii) froze
subject-level cross-validation folds and locked the statistical hierarchy before any feature–outcome
relationship was examined; and (iii) assessed whether the analysis could be replicated, with
identical feature definitions, in the related OpenNeuro datasets. Our objective was not to announce
a biomarker discovery but to test, rigorously, whether stable evidence is detectable here and
whether the question is even answerable with the available public data.

---

## 2. Methods

### 2.1 Study design
This is a retrospective reanalysis of public, deidentified OpenNeuro EEG data. An internal, version-controlled analysis plan - covering the cohort, feature definitions, statistical hierarchy, leakage rules, and missing-data strategy - was locked before outcome modeling and before any feature-outcome relationship was examined (Supplement: *Final Locked Analysis Plan*). Throughout, "preregistered" refers to this internal, version-controlled pre-outcome-modeling lock. The framework is **estimation-first**: interpretation is anchored to effect sizes and confidence intervals rather than dichotomized significance, and **no causal claims** are made. The locked analysis plan is included in the Supplement and in the version-controlled code repository (§Code availability), where its pre-modeling timestamp is recorded in the commit history.

### 2.2 Datasets
We used four OpenNeuro datasets from a single longitudinal research program (University of New
Mexico; J.F. Cavanagh and colleagues; data collected 2016–2018):

- **ds003522 (discovery)** [15]. Three-stimulus auditory oddball with **embedded eyes-closed/eyes-open
  resting blocks**; sub-acute/early post-injury mTBI, controls, and a chronic-TBI arm; three sessions; longitudinal
  clinical outcomes for the sub-acute/early post-injury mTBI/control cohort. DOI 10.18112/openneuro.ds003522.v1.1.0.
- **ds005114 (designated replication)** [16]. DPX (dot-pattern expectancy) cognitive-control task;
  sub-acute/early post-injury mTBI/control; assessed for replication feasibility.
- **ds003523 (designated replication)** [17]. Visual working-memory task; acute/sub-acute TBI/control; assessed
  for feature availability.
- **ds003490 (paradigm reference)** [18]. Same three-stimulus oddball + rest paradigm but a
  **Parkinson's** cohort; feature-extraction-compatible yet outcome/population-incompatible.

All datasets used 500-Hz BrainVision EEG stored as EEGLAB .set/.fdt (BIDS-EEG).

### 2.3 Participants and identity resolution
The same individuals recur across these datasets under different BIDS labels; the stable unique key
is the scan-generated **URSI** (here subject_uid). Public BIDS labels are dataset-local identifiers
and should not be treated as cross-dataset identities without a stable participant key. We did **not** assume BIDS sub-0XX labels
were stable across datasets, and we did not use the recording id (Original_ID) as the identity key
because one value (3013) maps to two distinct URSIs (M87138342 vs M87138432, an apparent
transposition; Supplement). All merging and cross-validation splitting used subject_uid. The
**chronic-TBI arm was excluded** from the Session-3 NSI prediction cohort because it has no longitudinal
clinical outcome; clinical-only subjects without EEG were documented rather than silently dropped
(Supplement). The source README describes the longitudinal group as sub-acute mTBI at Session 1, whereas the dataset title uses acute TBI. In local clinical metadata, the 44 ds003522 Group-0 participants with Session-1 EEG spanned 1-16 days since injury (median 11; the README describes 3-14 days). We therefore use sub-acute/early post-injury mTBI for the discovery cohort. The cohort comprised Group-0 participants with a usable Session-1 EEG and a non-missing Session-3 outcome (**n = 25**). Effective analytic samples were 25 (resting-only models), 21 (ERP and primary combined models; see §2.7), and 20 in the prespecified eyes-open-low sensitivity excluding sub-068. The locked plan's combined-panel N = 20 is retained as a transparent execution-note discrepancy: sub-068 had valid eyes-closed rest and reliable ERP features and was therefore retained in the primary n = 21 analysis.

### 2.4 Clinical outcomes
The **primary outcome** was the **Session-3 Neurobehavioral Symptom Inventory (NSI) total** [19], computed as the sum of somatic, cognitive, and emotional subscales; no precomputed total exists in the source. Outcomes were obtained from the cohort's aggregated clinical workbook, joined to EEG by URSI, and string missing-tokens ("na", "NR", "m") were mapped to missing. Prespecified secondary outcomes, reported as context, were the Session-3 Rivermead Post-Concussion Symptoms Questionnaire total [20], S1-to-S3 NSI change, and S1-to-S3 Rivermead change; change scores were defined as Session 3 minus Session 1, so positive values indicate higher/worse symptom burden at Session 3 relative to Session 1. The NSI total was right-skewed but below the prespecified transformation threshold (skewness = 0.85 < 1.0) and was therefore analysed on the **raw scale** (n = 25: mean 15.1, SD 15.7, median 9, range 0-51). No binary "persistent symptoms" endpoint was defined because the source documentation contains no established threshold. Attrition was substantial (44 Group-0 participants with Session-1 EEG, 25 with Session-3 NSI) and was evaluated with the prespecified completer/non-completer comparison.

### 2.5 EEG acquisition and task structure (ds003522)
Continuous EEG was recorded at **500 Hz** from **63 scalp electrodes** (international 10–10 system)
plus vertical EOG (VEOG) and ECG (EKG) channels (65 channels total), with an online reference at
**CPz** and a 60-Hz power line (BrainVision actiCHamp). Each Session-1 recording (~15–28 min)
contained, in order, an eyes-closed block, an eyes-open block, an oddball run, and a second cycle of
eyes-closed/eyes-open rest and oddball (Figure 2); resting and task segments were demarcated by event
markers, yielding ~120 s each of eyes-closed and eyes-open rest and, per recording, 184 standard, 38
target, and 38 novel tones. A single EEGLAB boundary event occurred at recording onset in every
file; no internal discontinuities were detected. One participant (sub-040) lacked curated tone labels (tones
stored only as raw stimulus codes) and was excluded from ERP analyses without inferring the
non-standard mapping.

### 2.6 EEG preprocessing
Preprocessing used MNE-Python (v1.12) [21], with dataset handling supported by MNE-BIDS [22], using a
single fixed parameter set applied identically to all participants, chosen **without reference to any
outcome**; raw files
were never modified (Figure 3). The pipeline was **boundary-aware**: the recording-onset boundary event was converted
to a BAD_boundary annotation and the FIR filter was constrained not to span annotated discontinuities. For
each recording we (i) typed VEOG/EKG as non-EEG (excluded from referencing, montage, and features);
(ii) applied a 60-Hz notch; (iii) band-pass filtered 0.5–45 Hz; (iv) reinstated the online reference
CPz, assigned a standard 10–20 montage, and re-referenced to the average of the 64 EEG channels; and
(v) performed within-participant bad-channel detection (robust z-score of log-variance > 4, or flat
channels), interpolating flagged channels by spherical splines (the reinstated reference was exempt). Bad-channel
detection was performed after average rereferencing. For ERPs an additional 40-Hz low-pass was applied before epoching. **Quality control:** all 25
recordings were readable with uniform sampling rate and channel structure, no flat/NaN/zero-filled or
dataset-marked bad channels, and 0–3 (predominantly frontal-ocular) channels interpolated per
participant; no QC failure threatened feasibility.

### 2.7 Feature extraction
**Resting-state** analyses used the **eyes-closed** condition as primary (eyes-open as a sensitivity
condition). Eyes-closed/eyes-open blocks were segmented from their marker trains, screened for
discontinuities, divided into non-overlapping 2-s segments, and segments exceeding 150 µV
peak-to-peak rejected. Because rest blocks were embedded within a task recording, transition-related
carryover, fatigue, and vigilance effects cannot be fully excluded and are treated as limitations. Power spectral density (Welch, 2-s windows, 50% overlap, 1–45 Hz) was averaged
within frontal/central/parietal/occipital and global regions. We derived the **posterior individual
alpha frequency** (7–13 Hz peak of the parietal–occipital spectrum; this canonical adult alpha window would not capture pathological slowing below 7 Hz) [7], the **global aperiodic
exponent** (specparam v2.0.0; fixed aperiodic mode; 1–40 Hz fit; peak width limits 1–8 Hz; maximum six peaks; minimum peak height 0.0; peak threshold 2.0) [6], the **frontal theta/alpha ratio**,
**occipital relative alpha power**, and (exploratory) spectral entropy.
Eyes-closed features were usable for all 25 participants. **ERP** analyses epoched −200–800 ms around
tones, baseline-corrected (−200–0 ms), rejected boundary-overlapping and >150 µV epochs, and
quantified the **P3b** (target, parietal Pz/CPz/POz, 300–600 ms) and **P3a** (novel, frontocentral
Fz/FCz/Cz, 250–400 ms), reporting **mean-window amplitude (primary)**, peak amplitude (sensitivity),
and peak latency. ERP components required ≥ 15 retained rare-tone epochs; with this criterion and the
sub-040 exclusion, ERP features were usable for 21 participants. ERP complete-case filtering may be
informative if artifact burden, fatigue, symptoms, sleep, medication, or age are related to retained rare-tone epochs.

### 2.8 Statistical analysis
The analysis hierarchy was **locked before outcome modeling** (Supplement). Because the full
specification (8 EEG features + age + sex) exceeds the events-per-variable supportable at n ≈ 20–25,
the primary confirmatory model was a **parsimonious linear regression** carrying one biomarker per
domain:

Primary model: S3_NSI_Total ~ Global_Aperiodic_Exponent + Posterior_IAF + P3b_Amplitude + Age + Sex.

The **secondary confirmatory** model was an **Elastic Net** [23] over the full locked panel +
covariates; the full unpenalized 10-term OLS was reported **for transparency only** (descriptive,
potentially overfit); ridge, LASSO, random forest, and gradient boosting (XGBoost) were
**exploratory**. All scaling, imputation, and hyperparameter tuning were fit **within training folds
only**, using subject-level folds frozen before feature extraction. Consistent with an
estimation-first stance and prediction-model reporting guidance [24,25], we emphasize standardized β
coefficients, 95% confidence intervals, and effect sizes over dichotomized significance; we also
report p-values (Benjamini–Hochberg FDR within the predictor family), adjusted R²,
leave-one-subject-out coefficient stability, and residual/influence diagnostics. Out-of-fold R² and MAE were retained as leakage-safety transparency metrics rather than stable model-ranking estimates; at n = 21, fold-level test sets are very small, and even the age+sex baseline had negative out-of-fold R². Prespecified secondary outcomes, the prespecified sensitivity battery, and the descriptive attrition check were completed or explicitly documented in a prespecification-fidelity audit. No exploratory model was elevated to confirmatory status. Analyses used Python 3.14 with MNE 1.12, specparam 2.0, scikit-learn 1.9 [26], statsmodels 0.14, numpy, and pandas, with fixed seeds; code and frozen folds are released (§Code availability).

### 2.9 Replication feasibility
Because the locked features derive from eyes-closed rest and the auditory oddball, we determined
whether those paradigms exist in the designated replication datasets by scanning Session-1 event
markers. ds005114 was scanned across **all 91** Session-1 recordings; ds003523 and ds003490 were
scanned by sample. A feature was deemed extractable with its preregistered definition only if its
source paradigm was present. We did **not** substitute features across paradigms (e.g., relabeling a
DPX probe-evoked P3 as "P3b," or computing "rest" from task EEG), as such substitution would modify
the locked definitions and conflate brain states.

---

## 3. Results

### 3.1 Cohort construction and feature feasibility
From the sub-acute/early post-injury mTBI arm of ds003522, 25 participants had a usable Session-1 EEG and a Session-3 NSI
total (Figure 1; Table 2). All 25 recordings passed read QC with uniform acquisition (Section 2.6).
Locked usability criteria yielded 25 participants for resting-only models and 21 for ERP and combined
models (four ERP exclusions: one lacking curated tone labels, three with fewer than 15 retained
rare-tone epochs). Extracted features were physiologically plausible (e.g., posterior individual
alpha frequency clustered near 10 Hz; aperiodic fits R² ≈ 0.99) (Supplement Table S1).

### 3.2 Primary confirmatory analysis
The parsimonious model (n = 21; approximately 15 residual degrees of freedom) showed weak in-sample fit and poor expected explanatory value (R² = 0.11, adjusted
R² = −0.19, omnibus F p = 0.86). **No predictor's 95% confidence interval excluded zero** (Table 4;
Figure 4). The largest standardized association was P3b amplitude (β = 0.24, 95% CI −0.40 to 0.88,
p = 0.43), followed by posterior individual alpha frequency (β = −0.15, 95% CI −0.83 to 0.52) and the
global aperiodic exponent (β = −0.02, 95% CI −0.83 to 0.79); age and sex were likewise uninformative.
After FDR correction all p-values were 0.96, and heteroscedasticity-consistent inference was
materially identical (p = 0.64–0.97). Distributional diagnostics did not strongly reject normality or homoscedasticity (Shapiro–Wilk p = 0.09;
Breusch–Pagan p = 0.50; Durbin–Watson = 1.86), but influence diagnostics were concerning at this sample size:
three of 21 participants exceeded Cook's D > 4/n, including one externally studentized residual of 3.6.
No participant was excluded post hoc solely on the basis of influence diagnostics; the outlier is retained as
part of the target cohort, and its influence reinforces the instability of n = 21 modeling. In leave-one-subject-out
refitting, **no predictor retained a stable sign**, indicating the cohort is too small to estimate even this five-term
model dependably.

### 3.3 Secondary confirmatory analysis (Elastic Net)
The Elastic Net selected a penalty (α = 43.2, mixing parameter = 0.10) that **shrank all ten
coefficients to zero**; the retained model was the intercept (14.6, the cohort mean). Out-of-fold
performance was at or below a mean predictor (R² = −0.06, 95% CI −0.50 to −0.02; MAE = 13.3 NSI
points), with predictions compressed to a near-constant line across the full observed range (Figure
5). A negative out-of-fold R² indicates that held-out predictions were worse than a mean-prediction
benchmark; here, penalization selected the mean because the locked features did not provide stable
fold-generalizing corrections.

### 3.4 Supportive and transparency analyses
Domain-specific models reproduced this pattern (Table 4; Supplement Table S5). The resting-only model
(n = 25) had the largest in-sample fit (R² = 0.31) but a near-zero adjusted R² (0.08), a
non-significant omnibus test (p = 0.29), and negative out-of-fold R² (−0.59); the ERP-only model
(n = 21) was similarly uninformative (adjusted R² = −0.12; out-of-fold R² = −1.13). The full 10-term
OLS, reported for transparency only, illustrated overfitting at this sample size (in-sample R² = 0.39
but adjusted R² = −0.22; design condition number ≈ 22,000; out-of-fold R² = −3.58); it is descriptive
and not used for inference.

### 3.5 Prespecified secondary outcomes, sensitivities, and attrition checks
A prespecification-fidelity audit completed the internally locked H2-H4 secondary outcomes and prespecified sensitivity battery without changing frozen folds or locked feature definitions (Supplement Tables S7-S11). For S3 Rivermead total (n = 19) and S1-to-S3 NSI change (n = 21), the parsimonious secondary models did not yield coefficient intervals excluding zero and out-of-fold R² remained negative. For S1-to-S3 Rivermead change, defined as Session 3 minus Session 1 total so that positive values indicate higher/worse symptom burden at Session 3, P3b amplitude showed a prespecified secondary association (standardized beta = 0.66, 95% CI 0.21 to 1.11, FDR p = 0.035; adjusted R² = 0.45; out-of-fold R² = 0.25), but estimates were unstable with wide confidence intervals and were not externally replicated. This result is therefore treated as secondary and hypothesis-generating, and it does not alter the primary conclusion based on Session-3 NSI burden. Sensitivity analyses (HC3 inference, peak-amplitude ERP metrics, eyes-open resting analogues, predictor-only MICE, low-trial ERP inclusion, added injury covariates, Session-2 outcome timing, and log1p outcome scale) did not identify a stable primary NSI association absent from the primary analysis. The internally locked 0.1-Hz high-pass branch and sub-040 S-code ERP recovery were documented as unexecuted because no frozen 0.1-Hz feature branch or operationalized sub-040 event mapping existed. Descriptive attrition comparison included 25 S3 completers and 19 non-completers; no IPW model was added because the locked plan did not define a numeric imbalance trigger.

### 3.6 Exploratory analyses
Exploratory penalized (ridge, LASSO) and flexible (random forest, gradient boosting) learners all
produced negative out-of-fold R² (−0.06 to −0.36; Table 4; Supplement Table S5); the least-poor
models were those regularizing most strongly toward the mean, and flexible learners recovered no
non-linear structure. Adding spectral entropy did not change any result. No exploratory model was elevated to confirmatory status, and these exploratory negative results are not used as
independent proof of no effect.

### 3.7 Replication feasibility
Across **all 91** Session-1 recordings of ds005114, **0 contained an eyes-closed/eyes-open rest marker
and 0 contained an auditory-oddball tone; 91/91 contained DPX cue/probe events** (Table 5; Figure 6).
Consequently **none of the eight locked features was extractable with its preregistered definition**.
ds003523 (visual working memory) showed the same absence. The one paradigm-matched dataset, ds003490,
permits extraction of all eight features but is a **Parkinson's cohort without a post-concussive
outcome**. **No available dataset matched both the EEG paradigm/state and the clinical outcome**, so
a feature-identical clinical replication model was not estimable without changing the locked estimand; discovery estimates are shown with explicit
"not estimable" replication status in Figure 7. Because datasets derive from a related longitudinal program,
any paradigm-compatible reuse would still require subject-identity checks to distinguish independent replication
from within-program validation. We did not estimate a nominal replication model because doing so would have required redefining the locked features or changing the clinical estimand.

---

## 4. Discussion

In a preregistered, leakage-safe longitudinal reanalysis, a compact panel of early resting-state and
task-evoked EEG features did not provide **stable primary evidence** for predicting later Session-3 NSI symptom burden
after sub-acute/early post-injury mTBI. Standardized associations were small with intervals spanning zero, coefficients were
unstable to single observations, cross-validated performance was unstable and negative,
and the penalized full-panel model retained no feature for the primary NSI outcome. A planned replication in related public datasets
was **infeasible** because they did not share both the EEG paradigm/state and clinical outcome structure
required to reproduce the locked feature definitions.

**Interpretation of the null.** This is **not** evidence that EEG is irrelevant to post-concussive
recovery. With ~20 participants, confidence intervals reached ±0.8 SD and the data are uninformative
about modest true associations; the leave-one-out instability of every coefficient shows the cohort
is too small to estimate even a three-biomarker model dependably. The result is best described as
**inconclusive and underpowered**, indicating that the tested feature panel in this small public
cohort did not recover stable held-out performance under leakage-safe resampling.

**Secondary-outcome context.** The fidelity audit completed the prespecified secondary outcomes. Prespecified secondary Rivermead-change analyses showed a P3b association for change defined as Session 3 minus Session 1, but estimates were unstable with wide confidence intervals and were not externally replicated. This result is therefore treated as secondary and hypothesis-generating, and it does not alter the primary conclusion based on Session-3 NSI burden.

**Why the Elastic Net result matters.** A penalized model free to weight any subset of the primary NSI panel collapsed to the **intercept-only (mean) predictor**, providing no evidence for a recoverable multivariable signal under the locked feature set and resampling scheme. The cross-validation results should not be interpreted as a precise ranking of models. Rather, they show that under a leakage-safe resampling scheme no model recovered stable held-out performance in this cohort.

**Leakage prevention and the prior literature.** Our discovery result is more conservative than much
of the resting-EEG and P3 mTBI literature [5,8]. Several design features may explain this: a
prospective (early-EEG → later-outcome) rather than cross-sectional target; integration of resting
and ERP features for the same individuals, removing the freedom to report whichever modality looks
strongest; and a leakage-safe, preregistered pipeline in which folds were frozen before feature
extraction and the model hierarchy fixed before any feature–outcome look. Pipelines without such
safeguards can yield optimistic performance that does not generalize [9,10,11]. That a rigorously
specified
pipeline did not recover a large effect should temper confidence in small, flexibly analysed positive
reports.

**Replication infeasibility and the public-data lesson.** The existence of "three mTBI EEG datasets"
overstates the replication resource: because the same participants were run through **different
tasks** and only one session included rest, any specific feature panel is typically measurable in
only one dataset. Replication therefore requires not merely another sample but a **paradigm- and
state-matched** sample — a constraint easy to overlook when datasets are described by population
rather than acquisition protocol. Dataset availability does not guarantee hypothesis-level
reproducibility.

**Clinical practice and research implications.** These findings do not support using the tested EEG features as patient-level prognostic markers for post-concussive symptom burden. More broadly, they caution against translating small-sample EEG biomarker associations into clinical risk stratification without leakage-safe validation in paradigm-matched cohorts. For clinical neurophysiology researchers, the practical lesson is that public dataset availability is not equivalent to replication readiness: task paradigm, resting state, outcome timing, and subject identity structure must all match the locked estimand.

**Why we did not redefine features.** Relabeling the DPX probe-evoked P3 as "P3b," or computing
"resting" spectra from eyes-open task EEG, would have changed the locked feature definitions by
substituting a different ERP component evoked by a different stimulus, or by conflating eyes-closed
rest with eyes-open active task states. We did not estimate a nominal replication model because doing
so would have required redefining the locked features or changing the clinical estimand.

**Strengths.** Use of public data; transparent, released code and frozen folds; explicit identity
resolution (URSI, with the 3013 collision handled); a locked model hierarchy and prespecified
features; boundary-aware preprocessing; null results reported with effect sizes, confidence intervals, influence diagnostics, and out-of-fold performance; and a
formal replication-feasibility audit.

---

## 5. Limitations

The dominant limitation is **sample size**: ~20-25 sub-acute/early post-injury mTBI participants with Session-3 NSI outcomes powered the study only for large effects and yielded unstable estimates; confidence intervals remain compatible with modest associations. Additional limitations include informative **attrition** from Session 1 to Session 3 (descriptive completer/non-completer comparison was completed, but IPW was not added because the locked plan did not operationalize a trigger); reliance on a **single discovery dataset** for the locked feature panel; the **absence of a true external replication dataset**; **ERP reliability exclusions** that may be informative if artifact burden, fatigue, symptoms, sleep, medication, or age are related to retained rare-tone epochs; a small-sample prespecified secondary Rivermead-change association treated as hypothesis-generating; **public-dataset metadata constraints**; a single site and device; self-report symptom outcomes; resting EEG extracted from blocks embedded within continuous task recordings rather than standalone rest runs; no ICA/SSP/EOG-regression ocular correction, leaving frontal spectral measures, especially theta/alpha ratio, sensitive to ocular, muscle, and vigilance-related artifacts; bad-channel detection after average rereferencing, although 19/25 participants had no interpolated channels and 6/25 had 1-3 interpolated channels; a locked posterior IAF window that would not capture pathological slowing below 7 Hz; exported specparam fit R2 values as low as 0.735 without outcome-informed exclusion; and the **absence of causal inference** by design.

---

## 6. Conclusions

In this leakage-safe OpenNeuro reanalysis, a biologically motivated resting-state and ERP EEG feature
panel did not show stable evidence of predicting later Session-3 NSI symptom burden after
sub-acute/early post-injury mTBI. Planned public-dataset replication was infeasible because related datasets did not share both
the EEG paradigm/state and the clinical-outcome structure needed for feature-identical validation. We
interpret these findings as inconclusive and underpowered rather than as proof that no EEG biomarker signal exists in mTBI. Future
EEG biomarker studies in mTBI require larger, longitudinal, paradigm-matched cohorts with harmonized
symptom outcomes and prespecified, leakage-safe analytic plans; the present study contributes a
transparent, reproducible template and an explicit account of what such validation will demand.

---

## 7. Data availability
This study used publicly available OpenNeuro datasets. Raw EEG and metadata are available from
OpenNeuro at ds003522 (doi:10.18112/openneuro.ds003522.v1.1.0) [15], ds005114
(doi:10.18112/openneuro.ds005114.v1.0.0) [16], ds003523 (doi:10.18112/openneuro.ds003523.v1.1.0)
[17], and ds003490 (doi:10.18112/openneuro.ds003490.v1.1.0) [18]. No new human data were collected.
Raw EEG data are not redistributed in the code repository. Derived analysis tables (cohort
crosswalk, feature matrices, model outputs) are provided in the Supplement and the repository.

## 8. Code availability
Analysis code and derived manuscript materials (download, identity resolution, preprocessing,
feature extraction, frozen cross-validation folds, models, figures, and manuscript-supporting
materials) are available in the public GitHub repository: https://github.com/blakepi/openneuro-tbi-eeg-biomarker-reanalysis. The final reviewer-facing GitHub release `v1.0.1-cnp-submission-final` is archived on Zenodo at https://doi.org/10.5281/zenodo.20682573 (DOI: 10.5281/zenodo.20682573). Raw EEG data are publicly available from OpenNeuro and are not redistributed in the code repository. The repository is released under the MIT License; the locked analysis plan and machine-readable bibliography files are included.
A post-analysis reproducibility audit regenerated the frozen analysis outputs into
`outputs/reanalysis_audit_20260612_115010/` without overwriting the original outputs; all 25
analytic ds003522 Session-1 `.set/.fdt` pairs were verified as data-readable with MNE, all 44
prespecified numeric checks matched the frozen outputs, and the only non-exact artifact was a
non-scientific `--dry-run` download-manifest difference. This audit establishes internal
computational reproducibility under the available local environment; it should not be
interpreted as independent external validation or independent code review.
Environment: Python 3.14; MNE 1.12; MNE-BIDS; specparam 2.0; scikit-learn 1.9; statsmodels
0.14; xgboost 3.2.

## 9. Ethics statement
This study used publicly available, deidentified data from OpenNeuro and did not involve interaction
with human participants or access to identifiable private information. The project was considered
exempt from institutional review board review. No IRB protocol number was assigned because the
project used publicly available, deidentified data and was considered exempt. The original data were
collected by the source investigators under their institutional approvals and are distributed under
CC0; this analysis adheres to those terms.

## 10. Author contributions
**Gregory Blake Pierpoint:** Conceptualization, Methodology, Software, Validation, Formal analysis,
Investigation, Data curation, Writing – original draft, Writing – review & editing, Visualization,
Project administration.

## 11. Funding
No funding was received for this work.

## 12. Conflicts of interest
The author declares no conflicts of interest.

## 13. Acknowledgments
The author thanks the investigators who collected and openly shared the source datasets (J.F.
Cavanagh, D. Quinn, and colleagues) via OpenNeuro, and the OpenNeuro and BIDS communities; this
acknowledgment does not imply their endorsement. AI-assisted coding and writing tools were used to
support code generation, manuscript organization, and editing. The author reviewed, verified, and
takes full responsibility for all analyses, interpretations, and manuscript content.

---

## 14. References

*Vancouver style, numbered by order of first citation.*

1. Cassidy JD, Carroll LJ, Peloso PM, et al. Incidence, risk factors and prevention of mild
   traumatic brain injury: results of the WHO Collaborating Centre Task Force on Mild Traumatic
   Brain Injury. J Rehabil Med. 2004;36(Suppl 43):28-60. doi:10.1080/16501960410023732.
2. Carroll LJ, Cassidy JD, Peloso PM, et al. Prognosis for mild traumatic brain injury: results of
   the WHO Collaborating Centre Task Force on Mild Traumatic Brain Injury. J Rehabil Med.
   2004;36(Suppl 43):84-105. PMID:15083873.
3. Polinder S, Cnossen MC, Real RGL, et al. A multidimensional approach to post-concussion symptoms
   in mild traumatic brain injury. Front Neurol. 2018;9:1113. doi:10.3389/fneur.2018.01113.
4. Rapp PE, Keyser DO, Albano A, et al. Traumatic brain injury detection using electrophysiological
   methods. Front Hum Neurosci. 2015;9:11. doi:10.3389/fnhum.2015.00011.
5. Nwakamma MC, Stillman AM, Gabard-Durnam LJ, et al. Slowing of parameterized resting-state EEG
   after mild traumatic brain injury. Neurotrauma Rep. 2024;5(1):448-461. doi:10.1089/neur.2024.0004.
6. Donoghue T, Haller M, Peterson EJ, et al. Parameterizing neural power spectra into periodic and
   aperiodic components. Nat Neurosci. 2020;23:1655-1665. doi:10.1038/s41593-020-00744-x.
7. Klimesch W. EEG alpha and theta oscillations reflect cognitive and memory performance: a review
   and analysis. Brain Res Rev. 1999;29(2-3):169-195. doi:10.1016/S0165-0173(98)00056-3.
8. Li H, Li J, Li N, et al. P300 as a potential indicator in the evaluation of neurocognitive
   disorders after traumatic brain injury. Front Neurol. 2021;12:690792. doi:10.3389/fneur.2021.690792.
9. Rosenblatt M, Tejavibulya L, Jiang R, Noble S, Scheinost D. Data leakage inflates prediction
   performance in connectome-based machine learning models. Nat Commun. 2024;15:1829.
   doi:10.1038/s41467-024-46150-w.
10. Varoquaux G. Cross-validation failure: small sample sizes lead to large error bars. NeuroImage.
    2018;180:68-77. doi:10.1016/j.neuroimage.2017.06.061.
11. Pulini AA, Kerr WT, Loo SK, Lenartowicz A. Effects of sample size and circular analysis on
    prediction accuracy in neuroimaging studies. J Neural Eng. 2019;16(2):026018.
    doi:10.1088/1741-2552/aafc8b.
12. Markiewicz CJ, Gorgolewski KJ, Feingold F, et al. The OpenNeuro resource for sharing of
    neuroscience data. eLife. 2021;10:e71774. doi:10.7554/eLife.71774.
13. Gorgolewski KJ, Auer T, Calhoun VD, et al. The brain imaging data structure, a format for
    organizing and describing outputs of neuroimaging experiments. Sci Data. 2016;3:160044.
    doi:10.1038/sdata.2016.44.
14. Pernet CR, Appelhoff S, Gorgolewski KJ, Flandin G, Phillips C, Delorme A, Oostenveld R. EEG-BIDS,
    an extension to the brain imaging data structure for electroencephalography. Sci Data.
    2019;6:103. doi:10.1038/s41597-019-0104-8.
15. Cavanagh JF, Quinn D. EEG: Three-Stim Auditory Oddball and Rest in Acute and Chronic TBI.
    OpenNeuro dataset ds003522, version 1.1.0. doi:10.18112/openneuro.ds003522.v1.1.0.
16. Cavanagh JF. EEG: DPX Cognitive Control Task in Acute Mild TBI. OpenNeuro dataset ds005114,
    version 1.0.0. doi:10.18112/openneuro.ds005114.v1.0.0.
17. Cavanagh JF. EEG: Visual Working Memory in Acute TBI. OpenNeuro dataset ds003523, version 1.1.0.
    doi:10.18112/openneuro.ds003523.v1.1.0.
18. Cavanagh JF. EEG: 3-Stim Auditory Oddball and Rest in Parkinson's. OpenNeuro dataset ds003490,
    version 1.1.0. doi:10.18112/openneuro.ds003490.v1.1.0.
19. Cicerone KD, Kalmar K. Persistent postconcussion syndrome: the structure of subjective complaints
    after mild traumatic brain injury. J Head Trauma Rehabil. 1995;10(3):1-17.
20. King NS, Crawford S, Wenden FJ, Moss NEG, Wade DT. The Rivermead Post Concussion Symptoms
    Questionnaire: a measure of symptoms commonly experienced after head injury and its reliability.
    J Neurol. 1995;242(9):587-592. doi:10.1007/BF00868811.
21. Gramfort A, Luessi M, Larson E, et al. MEG and EEG data analysis with MNE-Python. Front Neurosci.
    2013;7:267. doi:10.3389/fnins.2013.00267.
22. Appelhoff S, Sanderson M, Brooks TL, et al. MNE-BIDS: organizing electrophysiological data into
    the BIDS format and facilitating their analysis. J Open Source Softw. 2019;4(44):1896.
    doi:10.21105/joss.01896.
23. Zou H, Hastie T. Regularization and variable selection via the elastic net. J R Stat Soc Series B
    Stat Methodol. 2005;67(2):301-320. doi:10.1111/j.1467-9868.2005.00503.x.
24. Collins GS, Dhiman P, Ma J, et al. TRIPOD+AI statement: updated guidance for reporting clinical
    prediction models that use regression or machine learning methods. BMJ. 2024;385:e078378.
    doi:10.1136/bmj-2023-078378.
25. Wasserstein RL, Lazar NA. The ASA statement on p-values: context, process, and purpose. Am Stat.
    2016;70(2):129-133. doi:10.1080/00031305.2016.1154108.
26. Pedregosa F, Varoquaux G, Gramfort A, et al. Scikit-learn: machine learning in Python. J Mach
    Learn Res. 2011;12:2825-2830.

---

## 15. Figure legends

**Figure 1. Study design and cohort flow.** Participant accounting from OpenNeuro ds003522 to each
effective analytic sample. The chronic-TBI arm (no longitudinal outcome) and controls (not part of
within-mTBI prediction) exit outcome modeling. Modality-specific quality control yields 25
(resting), 21 (ERP), and 21 (combined-panel) analytic samples. Subject-level cross-validation folds
were frozen before EEG processing; exclusions were applied within each participant's pre-assigned
fold and folds were never regenerated.

**Figure 2. Structure of the ds003522 continuous Session-1 recording.** A single continuous
recording (~15–28 min) contained eyes-closed and eyes-open resting blocks bracketing two
auditory-oddball runs. Resting and task segments were identified from event markers; a single
boundary event at recording onset (no internal discontinuities) was handled by a boundary-aware
pipeline. Resting blocks provided spectral/aperiodic features; oddball runs provided P3b (target)
and P3a (novel) ERPs.

**Figure 3. EEG preprocessing and feature-extraction pipeline.** A single fixed parameter set,
selected without reference to any outcome, was applied to every recording; raw files were never
modified. The boundary-aware pipeline branched into resting-state (0.5–45 Hz) and ERP (+40-Hz
low-pass) streams. Schematic; no outcome data shown.

**Figure 4. Primary-model coefficient forest plot.** Standardized β coefficients (points) with 95%
confidence intervals (bars) for the primary parsimonious model (n = 21); resting features in teal,
ERP in orange, covariates in grey, with a colour legend and predictor labels identifying each
feature family. All intervals span zero (dashed line).

**Figure 5. Out-of-fold predicted versus observed NSI (Elastic Net).** Out-of-fold predictions
versus observed Session-3 NSI total. Predictions collapse toward the cohort mean (dotted line) across
the full observed range (0–51), consistent with the penalized model retaining no feature
(R²_oof = −0.06). The dashed line is identity.

**Figure 6. Dataset × feature availability matrix.** Extractability of each locked feature, with its
preregistered definition, by dataset (green = extractable). ds005114 and ds003523 lack eyes-closed
rest and the auditory oddball (0/8); ds003490 supports all eight features but is a Parkinson's cohort
without a post-concussive outcome.

**Figure 7. Discovery estimates with replication status.** Frozen discovery standardized
β coefficients (95% CI) for the primary-model EEG predictors, annotated to indicate that replication
in ds005114 is not estimable because the source paradigms are absent.

**Supplementary figures S1–S5.** S1, partial (added-variable) plots for the primary EEG predictors;
S2, Elastic Net coefficient path; S3, out-of-fold calibration; S4, resting-versus-ERP standardized
contribution from the full-panel (descriptive) model; S5, specparam fit-quality distribution.

---

## 16. Tables

## Table 1. Dataset and cohort overview

| Dataset | Role | Paradigm | Embedded rest | Groups | Sessions | EEG (n with _eeg.set, S1) | Outcome (NSI/Rivermead) |
|---|---|---|:--:|---|:--:|---:|:--:|
| **ds003522** | **Discovery** | Three-stimulus auditory oddball + rest | Yes (EC/EO) | sub-acute/early post-injury mTBI / control / chronic TBI | 3 | 96 | Yes |
| ds005114 | Designated replication | DPX cognitive control | No | acute mTBI / control | 3 | 91 | Yes |
| ds003523 | Designated replication | Visual working memory | No | acute TBI / control | 3 | 91 | Yes (via shared workbook) |
| ds003490 | Paradigm reference | Three-stimulus auditory oddball + rest | Yes (EC/EO) | **Parkinson's disease** (25 PD / 25 control) | 2 | not analysed (paradigm reference) | **No (no post-concussive outcome)** |

*All datasets: 500-Hz BrainVision EEG, EEGLAB .set/.fdt, online reference CPz, 60-Hz line. The
discovery and replication datasets derive from one longitudinal UNM cohort (Cavanagh et al.,
2016–2018); the same individuals recur across the three TBI datasets and were deduplicated on a
stable unique identifier (URSI). ds003490 is a separate Parkinson's-disease cohort (50 participants,
25 PD / 25 control, 2 sessions) used only to assess feature extractability, not analysed for outcome.
EC = eyes-closed; EO = eyes-open. Source: outputs/metadata_summary_tables/,
outputs/analysis/replication_feature_availability.csv, OpenNeuro dataset records [15,16,17,18].*

## Table 2. Participant flow and analytic sample (ds003522)

| Stage | n | Notes |
|---|---:|---|
| ds003522 participants with EEG | 96 | sub-acute/early post-injury mTBI + control + chronic TBI |
| Sub-acute/early post-injury mTBI arm (Group 0) | 44 | chronic TBI (25) and controls (27) excluded from outcome cohort |
| … with usable Session-1 EEG (read QC) | 44 | 25/25 of the eligible-with-outcome subset readable; uniform 500 Hz / 65 ch |
| … with non-missing Session-3 NSI total | **25** | **eligible discovery cohort** |
| Resting (eyes-closed) usable (≥ 40 s clean) | **25** | all eligible subjects |
| ERP usable (≥ 15 Target & Novel epochs; tone labels present) | **21** | − sub-040 (no curated tone labels); − 3 with < 15 rare-tone epochs |
| Combined panel (primary model) | **21** | resting + reliable ERP |
| Sensitivity (drop 1 eyes-open-low subject) | 20 | prespecified; conclusions unchanged |

*The public BIDS metadata contains 44 Group-0 mTBI participants with Session-1 EEG records; the exact reason a source article may report a smaller analytic subset was not verifiable from local BIDS metadata alone. Cohort-level longitudinal attrition (whole UNM cohort, both groups): symptom outcomes ~91 (S1) →
~78 (S2) → ~62 (S3). The chronic-TBI arm has single-session EEG and no longitudinal outcome.
Quality-control exclusions were applied within each participant's pre-assigned, frozen
cross-validation fold; folds were never regenerated. Source:
outputs/metadata_summary_tables/attrition_by_session.csv,
outputs/features/ds003522_s1_subject_usability.csv,
outputs/analysis/ds003522_s1_analysis_table.csv.*

## Table 3. Locked EEG feature panel

| # | Feature | Modality | State / task | Region | Definition (preregistered) | Primary | Secondary | Exploratory |
|---|---|---|---|---|---|:--:|:--:|:--:|
| 1 | Global aperiodic exponent | Resting | Eyes-closed | Global | specparam (fixed mode) 1/f exponent, 1–40 Hz fit | ✓ | ✓ | |
| 2 | Posterior IAF | Resting | Eyes-closed | Parietal–occipital | 7–13 Hz spectral peak frequency | ✓ | ✓ | |
| 3 | Frontal theta/alpha ratio | Resting | Eyes-closed | Frontal | θ(4–8 Hz)/α(8–12 Hz) absolute power | | ✓ | |
| 4 | Occipital relative alpha | Resting | Eyes-closed | Occipital | α power / total (1–45 Hz) power | | ✓ | |
| 5 | P3b amplitude | ERP | Oddball — Target | Parietal (Pz/CPz/POz) | mean amplitude 300–600 ms (peak = sensitivity) | ✓ | ✓ | |
| 6 | P3b latency | ERP | Oddball — Target | Parietal | peak latency 300–600 ms | | ✓ | |
| 7 | P3a amplitude | ERP | Oddball — Novel | Frontocentral (Fz/FCz/Cz) | mean amplitude 250–400 ms (peak = sensitivity) | | ✓ | |
| 8 | P3a latency | ERP | Oddball — Novel | Frontocentral | peak latency 250–400 ms | | ✓ | |
| 9 | Spectral entropy | Resting | Eyes-closed | Global | Shannon entropy of normalized PSD (1–45 Hz) | | | ✓ |

*Primary model = features 1, 2, 5 + age + sex (parsimonious, one biomarker per domain). Secondary
(Elastic Net) and transparency (full OLS) models = features 1–8 + age + sex. Feature 9 (spectral
entropy) is exploratory only. Eyes-closed is the primary resting condition; eyes-open versions are
sensitivity analyses. Source: final_locked_analysis_plan.md, scripts/_eeg_common.py,
outputs/features/.*

## Table 4. Model results

### 4A. Primary confirmatory model — coefficients
S3_NSI_Total ~ Global_Aperiodic_Exponent + Posterior_IAF + P3b_Amplitude + Age + Sex (OLS, n = 21;
R² = 0.11, adjusted R² = −0.19, omnibus F p = 0.86; raw NSI scale)

| Predictor | β (raw) | Std. β | 95% CI (std.) | p | p (FDR) |
|---|---:|---:|---:|---:|---:|
| Global aperiodic exponent | −1.42 | −0.02 | −0.83 to 0.79 | 0.96 | 0.96 |
| Posterior IAF | −2.58 | −0.15 | −0.83 to 0.52 | 0.64 | 0.96 |
| P3b amplitude | 2.07 | 0.24 | −0.40 to 0.88 | 0.43 | 0.96 |
| Age | −0.06 | −0.04 | −0.83 to 0.75 | 0.92 | 0.96 |
| Sex | −4.85 | −0.13 | −0.71 to 0.44 | 0.63 | 0.96 |

*No 95% CI excludes zero. Heteroscedasticity-consistent (HC3) p-values: 0.64–0.97. Leave-one-subject-
out: no predictor sign-stable. Source: outputs/analysis/model_coefficients.csv,
outputs/analysis/loo_coefficient_stability.csv, outputs/analysis/diagnostics.json.*

### 4B. Out-of-fold performance (frozen folds)

| Model | Tier | n | Out-of-fold R² (95% CI) | MAE | adj. R² (in-sample) |
|---|---|---:|---:|---:|---:|
| Baseline (age + sex) | reference | 21 | −0.40 (−1.36, −0.13) | 15.7 | — |
| **Primary parsimonious** | **primary confirmatory** | 21 | **−1.38 (−2.85, −0.89)** | 19.2 | −0.19 |
| **Elastic Net (full panel)** | **secondary confirmatory** | 21 | **−0.06 (−0.50, −0.02)** | 13.3 | — (0/10 coef ≠ 0) |
| Full 10-term OLS | transparency (descriptive) | 21 | −3.58 (−9.82, −1.81) | 27.5 | −0.22 |
| Resting-only OLS | supportive | 25 | −0.59 (−2.07, −0.08) | 16.7 | 0.08 |
| ERP-only OLS | supportive | 21 | −1.13 (−2.83, −0.38) | 17.1 | −0.12 |
| Ridge | exploratory | 21 | −0.14 (−0.61, −0.03) | 13.6 | — |
| LASSO | exploratory | 21 | −0.06 (−0.50, −0.02) | 13.3 | — |
| Random Forest | exploratory | 21 | −0.29 (−1.14, −0.06) | 14.9 | — |
| XGBoost | exploratory | 21 | −0.36 (−1.36, 0.09) | 14.7 | — |

*Out-of-fold R²/MAE are leakage-safety transparency metrics, not stable model-ranking estimates at n = 21. All EEG models had negative out-of-fold R². The least-poor penalized models performed less poorly than the age+sex baseline only by shrinking to, or near, a mean/intercept predictor rather than by retaining a reproducible EEG feature signal. The Elastic Net selected α = 43.2, mixing parameter = 0.10, and shrank all 10 coefficients to zero (intercept = 14.6, the cohort mean). Source: outputs/analysis/cv_performance.csv,
outputs/analysis/elasticnet_coefficients.csv, outputs/analysis/model_fit_summary.csv.*

## Table 5. Replication feasibility matrix

| Dataset | Task | Eyes-closed rest | Auditory oddball | Locked features extractable | NSI / post-concussive outcome | Replication status |
|---|---|:--:|:--:|:--:|:--:|---|
| **ds003522** (discovery) | oddball + rest | ✓ | ✓ | **8 / 8** | ✓ | reference (discovery) |
| **ds005114** (designated) | DPX | ✗ (0/91) | ✗ (0/91) | **0 / 8** | ✓ | **infeasible — paradigm & state absent** |
| **ds003523** (designated) | visual working memory | ✗ | ✗ | **0 / 8** | ✓ | **infeasible — paradigm & state absent** |
| **ds003490** (paradigm ref.) | oddball + rest | ✓ | ✓ | 8 / 8 | ✗ (Parkinson's; no PCS) | not applicable — wrong population/outcome |

*ds005114 was scanned across all 91 Session-1 recordings: 0 contained an eyes-closed/eyes-open rest
marker, 0 contained an auditory-oddball tone, and 91/91 contained DPX cue/probe events. No dataset
matches both the EEG paradigm/state and the clinical outcome required for feature-identical
replication. Cross-paradigm feature substitution (e.g., DPX probe P3 → "P3b"; task EEG → "rest") was
rejected as it would modify the locked feature definitions. Source:
outputs/analysis/replication_feature_availability.csv,
outputs/analysis/replication_effect_size_comparison.csv.*

All numeric values in these tables are reproduced from the frozen analysis outputs in outputs/analysis/ and outputs/metadata_summary_tables.
