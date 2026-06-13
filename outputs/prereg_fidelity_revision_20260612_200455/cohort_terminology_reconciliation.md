# Cohort Terminology Reconciliation

Local source checks:
- ds003522 README describes the dataset as control, sub-acute mild TBI, and chronic TBI, while dataset_description.json title uses 'Acute and Chronic TBI'.
- participants.json labels Group zero as mTBI, one as Control, and two as Chronic TBI.
- Public BIDS participants.tsv contains 44 Group-0 mTBI participants in ds003522.
- In the local clinical workbook, Session-1 days-since-injury for those 44 participants ranges from 1 to 16 days (median 11); 5/44 are outside a strict 3-14 day window.

Recommended wording: sub-acute/early post-injury mTBI at first mention, with the public README's 3-14 day description and the local metadata's 1-16 day observed range documented in the supplement.

n = 44 versus source-publication n = 38: the public BIDS metadata contains 44 group-code-0 mTBI participants with Session-1 EEG records. The exact reason a source article reports a smaller analytic subset was not verifiable from local BIDS metadata alone, so the manuscript should state that the present reanalysis follows the public BIDS metadata and documents subsequent outcome/ERP exclusions.
