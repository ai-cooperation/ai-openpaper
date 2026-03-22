# OP-2026-001 Progress — LLM Hallucination Rates Meta-Analysis

**Last updated**: 2026-03-22
**Status**: ⏸️ 圖表需重做，內容框架已穩定
**Version**: v8 (pushed to repo)

## 已確定（不要再改）

### 文獻 ✅
- 38 篇 DOI 驗證通過（100%），references.bib 作者名已修正
- 14 篇有可量化幻覺率，24 篇質性納入

### 真實統計數據 ✅
- **唯一數據源**: `meta_analysis_results.json`（由 `compute_meta_analysis.py` 計算）
- Pooled rate: **25.0%** (95% CI: 16.3–36.3%), k=14
- I² = 99.9%, Q = 9,722.27, p < .001
- Egger's p = 0.987（無出版偏誤）
- Domain subgroups: Medical 10.3% (k=5), Legal 28.6% (k=1), General 37.6% (k=7), Sci.Writing 47.0% (k=1)
- 14 篇個別研究數據：

| Study | Rate | N | Domain |
|-------|------|---|--------|
| Asgari2025 | 1.47% | 12,999 | medical |
| Hasnain2025 | 10.0% | 500 | medical |
| Yoon2025 | 12.47% | 6,523 | medical |
| Moayeri2024 | 15.0% | 1,000 | general |
| Loi2024 | 15.8% | 1,212 | medical |
| Fernandez2025 | 31.0% | 2,000 | medical |
| Molli2026 | 26.5% | 500 | general |
| Min2023 | 28.4% | 500 | general |
| Gui2025 | 28.57% | 140 | legal |
| Li2023 | 38.0% | 35,000 | general |
| Lin2022 | 42.0% | 817 | general |
| Athaluri2023 | 47.0% | 200 | sci.writing |
| Semnani2023 | 57.1% | 500 | general |
| Rahman2025 | 65.0% | 20,991 | general |

### QMD 內容 ✅
- 引用全部正確（38/38 match，0 dead refs）
- ^S^ 全部移除（0 remaining）
- Methods 誠實描述 AI pipeline（非假 "two reviewers"）
- CSL: APA 7th（AI Openpaper 標準格式）

### LaTeX 排版設定 ✅
- fig-pos: H + \usepackage{float}
- booktabs, arraystretch 1.15
- floatsep/textfloatsep 收緊

## 需要重做（下一個 Session）

### 圖表全部重畫（一次到位）

**規則**：
1. 全部用 matplotlib 從 `meta_analysis_results.json` 讀取真實數據
2. 套用 figure-design skill + reading-glasses skill
3. 每張圖畫完後**立即目視驗證**（Read PNG），確認後才進下一張
4. 圖片比例：bar chart 2:1, forest/funnel 3:2, PRISMA 3:2
5. 字級：軸標 ≥16pt bold, tick ≥14pt, 數據標 ≥13pt

**5 張圖的設計方向**：

| 圖 | 類型 | 比例 | 注意事項 |
|----|------|------|---------|
| Fig 1 | PRISMA flow | 3:2 | 用 matplotlib patches，**保持 TB（上到下）結構**，不要改 LR。放大字級。 |
| Fig 2 | Forest plot | 3:2 | 回到**第一版的佈局風格**（左邊作者名，右邊 square+CI），14 篇真實數據 |
| Fig 3 | Domain subgroup bar | 2:1 | 水平 bar，4 個 domain，真實數據 |
| Fig 4 | Model comparison bar | 2:1 | 水平 bar，7 個 model family，真實數據 |
| Fig 5 | Funnel plot | 3:2 | X 軸 0-80%（無負值），14 個真實數據點，正確的 pseudo-CI |

### Paper Review
- 目標門檻：**≥ 85/100** 才通過上架
- Major Revision 可接受

## 檔案位置

```
/tmp/ai-openpaper/papers/2026-001/
├── paper_draft_v0.qmd          # 主文（v8，內容穩定）
├── references.bib              # 38 篇，作者名正確
├── apa.csl                     # APA 7th
├── meta_analysis_results.json  # 真實計算結果（唯一數據源）
├── compute_meta_analysis.py    # 計算腳本
├── figures/
│   ├── gen_figures.py          # matplotlib 圖表生成腳本（需修正）
│   ├── gen_prisma.py           # PRISMA 生成腳本（需修正）
│   ├── fig1_prisma.png         # 需重做
│   ├── fig2_forest.png         # 需重做
│   ├── fig3_subgroup_domain.png # 需重做
│   ├── fig4_model_comparison.png # 需重做
│   └── fig5_funnel.png         # 需重做
├── phase9_gate_check.md        # Stage 1 報告
├── phase9_paper_review.md      # Stage 2 報告（需重跑）
├── phase9_elite_review.md      # Stage 3 報告（需重跑）
└── review-report.md            # AI review（需重跑）
```

## GitHub
- Repo: https://github.com/ai-cooperation/ai-openpaper
- Site: https://ai-cooperation.github.io/ai-openpaper/
- DNS 待設定: openpaper.cooperation.tw
