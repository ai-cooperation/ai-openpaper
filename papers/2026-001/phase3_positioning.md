# Research Positioning — LLM Hallucination Rates Meta-Analysis

## Literature Landscape

The literature on LLM hallucination can be organized into four streams:

### Stream 1: Hallucination Taxonomy & Surveys (Narrative)
Comprehensive surveys by Huang et al. (2025, 391 citations), Ji et al. (2023), and Rawte et al. (2023) catalog hallucination types (intrinsic vs extrinsic, factual vs faithfulness) and mitigation strategies. These are narrative reviews without quantitative synthesis. The multimodal hallucination survey by Chen et al. (2026, IJCV) extends this taxonomy to vision-language models.

### Stream 2: Evaluation Benchmarks & Frameworks
TruthfulQA (Lin et al. 2022), FActScore (Min et al. 2023), HaluEval (Li et al. 2023), SelfCheckGPT (Manakul et al. 2023), and HalluLens (Bang et al. 2025) provide standardized evaluation tools. DefAn (Rahman et al. 2025) tests 9 models on 20,000+ prompts. These papers report model-specific rates but each uses different metrics and domains.

### Stream 3: Domain-Specific Empirical Studies
Medical: Yoon et al. (2025, JCO) meta-analyzed 39 studies in oncology (pooled 12.47%). Khoruzhaya et al. (2026) found 1.47%–61.6% range in medical summarization. Asgari et al. (2025, NPJ Digital Med) reported 1.47% in clinical text. Legal: Gui et al. (2025) found 28.57% citation omissions. Finance/general: sparse.

### Stream 4: Mitigation & RAG Studies
CHECK (Fernandez et al. 2025), MEGA-RAG (Xu et al. 2025), WikiChat (Semnani et al. 2023) show hallucination reduction techniques. These report baseline rates before mitigation, providing useful data points.

## Gap Matrix

| Gap | Description | Existing Work | Our Approach |
|-----|-------------|---------------|--------------|
| G1 | No cross-domain quantitative synthesis | Individual domain studies exist (medical, legal) but no pooled analysis across domains | Random-effects meta-analysis with domain as moderator |
| G2 | No systematic model-family comparison | Benchmark papers test specific models but results are not statistically compared across studies | Subgroup analysis by model family (GPT, Claude, Gemini, Llama, Mistral) |
| G3 | Evaluation method bias unquantified | Different studies use different metrics (human, NLI, QA-based) with no analysis of how this affects reported rates | Meta-regression with evaluation method as covariate |

## Differentiation Statement

"Unlike previous narrative surveys that catalog hallucination types and mitigation strategies, this study provides the first quantitative meta-analysis of reported hallucination rates across 38+ empirical studies, systematically examining how model family, application domain, and evaluation methodology moderate the observed rates."
