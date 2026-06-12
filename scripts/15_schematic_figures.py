#!/usr/bin/env python
"""
15_schematic_figures.py
=======================
Render the three schematic manuscript figures (study/cohort flow, continuous-recording
structure, preprocessing+feature pipeline) from already-established facts. These are
drawings, not analyses: no outcome is read and no model is fit. Numbers are taken from the
frozen Phase 0-4 outputs.

Figures -> outputs/figures/
    fig_study_flow.png
    fig_recording_structure.png
    fig_pipeline.png
"""
from __future__ import annotations
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

FIG = Path(__file__).resolve().parents[1] / "outputs" / "figures"
FIG.mkdir(parents=True, exist_ok=True)
TEAL, ORANGE, GREY, SLATE = "#1b9e95", "#e6841e", "#777777", "#34495e"
plt.rcParams.update({"font.size": 8.5, "figure.dpi": 300})


def box(ax, x, y, w, h, text, fc="#eef3f6", ec=SLATE, fs=8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.02",
                                fc=fc, ec=ec, lw=1.1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, wrap=True)


def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=11,
                                 color=SLATE, lw=1.1))


def study_flow():
    fig, ax = plt.subplots(figsize=(6.6, 7.4)); ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    box(ax, .18, .90, .64, .065, "OpenNeuro ds003522 — acute mTBI / control / chronic TBI\n"
                                 "(BIDS; 3 sessions; 96 participants with EEG)", fc="#e8eef2")
    box(ax, .60, .785, .38, .07, "Excluded from outcome cohort:\n• Chronic TBI (n=25): no longitudinal outcome\n"
                                 "• Controls: not in within-mTBI prediction", fc="#f4f0e8", fs=7)
    box(ax, .18, .80, .34, .05, "Acute mTBI arm (Group 0)", fc=TEAL+"33")
    box(ax, .18, .70, .34, .055, "with usable Session-1 EEG\n(read QC: 25/25 readable)", fc=TEAL+"33")
    box(ax, .14, .595, .44, .065, "Eligible discovery cohort:\nacute mTBI + S1 EEG + S3 NSI total\nn = 25", fc=TEAL+"55")
    # modality split
    box(ax, .04, .43, .28, .085, "Resting (eyes-closed)\nusable\nn = 25", fc=TEAL+"33", fs=8)
    box(ax, .36, .43, .28, .095, "ERP usable\nn = 21\n(−sub-040 no tone labels;\n−3 with <15 rare-tone epochs)", fc=ORANGE+"33", fs=7.5)
    box(ax, .68, .43, .28, .085, "Combined panel\n(primary model)\nn = 21", fc="#e0e6ea", fs=8)
    box(ax, .30, .30, .40, .06, "Frozen subject-level CV folds (seed 42)\nfixed BEFORE feature extraction", fc="#dfeae4", fs=7.5)
    box(ax, .12, .17, .76, .075, "Pre-registered, leakage-safe modeling (Phase 4):\nprimary OLS · Elastic Net · supportive · transparency · exploratory\n"
                                 "scaling/imputation/tuning fit within training folds only", fc="#eef3f6", fs=7.5)
    box(ax, .12, .055, .76, .065, "Planned replication (ds005114): INFEASIBLE — 0/8 locked features extractable\n"
                                  "(no rest, no oddball). Discovery null untested in independent data.", fc="#fdecea", ec="#c0392b", fs=7.5)
    for a in [(.5,.90,.5,.855),(.35,.80,.35,.755),(.35,.70,.35,.66),(.36,.595,.18,.515),
              (.36,.595,.5,.525),(.36,.595,.82,.515),(.5,.43,.5,.36),(.5,.30,.5,.245),
              (.5,.17,.5,.12)]:
        arrow(ax, *a)
    arrow(ax, .52, .82, .60, .82)
    ax.set_title("Figure 1. Study design and cohort flow", fontsize=10, loc="left")
    fig.savefig(FIG / "fig_study_flow.png", bbox_inches="tight"); plt.close(fig)


def recording_structure():
    fig, ax = plt.subplots(figsize=(8.4, 2.6)); ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    segs = [("Eyes\nClosed", TEAL, .10), ("Eyes\nOpen", TEAL, .10),
            ("Oddball run 1\n(Standard / Target / Novel)", ORANGE, .22),
            ("Eyes\nClosed", TEAL, .10), ("Eyes\nOpen", TEAL, .10),
            ("Oddball run 2\n(Standard / Target / Novel)", ORANGE, .22)]
    x = .03
    for label, c, w in segs:
        ax.add_patch(FancyBboxPatch((x, .35), w, .34, boxstyle="round,pad=0.005",
                                    fc=c + "55", ec=c, lw=1.3))
        ax.text(x + w / 2, .52, label, ha="center", va="center", fontsize=8)
        x += w + .004
    ax.annotate("", xy=(x, .30), xytext=(.03, .30),
                arrowprops=dict(arrowstyle="-|>", color=SLATE, lw=1.2))
    ax.text(.5, .20, "continuous recording, ~15–28 min  •  single boundary event at t = 0 (no internal splices)",
            ha="center", fontsize=8, color="#444")
    ax.text(.03, .80, "Rest (eyes-closed/eyes-open)  →  resting spectral & aperiodic features",
            fontsize=7.5, color=TEAL)
    ax.text(.55, .80, "Oddball  →  P3b (Target) / P3a (Novel) ERPs", fontsize=7.5, color=ORANGE)
    ax.set_title("Figure 2. Structure of the ds003522 continuous Session-1 recording", fontsize=10, loc="left")
    fig.savefig(FIG / "fig_recording_structure.png", bbox_inches="tight"); plt.close(fig)


def pipeline():
    fig, ax = plt.subplots(figsize=(7.2, 4.6)); ax.axis("off")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    steps = [
        "Raw EEGLAB .set/.fdt — 500 Hz, 65 ch, online ref CPz  (raw retained unmodified)",
        "Type non-EEG channels (VEOG→EOG, EKG→ECG)",
        "Boundary-aware: 'boundary' → BAD_boundary; segment-wise filter guard",
        "Notch 60 Hz  →  band-pass 0.5–45 Hz (FIR)",
        "Reinstate CPz → standard 10–20 montage → average reference (64 EEG)",
        "Within-subject bad-channel detection (robust z>4) → interpolation",
    ]
    y = .88
    for s in steps:
        box(ax, .06, y, .70, .072, s, fc="#eef3f6", fs=7.3);
        if y > .2: arrow(ax, .41, y, .41, y - .026)
        y -= .098
    # branch
    box(ax, .06, .12, .34, .12, "Resting branch (0.5–45 Hz)\nEC/EO blocks → Welch PSD →\nIAF, aperiodic exp, θ/α, occ. α", fc=TEAL+"33", fs=7)
    box(ax, .44, .12, .34, .12, "ERP branch (+40 Hz low-pass)\nepoch tones → P3b (Target)\nP3a (Novel): amp & latency", fc=ORANGE+"33", fs=7)
    arrow(ax, .25, .295, .23, .24); arrow(ax, .57, .295, .61, .24)
    ax.text(.83, .55, "No outcome\ninformation\nused at any\nstep", rotation=90, ha="center",
            va="center", fontsize=8, color="#c0392b",
            bbox=dict(boxstyle="round", fc="#fdecea", ec="#c0392b"))
    ax.set_title("Figure 3. EEG preprocessing and feature-extraction pipeline", fontsize=10, loc="left")
    fig.savefig(FIG / "fig_pipeline.png", bbox_inches="tight"); plt.close(fig)


def main():
    study_flow(); recording_structure(); pipeline()
    print("Schematic figures written: fig_study_flow.png, fig_recording_structure.png, fig_pipeline.png")


if __name__ == "__main__":
    main()
