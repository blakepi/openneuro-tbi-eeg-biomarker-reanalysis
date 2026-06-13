# Preregistration-Fidelity Revision Change Log

Timestamp: 20260612_200455

## Backup
- Created backup directory: journal_submission\pre_prereg_fidelity_revision_backup_20260612_200455
- Created output directory: outputs\prereg_fidelity_revision_20260612_200455
- Created report directory: journal_submission\prereg_fidelity_revision_report_20260612_200455

## Changes
- Completed targeted preregistration-fidelity and reviewer-hardening revision without altering locked feature definitions, subject identity rules, frozen folds, or primary Phase 6 results.

## Preregistration-fidelity manuscript integration
- Added prespecified secondary outcome reporting; H4 S1-to-S3 Rivermead change showed a secondary P3b association that is explicitly not promoted to the primary conclusion.
- Added sensitivity-battery reporting and documented non-executed 0.1-Hz high-pass and sub-040 S-code branches.
- Added completer/non-completer attrition comparison and IPW rationale.
- Reconciled n = 20 vs n = 21 in main text and supplement execution notes.
- Softened OOF R2/model-ranking language and clarified Phase 6 as internal computational reproducibility, not external validation.
- Updated terminology to sub-acute/early post-injury mTBI and documented public BIDS n = 44.
- Added specparam fit-quality table and Figure S5 distribution; added ocular/bad-channel/alpha-window caveats.
- Updated article type, title-page counts, cover letter, highlights, table sources, figure package, and submission manifest.

## Final packaging and QA corrections
- Inserted Supplementary Figure S5 into the rendered supplement image appendix after visual QA showed S5 was cited and packaged but not appended as an image page.
- Replaced stale rendered main-manuscript legend text from Supplementary Figures S1-S4 to S1-S5.
- Replaced overstrong `generalizable prediction` wording with held-out-performance language.
- Corrected title-page abstract word count to 237 words.
- Regenerated Word/PDF/TXT/PNG/contact-sheet QA outputs under `visual_qa/`.
- Regenerated `journal_submission/submission_file_manifest.csv` after final render.

## Author approval wording check
- Tightened the prespecified Rivermead-change wording in the abstract, Results, Discussion, highlights, Limitations, and Supplementary Table S7 to state that the P3b association is secondary and hypothesis-generating, was not externally replicated, and does not alter the primary Session-3 NSI conclusion.
- Updated final readiness decision to `Ready` after the Rivermead-change wording check.

## Emergency final text-integrity cleanup
- Cleaned remaining copy-merge artifacts in the final DOCX package without rerunning analyses or changing locked scientific results.
- Repaired Methods 2.4, Methods 2.8, Introduction, Discussion, Limitations, Conclusions, main Table 4B note, Supplement S.3/S.4, supplement table order, supplementary figure file list, and cover-letter declaration.
- Removed production-only supplement notes and the empty supplementary-image placeholder appendix.
- Re-rendered all DOCX files to PDF/TXT/PNG/contact sheets with Microsoft Word and visually inspected the changed pages.
- Regenerated `journal_submission/submission_file_manifest.csv` after final cleanup and render.

## Reviewer-facing repository finalization
- Reviewer-facing repository finalization updated README/package-state wording, removed process-history language, clarified the internal version-controlled analysis lock, defined S1-to-S3 change as Session 3 minus Session 1, renumbered references in first-citation order, and prepared release metadata for `v1.0.0-cnp-submission`. No scientific analyses were rerun.

## Zenodo DOI finalization
- Added Zenodo DOI `10.5281/zenodo.20682573` (https://doi.org/10.5281/zenodo.20682573) to citation, release, repository, and submission materials. No scientific analyses were rerun and no locked results were changed.
