# Visual QA Report

Timestamp: 2026-06-13 13:40:12 -04:00

## Render Method

Rendered the current submission DOCX files with Microsoft Word COM using:

`audit/render_prereg_submission_docx_word.py`

Outputs were written to:

`journal_submission/prereg_fidelity_revision_report_20260612_200455/visual_qa/`

The render pass exported each DOCX to PDF, exported plain text for scan checks, rendered PDF pages to PNG with `pdftoppm`, and produced contact sheets.

## Rendered Files

| File | PDF pages | QA artifacts |
|---|---:|---|
| title_page_cnp.docx | 2 | PDF, text export, page PNGs, contact sheet |
| cover_letter_cnp.docx | 1 | PDF, text export, page PNGs, contact sheet |
| main_manuscript_cnp.docx | 20 | PDF, text export, page PNGs, contact sheet |
| supplement_cnp.docx | 23 | PDF, text export, page PNGs, contact sheet |
| highlights.docx | 1 | PDF, text export, page PNGs, contact sheet |

Manifest: `visual_qa/render_manifest.csv`

## Visual Inspection

Contact sheets inspected:

- `visual_qa/contact_sheet_title_page_cnp.png`
- `visual_qa/contact_sheet_cover_letter_cnp.png`
- `visual_qa/contact_sheet_main_manuscript_cnp.png`
- `visual_qa/contact_sheet_supplement_cnp.png`
- `visual_qa/contact_sheet_highlights.png`

Detailed page PNGs inspected for the changed sections:

- `visual_qa/main_manuscript_cnp/page-19.png`
- `visual_qa/supplement_cnp/page-06.png`
- `visual_qa/supplement_cnp/page-07.png`
- `visual_qa/supplement_cnp/page-08.png`
- `visual_qa/supplement_cnp/page-09.png`
- `visual_qa/supplement_cnp/page-10.png`
- `visual_qa/supplement_cnp/page-11.png`

Result: no blank pages, broken table order, production-note pages, empty supplementary-image placeholders, or unreadable page-scale rendering problems were observed. Main Table 4B renders with the revised out-of-fold performance note. Supplementary Tables S1-S11 render sequentially, and the Figure S5 file entry is present as `FigureS5_specparam_fit_quality.png`.

## Text Scan

Rendered TXT exports for the five final DOCX files were scanned for the user-specified forbidden copy-merge and production strings.

Final rendered-DOCX scan result: no hits.

Positive confirmations in rendered text:

- cover letter includes the replacement conflict/funding/COI declaration
- main Table 4B includes the revised least-poor penalized-model note
- supplement S.3 contains the clean outcome-construction sentence
- supplement tables are sequential from S1 through S11
- supplement figure file list includes `FigureS5_specparam_fit_quality.png`

## Manifest

`journal_submission/submission_file_manifest.csv` was regenerated after final render. Current page counts are main manuscript 20, supplement 23, title page 2, cover letter 1, highlights 1. The manifest includes Figure S5 and Supplementary Tables S7-S11.

## Conclusion

Visual QA complete. No blocking formatting, stale production-note, duplicate-fragment, or package-render issue remains.
