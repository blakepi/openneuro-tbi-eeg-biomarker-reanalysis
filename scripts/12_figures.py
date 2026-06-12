#!/usr/bin/env python
"""
12_figures.py
=============
Phase 4 publication figures. All figures depict the pre-registered model outputs; none
introduces a new analysis. Family colours: resting = teal, ERP = orange, covariate = grey.

Figures -> outputs/figures/
    fig_coefficient_forest.png        standardized betas + 95% CI (primary model)
    fig_partial_effects.png           added-variable plots (primary EEG predictors)
    fig_elasticnet_path.png           coefficient shrinkage path vs penalty
    fig_calibration.png               out-of-fold calibration (ElasticNet, primary)
    fig_predicted_vs_observed.png     out-of-fold predicted vs observed NSI
    fig_family_contribution.png       resting vs ERP standardized contribution
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import enet_path
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
AN = ROOT / "outputs" / "analysis"
FIG = ROOT / "outputs" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

TEAL, ORANGE, GREY = "#1b9e95", "#e6841e", "#777777"
PANEL = ["Global_Aperiodic_Exponent", "Posterior_IAF", "Frontal_Theta_Alpha_Ratio",
         "Occipital_Relative_Alpha", "P3b_Amplitude", "P3b_Latency",
         "P3a_Amplitude", "P3a_Latency", "Age", "Sex"]
PRIMARY = ["Global_Aperiodic_Exponent", "Posterior_IAF", "P3b_Amplitude", "Age", "Sex"]
FAMILY = {"Global_Aperiodic_Exponent": "rest", "Posterior_IAF": "rest",
          "Frontal_Theta_Alpha_Ratio": "rest", "Occipital_Relative_Alpha": "rest",
          "P3b_Amplitude": "erp", "P3b_Latency": "erp", "P3a_Amplitude": "erp",
          "P3a_Latency": "erp", "Age": "cov", "Sex": "cov"}
COL = {"rest": TEAL, "erp": ORANGE, "cov": GREY}
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 300})


def load():
    df = pd.read_csv(AN / "ds003522_s1_analysis_table.csv")
    coef = pd.read_csv(AN / "model_coefficients.csv")
    cv = pd.read_csv(AN / "cv_performance.csv")
    oof = pd.read_csv(AN / "oof_predictions.csv")
    return df, coef, cv, oof


def subset(df, preds, need_erp):
    m = df[preds + ["S3_NSI_Total"]].notna().all(axis=1) & df["ec_rest_reliable"]
    if need_erp:
        m = m & df["erp_reliable"]
    return df[m].copy()


def fig_forest(coef):
    c = coef[coef.model == "primary_parsimonious"].copy()
    c["fam"] = c.predictor.map(FAMILY)
    c = c.iloc[::-1]
    fig, ax = plt.subplots(figsize=(5.2, 3.0))
    y = np.arange(len(c))
    ax.errorbar(c.std_beta, y, xerr=[c.std_beta - c.std_ci_low, c.std_ci_high - c.std_beta],
                fmt="o", color="k", ecolor="grey", capsize=3, lw=1, ms=5,
                markerfacecolor="none")
    for yi, (_, r) in zip(y, c.iterrows()):
        ax.plot(r.std_beta, yi, "o", color=COL[r.fam], ms=6)
    ax.axvline(0, color="k", lw=0.8, ls="--")
    ax.set_yticks(y); ax.set_yticklabels(c.predictor)
    ax.set_xlabel("Standardized β (95% CI)  —  S3 NSI total")
    ax.set_title("Primary parsimonious model (n=21)", fontsize=9)
    handles = [plt.Line2D([], [], marker="o", ls="", color=COL[k],
               label={"rest": "resting", "erp": "ERP", "cov": "covariate"}[k])
               for k in ["rest", "erp", "cov"]]
    ax.legend(handles=handles, frameon=False, fontsize=7, loc="lower right")
    fig.tight_layout(); fig.savefig(FIG / "fig_coefficient_forest.png"); plt.close(fig)


def fig_partial(df):
    d = subset(df, PRIMARY, need_erp=True)
    eeg = ["Global_Aperiodic_Exponent", "Posterior_IAF", "P3b_Amplitude"]
    y = d["S3_NSI_Total"].astype(float)
    fig, axes = plt.subplots(1, 3, figsize=(8.2, 2.9))
    for ax, focus in zip(axes, eeg):
        others = [p for p in PRIMARY if p != focus]
        # residualize y and focus on the other predictors (added-variable plot)
        ry = sm.OLS(y, sm.add_constant(d[others].astype(float))).fit().resid
        rx = sm.OLS(d[focus].astype(float),
                    sm.add_constant(d[others].astype(float))).fit().resid
        ax.scatter(rx, ry, color=COL[FAMILY[focus]], s=26, edgecolor="k", lw=0.4, alpha=0.85)
        b = np.polyfit(rx, ry, 1)
        xs = np.linspace(rx.min(), rx.max(), 50)
        ax.plot(xs, np.polyval(b, xs), color="k", lw=1.2)
        ax.axhline(0, color="grey", lw=0.6, ls=":")
        ax.set_title(focus.replace("_", " "), fontsize=8)
        ax.set_xlabel("predictor | others");
    axes[0].set_ylabel("S3 NSI | others")
    fig.suptitle("Added-variable (partial) plots — primary model", fontsize=9)
    fig.tight_layout(); fig.savefig(FIG / "fig_partial_effects.png"); plt.close(fig)


def fig_enet_path(df):
    d = subset(df, PANEL, need_erp=True)
    X = StandardScaler().fit_transform(
        SimpleImputer(strategy="median").fit_transform(d[PANEL].astype(float)))
    y = d["S3_NSI_Total"].astype(float).to_numpy()
    yc = y - y.mean()
    alphas, coefs, _ = enet_path(X, yc, l1_ratio=0.1, alphas=100)
    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    for i, p in enumerate(PANEL):
        ax.plot(np.log10(alphas), coefs[i], color=COL[FAMILY[p]], lw=1.3,
                label=p if FAMILY[p] != "cov" else None)
    ax.axhline(0, color="k", lw=0.8, ls="--")
    ax.set_xlabel("log10(penalty α)"); ax.set_ylabel("standardized coefficient")
    ax.set_title("Elastic Net coefficient path (l1_ratio=0.10)", fontsize=9)
    ax.legend(fontsize=6, frameon=False, ncol=2, loc="upper right")
    fig.tight_layout(); fig.savefig(FIG / "fig_elasticnet_path.png"); plt.close(fig)


def fig_calibration(oof):
    fig, ax = plt.subplots(figsize=(4.4, 4.2))
    for name, col in [("secondary_elasticnet", TEAL), ("primary_parsimonious", "k")]:
        o = oof[oof.model == name]
        if o.empty:
            continue
        ax.scatter(o.y_pred, o.y_true, color=col, s=28, alpha=0.7, edgecolor="w",
                   lw=0.4, label=name.replace("_", " "))
    lim = [min(oof.y_true.min(), oof.y_pred.min()) - 2, oof.y_true.max() + 2]
    ax.plot(lim, lim, "k--", lw=0.9, label="identity")
    ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_xlabel("Out-of-fold predicted NSI"); ax.set_ylabel("Observed S3 NSI")
    ax.set_title("Calibration (out-of-fold)", fontsize=9)
    ax.legend(fontsize=7, frameon=False, loc="upper left")
    fig.tight_layout(); fig.savefig(FIG / "fig_calibration.png"); plt.close(fig)


def fig_pred_obs(oof, cv):
    o = oof[oof.model == "secondary_elasticnet"]
    r2 = cv.loc[cv.model == "secondary_elasticnet", "r2_oof"].iloc[0]
    fig, ax = plt.subplots(figsize=(4.4, 4.2))
    ax.scatter(o.y_true, o.y_pred, color=TEAL, s=34, edgecolor="k", lw=0.4, alpha=0.85)
    lim = [-2, max(o.y_true.max(), o.y_pred.max()) + 3]
    ax.plot(lim, lim, "k--", lw=0.9)
    ax.axhline(o.y_true.mean(), color=GREY, lw=0.8, ls=":", label="mean-only predictor")
    ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_xlabel("Observed S3 NSI"); ax.set_ylabel("Predicted S3 NSI (out-of-fold)")
    ax.set_title(f"ElasticNet predicted vs observed (R²_oof={r2:+.2f})", fontsize=9)
    ax.legend(fontsize=7, frameon=False, loc="upper left")
    fig.tight_layout(); fig.savefig(FIG / "fig_predicted_vs_observed.png"); plt.close(fig)


def fig_family(coef):
    c = coef[coef.model == "transparency_full_OLS"].copy()
    c["fam"] = c.predictor.map(FAMILY)
    c["abs_std"] = c.std_beta.abs()
    c = c.sort_values("abs_std")
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    ax.barh(c.predictor, c.abs_std, color=[COL[f] for f in c.fam], edgecolor="k", lw=0.4)
    ax.set_xlabel("|standardized β|  (full-panel OLS, descriptive)")
    ax.set_title("Resting vs ERP contribution (full panel)", fontsize=9)
    handles = [plt.Rectangle((0, 0), 1, 1, color=COL[k])
               for k in ["rest", "erp", "cov"]]
    ax.legend(handles, ["resting", "ERP", "covariate"], frameon=False, fontsize=7)
    fig.tight_layout(); fig.savefig(FIG / "fig_family_contribution.png"); plt.close(fig)


def main():
    df, coef, cv, oof = load()
    fig_forest(coef)
    fig_partial(df)
    fig_enet_path(df)
    fig_calibration(oof)
    fig_pred_obs(oof, cv)
    fig_family(coef)
    print("Figures written to", FIG)
    for f in sorted(FIG.glob("*.png")):
        print("  ", f.name)


if __name__ == "__main__":
    main()
