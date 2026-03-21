# Research Concept — LLM Hallucination Rates Meta-Analysis

## Research Question

**Primary RQ**: What is the overall hallucination rate of large language models across different models, domains, and evaluation methods, based on published empirical studies from 2022–2026?

**Secondary RQs**:
- RQ2: How do hallucination rates vary across model families (GPT, Claude, Gemini, Llama, Mistral)?
- RQ3: How do hallucination rates differ across application domains (medicine, law, finance, education, general QA)?
- RQ4: To what extent do evaluation methods (human judgment, automated metrics, reference-based) influence reported hallucination rates?
- RQ5: Is there a temporal trend — are newer models producing fewer hallucinations?

## Study Type

**Quantitative Meta-Analysis** following PRISMA 2020 guidelines.

- Population: Published empirical studies reporting LLM hallucination rates
- Intervention/Exposure: Use of specific LLM models for text generation tasks
- Comparator: Cross-model and cross-domain comparisons
- Outcome: Hallucination rate (proportion of generated content containing factual errors, fabricated references, or unsupported claims)

## Core Hypothesis

H1: Overall pooled hallucination rate across LLMs is between 5–25%, with significant heterogeneity driven by model family, domain complexity, and evaluation methodology.

H2: Closed-source frontier models (GPT-4, Claude 3.5, Gemini Pro) exhibit lower hallucination rates than open-source alternatives of comparable parameter count.

H3: Domain-specific hallucination rates are highest in medicine and law (requiring precise factual recall) and lowest in creative/general tasks.

H4: Studies using automated evaluation metrics report systematically different hallucination rates compared to human evaluation.

## Three Contributions

1. **Methodological**: First comprehensive quantitative meta-analysis of LLM hallucination rates across models and domains, providing pooled effect sizes with confidence intervals — moving beyond narrative reviews.

2. **Empirical**: Quantification of heterogeneity sources (model family, domain, evaluation method, temporal trend) through subgroup analysis and meta-regression, establishing evidence-based benchmarks.

3. **Practical**: Evidence-based guidelines for practitioners on expected hallucination rates by model-domain combination, informing model selection and risk assessment in high-stakes applications.

## Three Limitations in Existing Literature

1. **No quantitative synthesis**: Existing surveys (e.g., Ji et al. 2023, Huang et al. 2023, Rawte et al. 2023) are narrative reviews — they catalog hallucination types and mitigation strategies but do not statistically synthesize reported rates across studies.

2. **Inconsistent metrics**: Studies use different definitions of "hallucination" (factual error, fabrication, unfaithfulness) and different measurement methods (human rating, NLI-based, QA-based), making cross-study comparison difficult without formal meta-analytic methods.

3. **No moderator analysis**: No study has systematically tested whether model size, training data recency, RLHF alignment, or domain complexity moderate hallucination rates — questions that require meta-regression to answer properly.

## Target Platform

- Platform: AI Openpaper (openpaper.cooperation.tw)
- Type: AI-generated meta-analysis (seed paper #1)
- Review: 12-dimension AI peer review
- Archive: Zenodo DOI

## Expected Results Range (for simulated data planning)

- Overall pooled hallucination rate: 8–20%
- Medical domain: 15–30%
- Legal domain: 12–25%
- General QA: 3–10%
- GPT-4 class models: 5–15%
- Open-source 7B models: 15–35%
- I² heterogeneity: 85–95% (high, expected for cross-domain synthesis)
- Studies included: 40–80 (after PRISMA screening)

## PRISMA Protocol

- Databases: Semantic Scholar API, OpenAlex API, CrossRef API (for DOI verification)
- Search terms: "LLM hallucination rate" OR "large language model factual accuracy" OR "LLM factual error" OR "hallucination benchmark" OR "LLM faithfulness evaluation"
- Inclusion: Empirical studies reporting quantitative hallucination rates for specific LLMs
- Exclusion: Pure methodology papers, mitigation-only studies without baseline rates, non-English, preprints without peer review (except arXiv with >10 citations)
- Time range: January 2022 – March 2026
- Quality assessment: Modified Newcastle-Ottawa Scale adapted for LLM evaluation studies
