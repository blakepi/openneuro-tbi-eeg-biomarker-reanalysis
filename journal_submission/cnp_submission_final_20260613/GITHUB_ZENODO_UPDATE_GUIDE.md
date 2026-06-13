# GitHub / Zenodo metadata synchronization guide

Goal: make the public repository, GitHub release page, CITATION.cff, .zenodo.json, README, and manuscript DOI language all say the same thing.

Current preferred title:

Leakage-Safe EEG Biomarker Analysis After Mild Traumatic Brain Injury: An Internally Locked OpenNeuro Reanalysis and Replication Feasibility Study

Current DOI in manuscript materials:

10.5281/zenodo.20682573

## Option A - fastest cleanup if the DOI is already minted for v1.0.0

Use this if Zenodo already shows DOI 10.5281/zenodo.20682573 for the v1.0.0-cnp-submission archive and you do not want to mint a new version.

```powershell
cd C:\Research\EEG\openneuro-tbi-eeg-biomarker-reanalysis

git status

# Replace remaining repo metadata wording from the old public-preregistration title/framing
# to the current internally locked title/framing, and replace any stale DOI-placeholder text
# with the DOI below.

git diff -- README.md CITATION.cff .zenodo.json RELEASE_NOTES_CNP_SUBMISSION.md
git add README.md CITATION.cff .zenodo.json RELEASE_NOTES_CNP_SUBMISSION.md
git commit -m "Synchronize CNP repository and Zenodo metadata"
git push
```

Then update the existing GitHub release notes without changing the tag:

```powershell
# Requires GitHub CLI authenticated with: gh auth login
$notes = Get-Content RELEASE_NOTES_CNP_SUBMISSION.md -Raw
gh release edit v1.0.0-cnp-submission --title "CNP submission package" --notes "$notes"
```

Browser alternative: GitHub repo -> Releases -> v1.0.0-cnp-submission -> pencil/edit -> replace the body with RELEASE_NOTES_CNP_SUBMISSION.md -> Update release.

Zenodo browser check: Zenodo -> profile menu -> GitHub -> select this repository/release -> confirm the release succeeded and the record DOI is 10.5281/zenodo.20682573. If the Zenodo record title still uses the old public-preregistration title, edit the Zenodo record metadata title manually to the current "Internally Locked" title if Zenodo allows it for the published record.

## Option B - cleanest archival provenance if v1.0.0 source archive captured older metadata

Use this if you want the source archive itself to contain the fixed README/CITATION/.zenodo files. This creates a new GitHub release and usually a new Zenodo version DOI. After Zenodo mints the DOI, update the manuscript Code availability section and cover letter before upload.

```powershell
cd C:\Research\EEG\openneuro-tbi-eeg-biomarker-reanalysis

git status
# First run the text replacement and commit steps from Option A, if not already done.

git tag v1.0.1-cnp-submission
git push origin main
git push origin v1.0.1-cnp-submission

$notes = Get-Content RELEASE_NOTES_CNP_SUBMISSION.md -Raw
gh release create v1.0.1-cnp-submission --title "CNP submission package v1.0.1" --notes "$notes"
```

Then in Zenodo: profile menu -> GitHub -> select repository -> wait for v1.0.1-cnp-submission to process -> open record DOI. Copy the new DOI into:

- README.md
- CITATION.cff
- .zenodo.json description or identifiers if needed
- main manuscript Code availability section
- cover letter data/code availability paragraph
- title page only if you add a DOI/deposition note there

## Final verification checklist

```powershell
git grep -n "<old-title-or-stale-doi-placeholder-or-stale-registered-secondary-sensitivity-wording>"
gh release view v1.0.0-cnp-submission --json tagName,name,body,url
```

Expected: no accidental old public-preregistration wording remains unless it appears only in historical notes clearly labelled as historical. The GitHub release body should no longer contain stale DOI-placeholder language if the DOI is minted.
