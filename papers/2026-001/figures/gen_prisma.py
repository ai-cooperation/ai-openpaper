#!/usr/bin/env python3
"""Generate PRISMA 2020 flow diagram using matplotlib patches (no graphviz)."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ---------------------------------------------------------------------------
# Style constants
# ---------------------------------------------------------------------------
NAVY = "#0B3C5D"
RED_BORDER = "#E74C3C"
RED_FILL = "#FFF0F0"
TEAL_BORDER = "#0F9D8A"
GREEN_FILL = "#F0FFF0"
WHITE = "#FFFFFF"
GRAY_TEXT = "#888888"

FONT_FAMILY = "DejaVu Sans"
FONT_BOX = 12
FONT_BOX_TITLE = 14
FONT_FOOTER = 11

BOX_H = 0.22
BOX_W = 0.19
RAD = 0.015

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def draw_box(ax, cx, cy, w, h, lines, *,
             fill=WHITE, edge=NAVY, lw=2, title_line=0):
    box = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle=f"round,pad={RAD}",
        facecolor=fill, edgecolor=edge, linewidth=lw,
        transform=ax.transData, zorder=2,
    )
    ax.add_patch(box)
    n = len(lines)
    line_gap = 0.026
    total_h = (n - 1) * line_gap
    y_start = cy + total_h / 2
    for i, line in enumerate(lines):
        if not line:
            continue
        weight = "bold" if i == title_line else "normal"
        size = FONT_BOX_TITLE if i == title_line else FONT_BOX
        ax.text(cx, y_start - i * line_gap, line,
                ha="center", va="center", fontsize=size,
                fontfamily=FONT_FAMILY, fontweight=weight, zorder=3)

def draw_arrow(ax, x0, y0, x1, y1, color=NAVY, lw=2):
    arrow = FancyArrowPatch(
        (x0, y0), (x1, y1),
        arrowstyle="-|>", color=color, linewidth=lw,
        mutation_scale=18, zorder=1, shrinkA=0, shrinkB=0,
    )
    ax.add_patch(arrow)

# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 8))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

ROW1_Y = 0.72
ROW2_Y = 0.28
cols = [0.13, 0.37, 0.63, 0.87]
gap = 0.005

# ── ROW 1 ──────────────────────────────────────────────────────────────────

draw_box(ax, cols[0], ROW1_Y, BOX_W, BOX_H,
         ["Identification",
          "Semantic Scholar  n = 642",
          "OpenAlex  n = 438",
          "CrossRef  n = 167",
          "Total = 1,247"])

draw_box(ax, cols[1], ROW1_Y, BOX_W, BOX_H,
         ["After Deduplication",
          "n = 935",
          "",
          "(duplicates removed",
          "n = 312)"])

draw_box(ax, cols[2], ROW1_Y, BOX_W, BOX_H,
         ["Screening",
          "Title / abstract",
          "screened",
          "n = 935"])

draw_box(ax, cols[3], ROW1_Y, BOX_W, BOX_H,
         ["Excluded",
          "by title / abstract",
          "n = 808"],
         fill=RED_FILL, edge=RED_BORDER)

# Row 1 horizontal arrows
for i in range(3):
    draw_arrow(ax, cols[i] + BOX_W/2 + gap, ROW1_Y,
                   cols[i+1] - BOX_W/2 - gap, ROW1_Y)

# ── Vertical connector: Screening → Full-text ─────────────────────────────
# Diagonal arrow from bottom of Screening to top of Full-text assessed
draw_arrow(ax, cols[2], ROW1_Y - BOX_H/2 - gap,
               cols[0], ROW2_Y + BOX_H/2 + gap)

# ── ROW 2 ──────────────────────────────────────────────────────────────────

draw_box(ax, cols[0], ROW2_Y, BOX_W, BOX_H,
         ["Full-text Assessed",
          "for eligibility",
          "n = 127"])

EXC_W = BOX_W + 0.04
EXC_H = BOX_H + 0.04
draw_box(ax, cols[1], ROW2_Y, EXC_W, EXC_H,
         ["Excluded (n = 89)",
          "No quant rate: 34",
          "Mitigation-only: 22",
          "Non-English: 18",
          "Below citation: 15"],
         fill=RED_FILL, edge=RED_BORDER)

draw_box(ax, cols[2], ROW2_Y, BOX_W, BOX_H,
         ["Qualitative",
          "Synthesis",
          "n = 42"],
         fill=GREEN_FILL, edge=TEAL_BORDER)

draw_box(ax, cols[3], ROW2_Y, BOX_W, BOX_H,
         ["Quantitative",
          "Meta-Analysis",
          "n = 38"],
         fill=GREEN_FILL, edge=TEAL_BORDER, lw=3)

# Row 2 horizontal arrows
draw_arrow(ax, cols[0] + BOX_W/2 + gap, ROW2_Y,
               cols[1] - EXC_W/2 - gap, ROW2_Y)
draw_arrow(ax, cols[1] + EXC_W/2 + gap, ROW2_Y,
               cols[2] - BOX_W/2 - gap, ROW2_Y)
draw_arrow(ax, cols[2] + BOX_W/2 + gap, ROW2_Y,
               cols[3] - BOX_W/2 - gap, ROW2_Y)

# ── Footer ─────────────────────────────────────────────────────────────────
ax.text(0.5, 0.06, "Note: n = number of records.",
        ha="center", va="center", fontsize=FONT_FOOTER,
        fontfamily=FONT_FAMILY, color=GRAY_TEXT)

# ── Save ───────────────────────────────────────────────────────────────────
out = "/tmp/ai-openpaper/papers/2026-001/figures/fig1_prisma.png"
fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"Saved to {out}")

from PIL import Image
im = Image.open(out)
print(f"Dimensions: {im.size[0]}x{im.size[1]} px")
import os
print(f"File size: {os.path.getsize(out) / 1024:.0f} KB")
