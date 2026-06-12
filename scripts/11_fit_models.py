#!/usr/bin/env python
"""
11_fit_models.py
================
Phase 4: fit the pre-registered models EXACTLY as locked in
reports/final_locked_analysis_plan.md. No predictor is added/removed; no tier is
promoted; the frozen folds are used as-is (subjects failing the locked §3 usability
gates are dropped from their assigned fold, never reshuffled).

Leakage safety: every cross-validated metric uses the frozen fold labels; scaling and
(sensitivity) imputation are fit inside training folds only via sklearn Pipelines; the
outcome never informs preprocessing or feature selection.

Models
------
PRIMARY confirmatory  : OLS  S3_NSI ~ aperiodic_exp + IAF + P3b_amp + Age + Sex     (n=21)
SECONDARY confirmatory: ElasticNet over full 8-feature panel + Age + Sex            (n=21)
TRANSPARENCY          : full 10-term OLS (descriptive; potentially overfit)         (n=21)
SUPPORTIVE            : resting-only OLS (n=25); ERP-only OLS (n=21)
EXPLORATORY           : Ridge, LASSO, RandomForest, XGBoost
BASELINE              : Age + Sex only (reference for "does EEG add information")

Outputs -> outputs/analysis/
"""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np
import pandas as pd
from scipy import stats

import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.stattools import durbin_watson

from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import ElasticNetCV, LassoCV, RidgeCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import xgboost as xgb

warnings.simplefilter("ignore")
RNG = 42
ROOT = Path(__file__).resolve().parents[1]
AN = ROOT / "outputs" / "analysis"
AN.mkdir(parents=True, exist_ok=True)

OUTCOME = "S3_NSI_Total"
PRIMARY = ["Global_Aperiodic_Exponent", "Posterior_IAF", "P3b_Amplitude", "Age", "Sex"]
PANEL = ["Global_Aperiodic_Exponent", "Posterior_IAF", "Frontal_Theta_Alpha_Ratio",
         "Occipital_Relative_Alpha", "P3b_Amplitude", "P3b_Latency",
         "P3a_Amplitude", "P3a_Latency", "Age", "Sex"]
RESTING = ["Global_Aperiodic_Exponent", "Posterior_IAF", "Frontal_Theta_Alpha_Ratio",
           "Occipital_Relative_Alpha", "Age", "Sex"]
ERP = ["P3b_Amplitude", "P3b_Latency", "P3a_Amplitude", "P3a_Latency", "Age", "Sex"]
BASELINE = ["Age", "Sex"]


# --------------------------------------------------------------------------- #
def subset(df, predictors, need_erp):
    m = df[predictors + [OUTCOME]].notna().all(axis=1) & df["ec_rest_reliable"]
    if need_erp:
        m = m & df["erp_reliable"]
    return df[m].copy()


def fit_ols(d, predictors, label):
    """Raw-units + standardized OLS; return coefficient table and fit object."""
    X = d[predictors].astype(float)
    y = d[OUTCOME].astype(float)
    Xc = sm.add_constant(X)
    res = sm.OLS(y, Xc).fit()
    # standardized (z X and z y)
    Xz = (X - X.mean()) / X.std(ddof=1)
    yz = (y - y.mean()) / y.std(ddof=1)
    res_z = sm.OLS(yz, sm.add_constant(Xz)).fit()
    ci = res.conf_int(0.05)
    rows = []
    for p in predictors:
        rows.append({
            "model": label, "predictor": p,
            "beta": res.params[p], "se": res.bse[p],
            "ci_low": ci.loc[p, 0], "ci_high": ci.loc[p, 1],
            "p_value": res.pvalues[p],
            "std_beta": res_z.params[p],
            "std_ci_low": res_z.conf_int(0.05).loc[p, 0],
            "std_ci_high": res_z.conf_int(0.05).loc[p, 1],
        })
    info = {"model": label, "n": int(d.shape[0]), "n_predictors": len(predictors),
            "r2": res.rsquared, "adj_r2": res.rsquared_adj,
            "f_pvalue": res.f_pvalue, "aic": res.aic, "bic": res.bic}
    return pd.DataFrame(rows), info, res, (X, y)


def fdr_bh(pvals):
    p = np.asarray(pvals, float)
    n = len(p)
    order = np.argsort(p)
    adj = np.empty(n)
    prev = 1.0
    for rank, idx in enumerate(reversed(order)):
        i = n - rank
        prev = min(prev, p[idx] * n / i)
        adj[idx] = prev
    return adj


def ols_diagnostics(res, X, y, label):
    resid = res.resid
    sh_w, sh_p = stats.shapiro(resid)
    bp = het_breuschpagan(resid, res.model.exog)
    infl = res.get_influence()
    cooks = infl.cooks_distance[0]
    lev = infl.hat_matrix_diag
    stud = infl.resid_studentized_external
    dffits = infl.dffits[0]
    diag = {
        "model": label, "n": int(len(y)),
        "shapiro_W": float(sh_w), "shapiro_p": float(sh_p),
        "breusch_pagan_LM": float(bp[0]), "breusch_pagan_p": float(bp[1]),
        "durbin_watson": float(durbin_watson(resid)),
        "condition_number": float(np.linalg.cond(res.model.exog)),
        "max_cooks_d": float(np.max(cooks)),
        "cooks_threshold_4overn": float(4.0 / len(y)),
        "n_high_cooks": int(np.sum(cooks > 4.0 / len(y))),
        "max_leverage": float(np.max(lev)),
        "max_abs_studentized_resid": float(np.max(np.abs(stud))),
    }
    return diag, pd.DataFrame({"cooks_d": cooks, "leverage": lev,
                               "studentized_resid": stud, "dffits": dffits})


def loo_coefficient_stability(d, predictors, label):
    """Leave-one-subject-out refit; report coefficient range per predictor."""
    rows = []
    base = sm.OLS(d[OUTCOME].astype(float),
                  sm.add_constant(d[predictors].astype(float))).fit().params
    coefs = {p: [] for p in predictors}
    for i in d.index:
        dd = d.drop(index=i)
        r = sm.OLS(dd[OUTCOME].astype(float),
                   sm.add_constant(dd[predictors].astype(float))).fit()
        for p in predictors:
            coefs[p].append(r.params[p])
    for p in predictors:
        arr = np.array(coefs[p])
        rows.append({"model": label, "predictor": p, "beta_full": base[p],
                     "loo_min": arr.min(), "loo_max": arr.max(),
                     "loo_sign_stable": bool(np.all(np.sign(arr) == np.sign(base[p])))})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
def oof_predict(factory, d, predictors):
    """Out-of-fold predictions using the FROZEN fold labels. Pipeline (impute+scale+est)
    is fit on training folds only. Returns (y_true, y_pred, per-fold list)."""
    y = d[OUTCOME].astype(float).to_numpy()
    X = d[predictors].astype(float).to_numpy()
    folds = d["fold"].to_numpy()
    yhat = np.full(len(y), np.nan)
    for f in sorted(np.unique(folds)):
        te = folds == f
        tr = ~te
        if tr.sum() < 3 or te.sum() == 0:
            continue
        pipe = factory()
        pipe.fit(X[tr], y[tr])
        yhat[te] = pipe.predict(X[te])
    ok = ~np.isnan(yhat)
    return y[ok], yhat[ok]


def perf(y, yhat):
    if len(y) < 3:
        return {"n": int(len(y)), "r2_oof": np.nan, "mae": np.nan, "rmse": np.nan}
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    return {"n": int(len(y)), "r2_oof": float(1 - ss_res / ss_tot),
            "mae": float(np.mean(np.abs(y - yhat))),
            "rmse": float(np.sqrt(np.mean((y - yhat) ** 2)))}


def boot_ci_metric(y, yhat, fn, n=2000):
    rng = np.random.default_rng(RNG)
    vals = []
    idx = np.arange(len(y))
    for _ in range(n):
        b = rng.choice(idx, len(idx), replace=True)
        if len(np.unique(y[b])) < 2:
            continue
        vals.append(fn(y[b], yhat[b]))
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def r2_fn(y, yhat):
    return 1 - np.sum((y - yhat) ** 2) / np.sum((y - y.mean()) ** 2)


# pipeline factories (impute median -> standardize -> estimator); all fit in-fold
def pipe_linear(est):
    return lambda: Pipeline([("imp", SimpleImputer(strategy="median")),
                             ("sc", StandardScaler()), ("est", est())])

def f_ols():
    from sklearn.linear_model import LinearRegression
    return Pipeline([("imp", SimpleImputer(strategy="median")),
                     ("sc", StandardScaler()), ("est", LinearRegression())])

def f_enet():
    return Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler()),
                     ("est", ElasticNetCV(l1_ratio=[.1,.3,.5,.7,.9,.95,1.0],
                                          alphas=100, cv=4, random_state=RNG, max_iter=20000))])

def f_ridge():
    return Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler()),
                     ("est", RidgeCV(alphas=np.logspace(-3, 3, 50)))])

def f_lasso():
    return Pipeline([("imp", SimpleImputer(strategy="median")), ("sc", StandardScaler()),
                     ("est", LassoCV(alphas=100, cv=4, random_state=RNG, max_iter=20000))])

def f_rf():
    return Pipeline([("imp", SimpleImputer(strategy="median")),
                     ("est", RandomForestRegressor(n_estimators=500, min_samples_leaf=3,
                                                   random_state=RNG, n_jobs=1))])

def f_xgb():
    return Pipeline([("imp", SimpleImputer(strategy="median")),
                     ("est", xgb.XGBRegressor(n_estimators=300, max_depth=2, learning_rate=0.03,
                                              subsample=0.8, colsample_bytree=0.8,
                                              reg_lambda=2.0, random_state=RNG, n_jobs=1))])


# --------------------------------------------------------------------------- #
def main() -> None:
    df = pd.read_csv(AN / "ds003522_s1_analysis_table.csv")
    log_outcome = bool(df["primary_outcome_is_log"].iloc[0])
    print(f"Outcome scale: {'log1p(NSI)' if log_outcome else 'raw NSI'} (locked rule)\n")

    coef_tables, infos, diags, loo_tables, cv_rows, oof_store = [], [], [], [], [], {}

    # ---------- PRIMARY confirmatory ----------
    dP = subset(df, PRIMARY, need_erp=True)
    cT, info, resP, (XP, yP) = fit_ols(dP, PRIMARY, "primary_parsimonious")
    cT["p_fdr"] = fdr_bh(cT["p_value"].values)
    coef_tables.append(cT); infos.append(info)
    diag, infl = ols_diagnostics(resP, XP, yP, "primary_parsimonious")
    diags.append(diag)
    infl.insert(0, "subject_uid", dP["subject_uid"].values)
    infl.insert(1, "model", "primary_parsimonious")
    infl.to_csv(AN / "loo_influence.csv", index=False)
    loo_tables.append(loo_coefficient_stability(dP, PRIMARY, "primary_parsimonious"))
    # robust SE sensitivity
    resP_hc3 = sm.OLS(yP, sm.add_constant(XP)).fit(cov_type="HC3")
    diag["hc3_pvalues"] = {p: float(resP_hc3.pvalues[p]) for p in PRIMARY}

    print("PRIMARY (parsimonious) OLS  n=%d  adjR2=%.3f" % (info["n"], info["adj_r2"]))
    print(cT[["predictor", "beta", "ci_low", "ci_high", "p_value", "p_fdr", "std_beta"]]
          .round(3).to_string(index=False))
    print(f"  residuals: Shapiro p={diag['shapiro_p']:.3f}, BP p={diag['breusch_pagan_p']:.3f}, "
          f"max Cook's D={diag['max_cooks_d']:.3f} (>{diag['cooks_threshold_4overn']:.3f}: "
          f"{diag['n_high_cooks']})")

    # ---------- TRANSPARENCY full OLS ----------
    dF = subset(df, PANEL, need_erp=True)
    cF, infoF, resF, (XF, yF) = fit_ols(dF, PANEL, "transparency_full_OLS")
    cF["p_fdr"] = fdr_bh(cF["p_value"].values)
    coef_tables.append(cF); infos.append(infoF)
    diagF, _ = ols_diagnostics(resF, XF, yF, "transparency_full_OLS")
    diags.append(diagF)
    print(f"\nTRANSPARENCY full OLS  n={infoF['n']}  adjR2={infoF['adj_r2']:.3f}  "
          f"cond.no={diagF['condition_number']:.0f}  (DESCRIPTIVE; potentially overfit)")

    # ---------- SUPPORTIVE ----------
    dR = subset(df, RESTING, need_erp=False)
    cR, infoR, resR, (XR, yR) = fit_ols(dR, RESTING, "supportive_resting_only")
    cR["p_fdr"] = fdr_bh(cR["p_value"].values); coef_tables.append(cR); infos.append(infoR)
    diags.append(ols_diagnostics(resR, XR, yR, "supportive_resting_only")[0])
    dE = subset(df, ERP, need_erp=True)
    cE, infoE, resE, (XE, yE) = fit_ols(dE, ERP, "supportive_erp_only")
    cE["p_fdr"] = fdr_bh(cE["p_value"].values); coef_tables.append(cE); infos.append(infoE)
    diags.append(ols_diagnostics(resE, XE, yE, "supportive_erp_only")[0])
    print(f"SUPPORTIVE resting-only n={infoR['n']} adjR2={infoR['adj_r2']:.3f} | "
          f"ERP-only n={infoE['n']} adjR2={infoE['adj_r2']:.3f}")

    # ---------- CV performance (all models) ----------
    cv_specs = [
        ("baseline_age_sex", BASELINE, True, f_ols),
        ("primary_parsimonious", PRIMARY, True, f_ols),
        ("secondary_elasticnet", PANEL, True, f_enet),
        ("transparency_full_OLS", PANEL, True, f_ols),
        ("supportive_resting_only", RESTING, False, f_ols),
        ("supportive_erp_only", ERP, True, f_ols),
        ("exploratory_ridge", PANEL, True, f_ridge),
        ("exploratory_lasso", PANEL, True, f_lasso),
        ("exploratory_random_forest", PANEL, True, f_rf),
        ("exploratory_xgboost", PANEL, True, f_xgb),
    ]
    print("\nCross-validated out-of-fold performance (frozen folds):")
    for name, preds, need_erp, fac in cv_specs:
        d = subset(df, preds, need_erp)
        y, yhat = oof_predict(fac, d, preds)
        m = perf(y, yhat)
        m["model"] = name; m["predictors"] = len(preds)
        if m["n"] >= 5 and not np.isnan(m["r2_oof"]):
            lo, hi = boot_ci_metric(y, yhat, r2_fn)
            m["r2_oof_ci_low"], m["r2_oof_ci_high"] = lo, hi
        cv_rows.append(m)
        oof_store[name] = (y, yhat)
        print(f"  {name:28s} n={m['n']:2d}  R2_oof={m['r2_oof']:+.3f}  MAE={m['mae']:.2f}")

    # ---------- ElasticNet final coefficients (interpretation; refit full, in-fold CV) ----------
    dEN = subset(df, PANEL, need_erp=True)
    enpipe = f_enet(); enpipe.fit(dEN[PANEL].astype(float).to_numpy(),
                                  dEN[OUTCOME].astype(float).to_numpy())
    en = enpipe.named_steps["est"]
    encoef = pd.DataFrame({"model": "secondary_elasticnet", "predictor": PANEL,
                           "coef_standardized": en.coef_})
    encoef["selected"] = encoef["coef_standardized"] != 0
    encoef.to_csv(AN / "elasticnet_coefficients.csv", index=False)
    en_meta = {"alpha": float(en.alpha_), "l1_ratio": float(en.l1_ratio_),
               "n_selected": int((en.coef_ != 0).sum()), "intercept": float(en.intercept_)}
    print(f"\nElasticNet selected α={en_meta['alpha']:.3f} l1_ratio={en_meta['l1_ratio']:.2f} "
          f"-> {en_meta['n_selected']}/{len(PANEL)} non-zero coefficients")

    # ---------- SENSITIVITY: drop sub-068 (EO-low) -> n=20 reconciliation ----------
    d20 = dP[dP["rest_EO_usable_s"] >= 40.0]
    s_rows = []
    if len(d20) < len(dP):
        c20, i20, _, _ = fit_ols(d20, PRIMARY, "sensitivity_primary_n20")
        s_rows = c20.assign(n=i20["n"]).to_dict("records")
        print(f"\nSENSITIVITY primary dropping EO-low sub (n={i20['n']}): "
              f"adjR2={i20['adj_r2']:.3f}")

    # ---------- write everything ----------
    pd.concat(coef_tables, ignore_index=True).to_csv(AN / "model_coefficients.csv", index=False)
    pd.concat(loo_tables, ignore_index=True).to_csv(AN / "loo_coefficient_stability.csv", index=False)
    pd.DataFrame(cv_rows).to_csv(AN / "cv_performance.csv", index=False)
    pd.DataFrame(infos).to_csv(AN / "model_fit_summary.csv", index=False)
    # OOF predictions for figures
    oof_df = []
    for name, (y, yhat) in oof_store.items():
        for a, b in zip(y, yhat):
            oof_df.append({"model": name, "y_true": a, "y_pred": b})
    pd.DataFrame(oof_df).to_csv(AN / "oof_predictions.csv", index=False)
    with open(AN / "diagnostics.json", "w") as fh:
        json.dump({"ols_diagnostics": diags, "elasticnet": en_meta,
                   "outcome_log": log_outcome, "sensitivity_n20": s_rows}, fh, indent=2, default=float)
    print(f"\nWrote results to {AN}")


if __name__ == "__main__":
    main()
