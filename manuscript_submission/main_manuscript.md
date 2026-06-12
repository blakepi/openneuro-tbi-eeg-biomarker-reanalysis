# Leakage-Safe EEG Biomarker Analysis After Mild Traumatic Brain Injury: A Preregistered OpenNeuro Reanalysis and Replication Feasibility Study

**Running title:** Leakage-safe EEG biomarkers after mTBI

**Author:** Gregory Blake Pierpoint

**Affiliation:** Macon and Joan Brock Virginia Health Sciences, Eastern Virginia Medical School at
Old Dominion University, Norfolk, Virginia, USA

**Correspondence:** pierpogb@odu.edu · ORCID 0000-0001-8288-8549

---

## Abstract

*(Structured abstract, ~275 words — see `abstract.md`.)*

**Background.** Persistent post-concussive symptoms affect a clinically important minority after
mild traumatic brain injury (mTBI), yet acute prognostication is difficult. Resting-state and
task-evoked EEG have been proposed as prognostic biomarkers, but the supporting literature often
uses small samples and pipelines vulnerable to leakage and overfitting. **Objective.** To test, in
a preregistered, leakage-safe framework, whether early EEG features predict later symptom burden
after acute mTBI in a public dataset, and whether the analysis can be replicated in related public
datasets. **Methods.** We reanalysed OpenNeuro ds003522 (acute mTBI; auditory three-stimulus
oddball with embedded eyes-closed/eyes-open rest). Subjects were keyed on a stable identifier
(URSI); cross-validation folds were frozen before EEG processing; a biologically motivated feature
panel (posterior individual alpha frequency, global aperiodic exponent, frontal theta/alpha ratio,
occipital relative alpha, P3b/P3a amplitude and latency) was extracted with boundary-aware
preprocessing. The primary outcome was Session-3 Neurobehavioral Symptom Inventory (NSI) total.
The statistical hierarchy was locked before outcome modeling. **Results.** In the primary model
(n = 21), no predictor's 95% CI excluded zero (largest standardized β = 0.24, 95% CI −0.40–0.88;
adjusted R² = −0.19); coefficients were unstable under leave-one-out. The Elastic Net shrank all
coefficients to zero; every model produced negative out-of-fold R² and none exceeded an age+sex
baseline. Replication in ds005114 was infeasible (0/91 recordings contained rest or oddball
markers; 0/8 features extractable); ds003523 likewise; the one paradigm-matched dataset (ds003490)
is a Parkinson's cohort without a post-concussive outcome. **Conclusions.** No stable evidence
emerged that the tested EEG features predict persistent post-concussive symptoms; the result is
inconclusive and underpowered. Feature-identical public-dataset replication was infeasible owing to
paradigm fragmentation.

**Keywords:** mild traumatic brain injury; post-concussive symptoms; EEG; event-related potentials;
aperiodic activity; prognostic biomarkers; reproducibility; data leakage; preregistration; OpenNeuro

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
[2]. This motivates the search for an objective, physiologically grounded indicator
of the neural dysfunction that may underlie prolonged recovery.

Electroencephalography (EEG) is an attractive candidate: it is inexpensive, portable, temporally
precise, and directly indexes cortical dynamics, excitation/inhibition balance, and the timing of
information processing [4]. Two largely separate
literatures bear on mTBI. **Resting-state** studies report alpha-rhythm slowing, increased theta
and theta/alpha ratios, and — more recently — alterations in the **aperiodic (1/f)** component of
the spectrum interpreted as a marker of excitation/inhibition balance and neural noise [5,6,8].
**Task-evoked** studies, especially with the auditory oddball, report reduced amplitude and
prolonged latency of the **P3 family** of event-related potentials (ERPs), with the parietal P3b
indexing target evaluation and the frontocentral P3a indexing novelty orienting [7].

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
in which acute-mTBI participants underwent combined resting and auditory-oddball EEG within days of
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
This is a retrospective reanalysis of public, deidentified OpenNeuro EEG data. An internal analysis
plan — cohort, feature definitions, statistical hierarchy, leakage rules, and missing-data strategy
— was **locked before any outcome modeling** and before any feature–outcome relationship was
examined (Supplement: *Final Locked Analysis Plan*). The framework is **estimation-first**:
interpretation is anchored to effect sizes and confidence intervals rather than dichotomized
significance, and **no causal claims** are made. The locked analysis plan is included in the
Supplement and in the version-controlled code repository (§Code availability), where its
pre-modeling timestamp is recorded in the commit history.

### 2.2 Datasets
We used four OpenNeuro datasets from a single longitudinal research program (University of New
Mexico; J.F. Cavanagh and colleagues; data collected 2016–2018):

- **ds003522 (discovery)** [15]. Three-stimulus auditory oddball with **embedded eyes-closed/eyes-open
  resting blocks**; acute mTBI, controls, and a chronic-TBI arm; three sessions; longitudinal
  clinical outcomes for the acute-mTBI/control cohort. DOI 10.18112/openneuro.ds003522.v1.1.0.
- **ds005114 (designated replication)** [24]. DPX (dot-pattern expectancy) cognitive-control task;
  acute mTBI/control; assessed for replication feasibility.
- **ds003523 (designated replication)** [25]. Visual working-memory task; acute TBI/control; assessed
  for feature availability.
- **ds003490 (paradigm reference)** [26]. Same three-stimulus oddball + rest paradigm but a
  **Parkinson's** cohort; feature-extraction-compatible yet outcome/population-incompatible.

All datasets used 500-Hz BrainVision EEG stored as EEGLAB `.set/.fdt` (BIDS-EEG).

### 2.3 Participants and identity resolution
The same individuals recur across these datasets under different BIDS labels; the stable unique key
is the scan-generated **URSI** (here `subject_uid`). We did **not** assume BIDS `sub-0XX` labels
were stable across datasets, and we did not use the recording id (`Original_ID`) as the identity key
because one value (3013) maps to two distinct URSIs (`M87138342` vs `M87138432`, an apparent
transposition; Supplement). All merging and cross-validation splitting used `subject_uid`. The
**chronic-TBI arm was excluded** from the symptom-prediction cohort because it has no longitudinal
clinical outcome; clinical-only subjects without EEG were documented rather than silently dropped
(Supplement). The discovery cohort comprised acute-mTBI participants with a usable Session-1 EEG and
a non-missing Session-3 outcome (**n = 25**). Effective analytic samples were 25 (resting-only
models), 21 (ERP and combined models; see §2.7), and 20 (a prespecified sensitivity excluding one
participant with limited eyes-open data).

### 2.4 Clinical outcomes
The **primary outcome** was the **Session-3 Neurobehavioral Symptom Inventory (NSI) total** [19],
computed as the sum of somatic, cognitive, and emotional subscales (no precomputed total exists in
the source). Outcomes were obtained from the cohort's aggregated clinical workbook, joined to EEG by
URSI; string missing-tokens were mapped to missing. Secondary outcomes (prespecified, reported as
context) were the Session-3 Rivermead Post-Concussion Symptoms Questionnaire total [20] and
Session-1→Session-3 change scores. The NSI total was
right-skewed but below the prespecified transformation threshold (skewness = 0.85 < 1.0) and was
therefore analysed on the **raw scale** (n = 25: mean 15.1, SD 15.7, median 9, range 0–51). No binary
"persistent symptoms" outcome was defined, because the source documentation contains no established
threshold. Attrition was substantial (cohort-level symptom outcomes ~91 at Session 1 → ~62 at
Session 3) and is documented as potentially informative.

### 2.5 EEG acquisition and task structure (ds003522)
Continuous EEG was recorded at **500 Hz** from **63 scalp electrodes** (international 10–10 system)
plus vertical EOG (VEOG) and ECG (EKG) channels (65 channels total), with an online reference at
**CPz** and a 60-Hz power line (BrainVision actiCHamp). Each Session-1 recording (~15–28 min)
contained, in order, an eyes-closed block, an eyes-open block, an oddball run, and a second cycle of
eyes-closed/eyes-open rest and oddball (Figure 2); resting and task segments were demarcated by event
markers, yielding ~120 s each of eyes-closed and eyes-open rest and, per recording, 184 standard, 38
target, and 38 novel tones. A single EEGLAB `boundary` event occurred at recording onset in every
file, with no internal discontinuities. One participant (`sub-040`) lacked curated tone labels (tones
stored only as raw stimulus codes) and was excluded from ERP analyses without inferring the
non-standard mapping.

### 2.6 EEG preprocessing
Preprocessing used MNE-Python (v1.12) [16], with dataset handling supported by MNE-BIDS [17], using a
single fixed parameter set applied identically to all participants, chosen **without reference to any
outcome**; raw files
were never modified (Figure 3). The pipeline was **boundary-aware**: `boundary` events were converted
to `BAD_boundary` annotations and the FIR filter was constrained not to span discontinuities. For
each recording we (i) typed VEOG/EKG as non-EEG (excluded from referencing, montage, and features);
(ii) applied a 60-Hz notch; (iii) band-pass filtered 0.5–45 Hz; (iv) reinstated the online reference
CPz, assigned a standard 10–20 montage, and re-referenced to the average of the 64 EEG channels; and
(v) performed within-participant bad-channel detection (robust z-score of log-variance > 4, or flat
channels), interpolating flagged channels by spherical splines (the reinstated reference was exempt).
For ERPs an additional 40-Hz low-pass was applied before epoching. **Quality control:** all 25
recordings were readable with uniform sampling rate and channel structure, no flat/NaN/zero-filled or
dataset-marked bad channels, and 0–3 (predominantly frontal-ocular) channels interpolated per
participant; no QC failure threatened feasibility.

### 2.7 Feature extraction
**Resting-state** analyses used the **eyes-closed** condition as primary (eyes-open as a sensitivity
condition). Eyes-closed/eyes-open blocks were segmented from their marker trains, screened for
discontinuities, divided into non-overlapping 2-s segments, and segments exceeding 150 µV
peak-to-peak rejected. Power spectral density (Welch, 2-s windows, 50% overlap, 1–45 Hz) was averaged
within frontal/central/parietal/occipital and global regions. We derived the **posterior individual
alpha frequency** (7–13 Hz peak of the parietal–occipital spectrum) [8], the **global aperiodic
exponent** (specparam v2.0, fixed mode, 1–40 Hz) [6], the **frontal theta/alpha ratio**,
**occipital relative alpha power**, and (exploratory) spectral entropy.
Eyes-closed features were usable for all 25 participants. **ERP** analyses epoched −200–800 ms around
tones, baseline-corrected (−200–0 ms), rejected boundary-overlapping and >150 µV epochs, and
quantified the **P3b** (target, parietal Pz/CPz/POz, 300–600 ms) and **P3a** (novel, frontocentral
Fz/FCz/Cz, 250–400 ms), reporting **mean-window amplitude (primary)**, peak amplitude (sensitivity),
and peak latency. ERP components required ≥ 15 retained rare-tone epochs; with this criterion and the
`sub-040` exclusion, ERP features were usable for 21 participants.

### 2.8 Statistical analysis
The analysis hierarchy was **locked before outcome modeling** (Supplement). Because the full
specification (8 EEG features + age + sex) exceeds the events-per-variable supportable at n ≈ 20–25,
the primary confirmatory model was a **parsimonious linear regression** carrying one biomarker per
domain:

> `S3_NSI_Total ~ Global_Aperiodic_Exponent + Posterior_IAF + P3b_Amplitude + Age + Sex`.

The **secondary confirmatory** model was an **Elastic Net** [21] over the full locked panel +
covariates; the full unpenalized 10-term OLS was reported **for transparency only** (descriptive,
potentially overfit); ridge, LASSO, random forest, and gradient boosting (XGBoost) were
**exploratory**. All scaling, imputation, and hyperparameter tuning were fit **within training folds
only**, using subject-level folds frozen before feature extraction. Consistent with an
estimation-first stance and prediction-model reporting guidance [22,23], we emphasize standardized β
coefficients, 95% confidence intervals, and effect sizes over dichotomized significance; we also
report p-values (Benjamini–Hochberg FDR within the predictor family), adjusted R²,
leave-one-subject-out coefficient stability, and residual/influence diagnostics. Predictive
performance was the out-of-fold R²/MAE benchmarked against an age+sex baseline. No exploratory model
was promoted to confirmatory. Analyses used Python 3.14 with MNE 1.12, specparam 2.0, scikit-learn
1.9 [18], statsmodels 0.14, numpy, and pandas, with fixed seeds; code and frozen folds are released
(§Code availability).

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
From the acute-mTBI arm of ds003522, 25 participants had a usable Session-1 EEG and a Session-3 NSI
total (Figure 1; Table 2). All 25 recordings passed read QC with uniform acquisition (Section 2.6).
Locked usability criteria yielded 25 participants for resting-only models and 21 for ERP and combined
models (four ERP exclusions: one lacking curated tone labels, three with fewer than 15 retained
rare-tone epochs). Extracted features were physiologically plausible (e.g., posterior individual
alpha frequency clustered near 10 Hz; aperiodic fits R² ≈ 0.99) (Supplement Table S1).

### 3.2 Primary confirmatory analysis
The parsimonious model (n = 21) did not account for variance beyond chance (R² = 0.11, adjusted
R² = −0.19, omnibus F p = 0.86). **No predictor's 95% confidence interval excluded zero** (Table 4;
Figure 4). The largest standardized association was P3b amplitude (β = 0.24, 95% CI −0.40 to 0.88,
p = 0.43), followed by posterior individual alpha frequency (β = −0.15, 95% CI −0.83 to 0.52) and the
global aperiodic exponent (β = −0.02, 95% CI −0.83 to 0.79); age and sex were likewise uninformative.
After FDR correction all p-values were 0.96, and heteroscedasticity-consistent inference was
materially identical (p = 0.64–0.97). Residual diagnostics were unremarkable (Shapiro–Wilk p = 0.09;
Breusch–Pagan p = 0.50; Durbin–Watson = 1.86), but three of 21 participants exceeded the
Cook's-distance threshold (4/n = 0.19), including one outlier (externally studentized residual = 3.6).
In leave-one-subject-out refitting, **no predictor retained a stable sign**, indicating the cohort is
too small to estimate even this five-term model dependably.

### 3.3 Secondary confirmatory analysis (Elastic Net)
The Elastic Net selected a penalty (α = 43.2, mixing parameter = 0.10) that **shrank all ten
coefficients to zero**; the retained model was the intercept (14.6, the cohort mean). Out-of-fold
performance was at or below a mean predictor (R² = −0.06, 95% CI −0.50 to −0.02; MAE = 13.3 NSI
points), with predictions compressed to a near-constant line across the full observed range (Figure
5).

### 3.4 Supportive and transparency analyses
Domain-specific models reproduced this pattern (Table 4; Supplement Table S5). The resting-only model
(n = 25) had the largest in-sample fit (R² = 0.31) but a near-zero adjusted R² (0.08), a
non-significant omnibus test (p = 0.29), and negative out-of-fold R² (−0.59); the ERP-only model
(n = 21) was similarly uninformative (adjusted R² = −0.12; out-of-fold R² = −1.13). The full 10-term
OLS, reported for transparency only, illustrated overfitting at this sample size (in-sample R² = 0.39
but adjusted R² = −0.22; design condition number ≈ 22,000; out-of-fold R² = −3.58); it is descriptive
and not used for inference.

### 3.5 Exploratory analyses
Exploratory penalized (ridge, LASSO) and flexible (random forest, gradient boosting) learners all
produced negative out-of-fold R² (−0.06 to −0.36; Table 4; Supplement Table S5); the least-poor
models were those regularizing most strongly toward the mean, and flexible learners recovered no
non-linear structure. Adding spectral entropy did not change any result. No exploratory analysis is
central to the conclusions.

### 3.6 Replication feasibility
Across **all 91** Session-1 recordings of ds005114, **0 contained an eyes-closed/eyes-open rest marker
and 0 contained an auditory-oddball tone; 91/91 contained DPX cue/probe events** (Table 5; Figure 6).
Consequently **none of the eight locked features was extractable with its preregistered definition**.
ds003523 (visual working memory) showed the same absence. The one paradigm-matched dataset, ds003490,
permits extraction of all eight features but is a **Parkinson's cohort without a post-concussive
outcome**. **No available dataset matched both the EEG paradigm/state and the clinical outcome**, so
the requested replication models could not be fit; discovery estimates are shown with explicit
"not estimable" replication status in Figure 7. We did not manufacture a replication by redefining
features.

---

## 4. Discussion

In a preregistered, leakage-safe longitudinal reanalysis, a compact panel of early resting-state and
task-evoked EEG features showed **no stable evidence** of predicting persistent post-concussive
symptom burden at ~4 months after acute mTBI. Standardized associations were small with intervals
spanning zero, coefficients were unstable to single observations, every out-of-fold model
performed at or below a demographic baseline, and the penalized full-panel model retained no feature.
A planned replication in related public datasets was **infeasible** because they did not share the
paradigm and resting state required to measure the locked features.

**Interpretation of the null.** This is **not** evidence that EEG is irrelevant to post-concussive
recovery. With ~20 participants, confidence intervals reached ±0.8 SD and the data are uninformative
about modest true associations; the leave-one-out instability of every coefficient shows the cohort
is too small to estimate even a three-biomarker model dependably. The result is best described as
**inconclusive and underpowered**, indicating that the tested feature panel in this small public
cohort did not produce stable, generalizable prediction.

**Why the Elastic Net result matters.** A penalized model free to weight any subset of the panel
preferred the **intercept-only (mean) predictor**, arguing against a hidden robust multivariable
signal that a single linear model might have missed. This convergence of penalized, flexible, and
parsimonious models on the mean strengthens the conclusion that no stable signal is present **in
these data**.

**Leakage prevention and the prior literature.** Our discovery result is more conservative than much
of the resting-EEG and P3 mTBI literature [5,7]. Several design features may explain this: a
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

**Why we did not redefine features.** Relabeling the DPX probe-evoked P3 as "P3b," or computing
"resting" spectra from eyes-open task EEG, would have produced nominal replication numbers but
modified the locked feature definitions — substituting a different ERP component evoked by a
different stimulus, or conflating eyes-closed with eyes-open active states (the alpha-band features
are strongly state-dependent). Declining these maintains biological and methodological comparability
and preserves the meaning of "replication."

**Strengths.** Use of public data; transparent, released code and frozen folds; explicit identity
resolution (URSI, with the 3013 collision handled); a locked model hierarchy and prespecified
features; boundary-aware preprocessing; honest null reporting in an estimation-first framework; and a
formal replication-feasibility audit.

---

## 5. Limitations

The dominant limitation is **sample size**: ~20–25 acute-mTBI participants carried to the four-month
outcome power the study only for large effects and yield unstable estimates. Additional limitations
include informative **attrition** from acute to chronic assessment (modeled as complete-case in the
primary analysis, with a prespecified inverse-probability-weighted sensitivity deferred); reliance on
a **single discovery dataset** for the locked feature panel; the **absence of a true external
replication dataset**; **ERP reliability exclusions** that further reduce N; underpowered secondary
analyses; **public-dataset metadata constraints** (e.g., outcomes in a supplementary workbook; one
unpublished related dataset); a single site and device; self-report symptom outcomes; resting EEG
extracted from blocks embedded within the task recording rather than a standalone run; and the
**absence of causal inference** by design.

---

## 6. Conclusions

In this leakage-safe OpenNeuro reanalysis, a biologically motivated resting-state and ERP EEG feature
panel did not show stable evidence of predicting persistent post-concussive symptoms after acute
mTBI. Planned public-dataset replication was infeasible because related datasets did not share both
the EEG paradigm/state and the clinical-outcome structure needed for feature-identical validation. We
interpret these findings as inconclusive and underpowered rather than as evidence of absence. Future
EEG biomarker studies in mTBI require larger, longitudinal, paradigm-matched cohorts with harmonized
symptom outcomes and prespecified, leakage-safe analytic plans; the present study contributes a
transparent, reproducible template and an explicit account of what such validation will demand.

---

## 7. Data availability
This study used publicly available OpenNeuro datasets. Raw EEG and metadata are available from
OpenNeuro at ds003522 (doi:10.18112/openneuro.ds003522.v1.1.0) [15], ds005114
(doi:10.18112/openneuro.ds005114.v1.0.0) [24], ds003523 (doi:10.18112/openneuro.ds003523.v1.1.0)
[25], and ds003490 (doi:10.18112/openneuro.ds003490.v1.1.0) [26]. No new human data were collected.
Raw EEG data are not redistributed in the code repository. Derived analysis tables (cohort
crosswalk, feature matrices, model outputs) are provided in the Supplement and the repository.

## 8. Code availability
Analysis code and derived manuscript materials (download, identity resolution, preprocessing,
feature extraction, frozen cross-validation folds, models, and figures) are available at the GitHub
repository: https://github.com/gblakepierpoint/openneuro-tbi-eeg-biomarker-reanalysis. The submitted
version corresponds to commit a995ac0
(a995ac0edddf83fb2a381e253dc6e17f7053f230). The repository is released under the MIT License; the
locked analysis plan is included.
Environment: Python 3.14; MNE 1.12; MNE-BIDS; specparam 2.0; scikit-learn 1.9; statsmodels 0.14;
xgboost 3.2.

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

*Vancouver style, numbered by order of first citation. Machine-readable entries are in
`references.bib`.*

1. Cassidy JD, Carroll LJ, Peloso PM, et al. Incidence, risk factors and prevention of mild
   traumatic brain injury: results of the WHO Collaborating Centre Task Force on Mild Traumatic
   Brain Injury. J Rehabil Med. 2004;36(Suppl 43):28–60. doi:10.1080/16501960410023732.
2. Carroll LJ, Cassidy JD, Peloso PM, et al. Prognosis for mild traumatic brain injury: results of
   the WHO Collaborating Centre Task Force on Mild Traumatic Brain Injury. J Rehabil Med.
   2004;36(Suppl 43):84–105. PMID:15083873.
3. Polinder S, Cnossen MC, Real RGL, et al. A multidimensional approach to post-concussion symptoms
   in mild traumatic brain injury. Front Neurol. 2018;9:1113. doi:10.3389/fneur.2018.01113.
4. Rapp PE, Keyser DO, Albano A, et al. Traumatic brain injury detection using electrophysiological
   methods. Front Hum Neurosci. 2015;9:11. doi:10.3389/fnhum.2015.00011.
5. Nwakamma MC, Stillman AM, Gabard-Durnam LJ, et al. Slowing of parameterized resting-state EEG
   after mild traumatic brain injury. Neurotrauma Rep. 2024;5(1):448–461. doi:10.1089/neur.2024.0004.
6. Donoghue T, Haller M, Peterson EJ, et al. Parameterizing neural power spectra into periodic and
   aperiodic components. Nat Neurosci. 2020;23:1655–1665. doi:10.1038/s41593-020-00744-x.
7. Li H, Li J, Li N, et al. P300 as a potential indicator in the evaluation of neurocognitive
   disorders after traumatic brain injury. Front Neurol. 2021;12:690792. doi:10.3389/fneur.2021.690792.
8. Klimesch W. EEG alpha and theta oscillations reflect cognitive and memory performance: a review
   and analysis. Brain Res Rev. 1999;29(2–3):169–195. doi:10.1016/S0165-0173(98)00056-3.
9. Rosenblatt M, Tejavibulya L, Jiang R, Noble S, Scheinost D. Data leakage inflates prediction
   performance in connectome-based machine learning models. Nat Commun. 2024;15:1829.
   doi:10.1038/s41467-024-46150-w.
10. Varoquaux G. Cross-validation failure: small sample sizes lead to large error bars. NeuroImage.
    2018;180:68–77. doi:10.1016/j.neuroimage.2017.06.061.
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
16. Gramfort A, Luessi M, Larson E, et al. MEG and EEG data analysis with MNE-Python. Front Neurosci.
    2013;7:267. doi:10.3389/fnins.2013.00267.
17. Appelhoff S, Sanderson M, Brooks TL, et al. MNE-BIDS: organizing electrophysiological data into
    the BIDS format and facilitating their analysis. J Open Source Softw. 2019;4(44):1896.
    doi:10.21105/joss.01896.
18. Pedregosa F, Varoquaux G, Gramfort A, et al. Scikit-learn: machine learning in Python. J Mach
    Learn Res. 2011;12:2825–2830.
19. Cicerone KD, Kalmar K. Persistent postconcussion syndrome: the structure of subjective complaints
    after mild traumatic brain injury. J Head Trauma Rehabil. 1995;10(3):1–17.
20. King NS, Crawford S, Wenden FJ, Moss NEG, Wade DT. The Rivermead Post Concussion Symptoms
    Questionnaire: a measure of symptoms commonly experienced after head injury and its reliability.
    J Neurol. 1995;242(9):587–592. doi:10.1007/BF00868811.
21. Zou H, Hastie T. Regularization and variable selection via the elastic net. J R Stat Soc Series B
    Stat Methodol. 2005;67(2):301–320. doi:10.1111/j.1467-9868.2005.00503.x.
22. Collins GS, Dhiman P, Ma J, et al. TRIPOD+AI statement: updated guidance for reporting clinical
    prediction models that use regression or machine learning methods. BMJ. 2024;385:e078378.
    doi:10.1136/bmj-2023-078378.
23. Wasserstein RL, Lazar NA. The ASA statement on p-values: context, process, and purpose. Am Stat.
    2016;70(2):129–133. doi:10.1080/00031305.2016.1154108.
24. Cavanagh JF. EEG: DPX Cognitive Control Task in Acute Mild TBI. OpenNeuro dataset ds005114,
    version 1.0.0. doi:10.18112/openneuro.ds005114.v1.0.0.
25. Cavanagh JF. EEG: Visual Working Memory in Acute TBI. OpenNeuro dataset ds003523, version 1.1.0.
    doi:10.18112/openneuro.ds003523.v1.1.0.
26. Cavanagh JF. EEG: 3-Stim Auditory Oddball and Rest in Parkinson's. OpenNeuro dataset ds003490,
    version 1.1.0. doi:10.18112/openneuro.ds003490.v1.1.0.

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

**Figure 7 (optional). Discovery estimates with replication status.** Frozen discovery standardized
β coefficients (95% CI) for the primary-model EEG predictors, annotated to indicate that replication
in ds005114 is not estimable because the source paradigms are absent.

**Supplementary figures S1–S4.** S1, partial (added-variable) plots for the primary EEG predictors;
S2, Elastic Net coefficient path; S3, out-of-fold calibration; S4, resting-versus-ERP standardized
contribution from the full-panel (descriptive) model.

---

## 16. Tables

*Main tables are provided in `manuscript_submission/tables/` (Tables 1–5) and summarized below;
supplementary tables S1–S6 are in the Supplement.*

- **Table 1.** Dataset and cohort overview (ds003522, ds005114, ds003523, ds003490).
- **Table 2.** Participant flow and analytic sample.
- **Table 3.** Locked EEG feature panel.
- **Table 4.** Primary, secondary, supportive, and exploratory model results.
- **Table 5.** Replication feasibility matrix.

*(All numeric values in this manuscript are reproduced from the frozen analysis outputs in
`outputs/analysis/` and `outputs/metadata_summary_tables/`; see `submission_readiness_audit.md` for
the value-to-source map.)*
