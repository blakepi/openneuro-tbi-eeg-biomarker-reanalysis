# One-shot Codex prompt: synchronize GitHub/Zenodo metadata for CNP submission

You are working in the local repository:

C:\Research\EEG\openneuro-tbi-eeg-biomarker-reanalysis

Task: perform a repository-only metadata cleanup for a Clinical Neurophysiology Practice submission package. Do not rerun scientific analyses. Do not modify frozen outputs, feature files, CV folds, model outputs, figures, or raw/processed data. This is metadata/reviewer-facing documentation only.

Target manuscript/repository title:

Leakage-Safe EEG Biomarker Analysis After Mild Traumatic Brain Injury: An Internally Locked OpenNeuro Reanalysis and Replication Feasibility Study

Current DOI to use if already minted:

10.5281/zenodo.20682573
https://doi.org/10.5281/zenodo.20682573

Required edits:

1. Search the repo for inaccurate wording:
   - old public-preregistration title language;
   - lowercase public-preregistration claims;
   - stale DOI-placeholder language;
   - stale registered-secondary or registered-sensitivity phrasing in current manuscript/release text.

2. Replace public-facing manuscript/repository metadata wording so it consistently uses "Internally Locked" and "internally locked" rather than implying public preregistration. Historical locked-analysis-plan text may remain only if it is explicitly about the internal/version-controlled lock and does not imply a public registry entry.

3. Update README.md, CITATION.cff, .zenodo.json, RELEASE_NOTES_CNP_SUBMISSION.md, code_availability.md, and any repository metadata files that still show the old title or stale DOI-placeholder language.

4. Ensure release notes state:
   - the final title above;
   - the release is reviewer-facing and does not rerun or change frozen analyses;
   - primary result: no stable primary EEG predictive signal for Session-3 NSI symptom burden;
   - secondary result: P3b / S1-to-S3 Rivermead change is hypothesis-generating;
   - replication feasibility: no surveyed dataset matched both required EEG paradigm/state and post-concussive outcome structure;
   - Zenodo DOI: 10.5281/zenodo.20682573.

5. Validate metadata syntax:
   - parse .zenodo.json as JSON;
   - parse or at least sanity-check CITATION.cff as YAML if tooling is available;
   - run a targeted stale-language grep for old title, stale DOI-placeholder, and registered-secondary/sensitivity wording, then report remaining historical hits with justification.

6. Commit only metadata/reviewer-facing docs:

   git add README.md CITATION.cff .zenodo.json RELEASE_NOTES_CNP_SUBMISSION.md code_availability.md [any other metadata docs edited]
   git commit -m "Synchronize CNP repository and Zenodo metadata"

7. Do not create or push a tag unless explicitly instructed after review. Instead, print the exact commands for either:
   - updating the existing GitHub release notes for v1.0.0-cnp-submission using `gh release edit`, or
   - creating v1.0.1-cnp-submission if a new source archive is desired.

Acceptance criteria:

- No public-facing repo metadata implies public preregistration.
- No GitHub release notes say Zenodo DOI is pending if the DOI is already minted.
- README/CITATION/.zenodo/release notes/manuscript code-availability language are consistent.
- Scientific outputs are untouched.
- Git diff is small, explainable, and limited to metadata/reviewer-facing text.
