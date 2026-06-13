# ds003490 Download Smoke Test

Status: succeeded for a targeted single-recording download.

Official OpenNeuro CLI 5.2.0 was available only through the explicit Deno executable in this shell; its download command supports whole-dataset downloads only (dataset, destination, version/draft). The installed `openneuro.cmd` shim is present but fails because `deno` is not on PATH.

The minimal raw-data smoke test therefore used `openneuro-py` with `--include sub-001/ses-01/eeg` for ds003490 tag 1.1.0. This downloaded a real EEGLAB `.set`/`.fdt` pair, not just a manifest.

- `.set`: `data\openneuro\ds003490\sub-001\ses-01\eeg\sub-001_ses-01_task-Rest_eeg.set` (1518144 bytes)
- `.fdt`: `data\openneuro\ds003490\sub-001\ses-01\eeg\sub-001_ses-01_task-Rest_eeg.fdt` (78818800 bytes)
- MNE status: read_ok

No full D2 analysis was started.
