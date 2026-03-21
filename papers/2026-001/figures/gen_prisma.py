#!/usr/bin/env python3
"""
Generate a publication-quality PRISMA 2020 flow diagram using Graphviz.

Output:
  - fig1_prisma.svg
  - fig1_prisma.png (300 DPI)
"""

import graphviz
import os
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent

# ── Color palette ──────────────────────────────────────────────────────
NAVY = "#0B3C5D"
WHITE = "#FFFFFF"
EXCL_FILL = "#FFF0F0"
EXCL_BORDER = "#E74C3C"
INCL_FILL = "#F0FFF0"
INCL_BORDER = "#0F9D8A"
NOTE_COLOR = "#666666"

# ── Common node attributes ─────────────────────────────────────────────
COMMON = dict(
    shape="box",
    style="rounded,filled",
    fontname="Arial",
    fontsize="14",
    penwidth="2",
    margin="0.25,0.15",
)

MAIN_BOX = {**COMMON, "fillcolor": WHITE, "color": NAVY, "fontcolor": NAVY}
EXCL_BOX = {**COMMON, "fillcolor": EXCL_FILL, "color": EXCL_BORDER, "fontcolor": EXCL_BORDER}
INCL_BOX = {**COMMON, "fillcolor": INCL_FILL, "color": INCL_BORDER, "fontcolor": INCL_BORDER}

EDGE_ATTR = dict(color=NAVY, penwidth="2", arrowsize="0.9")


def build_diagram() -> graphviz.Digraph:
    g = graphviz.Digraph(
        "PRISMA",
        format="svg",
        engine="dot",
        graph_attr=dict(
            rankdir="TB",
            dpi="300",
            bgcolor="white",
            pad="0.5",
            nodesep="0.6",
            ranksep="0.7",
            fontname="Arial",
            size="8,11",
        ),
        node_attr=dict(fontname="Arial"),
        edge_attr=EDGE_ATTR,
    )

    # ── Phase labels (left column) ─────────────────────────────────────
    phase_attr = dict(
        shape="plaintext",
        fontname="Arial",
        fontsize="13",
        fontcolor=NAVY,
        width="1.2",
    )
    g.node("phase_id", label="Identification", **phase_attr)
    g.node("phase_sc", label="Screening", **phase_attr)
    g.node("phase_el", label="Eligibility", **phase_attr)
    g.node("phase_in", label="Included", **phase_attr)

    # ── Identification row ─────────────────────────────────────────────
    g.node(
        "db_search",
        label=(
            "Records identified through\n"
            "database searching\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "Semantic Scholar (n = 642ˢ)\n"
            "OpenAlex (n = 438ˢ)\n"
            "CrossRef (n = 167ˢ)\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "Total (n = 1,247ˢ)"
        ),
        **MAIN_BOX,
    )

    # ── Duplicates removed ─────────────────────────────────────────────
    g.node(
        "duplicates",
        label="Duplicates removed\n(n = 312ˢ)",
        **EXCL_BOX,
    )

    # ── Screening row ──────────────────────────────────────────────────
    g.node(
        "screened",
        label="Records screened\n(n = 935ˢ)",
        **MAIN_BOX,
    )

    g.node(
        "excl_screen",
        label="Excluded by\ntitle/abstract\n(n = 808ˢ)",
        **EXCL_BOX,
    )

    # ── Eligibility row ────────────────────────────────────────────────
    g.node(
        "fulltext",
        label="Full-text articles\nassessed for eligibility\n(n = 127ˢ)",
        **MAIN_BOX,
    )

    g.node(
        "excl_fulltext",
        label=(
            "Full-text articles excluded,\n"
            "with reasons (n = 89ˢ)\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "No quantitative rate (n = 34ˢ)\n"
            "Mitigation-only, no baseline (n = 22ˢ)\n"
            "Non-English (n = 18ˢ)\n"
            "Below citation threshold (n = 15ˢ)"
        ),
        **EXCL_BOX,
    )

    # ── Inclusion row ──────────────────────────────────────────────────
    g.node(
        "qual_synth",
        label="Studies included in\nqualitative synthesis\n(n = 42ˢ)",
        **INCL_BOX,
    )

    g.node(
        "quant_synth",
        label="Studies included in\nquantitative meta-analysis\n(n = 38)",
        **{**INCL_BOX, "penwidth": "3"},
    )

    # ── Footer note ────────────────────────────────────────────────────
    g.node(
        "note",
        label="Note: Values marked ˢ are simulated. n = number of records.",
        shape="none",
        fontname="Arial",
        fontsize="11",
        fontcolor=NOTE_COLOR,
    )

    # ── Edges (main flow) ──────────────────────────────────────────────
    g.edge("db_search", "screened", label="  After\n  deduplication")
    g.edge("screened", "fulltext")
    g.edge("fulltext", "qual_synth")
    g.edge("qual_synth", "quant_synth")
    g.edge("quant_synth", "note", style="invis")

    # ── Edges (exclusion, rightward) ───────────────────────────────────
    g.edge("db_search", "duplicates", label="", constraint="false")
    g.edge("screened", "excl_screen", label="", constraint="false")
    g.edge("fulltext", "excl_fulltext", label="", constraint="false")

    # ── Rank alignment ─────────────────────────────────────────────────
    with g.subgraph() as s:
        s.attr(rank="same")
        s.node("phase_id")
        s.node("db_search")

    with g.subgraph() as s:
        s.attr(rank="same")
        s.node("db_search")
        s.node("duplicates")

    with g.subgraph() as s:
        s.attr(rank="same")
        s.node("phase_sc")
        s.node("screened")
        s.node("excl_screen")

    with g.subgraph() as s:
        s.attr(rank="same")
        s.node("phase_el")
        s.node("fulltext")
        s.node("excl_fulltext")

    with g.subgraph() as s:
        s.attr(rank="same")
        s.node("phase_in")
        s.node("qual_synth")

    # Invisible edges to enforce phase label ordering
    g.edge("phase_id", "phase_sc", style="invis")
    g.edge("phase_sc", "phase_el", style="invis")
    g.edge("phase_el", "phase_in", style="invis")

    return g


def main():
    g = build_diagram()

    # Render SVG
    svg_path = str(OUTPUT_DIR / "fig1_prisma")
    g.render(filename=svg_path, format="svg", cleanup=True)
    print(f"SVG saved: {svg_path}.svg")

    # Render PNG at 300 DPI
    g.render(filename=svg_path, format="png", cleanup=True)
    print(f"PNG saved: {svg_path}.png")

    # Verify with PIL
    try:
        from PIL import Image

        img = Image.open(f"{svg_path}.png")
        w, h = img.size
        print(f"PNG dimensions: {w} x {h} px")
        file_size = os.path.getsize(f"{svg_path}.png")
        print(f"PNG file size: {file_size / 1024:.1f} KB")

        if w < 400 or h < 400:
            print("WARNING: Image dimensions seem too small.")
        else:
            print("Verification passed.")
    except ImportError:
        print("PIL not available; skipping dimension check.")
        file_size = os.path.getsize(f"{svg_path}.png")
        print(f"PNG file size: {file_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
