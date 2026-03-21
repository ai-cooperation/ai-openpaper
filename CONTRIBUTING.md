# Contributing to AI Openpaper

## Who Can Submit?

Anyone using AI to generate systematic reviews, meta-analyses, or scoping reviews. The paper must be **AI-generated** — this is a platform for demonstrating AI research capability.

## Submission Process

### 1. Prepare Your Paper

Your paper must include:

```
papers/YYYY-NNN/
├── paper.pdf           # The paper (PDF format)
├── metadata.json       # Structured metadata (see schema below)
├── references.bib      # BibTeX file with all references
└── figures/            # (optional) Source figure files
```

### 2. Metadata Schema

Create a `metadata.json` with the following fields:

```json
{
  "paper_id": "OP-2026-001",
  "title": "Your Paper Title",
  "model_used": "Claude Opus 4 / GPT-4o / Gemini 2.5 Pro / etc.",
  "pipeline_description": "Brief description of the generation pipeline",
  "abstract": "Paper abstract (max 300 words)",
  "date_generated": "2026-03-21",
  "paper_type": "meta-analysis | systematic-review | scoping-review",
  "tags": ["domain-tag-1", "domain-tag-2"],
  "target_domain": "e.g., Finance, Healthcare, Education",
  "reference_count": 45,
  "doi_verification_rate": 0.96,
  "figures_count": 5,
  "tables_count": 3,
  "prisma_compliant": true,
  "data_sources": ["CrossRef", "Semantic Scholar", "OpenAlex"],
  "open_access_only": true
}
```

### 3. Submit via Pull Request

1. **Fork** this repository
2. Create your paper directory under `papers/` with the next available number
3. Add your files (PDF, metadata.json, references.bib)
4. Open a **Pull Request** — the PR template will guide you through the checklist

### 4. AI Review

After your PR is opened:
- A maintainer will run the 12-dimension AI review
- The review report will be committed to your PR as `review-report.md`
- You may be asked to revise based on the review
- Once accepted, your paper is merged and listed on the site

## Quality Requirements

### Hard Requirements (must pass)

- [ ] **DOI verification rate >= 95%** — verified via CrossRef + Semantic Scholar + OpenAlex
- [ ] **Zero hallucinated citations** — every reference must be a real, published paper
- [ ] **Open access only** — all source papers must be OA or referenced by abstract/metadata only
- [ ] **Full provenance** — AI model, pipeline version, and data sources documented
- [ ] **PRISMA compliance** — systematic reviews must follow PRISMA reporting guidelines
- [ ] **Publication-quality figures** — SVG or 300dpi PNG, properly labeled

### Soft Requirements (evaluated in review)

- Literature coverage completeness
- Statistical methodology appropriateness
- Writing clarity and academic tone
- Balanced limitations discussion
- Actionable practical implications

## Paper Numbering

Papers are numbered sequentially within each year:
- `OP-2026-001` — first paper of 2026
- `OP-2026-002` — second paper of 2026
- etc.

Check existing `papers/` directories to determine the next available number.

## Review Dimensions (1-5 scale)

Your paper will be scored on 12 dimensions:

| # | Dimension | Weight |
|---|-----------|--------|
| 1 | Novelty & Contribution | High |
| 2 | Literature Coverage | Critical |
| 3 | Methodological Rigor | Critical |
| 4 | Statistical Validity | Critical |
| 5 | Writing Quality | Medium |
| 6 | Figure & Table Quality | Medium |
| 7 | Reference Verification | Critical |
| 8 | PRISMA/MOOSE Compliance | High |
| 9 | Reproducibility | High |
| 10 | Limitations Acknowledgment | Medium |
| 11 | Practical Implications | Medium |
| 12 | Overall Coherence | High |

Papers scoring below 3.0 on any **Critical** dimension will be sent back for revision.

## Questions?

Open an [issue](https://github.com/ai-cooperation/ai-openpaper/issues) on this repository.
