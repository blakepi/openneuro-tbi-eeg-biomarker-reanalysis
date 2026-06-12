#!/usr/bin/env python
"""
14_replication_figures.py
=========================
Phase 5 figures. Because no locked feature is extractable in ds005114, there are no
replication coefficients to plot against discovery; the figures therefore depict (1) the
frozen discovery estimates annotated with their replication status, and (2) the
feature-availability matrix that explains why an outcome replication is infeasible.

Figures -> outputs/figures/
    fig_discovery_vs_replication_forest.png
    fig_feature_availability_matrix.png      (serves as the coefficient-agreement panel)
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
AN = ROOT / "outputs" / "analysis"
FIG = ROOT / "outputs" / "figures"
FIG.mkdir(parents=True, exist_ok=True)
TEAL, ORANGE, GREY, RED = "#1b9e95", "#e6841e", "#777777", "#c0392b"
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 300})
FAMILY = {"Global_Aperiodic_Exponent": "rest", "Posterior_IAF": "rest", "P3b_Amplitude": "erp"}
COL = {"rest": TEAL, "erp": ORANGE, "cov": GREY}


def fig_forest():
    disc = pd.read_csv(AN / "model_coefficients.csv")
    disc = disc[disc.model == "primary_parsimonious"]
    disc = disc[disc.predictor.isin(["Global_Aperiodic_Exponent", "Posterior_IAF",
                                     "P3b_Amplitude"])].iloc[::-1]
    fig, ax = plt.subplots(figsize=(7.0, 2.8))
    y = np.arange(len(disc))
    for yi, (_, r) in zip(y, disc.iterrows()):
        c = COL[FAMILY[r.predictor]]
        ax.errorbar(r.std_beta, yi, xerr=[[r.std_beta - r.std_ci_low], [r.std_ci_high - r.std_beta]],
                    fmt="o", color=c, ecolor=c, capsize=3, ms=7, lw=1.4)
    ax.axvline(0, color="k", lw=0.8, ls="--")
    ax.set_yticks(y); ax.set_yticklabels(disc.predictor)
    ax.set_xlabel("Standardized β (95% CI) — DISCOVERY (ds003522, n=21)")
    ax.set_xlim(-1.1, 1.1)
    # replication-status band on the right
    ax.text(1.16, 0.5, "REPLICATION (ds005114)\nNOT ESTIMABLE\nparadigm & rest absent",
            transform=ax.get_yaxis_transform(), ha="left", va="center", fontsize=8,
            color=RED, bbox=dict(boxstyle="round", fc="#fdecea", ec=RED, lw=1))
    ax.set_title("Discovery estimates and replication status", fontsize=9)
    fig.subplots_adjust(right=0.62, left=0.28)
    fig.savefig(FIG / "fig_discovery_vs_replication_forest.png", bbox_inches="tight")
    plt.close(fig)


def fig_matrix():
    av = pd.read_csv(AN / "replication_feature_availability.csv")
    feats = ["Global_Aperiodic_Exponent", "Posterior_IAF", "Frontal_Theta_Alpha_Ratio",
             "Occipital_Relative_Alpha", "P3b_Amplitude", "P3b_Latency",
             "P3a_Amplitude", "P3a_Latency"]
    order = ["ds003522", "ds005114", "ds003523", "ds003490"]
    labels = {"ds003522": "ds003522\n(discovery, mTBI)",
              "ds005114": "ds005114\n(DPX, mTBI)",
              "ds003523": "ds003523\n(VWM, TBI)",
              "ds003490": "ds003490\n(oddball+rest, PARKINSON'S)"}
    M = np.zeros((len(order), len(feats)))
    for i, ds in enumerate(order):
        for j, f in enumerate(feats):
            v = av[(av.dataset == ds) & (av.feature == f)].extractable_locked_definition
            M[i, j] = 1 if (len(v) and bool(v.iloc[0])) else 0
    fig, ax = plt.subplots(figsize=(8.6, 3.0))
    ax.imshow(M, cmap=ListedColormap(["#fadbd8", "#abebc6"]), vmin=0, vmax=1, aspect="auto")
    for i in range(len(order)):
        for j in range(len(feats)):
            ax.text(j, i, "✓" if M[i, j] else "✗", ha="center", va="center",
                    color="#1e7d44" if M[i, j] else "#922b21", fontsize=11, fontweight="bold")
    ax.set_xticks(range(len(feats)))
    ax.set_xticklabels([f.replace("_", "\n") for f in feats], fontsize=6.5)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([labels[d] for d in order], fontsize=7.5)
    # family band under x labels
    for j, f in enumerate(feats):
        ax.add_patch(plt.Rectangle((j - 0.5, len(order) - 0.5), 1, 0.08,
                     color=TEAL if j < 4 else ORANGE, clip_on=False))
    ax.set_title("Extractability of the locked feature panel by dataset\n"
                 "(green = extractable with preregistered definition)", fontsize=9)
    note = ("ds005114 & ds003523: no eyes-closed rest, no auditory oddball → 0/8.   "
            "ds003490: 8/8 features BUT Parkinson's cohort with no post-concussive outcome.")
    fig.text(0.5, -0.02, note, fontsize=7, color="#444", ha="center", va="top")
    fig.tight_layout()
    fig.savefig(FIG / "fig_feature_availability_matrix.png", bbox_inches="tight")
    plt.close(fig)


def main():
    fig_forest()
    fig_matrix()
    print("Replication figures written:")
    for f in ["fig_discovery_vs_replication_forest.png", "fig_feature_availability_matrix.png"]:
        print("  ", f)


if __name__ == "__main__":
    main()
