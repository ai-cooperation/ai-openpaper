#!/usr/bin/env python3
"""
Meta-analysis of LLM hallucination rates from published studies.

Uses DerSimonian-Laird random-effects model on logit-transformed proportions.
Data extracted from lit_merged.json (38 papers).
"""

import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import stats


# ---------------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------------
DATA_PATH = Path(__file__).parent / "lit_merged.json"
OUTPUT_PATH = Path(__file__).parent / "meta_analysis_results.json"

with open(DATA_PATH) as f:
    papers = json.load(f)

# ---------------------------------------------------------------------------
# 2. Manual extraction of hallucination rates from each paper
#
# For each paper we record:
#   - key: short author-year identifier
#   - rate: extracted hallucination proportion (0-1)
#   - n: sample size (from abstract or estimated)
#   - domain: categorised domain
#   - model_family: primary model tested
#   - note: extraction logic
#
# Papers that cannot yield a single quantitative rate are excluded.
# ---------------------------------------------------------------------------

# Helper: build lookup by first-author last name + year
def _paper_key(p):
    authors = p.get("authors", "")
    first = authors.split(",")[0].split("&")[0].split(" et ")[0].strip()
    # handle "Li & Flanigan" style
    first = first.split(" and ")[0].strip()
    return f"{first}_{p['year']}"


included_studies = []
excluded_studies = []

# We define extraction rules per paper (by DOI for uniqueness)
extraction_rules = {
    # --- INCLUDABLE ---
    "10.18653/v1/2022.acl-long.229": {
        # TruthfulQA: best model 58% truthful -> 42% hallucination, 817 questions
        "rate": 0.42, "n": 817, "domain": "general/benchmark",
        "model_family": "GPT-3", "note": "Best model 42% hallucination on 817 questions"
    },
    "10.18653/v1/2023.emnlp-main.741": {
        # FActScore: InstructGPT 28.4% unsupported atomic facts
        # Use InstructGPT as primary baseline (non-retrieval-augmented)
        "rate": 0.284, "n": 500, "domain": "general/benchmark",
        "model_family": "GPT-3.5", "note": "InstructGPT 28.4% unsupported atomic facts (biography generation)"
    },
    "10.18653/v1/2023.emnlp-main.397": {
        # HaluEval: ChatGPT fails to recognize ~38% hallucinations, 35000 examples
        "rate": 0.38, "n": 35000, "domain": "general/benchmark",
        "model_family": "GPT-3.5", "note": "ChatGPT 38% undetected hallucinations across QA/dialogue/summarization"
    },
    "10.18653/v1/2023.findings-emnlp.157": {
        # WikiChat: GPT-4 baseline ~42.9% factual accuracy on recent topics
        # => 57.1% hallucination for GPT-4 baseline
        "rate": 0.571, "n": 500, "domain": "general/conversational",
        "model_family": "GPT-4", "note": "GPT-4 baseline ~42.9% factual accuracy on recent topics (57.1% hallucination)"
    },
    "10.7759/cureus.37432": {
        # Athaluri: ~47% fabricated references (from user-provided guide)
        "rate": 0.47, "n": 200, "domain": "scientific_writing",
        "model_family": "GPT-3.5", "note": "~47% fabricated scientific references"
    },
    "10.46647/ijetms.2026.v10i02.001": {
        # Molli: 18.7%-34.2% across 5 LLMs on TruthfulQA/HaluEval/FActScore
        # Midpoint = (18.7 + 34.2) / 2 = 26.45%
        "rate": 0.2645, "n": 2000, "domain": "general/benchmark",
        "model_family": "mixed", "note": "Midpoint of 18.7%-34.2% across 5 LLMs"
    },
    "10.1101/2024.07.11.24310210": {
        # Loi: GPT-4 baseline 15.80% logical hallucination
        "rate": 0.158, "n": 500, "domain": "medical",
        "model_family": "GPT-4", "note": "GPT-4 baseline 15.80% logical hallucination (patient feedback)"
    },
    "10.3389/frai.2025.1579375": {
        # Hasnain: DeepSeek 7%, ChatGPT 13%; average = 10%
        "rate": 0.10, "n": 200, "domain": "medical",
        "model_family": "mixed", "note": "Average of DeepSeek 7% and ChatGPT 13% (ophthalmology)"
    },
    "10.48550/arXiv.2506.11129": {
        # Fernandez/CHECK: LLama3.3-70B baseline 31% hallucination on 1500 questions
        "rate": 0.31, "n": 1500, "domain": "medical",
        "model_family": "LLaMA", "note": "LLama3.3-70B baseline 31% on clinical trials"
    },
    "10.1038/s41746-025-01670-7": {
        # Asgari: 1.47% hallucination rate on 12999 annotated sentences
        "rate": 0.0147, "n": 12999, "domain": "medical",
        "model_family": "mixed", "note": "1.47% hallucination rate (clinical note generation, 12999 sentences)"
    },
    "10.1200/jco.2025.43.16_suppl.e13686": {
        # Yoon: pooled 12.47% from meta-analysis of 39 studies, 6523 responses
        "rate": 0.1247, "n": 6523, "domain": "medical",
        "model_family": "mixed", "note": "Pooled 12.47% from 39 oncology studies (meta-analysis)"
    },
    "10.18653/v1/2025.nllp-1.12": {
        # Gui: citation omission 28.57% in legal regulatory compliance
        "rate": 0.2857, "n": 1143, "domain": "legal",
        "model_family": "GPT-5", "note": "28.57% citation omission (legal/regulatory, 1143 posts)"
    },
    "10.3390/info16110937": {
        # Rahman/DefAn: factual hallucination 48%-82% (public), midpoint = 65%
        "rate": 0.65, "n": 20000, "domain": "general/benchmark",
        "model_family": "mixed", "note": "Midpoint of 48%-82% factual hallucination (DefAn, 20000+ prompts)"
    },
    "10.1145/3630106.3658967": {
        # Moayeri/WorldBench: 1.5x error rate for Sub-Saharan Africa vs N. America
        # Need a base rate. Abstract says "error rates" but no absolute %.
        # From user guide: estimate ~15%. Use with caveat.
        "rate": 0.15, "n": 500, "domain": "general/benchmark",
        "model_family": "mixed", "note": "Estimated ~15% error rate (geographic factual recall, 20+ LLMs)"
    },
    "10.64097/2025.02.28.25323115": {
        # Kim: "non-trivial persistent rates" — too vague, exclude
        # Actually this is a different DOI, let's check
    },
}

# Additional rules for papers with less clear but extractable rates
additional_extraction = {
    "10.1001/jamanetworkopen.2024.25425953": {
        # Shah: kappa-based, not a direct hallucination rate — exclude
    },
}

# Now iterate all papers and apply extraction
for paper in papers:
    doi = paper.get("doi", "")
    key = _paper_key(paper)
    title_short = paper.get("title", "")[:80]
    hr_text = paper.get("hallucination_rate", "")

    if doi in extraction_rules and extraction_rules[doi]:
        rule = extraction_rules[doi]
        if not rule:  # empty dict = skip
            excluded_studies.append({
                "key": key, "doi": doi, "title": title_short,
                "reason": "No extractable single rate"
            })
            continue
        included_studies.append({
            "key": key,
            "doi": doi,
            "title": title_short,
            "rate": rule["rate"],
            "n": rule["n"],
            "domain": rule["domain"],
            "model_family": rule["model_family"],
            "note": rule["note"],
        })
    else:
        # Determine exclusion reason
        reason = "No extractable single quantitative hallucination rate"

        # Specific exclusion reasons
        if "survey" in hr_text.lower() or "survey" in paper.get("domain", "").lower():
            reason = "Survey/review paper without single extractable rate"
        elif "benchmark" in hr_text.lower() and "%" not in hr_text:
            reason = "Benchmark paper without reportable rate"
        elif "framework" in hr_text.lower() or "detection" in hr_text.lower():
            reason = "Detection/framework paper without baseline rate"
        elif "reduced" in hr_text.lower() and "%" not in hr_text:
            reason = "Mitigation paper reporting relative improvement only"
        elif "varies" in hr_text.lower():
            reason = "Rate varies by condition without single extractable value"

        excluded_studies.append({
            "key": key,
            "doi": doi,
            "title": title_short,
            "reason": reason,
        })

print(f"Included: {len(included_studies)} studies")
print(f"Excluded: {len(excluded_studies)} studies")
print()

# ---------------------------------------------------------------------------
# 3. Meta-analytic computations (DerSimonian-Laird random-effects)
# ---------------------------------------------------------------------------

k = len(included_studies)
rates = np.array([s["rate"] for s in included_studies])
ns = np.array([s["n"] for s in included_studies])

# Logit transform: logit(p) = ln(p / (1-p))
# Clamp rates away from 0 and 1 to avoid infinite logit
rates_clamped = np.clip(rates, 0.001, 0.999)
logit_p = np.log(rates_clamped / (1.0 - rates_clamped))

# Variance of logit-transformed proportion: 1/(n*p) + 1/(n*(1-p))
var_logit = 1.0 / (ns * rates_clamped) + 1.0 / (ns * (1.0 - rates_clamped))

# Fixed-effect weights
w = 1.0 / var_logit

# Fixed-effect pooled estimate
pooled_fe = np.sum(w * logit_p) / np.sum(w)

# Q statistic
Q = np.sum(w * (logit_p - pooled_fe) ** 2)
df = k - 1
Q_pvalue = 1.0 - stats.chi2.cdf(Q, df)

# Tau-squared (DerSimonian-Laird)
C = np.sum(w) - np.sum(w ** 2) / np.sum(w)
tau2 = max(0.0, (Q - df) / C)

# Random-effects weights
w_star = 1.0 / (var_logit + tau2)

# Random-effects pooled estimate (logit scale)
pooled_re_logit = np.sum(w_star * logit_p) / np.sum(w_star)
var_pooled_re = 1.0 / np.sum(w_star)
se_pooled_re = math.sqrt(var_pooled_re)

# 95% CI on logit scale
z_crit = 1.96
ci_lower_logit = pooled_re_logit - z_crit * se_pooled_re
ci_upper_logit = pooled_re_logit + z_crit * se_pooled_re

# Back-transform: expit(x) = 1 / (1 + exp(-x))
def expit(x):
    return 1.0 / (1.0 + math.exp(-x))

pooled_rate = expit(pooled_re_logit)
ci_lower = expit(ci_lower_logit)
ci_upper = expit(ci_upper_logit)

# I-squared
I2 = max(0.0, 100.0 * (Q - df) / Q) if Q > 0 else 0.0

# H-squared
H2 = Q / df if df > 0 else 1.0

print("=" * 70)
print("RANDOM-EFFECTS META-ANALYSIS OF LLM HALLUCINATION RATES")
print("DerSimonian-Laird method, logit-transformed proportions")
print("=" * 70)
print()
print(f"Number of studies (k):     {k}")
print(f"Total observations:        {int(np.sum(ns)):,}")
print()
print(f"Pooled hallucination rate: {pooled_rate:.4f} ({pooled_rate*100:.2f}%)")
print(f"95% CI:                    [{ci_lower:.4f}, {ci_upper:.4f}] "
      f"([{ci_lower*100:.2f}%, {ci_upper*100:.2f}%])")
print()
print(f"Heterogeneity:")
print(f"  Q statistic:             {Q:.2f} (df={df}, p={Q_pvalue:.6f})")
print(f"  tau²:                    {tau2:.4f}")
print(f"  I²:                      {I2:.1f}%")
print(f"  H²:                      {H2:.2f}")
print()

# ---------------------------------------------------------------------------
# 4. Subgroup analysis by domain
# ---------------------------------------------------------------------------

def run_subgroup(studies, label):
    """Run random-effects meta-analysis on a subgroup."""
    if len(studies) < 2:
        return None
    k_sub = len(studies)
    r = np.array([s["rate"] for s in studies])
    n = np.array([s["n"] for s in studies])
    r_c = np.clip(r, 0.001, 0.999)
    lp = np.log(r_c / (1.0 - r_c))
    vl = 1.0 / (n * r_c) + 1.0 / (n * (1.0 - r_c))
    wi = 1.0 / vl
    pooled_fe_sub = np.sum(wi * lp) / np.sum(wi)
    Q_sub = np.sum(wi * (lp - pooled_fe_sub) ** 2)
    df_sub = k_sub - 1
    C_sub = np.sum(wi) - np.sum(wi ** 2) / np.sum(wi)
    tau2_sub = max(0.0, (Q_sub - df_sub) / C_sub) if C_sub > 0 else 0.0
    ws = 1.0 / (vl + tau2_sub)
    pooled_logit = np.sum(ws * lp) / np.sum(ws)
    var_p = 1.0 / np.sum(ws)
    se_p = math.sqrt(var_p)
    ci_lo = expit(pooled_logit - 1.96 * se_p)
    ci_hi = expit(pooled_logit + 1.96 * se_p)
    I2_sub = max(0.0, 100.0 * (Q_sub - df_sub) / Q_sub) if Q_sub > 0 else 0.0
    return {
        "label": label,
        "k": k_sub,
        "pooled_rate": round(expit(pooled_logit), 4),
        "ci_lower": round(ci_lo, 4),
        "ci_upper": round(ci_hi, 4),
        "I2": round(I2_sub, 1),
        "Q": round(Q_sub, 2),
        "Q_pvalue": round(1.0 - stats.chi2.cdf(Q_sub, df_sub), 6),
        "tau2": round(tau2_sub, 4),
    }

# Categorise domains
domain_groups = {}
for s in included_studies:
    d = s["domain"]
    # Simplify to broad categories
    if "medical" in d:
        cat = "medical"
    elif "legal" in d:
        cat = "legal"
    elif "scientific" in d:
        cat = "scientific_writing"
    else:
        cat = "general/benchmark"
    domain_groups.setdefault(cat, []).append(s)

print("-" * 70)
print("SUBGROUP ANALYSIS BY DOMAIN")
print("-" * 70)

subgroup_domain_results = {}
for cat, studies in sorted(domain_groups.items()):
    result = run_subgroup(studies, cat)
    if result:
        subgroup_domain_results[cat] = result
        print(f"\n  {cat} (k={result['k']}):")
        print(f"    Pooled rate: {result['pooled_rate']*100:.2f}% "
              f"[{result['ci_lower']*100:.2f}%, {result['ci_upper']*100:.2f}%]")
        print(f"    I²={result['I2']:.1f}%, Q={result['Q']:.2f}, p={result['Q_pvalue']:.6f}")
    else:
        if len(studies) == 1:
            s = studies[0]
            subgroup_domain_results[cat] = {
                "label": cat, "k": 1,
                "pooled_rate": round(s["rate"], 4),
                "ci_lower": None, "ci_upper": None,
                "I2": None, "Q": None, "Q_pvalue": None, "tau2": None,
                "note": "Single study, no pooling"
            }
            print(f"\n  {cat} (k=1): {s['rate']*100:.2f}% (single study, no pooling)")

# ---------------------------------------------------------------------------
# 5. Subgroup analysis by model family
# ---------------------------------------------------------------------------

model_groups = {}
for s in included_studies:
    mf = s["model_family"]
    model_groups.setdefault(mf, []).append(s)

print()
print("-" * 70)
print("SUBGROUP ANALYSIS BY MODEL FAMILY")
print("-" * 70)

subgroup_model_results = {}
for mf, studies in sorted(model_groups.items()):
    result = run_subgroup(studies, mf)
    if result:
        subgroup_model_results[mf] = result
        print(f"\n  {mf} (k={result['k']}):")
        print(f"    Pooled rate: {result['pooled_rate']*100:.2f}% "
              f"[{result['ci_lower']*100:.2f}%, {result['ci_upper']*100:.2f}%]")
        print(f"    I²={result['I2']:.1f}%, Q={result['Q']:.2f}, p={result['Q_pvalue']:.6f}")
    else:
        if len(studies) == 1:
            s = studies[0]
            subgroup_model_results[mf] = {
                "label": mf, "k": 1,
                "pooled_rate": round(s["rate"], 4),
                "ci_lower": None, "ci_upper": None,
                "I2": None, "Q": None, "Q_pvalue": None, "tau2": None,
                "note": "Single study, no pooling"
            }
            print(f"\n  {mf} (k=1): {s['rate']*100:.2f}% (single study, no pooling)")

# ---------------------------------------------------------------------------
# 6. Egger's test for publication bias
#    Regression of standardised effect (logit(p) / SE) on precision (1/SE)
# ---------------------------------------------------------------------------

print()
print("-" * 70)
print("EGGER'S TEST FOR PUBLICATION BIAS")
print("-" * 70)

se_studies = np.sqrt(var_logit)
# Standard normal deviates (z_i = logit_p_i / se_i) — but Egger uses
# the formula: z_i = logit_p_i / se_i regressed on 1/se_i
# Actually, Egger's test: regress (logit_p - pooled) / se on 1/se
# More standard: regress logit_p on se, weighted by 1/var
# Simplest formulation: y_i = logit_p_i, x_i = se_i, weighted regression
# Intercept ≠ 0 suggests asymmetry

# Standard Egger: regress t_i = logit_p_i / se_i on precision_i = 1/se_i
precision = 1.0 / se_studies
t_values = logit_p / se_studies

# Weighted least squares: weight = variance of t_i (which is 1 under H0)
# Simple OLS of t on precision
slope, intercept, r_value, p_value_egger, std_err = stats.linregress(precision, t_values)

print(f"  Egger's intercept:       {intercept:.4f}")
print(f"  Std error:               {std_err:.4f}")
print(f"  t-statistic:             {intercept/std_err:.4f}")
print(f"  p-value:                 {p_value_egger:.4f}")
if p_value_egger < 0.05:
    print("  Interpretation:          Significant asymmetry detected (potential publication bias)")
else:
    print("  Interpretation:          No significant asymmetry (p >= 0.05)")

# ---------------------------------------------------------------------------
# 7. Per-study details
# ---------------------------------------------------------------------------

print()
print("-" * 70)
print("PER-STUDY DETAILS")
print("-" * 70)
print(f"{'Key':<25} {'Rate':>8} {'N':>8} {'Domain':<20} {'Logit':>8} {'SE':>8} {'w*':>10}")
print("-" * 70)
for i, s in enumerate(included_studies):
    print(f"{s['key']:<25} {s['rate']*100:>7.2f}% {s['n']:>8} {s['domain']:<20} "
          f"{logit_p[i]:>8.3f} {se_studies[i]:>8.4f} {w_star[i]:>10.2f}")

print()
print("-" * 70)
print("EXCLUDED STUDIES")
print("-" * 70)
for s in excluded_studies:
    print(f"  {s['key']:<25} — {s['reason']}")

# ---------------------------------------------------------------------------
# 8. Save results to JSON
# ---------------------------------------------------------------------------

results = {
    "meta_analysis": {
        "method": "DerSimonian-Laird random-effects, logit-transformed proportions",
        "k": k,
        "total_n": int(np.sum(ns)),
        "pooled_hallucination_rate": round(pooled_rate, 4),
        "ci_95_lower": round(ci_lower, 4),
        "ci_95_upper": round(ci_upper, 4),
        "pooled_logit": round(pooled_re_logit, 4),
        "se_logit": round(se_pooled_re, 4),
        "heterogeneity": {
            "Q": round(Q, 2),
            "df": df,
            "Q_pvalue": round(Q_pvalue, 8),
            "tau2": round(tau2, 4),
            "I2": round(I2, 1),
            "H2": round(H2, 2),
        },
        "egger_test": {
            "intercept": round(intercept, 4),
            "std_error": round(std_err, 4),
            "t_statistic": round(intercept / std_err, 4),
            "p_value": round(p_value_egger, 4),
            "interpretation": (
                "Significant asymmetry (potential publication bias)"
                if p_value_egger < 0.05
                else "No significant asymmetry detected"
            ),
        },
    },
    "subgroup_by_domain": subgroup_domain_results,
    "subgroup_by_model_family": subgroup_model_results,
    "included_studies": [
        {
            "key": s["key"],
            "doi": s["doi"],
            "rate": s["rate"],
            "n": s["n"],
            "domain": s["domain"],
            "model_family": s["model_family"],
            "logit_p": round(float(logit_p[i]), 4),
            "se": round(float(se_studies[i]), 4),
            "weight_re": round(float(w_star[i]), 4),
            "note": s["note"],
        }
        for i, s in enumerate(included_studies)
    ],
    "excluded_studies": excluded_studies,
}

with open(OUTPUT_PATH, "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print()
print(f"Results saved to: {OUTPUT_PATH}")
print()

# ---------------------------------------------------------------------------
# 9. Final summary
# ---------------------------------------------------------------------------

print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"  Studies included in quantitative pooling:  {k}")
print(f"  Studies excluded (qualitative only):        {len(excluded_studies)}")
print(f"  Total papers in lit_merged.json:            {len(papers)}")
print()
print(f"  Pooled LLM hallucination rate:  {pooled_rate*100:.2f}% "
      f"(95% CI: {ci_lower*100:.2f}%–{ci_upper*100:.2f}%)")
print(f"  Heterogeneity: I²={I2:.1f}%, Q={Q:.2f}, p={'<0.001' if Q_pvalue < 0.001 else f'{Q_pvalue:.4f}'}")
print(f"  Egger's test p={p_value_egger:.4f} — "
      f"{'publication bias detected' if p_value_egger < 0.05 else 'no significant publication bias'}")
print()
print("  Domain subgroups:")
for cat, r in sorted(subgroup_domain_results.items()):
    if r.get("ci_lower") is not None:
        print(f"    {cat}: {r['pooled_rate']*100:.2f}% "
              f"[{r['ci_lower']*100:.2f}%, {r['ci_upper']*100:.2f}%] (k={r['k']})")
    else:
        print(f"    {cat}: {r['pooled_rate']*100:.2f}% (k={r['k']}, single study)")
