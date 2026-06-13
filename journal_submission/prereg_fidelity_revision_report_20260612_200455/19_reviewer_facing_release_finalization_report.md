# Reviewer-Facing Release Finalization Report

Date: 2026-06-13

Decision: Ready

## Scope

This final pass performed text-integrity and release-package cleanup only. No analyses were rerun, and no scientific results, locked features, folds, models, or conclusions were changed.

## Confirmed Fixes

- Main manuscript duplicate and orphaned fragments were removed from Methods, Results, Discussion, Limitations, and Conclusions.
- Table 4B now states that all EEG models had negative out-of-fold R2 and explains the penalized-model comparison as shrinkage toward a mean/intercept predictor rather than evidence for a reproducible EEG feature signal.
- The secondary Rivermead-change result is described as secondary, unstable, not externally replicated, and hypothesis-generating.
- Supplement S.3 contains one clean outcome-definition paragraph with the Session 3 minus Session 1 change-score convention.
- Supplementary tables render in sequential order from S1 through S11.
- Production-only comments and blank supplementary-figure placeholders were excluded from the final files.
- Cover letter contains the required publication, funding, and conflict-of-interest declaration.
- Repository release metadata were prepared for tag `v1.0.0-cnp-submission`.

## Rendered QA

Microsoft Word export completed for:

- `main_manuscript_cnp.docx`
- `supplement_cnp.docx`
- `title_page_cnp.docx`
- `cover_letter_cnp.docx`
- `highlights.docx`

Rendered PDFs, text extracts, page PNGs, and contact sheets were generated under:

`journal_submission/prereg_fidelity_revision_report_20260612_200455/visual_qa/`

Visual inspection confirmed clean rendered PDFs/contact sheets for the main manuscript, supplement, title page, cover letter, and highlights. Detailed inspection of Table 4B and Supplementary Tables S7-S8 showed no overlap or broken table layout after the final table-formatting pass.

## Final String and Structure Checks

The active final DOCX files and freshly rendered TXT extracts were searched for the requested banned fragments. No hits were found.

Additional checks confirmed:

- Main manuscript citation first appearances run 1 through 26 in order in all Markdown manuscript copies.
- Highlight bullets are all <=85 characters.
- Supplementary tables appear in order S1-S11 in the source and rendered TXT.
- Figure S5 is listed as `FigureS5_specparam_fit_quality.png`.
- Submission manifest was refreshed after the final render.

## Release Notes

The final GitHub release should use tag:

`v1.0.0-cnp-submission`

Zenodo archiving should be performed from the public GitHub release after the tag is pushed. The DOI remains pending until Zenodo archives that release.
