#!/usr/bin/env python
"""
13_replication_feasibility.py
=============================
Phase 5: assess whether the locked ds003522 feature panel can be extracted, with its
preregistered definitions, in the designated replication cohort ds005114 (and the other
shared-program datasets). This determines whether an outcome replication is even possible
BEFORE any model is considered.

Method: scan Session-1 events.tsv marker labels for (a) eyes-closed/eyes-open RESTING
blocks — required for the four resting features — and (b) auditory-oddball Target/Novel
TONES — required for the four ERP features. A feature is "extractable with the locked
definition" only if its source paradigm is present.

This script reads no outcome and fits no model. It writes a transparent availability
matrix and an effect-size comparison scaffold (discovery vs replication).

Outputs -> outputs/analysis/
    replication_feature_availability.csv
    replication_effect_size_comparison.csv
"""
from __future__ import annotations

import io
import re
import urllib.request
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "metadata_cache"
AN = ROOT / "outputs" / "analysis"
AN.mkdir(parents=True, exist_ok=True)
S3 = "https://s3.amazonaws.com/openneuro.org"

DATASETS = {
    "ds003522": "EEG: 3-Stim Auditory Oddball + Rest in TBI (DISCOVERY)",
    "ds005114": "EEG: DPX Cognitive Control in mTBI (designated replication)",
    "ds003523": "EEG: Visual Working Memory in TBI (designated replication)",
    "ds003490": "EEG: 3-Stim Auditory Oddball + Rest in Parkinson's (paradigm match)",
}
LOCKED = ["Global_Aperiodic_Exponent", "Posterior_IAF", "Frontal_Theta_Alpha_Ratio",
          "Occipital_Relative_Alpha", "P3b_Amplitude", "P3b_Latency",
          "P3a_Amplitude", "P3a_Latency"]
FEATURE_SOURCE = {  # each locked feature -> required paradigm
    "Global_Aperiodic_Exponent": "rest", "Posterior_IAF": "rest",
    "Frontal_Theta_Alpha_Ratio": "rest", "Occipital_Relative_Alpha": "rest",
    "P3b_Amplitude": "oddball", "P3b_Latency": "oddball",
    "P3a_Amplitude": "oddball", "P3a_Latency": "oddball",
}


def s3_keys(dsid, maxk=600):
    fl = CACHE / dsid / "_filelist.txt"
    if fl.exists():
        return fl.read_text(encoding="utf-8").splitlines()
    import xml.etree.ElementTree as ET
    xml = urllib.request.urlopen(f"{S3}?list-type=2&prefix={dsid}/&max-keys={maxk}", timeout=40).read()
    return [e.text for e in ET.fromstring(xml).iter("{http://s3.amazonaws.com/doc/2006-03-01/}Key")]


def scan_markers(dsid, n=12):
    """Scan up to n Session-1 events.tsv for eyes-rest and oddball-tone markers."""
    keys = [k for k in s3_keys(dsid) if re.search(r"/ses-01/.*_events\.tsv$", k)]
    has_rest = has_tone = scanned = 0
    for k in keys[:n]:
        try:
            txt = urllib.request.urlopen(f"{S3}/{k}", timeout=30).read().decode()
            tt = set(pd.read_csv(io.StringIO(txt), sep="\t")
                       .get("trial_type", pd.Series(dtype=str)).dropna().astype(str))
            scanned += 1
            if any("eye" in t.lower() for t in tt):
                has_rest += 1
            if any("tone" in t.lower() for t in tt):
                has_tone += 1
        except Exception:
            pass
    return {"n_event_files_total": len(keys), "n_scanned": scanned,
            "rest_present": has_rest > 0, "oddball_present": has_tone > 0,
            "rest_hits": has_rest, "tone_hits": has_tone}


def main():
    print("Scanning Session-1 event markers for paradigm presence...\n")
    rows = []
    scan = {}
    for dsid, desc in DATASETS.items():
        s = scan_markers(dsid)
        scan[dsid] = s
        print(f"  {dsid}: rest={'YES' if s['rest_present'] else 'no':3s} "
              f"({s['rest_hits']}/{s['n_scanned']})  "
              f"oddball={'YES' if s['oddball_present'] else 'no':3s} "
              f"({s['tone_hits']}/{s['n_scanned']})  — {desc}")
        for feat in LOCKED:
            need = FEATURE_SOURCE[feat]
            ok = s["rest_present"] if need == "rest" else s["oddball_present"]
            rows.append({"dataset": dsid, "feature": feat, "required_paradigm": need,
                         "paradigm_present": s["rest_present"] if need == "rest" else s["oddball_present"],
                         "extractable_locked_definition": bool(ok)})
    avail = pd.DataFrame(rows)
    avail.to_csv(AN / "replication_feature_availability.csv", index=False)

    # discovery vs replication effect-size scaffold
    disc = pd.read_csv(AN / "model_coefficients.csv")
    disc = disc[disc.model == "primary_parsimonious"].set_index("predictor")
    rep_extractable = (avail[(avail.dataset == "ds005114") & (avail.extractable_locked_definition)]
                       .feature.tolist())
    comp = []
    for feat in ["Global_Aperiodic_Exponent", "Posterior_IAF", "P3b_Amplitude"]:  # primary panel EEG
        d = disc.loc[feat] if feat in disc.index else None
        comp.append({
            "predictor": feat,
            "discovery_std_beta": round(float(d["std_beta"]), 3) if d is not None else None,
            "discovery_ci": f"[{d['std_ci_low']:.2f}, {d['std_ci_high']:.2f}]" if d is not None else None,
            "discovery_p_fdr": round(float(d["p_fdr"]), 3) if d is not None else None,
            "replication_extractable_in_ds005114": feat in rep_extractable,
            "replication_std_beta": "NOT ESTIMABLE",
            "reason": f"{FEATURE_SOURCE[feat]} paradigm absent in ds005114 (DPX task; no "
                      f"{'eyes-closed rest' if FEATURE_SOURCE[feat]=='rest' else 'auditory oddball'})",
        })
    pd.DataFrame(comp).to_csv(AN / "replication_effect_size_comparison.csv", index=False)

    # summary
    print("\nLocked features extractable per dataset (of 8):")
    for dsid in DATASETS:
        n = int(avail[(avail.dataset == dsid)].extractable_locked_definition.sum())
        print(f"  {dsid}: {n}/8")
    print("\nFULL scan note: ds005114 was separately scanned across ALL 91 S1 recordings "
          "(0/91 rest, 0/91 oddball).")
    print(f"\nWrote replication_feature_availability.csv and replication_effect_size_comparison.csv")


if __name__ == "__main__":
    main()
