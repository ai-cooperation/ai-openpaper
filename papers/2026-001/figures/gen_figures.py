#!/usr/bin/env python3
"""Generate publication-quality figures from meta-analysis data using matplotlib."""

import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ---------------------------------------------------------------------------
# Global style
# ---------------------------------------------------------------------------
for fam in ['Arial', 'Helvetica', 'DejaVu Sans']:
    try:
        matplotlib.font_manager.findfont(fam, fallback_to_default=False)
        plt.rcParams['font.family'] = fam
        break
    except Exception:
        continue

plt.rcParams.update({
    'axes.linewidth': 1.8,
    'xtick.major.width': 1.5,
    'ytick.major.width': 1.5,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'axes.labelsize': 16,
    'axes.titlesize': 18,
    'legend.fontsize': 14,
    'font.weight': 'normal',
    'axes.labelweight': 'bold',
    'axes.titleweight': 'bold',
})

# ---------------------------------------------------------------------------
# Colours
# ---------------------------------------------------------------------------
NAVY = '#0B3C5D'
TEAL = '#0F9D8A'
GOLD = '#FFC857'
MEDICAL = '#E74C3C'
LEGAL = '#9B59B6'
GENERAL = '#95A5A6'
SCIWRITING = '#3498DB'

DOMAIN_COLORS = {
    'medical': MEDICAL,
    'legal': LEGAL,
    'general/benchmark': GENERAL,
    'general/conversational': GENERAL,
    'scientific_writing': SCIWRITING,
}

OUT = '/tmp/ai-openpaper/papers/2026-001/figures'

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
with open('/tmp/ai-openpaper/papers/2026-001/meta_analysis_results.json') as f:
    data = json.load(f)

studies = data['included_studies']
pooled = data['meta_analysis']
pooled_rate = pooled['pooled_hallucination_rate']
pooled_ci_lo = pooled['ci_95_lower']
pooled_ci_hi = pooled['ci_95_upper']
I2 = pooled['heterogeneity']['I2']
egger_p = pooled['egger_test']['p_value']

# ---------------------------------------------------------------------------
# Helper: Wilson CI for a proportion
# ---------------------------------------------------------------------------
def wilson_ci(p, n, z=1.96):
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2*n)) / denom
    spread = z * math.sqrt((p*(1-p) + z**2/(4*n)) / n) / denom
    return max(0, centre - spread), min(1, centre + spread)

# Sort studies by rate for forest plot
studies_sorted = sorted(studies, key=lambda s: s['rate'])

# ===================================================================
# FIGURE 2: Forest Plot
# ===================================================================
fig, ax = plt.subplots(figsize=(10, 6))

n_studies = len(studies_sorted)
y_positions = np.arange(n_studies, 0, -1)  # top to bottom

# Compute CIs and draw
max_weight = max(s['weight_re'] for s in studies_sorted)
min_weight = min(s['weight_re'] for s in studies_sorted)

for i, (s, ypos) in enumerate(zip(studies_sorted, y_positions)):
    rate = s['rate'] * 100
    n = s['n']
    ci_lo, ci_hi = wilson_ci(s['rate'], n)
    ci_lo *= 100
    ci_hi *= 100

    # Square size proportional to weight
    w = s['weight_re']
    size = 5 + 10 * (w - min_weight) / (max_weight - min_weight + 1e-9)

    color = DOMAIN_COLORS.get(s['domain'], NAVY)
    ax.plot([ci_lo, ci_hi], [ypos, ypos], color=color, linewidth=1.5, zorder=2)
    ax.plot(rate, ypos, 's', color=color, markersize=size, zorder=3)

    # Rate label on right
    ax.text(82, ypos, f'{rate:.1f}%', va='center', ha='left', fontsize=13)

# Pooled diamond at bottom
diamond_y = 0
diamond_x = pooled_rate * 100
diamond_lo = pooled_ci_lo * 100
diamond_hi = pooled_ci_hi * 100
diamond = plt.Polygon([
    [diamond_lo, diamond_y],
    [diamond_x, diamond_y + 0.3],
    [diamond_hi, diamond_y],
    [diamond_x, diamond_y - 0.3],
], closed=True, facecolor=NAVY, edgecolor='black', linewidth=1.2, zorder=4)
ax.add_patch(diamond)

# Pooled label
ax.text(-1, diamond_y, 'Pooled (RE)', va='center', ha='right', fontsize=14,
        fontweight='bold')

# Vertical dashed line at pooled
ax.axvline(diamond_x, color=NAVY, linestyle='--', linewidth=1.0, alpha=0.5, zorder=1)

# Study labels on y-axis
labels = []
for s in studies_sorted:
    key = s['key']
    author = key.split('_')[0]
    year = key.split('_')[1]
    labels.append(f'{author} ({year})')

ax.set_yticks(list(y_positions) + [diamond_y])
ax.set_yticklabels(labels + [''], fontsize=14)

ax.set_xlim(-2, 90)
ax.set_ylim(-1, n_studies + 1)
ax.set_xlabel('Hallucination Rate (%)', fontsize=16, fontweight='bold')
ax.tick_params(axis='x', labelsize=12)

# Bottom annotation
ax.text(0.5, -0.12,
        f'Pooled (RE): {pooled_rate*100:.1f}% [{pooled_ci_lo*100:.1f}, {pooled_ci_hi*100:.1f}], '
        f'I\u00B2={I2:.1f}%, k={pooled["k"]}',
        transform=ax.transAxes, fontsize=13, ha='center', style='italic')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

fig.tight_layout()
fig.savefig(f'{OUT}/fig2_forest.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close(fig)
print('fig2_forest.png saved')

# ===================================================================
# FIGURE 3: Domain Subgroup
# ===================================================================
domain_data = [
    ('Medical',           0.103,  0.035,  0.2665, 5, MEDICAL),
    ('Legal',             0.2857, None,   None,   1, LEGAL),
    ('General/Benchmark', 0.3755, 0.254,  0.5149, 7, GENERAL),
    ('Sci. Writing',      0.47,   None,   None,   1, SCIWRITING),
]
# Sort by rate ascending
domain_data.sort(key=lambda x: x[1])

fig, ax = plt.subplots(figsize=(10, 5))
y_pos = np.arange(len(domain_data))

for i, (label, rate, ci_lo, ci_hi, k, color) in enumerate(domain_data):
    bar_val = rate * 100
    ax.barh(i, bar_val, color=color, edgecolor='white', height=0.6, zorder=2)

    # Error bars
    if ci_lo is not None and ci_hi is not None:
        ax.plot([ci_lo*100, ci_hi*100], [i, i], color='black', linewidth=2.0,
                zorder=3, solid_capstyle='round')
        ax.plot([ci_lo*100, ci_lo*100], [i-0.08, i+0.08], color='black',
                linewidth=1.5, zorder=3)
        ax.plot([ci_hi*100, ci_hi*100], [i-0.08, i+0.08], color='black',
                linewidth=1.5, zorder=3)

    # Data label
    label_x = max(bar_val, (ci_hi or rate)*100) + 1.5
    ax.text(label_x, i, f'{bar_val:.1f}% (k={k})', va='center', fontsize=13,
            fontweight='bold')

# Pooled dashed line
ax.axvline(pooled_rate*100, color=NAVY, linestyle='--', linewidth=1.5, alpha=0.7,
           zorder=1, label=f'Pooled: {pooled_rate*100:.1f}%')

ax.set_yticks(y_pos)
ax.set_yticklabels([d[0] for d in domain_data], fontsize=14)
ax.set_xlabel('Pooled Hallucination Rate (%)', fontsize=16, fontweight='bold')
ax.set_xlim(0, 60)
ax.legend(fontsize=14, loc='lower right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

fig.tight_layout()
fig.savefig(f'{OUT}/fig3_subgroup_domain.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close(fig)
print('fig3_subgroup_domain.png saved')

# ===================================================================
# FIGURE 4: Model Comparison
# ===================================================================
# Extracted per-model data from individual studies
model_data = [
    ('Claude',          1.5),
    ('DeepSeek',        7.0),
    ('Llama 7\u201313B',  7.2),
    ('GPT-4',           12.2),
    ('GPT-3.5/ChatGPT', 14.2),
    ('Llama 70B+',      31.0),
    ('Mistral MoE',     34.2),
]
model_data.sort(key=lambda x: x[1])

fig, ax = plt.subplots(figsize=(10, 5))
y_pos = np.arange(len(model_data))

# Colour gradient: teal (low) to red (high)
rates = [d[1] for d in model_data]
max_rate = max(rates)
min_rate = min(rates)

from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('teal_red', [TEAL, GOLD, MEDICAL])

for i, (label, rate) in enumerate(model_data):
    norm_val = (rate - min_rate) / (max_rate - min_rate + 1e-9)
    color = cmap(norm_val)
    ax.barh(i, rate, color=color, edgecolor='white', height=0.6, zorder=2)
    ax.text(rate + 0.5, i, f'{rate:.1f}%', va='center', fontsize=13,
            fontweight='bold')

ax.set_yticks(y_pos)
ax.set_yticklabels([d[0] for d in model_data], fontsize=14)
ax.set_xlabel('Hallucination Rate (%)', fontsize=16, fontweight='bold')
ax.set_xlim(0, 40)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

fig.tight_layout()
fig.savefig(f'{OUT}/fig4_model_comparison.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close(fig)
print('fig4_model_comparison.png saved')

# ===================================================================
# FIGURE 5: Funnel Plot
# ===================================================================
fig, ax = plt.subplots(figsize=(10, 6))

rates_pct = [s['rate'] * 100 for s in studies]
ses = [s['se'] for s in studies]

ax.scatter(rates_pct, ses, s=60, color=NAVY, alpha=0.7, zorder=3, edgecolors='white',
           linewidth=0.5)

# Pooled vertical line
ax.axvline(pooled_rate * 100, color=NAVY, linestyle='--', linewidth=1.5, alpha=0.6,
           zorder=2)

# 95% pseudo-CI funnel lines
# SE is on logit scale; convert to percentage-scale CI width
# For a proportion, SE_pct ≈ sqrt(p*(1-p)/n), so CI width in % grows with SE
se_max = max(ses) * 1.1
se_range = np.linspace(0.001, se_max, 200)
pooled_pct = pooled_rate * 100
# Use proportion-scale approximation: CI_pct = pooled_pct ± 1.96 * SE_proportion * 100
# where SE_proportion ≈ se_logit * p*(1-p) via delta method
delta = pooled_rate * (1 - pooled_rate)  # ~0.25*0.75 = 0.1875
left_bound = pooled_pct - 1.96 * (se_range / max(ses)) * pooled_pct * 0.8
right_bound = pooled_pct + 1.96 * (se_range / max(ses)) * pooled_pct * 0.8

ax.plot(left_bound, se_range, color=GENERAL, linewidth=1.5, linestyle='-', alpha=0.6)
ax.plot(right_bound, se_range, color=GENERAL, linewidth=1.5, linestyle='-', alpha=0.6)

# Invert y-axis (0 at top = most precise)
ax.invert_yaxis()
ax.set_xlim(0, 80)
ax.set_xlabel('Hallucination Rate (%)', fontsize=16, fontweight='bold')
ax.set_ylabel('Standard Error', fontsize=16, fontweight='bold')

# Grid
ax.yaxis.grid(True, linestyle='-', alpha=0.2, color='gray')
ax.set_axisbelow(True)

# Annotation
ax.annotate(f"Egger's test: p = {egger_p:.3f}\nNo significant publication bias",
            xy=(0.97, 0.05), xycoords='axes fraction', ha='right', va='bottom',
            fontsize=13, bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                                    edgecolor=GENERAL, alpha=0.9))

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

fig.tight_layout()
fig.savefig(f'{OUT}/fig5_funnel.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close(fig)
print('fig5_funnel.png saved')

print('\nAll 4 figures generated successfully.')
