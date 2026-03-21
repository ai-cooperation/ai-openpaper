# Paper Structure — LLM Hallucination Rates Meta-Analysis

## Planned Sections

| Section | Target Words | Key Content |
|---------|-------------|-------------|
| Abstract | 250 | Objective, PRISMA method, N studies, pooled rate, key moderators |
| Introduction | 800 | Background → Problem → Gap → Contributions → Outline |
| Related Work | 700 | 4 literature streams + limitations of existing reviews |
| Methods | 1000 | PRISMA protocol, search strategy, inclusion/exclusion, data extraction, statistical methods |
| Results | 1000 | PRISMA flow, pooled rate, forest plot, subgroup analyses, meta-regression, publication bias |
| Discussion | 700 | Interpretation, practical implications, limitations, future work |
| Conclusion | 200 | Summary + key message |

**Total: ~4,650 words**

## Figure Plan (≥3 figures, ≥5 total with tables)

| Figure | Type | Narrative Role | Description |
|--------|------|---------------|-------------|
| fig1_prisma | Flow diagram | Framework | PRISMA 2020 flow diagram showing study selection |
| fig2_forest | Forest plot | Main Results | Overall pooled hallucination rate with study-level CIs |
| fig3_subgroup_domain | Grouped forest plot | Comparison | Subgroup analysis by domain (medical, legal, general, etc.) |
| fig4_subgroup_model | Grouped bar chart | Comparison | Hallucination rates by model family |
| fig5_funnel | Funnel plot | Validation | Publication bias assessment |

## Table Plan (≥2 tables)

| Table | Content |
|-------|---------|
| tbl1_studies | Characteristics of included studies (author, year, N, models, domain, rate, evaluation method) |
| tbl2_subgroup | Subgroup analysis results (by domain, model, evaluation method) with pooled rates and I² |
| tbl3_quality | Quality assessment scores (modified NOS) |

## Figure + Table Total: 5 figures + 3 tables = 8 (exceeds minimum of 5)

## Research Contract

- **Scope**: Quantitative meta-analysis of LLM hallucination rates
- **Data**: Only published empirical studies with quantitative rates
- **Method**: Random-effects meta-analysis (DerSimonian-Laird), I² heterogeneity, subgroup analysis, Egger's test
- **Limitations**: (1) Heterogeneous definitions of hallucination, (2) Publication bias toward novel/surprising rates, (3) Rapidly evolving field
