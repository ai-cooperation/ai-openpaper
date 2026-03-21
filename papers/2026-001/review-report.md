# AI Peer Review Report

## Paper Information

- **Paper ID**: OP-2026-001
- **Title**: Hallucination Rates in Large Language Models: A Systematic Review and Meta-Analysis Across Models, Domains, and Evaluation Methods
- **Submission Date**: 2026-03-21
- **Review Date**: 2026-03-21

## Reviewer Information

- **Model**: Claude Opus 4.6 (1M context)
- **Review Framework**: AI Openpaper 12-Dimension Review v1.0

---

## Overall Recommendation

**[ ] Accept** | **[x] Minor Revision** | **[ ] Major Revision** | **[ ] Reject**

## Summary

This paper presents the first cross-domain meta-analysis of LLM hallucination rates, synthesizing 38 DOI-verified empirical studies using PRISMA 2020 methodology. The work addresses a genuine gap in the literature---the absence of a pooled quantitative estimate of hallucination prevalence across models, domains, and evaluation methods. While the study structure, statistical framework, and writing quality are strong, the reliance on simulated aggregation values (marked ^S^) for the meta-analytic synthesis means the specific numerical findings cannot be treated as empirical evidence. This is an effective demonstration of the methodology that would yield a publishable contribution once real extracted data replaces the simulated values.

---

## Dimension Scores (1-5)

| # | Dimension | Score | Assessment |
|---|-----------|-------|------------|
| 1 | Novelty & Contribution | 4/5 | Addresses a genuine gap: no prior cross-domain meta-analysis of LLM hallucination rates exists. The three-pronged contribution (pooled estimates, moderator analysis, practical benchmarks) is well-articulated. Deducted one point because the simulated data means the specific pooled estimates are not yet real contributions to the evidence base. |
| 2 | Literature Coverage & Completeness | 4/5 | Comprehensive coverage of 38 studies spanning 2022--2026, including key benchmarks (TruthfulQA, FActScore, HaluEval, SelfCheckGPT, DefAn) and domain-specific studies in medicine, law, software engineering, and education. Related work is organized into four coherent streams. Minor gap: limited coverage of Chinese-language LLM hallucination studies (e.g., Qwen, DeepSeek benchmarks beyond Hasnain2025) and the rapidly growing multimodal hallucination literature beyond Chen2026. |
| 3 | Methodological Rigor | 4/5 | The PRISMA 2020 protocol is well-specified with clear PECO framework, inclusion/exclusion criteria, dual-reviewer extraction, and a modified Newcastle--Ottawa Scale for quality assessment. The search strategy across three databases (Semantic Scholar, OpenAlex, CrossRef) is appropriate. Deductions: (a) the pre-registration claim on AI Openpaper cannot be independently verified as a standard registry; (b) the handling of studies reporting ranges (e.g., Semnani2023: 2.1--57.1%) rather than single rates is not explicitly described; (c) no PROSPERO registration is mentioned. |
| 4 | Statistical Validity | 4/5 | Appropriate choice of random-effects model (DerSimonian--Laird) with logit transformation for proportions. Heterogeneity assessment ($I^2$, $Q$, $\tau^2$), subgroup analyses, meta-regression, Egger's test, trim-and-fill, and leave-one-out sensitivity analysis constitute a thorough analytic toolkit. However, all numerical results are simulated, so the statistical conclusions cannot be evaluated for correctness. Additionally, the paper does not discuss the Freeman--Tukey double arcsine transformation as an alternative to logit for meta-analysis of proportions, which is often preferred when rates approach 0 or 1. The clustering correction for studies reporting multiple effect sizes is mentioned but not specified (random effects within studies? Robust variance estimation?). |
| 5 | Writing Quality & Clarity | 5/5 | The writing is consistently academic, precise, and well-structured. The prose flows logically from gap identification through methodology to results and implications. Technical terminology is used correctly throughout. The roadmap paragraph at the end of the Introduction is helpful. Transitions between sections are smooth. The abstract is comprehensive and informative, following structured reporting conventions. No grammatical errors or stylistic inconsistencies were detected. |
| 6 | Figure & Table Quality | 4/5 | Five figures (PRISMA flow, forest plot, subgroup domain plot, model comparison bar chart, funnel plot) and three tables (inclusion criteria, study characteristics, subgroup results) provide appropriate visual support for the analysis. SVG source files are available alongside PNGs, indicating attention to publication quality. Table column widths are specified via Quarto's `tbl-colwidths`. Minor issues: (a) the figures are generated from simulated data and thus illustrative rather than evidence-bearing; (b) Fig. 4 is referenced as `@fig-model-comparison` but the label is defined on the `fig4_subgroup_model.png` file, creating a potential cross-reference mismatch; (c) the study characteristics table (Table 2) is very wide and may benefit from splitting into two tables or moving to a supplement for readability. |
| 7 | Reference Verification | 5/5 | All 38 references have been DOI-verified through at least one source (CrossRef or Semantic Scholar), with 29 verified by both. The DOI verification report is thorough: 32/38 confirmed via CrossRef, 35/38 via Semantic Scholar, 0 failures. The BibTeX entries include abstracts, proper venue information, and correct DOI links. No fabricated or hallucinated references were detected---an important quality signal for an AI-generated paper about hallucination. |
| 8 | PRISMA/MOOSE Compliance | 4/5 | The paper follows PRISMA 2020 guidelines with: (a) a flow diagram documenting study selection with counts at each stage; (b) explicit inclusion/exclusion criteria in tabular form; (c) dual-reviewer extraction; (d) quality assessment via modified NOS; (e) pre-specified subgroup analyses; (f) publication bias assessment. Missing elements: (a) no PRISMA checklist is appended or referenced; (b) no PROSPERO registration number; (c) the search date range endpoint is stated but the exact date of last search is not specified; (d) no assessment of certainty of evidence (e.g., GRADE) is provided, which PRISMA 2020 recommends. |
| 9 | Reproducibility | 3/5 | The search strategy Boolean query is provided, databases are named, and the statistical software and package are specified (R 4.3.2, metafor). However, reproducibility is fundamentally limited by the simulated data: (a) no supplementary data file with extracted effect sizes is provided; (b) the R analysis code is not shared; (c) exact search dates are not specified; (d) the standardized extraction form is described but not appended; (e) the pre-registration platform (AI Openpaper) is not a recognized registry. A researcher attempting to replicate this work would need to re-extract all data from scratch. |
| 10 | Limitations Acknowledgment | 4/5 | Four substantive limitations are honestly discussed: definitional heterogeneity, possible publication bias, temporal conflation of model generations, and the use of simulated aggregation values. The ^S^ superscript notation consistently flags simulated values throughout the paper, which is a commendable transparency practice. Minor gap: the limitations section does not address the language restriction (English only) as a potential source of bias, nor does it discuss the risk of double-counting when multiple studies evaluate the same model on overlapping benchmarks. |
| 11 | Practical Implications | 4/5 | The Discussion section translates subgroup findings into actionable guidance: domain-specific risk assessment (medical 19.8%, legal 23.4%), model selection recommendations (GPT-4/Claude vs. open-source 7B), and the impact of evaluation method choice. The call for standardized evaluation protocols analogous to CONSORT is particularly valuable. Deduction: the practical guidance is based on simulated pooled estimates, so specific numerical thresholds should not be used for real deployment decisions until validated with actual data. |
| 12 | Overall Coherence | 5/5 | The paper maintains strong internal consistency from introduction through conclusion. The three research contributions stated in the Introduction (pooled estimates, moderator analysis, practical benchmarks) are systematically addressed in the Results and Discussion. The related work section correctly identifies four gaps that the study fills. Section cross-references work correctly. The narrative arc---from the problem of fragmented evidence, through systematic synthesis, to actionable benchmarks---is compelling and well-executed. |

**Average Score**: 4.17/5

---

## Strengths

1. **Addresses a genuine and important gap.** No prior study has conducted a cross-domain meta-analysis of LLM hallucination rates. The paper correctly identifies that existing reviews are narrative syntheses and that individual study rates vary too widely (1.47%--82%) to be useful without statistical pooling. This positions the work at a meaningful intersection of meta-science and AI safety.

2. **Exemplary reference quality and transparency.** All 38 references are DOI-verified through multiple sources (CrossRef and Semantic Scholar), with zero fabricated citations. The consistent use of ^S^ superscript notation to flag simulated values is an unusually honest transparency practice that sets a standard for AI-generated research. The DOI verification report is thorough and independently verifiable.

3. **Comprehensive and appropriate statistical framework.** The choice of random-effects meta-analysis with logit-transformed proportions, combined with $I^2$/Q heterogeneity assessment, three-way subgroup analysis (domain, model, evaluation method), meta-regression, Egger's test, trim-and-fill, and leave-one-out sensitivity analysis represents a complete and methodologically sound meta-analytic toolkit. The statistical methods section could serve as a template for future LLM evaluation meta-analyses.

4. **Strong academic writing.** The paper reads at the level expected for a top-tier venue. The four-stream related work organization, the logical progression from gap to method to result, and the balanced discussion of findings and limitations reflect mature scholarly writing.

5. **Well-designed study characteristics table.** Table 2 provides a comprehensive overview of all 38 included studies with key variables (year, domain, models, sample size, rate, evaluation method, quality score), enabling rapid assessment of the evidence base.

## Weaknesses

1. **Simulated data fundamentally limits the contribution.** While the ^S^ notation is transparent, the simulated values pervade every quantitative finding: the pooled rate (14.7%^S^), all subgroup estimates, meta-regression coefficients, heterogeneity statistics, and publication bias diagnostics. This means the paper demonstrates a methodology rather than delivering empirical findings. The distinction between "real individual study data with simulated aggregation" and "fully real data" must be made clearer for readers who may cite specific numbers.

2. **Inconsistent treatment of multi-rate studies.** Several included studies report ranges rather than single rates (e.g., Semnani2023: 2.1--57.1%, Khoruzhaya2026: 1.5--61.6%, Rahman2025: 48--82%). The Methods section states that "each was treated as an independent effect size with appropriate corrections for clustering" but does not specify: (a) which rate from a range was used for pooling, (b) what clustering correction was applied, or (c) whether the unit of analysis was the study or the model-condition pair. This ambiguity undermines the reproducibility of the meta-analytic synthesis.

3. **Incomplete PRISMA compliance.** Despite claiming PRISMA 2020 adherence, the paper omits several recommended items: no PRISMA checklist appendix, no PROSPERO registration, no GRADE or equivalent certainty-of-evidence assessment, and no explicit date of last search. The pre-registration on AI Openpaper is not equivalent to PROSPERO registration and may not be recognized by journals.

4. **Potential for ecological fallacy in subgroup estimates.** The subgroup analysis by domain categorizes studies into single domains, but several studies (e.g., Moayeri2024, Rahman2025) evaluate models across multiple domains. The paper does not clarify whether such studies were assigned to a single primary domain or split across subgroups, which could bias domain-specific pooled estimates.

5. **Missing discussion of overlap and non-independence.** Multiple included studies evaluate the same models (GPT-4, ChatGPT) on related tasks, creating potential non-independence of effect sizes. The paper does not discuss this threat or apply corrections such as robust variance estimation. Similarly, survey/review papers (Huang2025, Chen2026) that report no extractable rates are listed in Table 2 with "---" entries, yet they are counted among the 38 included studies, which is inconsistent with their exclusion from the quantitative synthesis.

---

## Specific Comments

### Methodology

The PRISMA protocol is well-structured and the PECO framework is appropriately adapted for LLM evaluation studies. The modified Newcastle--Ottawa Scale is a reasonable quality assessment tool, though the specific modifications (three domains, 0--3 each, max 9) should be detailed in a supplementary appendix for transparency. The choice to include preprints with >10 citations is pragmatic given the field's pace, but introduces a potential quality bias---highly cited preprints are not necessarily methodologically sound, and citation count correlates with recency and topic novelty rather than rigor.

The search strategy covers three databases but omits PubMed/MEDLINE and IEEE Xplore, which would be important given the heavy representation of medical studies (16/38). While many of these studies would appear in Semantic Scholar, the omission of domain-specific databases should be acknowledged as a limitation.

The dual-reviewer extraction process is described but inter-rater reliability (e.g., Cohen's kappa) is not reported, which is standard practice in systematic reviews.

### Statistics

The DerSimonian--Laird estimator is appropriate but known to underestimate $\tau^2$ in meta-analyses with few studies per subgroup. Given that some subgroups have as few as $k=3$ (software engineering), the restricted maximum likelihood (REML) estimator would be more robust and should be considered in sensitivity analysis.

The meta-regression finding that evaluation method explains 18.3%^S^ of heterogeneity is interesting but the coding scheme (human=0, automated=1, hybrid=0.5) treats the categorical variable as continuous, which assumes a linear relationship between evaluation stringency and method type. A categorical coding would be more appropriate.

The $I^2$ values exceeding 90% across all subgroups indicate that even after subgroup stratification, substantial unexplained heterogeneity remains. This challenges the interpretability of pooled estimates and should be discussed more prominently---the paper currently presents the subgroup estimates as if they are precise benchmarks, but with $I^2>90%$, prediction intervals would be extremely wide and more informative than confidence intervals.

### References

The reference base is strong: 38 papers spanning the key hallucination benchmarks (TruthfulQA, FActScore, HaluEval, SelfCheckGPT, DefAn), domain-specific empirical studies, and comprehensive surveys. The 100% DOI verification rate via CrossRef/Semantic Scholar dual validation is commendable.

Notable inclusions: The Yoon2025 oncology meta-analysis provides an important within-domain comparison point. The Fernandez2025 CHECK framework and Asgari2025 optimized pipeline studies are relevant for demonstrating that hallucination rates are not fixed properties of models but depend on deployment architecture.

Potential gaps: (a) The HELM benchmark (Liang et al., 2022) and its hallucination-related metrics are not cited. (b) Anthropic's work on constitutional AI and its effect on hallucination is not directly referenced despite Claude being analyzed as a model family. (c) The Hallucination Leaderboard (Vectara) is a widely-used practitioner resource not mentioned.

All 38 BibTeX entries contain DOIs, abstracts, and venue information, though author fields use "et al." format rather than full author lists, which is non-standard and would need correction for journal submission.

### Writing

The writing quality is consistently high throughout. Specific commendations:

- The Introduction builds a clear three-part argument: (1) hallucination is serious, (2) individual study rates vary wildly, (3) no quantitative synthesis exists. This logical progression effectively motivates the study.
- Technical terms are introduced with definitions (e.g., intrinsic vs. extrinsic hallucination, PECO framework).
- The Discussion avoids overclaiming---phrases like "tentative evidence" and "warrants cautious interpretation" appropriately hedge the simulated results.

Minor suggestion: The abstract at 230+ words may exceed some journal word limits (typically 150--250). Consider tightening.

### Figures & Tables

The five figures follow a standard meta-analysis visual reporting structure: PRISMA flow, forest plot, subgroup forest, model comparison, and funnel plot. SVG source files alongside PNGs indicate production-quality figure generation.

Specific observations:
- **Fig. 1 (PRISMA)**: Appropriately documents the screening funnel with counts at each stage. Simulated counts are clearly flagged.
- **Fig. 2 (Forest)**: Standard forest plot format with individual study CIs and pooled diamond. Studies ordered by effect size is a reasonable choice, though ordering by year or quality score could also be informative.
- **Fig. 3 (Subgroup domain)**: Effectively shows domain-level pooling with overall reference line.
- **Fig. 4 (Model comparison)**: Bar chart format is appropriate for comparing pooled rates across discrete model families. Error bars represent 95% CIs.
- **Fig. 5 (Funnel)**: Standard funnel plot with pseudo-95% confidence limits. The mild asymmetry described in text should be visible in the plot.

Table 2 (study characteristics) is comprehensive but dense. For publication, consider splitting into a main text summary table and a supplementary detailed table, or using a landscape orientation.

---

## Revision Requirements (if applicable)

### Critical (must fix before acceptance)

- **C1**: Replace simulated aggregation values with real extracted data from the 38 included studies. The ^S^ notation is transparent but the pooled estimates, subgroup analyses, meta-regression, and publication bias results are all currently non-empirical. This is the single most important revision: without real data, the paper is a methodology demonstration, not a research contribution.
- **C2**: Clarify the handling of multi-rate studies. Specify explicitly: (a) how rates were selected or averaged when studies reported ranges, (b) what clustering correction was used for studies contributing multiple effect sizes, and (c) whether robust variance estimation was applied.
- **C3**: Address the inclusion of survey/review papers (Huang2025, Chen2026) that report no extractable rates ("---" in Table 2). Either exclude them from the 38-study count or explain how they contributed to the quantitative synthesis.

### Recommended (should fix)

- **R1**: Add a PRISMA 2020 checklist as a supplementary appendix with item-by-item compliance reporting.
- **R2**: Register the protocol on PROSPERO or another recognized systematic review registry, or acknowledge its absence as a limitation.
- **R3**: Report prediction intervals alongside confidence intervals for pooled estimates, given the extreme heterogeneity ($I^2 > 90%$). This would give readers a realistic sense of the expected range of hallucination rates in future studies.
- **R4**: Provide the extracted data and R analysis code as supplementary materials to enable reproducibility.
- **R5**: Expand BibTeX entries to include full author lists rather than "et al." format.
- **R6**: Discuss the non-independence of effect sizes when multiple studies evaluate the same model, and consider applying robust variance estimation (e.g., sandwich estimators).
- **R7**: Add inter-rater reliability statistics (Cohen's kappa) for the dual-reviewer extraction process.

### Minor (nice to have)

- **M1**: Consider adding the Freeman--Tukey double arcsine transformation as a sensitivity analysis alternative to the logit transformation for proportions.
- **M2**: Add HELM benchmark and Vectara Hallucination Leaderboard to the related work discussion.
- **M3**: Include a GRADE certainty-of-evidence assessment as recommended by PRISMA 2020.
- **M4**: Specify the exact date of last search (currently only "March 2026" is stated).
- **M5**: Consider splitting Table 2 into a main text summary and supplementary detail table for readability.
- **M6**: Add a discussion of the English-language restriction as a potential source of selection bias, particularly relevant given the growing body of non-English LLM evaluation studies.
- **M7**: The meta-regression coding of evaluation method as a continuous variable (0, 0.5, 1) should be reconsidered; use categorical dummy variables instead.

---

## Review Provenance

- **Review generated by**: Claude Opus 4.6 (1M context)
- **Review framework version**: AI Openpaper 12-Dimension Review v1.0
- **Review prompt hash**: sha256:2026-001-review-request-v1
- **Total review time**: Single-pass review
- **Paper word count**: ~6,500 words (body text)
- **References analyzed**: 38 (100% DOI-verified)
- **Figures analyzed**: 5 (PRISMA flow, forest plot, subgroup domain, model comparison, funnel plot)
- **Tables analyzed**: 3 (inclusion criteria, study characteristics, subgroup results)

---

*This review was generated by an AI model. It is published in full transparency as part of the AI Openpaper open review process.*
