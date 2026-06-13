# Emergency Final Text-Integrity Cleanup Report

Timestamp: 2026-06-13 13:40:12 -04:00

## Scope

Text-integrity and package-render cleanup only. No scientific analyses were rerun, and no locked features, folds, models, estimates, or conclusions were changed.

## Files Updated

- `journal_submission/main_manuscript_cnp.docx`
- `journal_submission/supplement_cnp.docx`
- `journal_submission/cover_letter_cnp.docx`
- `journal_submission/main_manuscript_cnp.md`
- `journal_submission/main_manuscript_formatted.md`
- `journal_submission/supplement_cnp.md`
- `journal_submission/cover_letter_cnp.md`
- `journal_submission/cover_letter_formatted.md`
- `journal_submission/supplement/supplementary_figures.md`
- `journal_submission/prereg_fidelity_revision_report_20260612_200455/14_visual_qa_report.md`
- `journal_submission/submission_file_manifest.csv`

## Command Log

| Step | Command | Key output |
|---|---|---|
| DOCX text repair | `python audit/emergency_final_text_cleanup.py` | Updated main manuscript, supplement, and cover letter DOCX files. |
| Table pagination controls | `python audit/fix_docx_table_pagination.py` | Updated table pagination controls for main manuscript and supplement DOCX files. |
| Word render/export | `python audit/render_prereg_submission_docx_word.py` | Rendered Word QA package under `journal_submission/prereg_fidelity_revision_report_20260612_200455/visual_qa`. |
| Rendered TXT scan | `rg` over the user-specified forbidden-string set in `visual_qa/*.txt` | No hits. |
| Supplement table order | `rg -n "Table S[0-9]+\\." visual_qa/supplement_cnp.txt` | Rendered order confirmed as S1, S2, S3, S4, S5, S6, S7, S8, S9, S10, S11. |
| Positive rendered-text checks | `rg` for final Table 4B, cover-letter, S.3, and Figure S5 confirmation text | Confirmed final Table 4B note, replacement cover-letter declaration, clean S.3 outcome sentence, and Figure S5 filename. |
| Manifest refresh | `python audit/update_prereg_submission_manifest.py` | Regenerated `journal_submission/submission_file_manifest.csv` with 28 rows. |

## Visual Inspection

Microsoft Word-rendered contact sheets were inspected for:

- title page
- cover letter
- main manuscript
- supplement
- highlights

Detailed page PNGs were inspected for the changed main Table 4B and Supplementary Tables S7-S11/Figure S5 pages. The rendered PDFs/PNGs showed no duplicate fragments, no production-note pages, no blank supplementary figure placeholders, no nonsequential supplement tables, and no obvious unreadable table overlap.

## Verification Results

- Duplicated Methods 2.4 outcome-construction text removed.
- Methods 2.8 orphan fragment removed; one software/environment sentence remains.
- Introduction EEG sentence deduplicated.
- Table 4B note replaced with the final least-poor penalized-model wording.
- Duplicated Discussion opening and Elastic Net fragment removed.
- Limitations grammar and duplicated old paragraph corrected.
- Conclusions use sub-acute/early post-injury terminology.
- Supplement S.3 and S.4 copy-merge artifacts corrected.
- Supplementary Tables render sequentially S1-S11.
- Production-only notes and blank image-placeholder appendix removed.
- Figure S5 is listed as `FigureS5_specparam_fit_quality.png`.
- Cover-letter conflict/funding/COI declaration replaced as requested.

## Final Decision

Ready.
