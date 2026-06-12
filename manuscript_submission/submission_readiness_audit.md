# Submission Readiness Audit (Final)

**Audit date:** 2026-06-12
**Status:** **Manuscript package finalized — zero unresolved placeholders.** Local repository
created and committed. Remote publish to GitHub is the only remaining step and requires the author's
authenticated GitHub account (commands in §4).

## 1. Placeholder count (target: all zero)

| Token | Count |
|---|---:|
| `[AUTHOR VERIFY]` | 0 |
| `[REFERENCE NEEDED]` | 0 |
| `TODO` | 0 |
| `PLACEHOLDER` | 0 |
| `COMMIT_HASH_PENDING` | 0 |

All author, affiliation, email, ORCID, ethics, funding, conflicts, data/code-availability, and
reference placeholders have been resolved with verified values. Unverifiable facts (e.g., journal
fees) were omitted rather than invented.

## 2. Overclaiming scan (manuscript prose)

| Term | Result |
|---|---|
| proven | 0 |
| validated | 0 (the only uses state *no validated threshold* and *not a validated prognostic tool*) |
| confirmed | 0 |
| diagnostic biomarker | 0 |
| predictive biomarker | 0 |
| failed replication | 0 (wording is "replication was infeasible") |

Calibrated language ("no stable evidence", "inconclusive", "underpowered", "did not generalize",
"replication was infeasible") is used throughout.

## 3. Sample-size consistency (by role)

| N | Role |
|---:|---|
| 25 | Eligible discovery cohort (acute mTBI, S1 EEG + S3 NSI); resting-only model |
| 21 | Primary, secondary, transparency, and ERP-only models (ERP reliability gate) |
| 20 | Prespecified sensitivity (additionally drops one eyes-open-low subject) |
| 91 | ds005114 Session-1 recordings scanned for replication feasibility |

Each value is used only in its correct role; none is interchanged.

## 4. Git integrity

| Item | Value |
|---|---|
| Repository (intended remote) | https://github.com/gblakepierpoint/openneuro-tbi-eeg-biomarker-reanalysis |
| Current branch | `main` |
| Package commit | `a995ac0` (`a995ac0edddf83fb2a381e253dc6e17f7053f230`) — full analysis + manuscript package |
| Remote / public status | **Not yet pushed in this environment** — GitHub CLI (`gh`) is not installed/authenticated here |
| Large raw EEG excluded | Yes — `.gitignore` excludes `data/`, `*.set/.fdt/.fif/.edf/.mat/.xlsx`, `.venv/`; staging audit confirmed 0 such files staged |
| Credentials staged | None |

**To publish (author runs once authenticated):**
```bash
# Option A — GitHub CLI:
gh auth status            # authenticate first if needed: gh auth login
gh repo create gblakepierpoint/openneuro-tbi-eeg-biomarker-reanalysis \
  --public --source=. --remote=origin \
  --description "Leakage-safe OpenNeuro EEG/mTBI biomarker reanalysis and replication feasibility study" \
  --push
# Option B — existing remote:
git remote add origin https://github.com/gblakepierpoint/openneuro-tbi-eeg-biomarker-reanalysis.git
git push -u origin main
# Suggested topics: openneuro eeg mild-traumatic-brain-injury mtbi clinical-neurophysiology
#                   reproducibility machine-learning biomarkers
```
After pushing, confirm the repository is public and commit `a995ac0` is present.

## 5. Result integrity (no results changed)

| Artifact | MD5 (first 8) | Status |
|---|---|---|
| `outputs/splits/frozen_cv_folds.csv` | `453fede5` | unchanged |
| `outputs/analysis/model_coefficients.csv` | `5f3d418e` | unchanged |
| `outputs/analysis/cv_performance.csv` | `660825f0` | unchanged |
| `outputs/features/*` | — | unchanged |

No new statistical models were run during finalization. The only scripts executed were marker scans
and figure rendering (`13`–`15`), which read no outcome and fit no model. The locked statistical
hierarchy and sample sizes are unchanged.

## 6. Manuscript readiness

| Item | Status |
|---|---|
| Abstract word count | ~288 words (within 250–300) |
| Figures present | 7 main + 4 supplementary (11 PNGs in `figures/`) |
| Tables present | 5 main (`tables/`) + 6 supplementary (`supplement/supplementary_tables.md`) |
| Supplement present | methods, tables, figures, final locked plan, replication audit |
| References present | 26 Vancouver-numbered; `references.bib` (26 entries); all cited, all in list (verified bidirectionally) |
| Cover letter | Present, finalized (single author, no funding, no conflicts, IRB-exempt) |
| Title page | Present, finalized |
| Data availability | Present (four OpenNeuro DOIs; raw not redistributed) |
| Code availability | Present (GitHub URL + commit `a995ac0`, MIT) |
| Ethics statement | Present (IRB-exempt; public deidentified data; no protocol number) |
| Conflicts statement | Present (none) |
| Funding statement | Present (none) |
| AI assistance disclosure | Present (acknowledgments; AI not an author) |

## 7. Remaining issues

**None internal to the package.** The single external action is the author-authenticated GitHub push
(§4); the manuscript already cites the canonical repository URL and commit, and `code_availability.md`
flags that the public push should be confirmed before the statement is relied upon in a submission.
After selecting a target journal, apply that journal's formatting, word limits, and highlight format
(the highlights file already provides a ≤85-character set).

## Number-to-source map (headline values)

| Reported value | Source |
|---|---|
| Primary n = 21; adj R² = −0.19; R² = 0.11; F p = 0.86 | `outputs/analysis/model_fit_summary.csv` |
| P3b std β = +0.24, 95% CI −0.40 to 0.88; FDR p ≈ 0.96 | `outputs/analysis/model_coefficients.csv` |
| OOF R²: baseline −0.40, primary −1.38, EN −0.06, full OLS −3.58, RF −0.29, XGB −0.36 | `outputs/analysis/cv_performance.csv` |
| Elastic Net all 10 coefficients = 0 | `outputs/analysis/elasticnet_coefficients.csv` |
| Resting-only n = 25; ERP-only n = 21 | `outputs/analysis/model_fit_summary.csv` |
| Outcome n = 25: mean 15.1, SD 15.7, median 9, range 0–51; skew 0.85 → raw NSI | `outputs/analysis/ds003522_s1_analysis_table.csv`; `reports/phase4_results.md` |
| ds005114 0/91 rest, 0/91 oddball, 91/91 DPX; 0/8 features | `reports/phase5_replication_results.md`; `outputs/analysis/replication_feature_availability.csv` |
| ds003490 8/8 features but Parkinson's (50; 25 PD/25 control; 2 sessions) | `outputs/analysis/replication_feature_availability.csv`; OpenNeuro ds003490 |
| 25/25 readable EEG; no feasibility-threatening QC failures | `reports/phase2_eeg_qc_report.md`; `outputs/qc/ds003522_s1_qc_summary.csv` |
| Dataset DOIs/versions | OpenNeuro `dataset_description.json` (verified) |
