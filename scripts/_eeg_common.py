"""
_eeg_common.py
==============
Shared, pre-registered constants for the ds003522 Session-1 feature pipeline
(scripts 06-09). Centralising these guarantees that preprocessing, rest features,
and ERP features all use identical montage / region / band definitions, and that
nothing here depends on the outcome (no leakage, no outcome-driven tuning).
"""
from __future__ import annotations
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "ds003522"
PROC_DIR = PROJECT_ROOT / "data" / "processed" / "ds003522_s1"
FEAT_DIR = PROJECT_ROOT / "outputs" / "features"
LOG_DIR = PROC_DIR / "logs"

# ---- acquisition facts (from *_eeg.json / channels.tsv, Phase 2/3 inspection) ----
SFREQ = 500.0
LINE_FREQ = 60.0
ONLINE_REF = "CPz"            # online reference; re-added before average reference
NON_EEG = {"VEOG": "eog", "EKG": "ecg"}   # channel-name -> MNE type

# ---- preprocessing parameters (frozen) ----
HP_HZ = 0.5                   # high-pass: removes DC/drift behind the EXTREME_AMP flag
LP_BROADBAND_HZ = 45.0        # saved broadband low-pass (serves spectral analysis)
LP_ERP_HZ = 40.0             # extra low-pass applied only in the ERP branch
MONTAGE = "standard_1020"
REFERENCE = "average"
BAD_CHAN_Z = 4.0              # |robust z of log-variance| beyond this -> bad (within-subject)

# ---- clinically meaningful scalp regions (10-10 labels; covers all 64 incl CPz) ----
REGIONS = {
    "frontal":   ["Fp1", "Fp2", "AF7", "AF3", "AFz", "AF4", "AF8",
                  "F7", "F5", "F3", "F1", "Fz", "F2", "F4", "F6", "F8",
                  "FT9", "FT7", "FT8", "FT10"],
    "central":   ["FC5", "FC3", "FC1", "FCz", "FC2", "FC4", "FC6",
                  "C5", "C3", "C1", "Cz", "C2", "C4", "C6", "T7", "T8",
                  "CP5", "CP3", "CP1", "CPz", "CP2", "CP4", "CP6",
                  "TP9", "TP7", "TP8", "TP10"],
    "parietal":  ["P7", "P5", "P3", "P1", "Pz", "P2", "P4", "P6", "P8"],
    "occipital": ["PO7", "PO3", "POz", "PO4", "PO8", "O1", "Oz", "O2"],
}
# "global" region = all scalp EEG channels (handled in code)

# ---- spectral bands (Hz) ----
BANDS = {"delta": (1.0, 4.0), "theta": (4.0, 8.0),
         "alpha": (8.0, 12.0), "beta": (13.0, 30.0)}
TOTAL_BAND = (1.0, 45.0)     # denominator for relative power
IAF_BAND = (7.0, 13.0)       # individual alpha peak search window
WELCH_WIN_S = 2.0            # Welch segment length
WELCH_OVERLAP = 0.5

# ---- resting segmentation marker labels (BIDS trial_type) ----
REST_LABELS = {"eyes_closed": "Eyes Closed: Every 1000 ms",
               "eyes_open":   "Eyes Open: Every 1000 ms"}
REST_GAP_S = 3.0             # gap > this splits marker train into separate blocks
REST_SEG_S = 2.0            # non-overlapping analysis segments within a rest block
REST_REJECT_UV = 150.0      # peak-to-peak reject threshold for a rest segment (uV)

# ---- oddball ERP definitions (BIDS trial_type names; pre-registered windows) ----
ERP_CONDITIONS = {"standard": "Standard Tone",
                  "target":   "Target Tone",
                  "novel":    "Novel Tone"}
ERP_TMIN, ERP_TMAX = -0.2, 0.8
ERP_BASELINE = (-0.2, 0.0)
ERP_REJECT_UV = 150.0        # peak-to-peak epoch reject (uV) on EEG
ERP_PICKS = {
    "P3a": ["Fz", "FCz", "Cz"],     # frontocentral, Novel
    "P3b": ["Pz", "CPz", "POz"],    # parietal, Target
    "N2":  ["Fz", "FCz", "Cz"],     # frontocentral
}
ERP_WINDOWS = {                      # seconds
    "P3a": (0.250, 0.400),
    "P3b": (0.300, 0.600),
    "N2":  (0.200, 0.350),
}


def region_of(ch: str) -> str | None:
    for region, chans in REGIONS.items():
        if ch in chans:
            return region
    return None
