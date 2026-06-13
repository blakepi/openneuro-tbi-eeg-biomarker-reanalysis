# Attrition Completer Definition

- Universe: 44 ds003522 group-code-0 mTBI participants with Session-1 EEG records and Session-1 clinical rows in the public BIDS/BigAgg metadata.
- S3 completers: 25 participants with non-missing Session-3 NSI total.
- S3 non-completers: 19 participants without Session-3 NSI total.
- EEG feature extraction for non-completers was not available locally because raw EEG was downloaded and processed only for the frozen analytic cohort with S3 outcome.
- The locked plan did not define an operational imbalance threshold for triggering IPW; therefore IPW was not added post hoc.
