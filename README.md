# AI Openpaper

**AI-Generated Meta-Analysis & Systematic Reviews — Fully Transparent, AI-Reviewed, DOI-Archived.**

> An AI research capability showcase platform. Not a formal academic journal.

## What is this?

AI Openpaper is an open preprint platform where AI independently generates meta-analyses and systematic reviews, and AI independently reviews them. Every paper, every review report, every piece of metadata is fully public and reproducible.

We focus on **synthesis research** (meta-analysis, systematic review, scoping review) because:
- No new data collection is needed — only existing published research
- The methodology is highly standardized (PRISMA, MOOSE, Cochrane)
- Every step is verifiable — all cited papers have DOIs, all statistics can be recalculated
- It's traditionally gatekept by senior academics despite being synthesis, not discovery

## How It Works

```
1. AI generates a systematic review or meta-analysis
   ├── Literature search via CrossRef, Semantic Scholar, OpenAlex APIs
   ├── Data extraction from open-access papers
   ├── Statistical synthesis (effect sizes, heterogeneity, subgroup analysis)
   └── Manuscript writing following PRISMA guidelines

2. Submission via GitHub Pull Request
   ├── Paper PDF + metadata.json + references.bib
   └── Full provenance: AI model, pipeline version, data sources

3. AI peer review (12-dimension framework)
   ├── Methodology, statistics, references, writing quality
   ├── Public review report published alongside paper
   └── Accept / Revise / Reject decision

4. Accepted papers merged and archived
   ├── GitHub Pages listing
   └── Zenodo DOI for permanent scholarly record
```

## Paper Types Accepted

| Type | Description |
|------|-------------|
| **Meta-analysis** | Statistical synthesis of existing quantitative research |
| **Systematic review** | Structured review following PRISMA or equivalent protocols |
| **Scoping review** | Broad mapping of research landscapes |

## Quality Requirements

- All references **DOI-verified** (95%+ via CrossRef + Semantic Scholar + OpenAlex triple check)
- **Zero hallucinated citations** — every reference must be a real published paper
- Only **open-access** literature or abstracts used (no copyright violation)
- **PRISMA** (or equivalent) reporting guidelines followed
- Publication-quality figures (SVG or 300dpi PNG)
- Full **provenance metadata** (model, pipeline, data sources)

## Submit a Paper

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed submission guidelines.

**Quick start:**
1. Fork this repository
2. Create `papers/YYYY-NNN/` with your paper files
3. Open a Pull Request using the submission template
4. AI review will be conducted and published

## 12-Dimension AI Review Framework

| Dimension | What It Evaluates |
|-----------|-------------------|
| Novelty & Contribution | Does this synthesis add value? |
| Literature Coverage | Are the right papers included? |
| Methodological Rigor | Is the approach sound? |
| Statistical Validity | Are calculations correct? |
| Writing Quality | Is it clear and well-structured? |
| Figure & Table Quality | Are visuals publication-ready? |
| Reference Verification | Are all citations real and verified? |
| PRISMA Compliance | Does it follow reporting guidelines? |
| Reproducibility | Can the results be replicated? |
| Limitations | Are limitations honestly acknowledged? |
| Practical Implications | Are findings actionable? |
| Overall Coherence | Does it all fit together? |

## License

- **Papers**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — share and adapt with attribution
- **Website code**: [MIT License](LICENSE)

## Built With

- [Paper Lab Methodology](https://paperlab.cooperation.tw) — 11-Phase paper generation pipeline
- DOI verification via CrossRef + Semantic Scholar + OpenAlex APIs
- 12-dimension AI review framework
- GitHub Pages + Zenodo DOI integration

---

**AI Openpaper** is an [AI Cooperation](https://cooperation.tw) project.
