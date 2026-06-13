# DOCX Conversion Notes

DOCX files were generated from the CNP Markdown sources in this folder using the bundled Codex Python runtime and `python-docx`.

Generated DOCX files:

- `journal_submission/main_manuscript_cnp.docx`
- `journal_submission/title_page_cnp.docx`
- `journal_submission/cover_letter_cnp.docx`
- `journal_submission/supplement_cnp.docx`
- `journal_submission/highlights.docx`

The DOCX files are editable Word documents suitable for portal upload. If further conversion is needed, use the Markdown files as the source of truth and convert with Pandoc or Word, preserving the same filenames and sections.

Render/visual QA note: automated DOCX creation and structural checks were performed in this environment. The packaged renderer could not complete visual QA because LibreOffice/soffice was not available on this system. Perform a final visual check in Microsoft Word before portal upload.
