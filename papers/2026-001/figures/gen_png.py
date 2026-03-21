#!/usr/bin/env python3
"""Convert all SVG figures to PNG for the LLM Hallucination Rates Meta-Analysis paper.

Usage:
    pip install cairosvg Pillow
    python gen_png.py

Output: PNG files alongside SVGs in the same directory.
"""

import sys
from pathlib import Path

FIGURES_DIR = Path(__file__).parent
SVG_FILES = sorted(FIGURES_DIR.glob("fig*.svg"))

# Target DPI and scale for publication quality (300 DPI)
# Base SVG width is 800px at 96 DPI screen resolution
# Scale factor = 300 / 96 = 3.125 => round to 3 for clean output
SCALE_FACTOR = 3


def convert_with_cairosvg(svg_path: Path, png_path: Path) -> bool:
    """Convert SVG to PNG using cairosvg."""
    try:
        import cairosvg
    except ImportError:
        return False

    cairosvg.svg2png(
        url=str(svg_path),
        write_to=str(png_path),
        scale=SCALE_FACTOR,
    )
    return True


def convert_with_pillow_and_cairosvg(svg_path: Path, png_path: Path) -> bool:
    """Convert SVG to PNG using cairosvg with Pillow for verification."""
    converted = convert_with_cairosvg(svg_path, png_path)
    if not converted:
        return False

    try:
        from PIL import Image

        img = Image.open(png_path)
        print(f"  Verified: {img.size[0]}x{img.size[1]}px, mode={img.mode}")
    except ImportError:
        print("  (Pillow not available for verification)")

    return True


def convert_with_inkscape(svg_path: Path, png_path: Path) -> bool:
    """Fallback: convert SVG to PNG using Inkscape CLI."""
    import subprocess

    try:
        result = subprocess.run(
            [
                "inkscape",
                str(svg_path),
                "--export-type=png",
                f"--export-filename={png_path}",
                f"--export-dpi={96 * SCALE_FACTOR}",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def convert_with_rsvg(svg_path: Path, png_path: Path) -> bool:
    """Fallback: convert SVG to PNG using rsvg-convert (librsvg)."""
    import subprocess

    try:
        result = subprocess.run(
            [
                "rsvg-convert",
                str(svg_path),
                "-z", str(SCALE_FACTOR),
                "-o", str(png_path),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def main() -> int:
    if not SVG_FILES:
        print(f"No SVG files found in {FIGURES_DIR}")
        return 1

    print(f"Converting {len(SVG_FILES)} SVG figures to PNG (scale={SCALE_FACTOR}x)")
    print(f"Directory: {FIGURES_DIR}\n")

    converters = [
        ("cairosvg", convert_with_pillow_and_cairosvg),
        ("rsvg-convert", convert_with_rsvg),
        ("inkscape", convert_with_inkscape),
    ]

    success_count = 0
    fail_count = 0

    for svg_path in SVG_FILES:
        png_path = svg_path.with_suffix(".png")
        print(f"Converting: {svg_path.name} -> {png_path.name}")

        converted = False
        for name, converter in converters:
            try:
                converted = converter(svg_path, png_path)
                if converted:
                    file_size_kb = png_path.stat().st_size / 1024
                    print(f"  OK ({name}, {file_size_kb:.1f} KB)")
                    success_count += 1
                    break
            except Exception as e:
                print(f"  {name} failed: {e}")

        if not converted:
            print(f"  FAILED: No converter available for {svg_path.name}")
            fail_count += 1

    print(f"\nDone: {success_count} converted, {fail_count} failed")

    if fail_count > 0:
        print("\nTo install cairosvg (recommended):")
        print("  pip install cairosvg Pillow")
        print("\nOr install rsvg-convert:")
        print("  brew install librsvg      # macOS")
        print("  apt install librsvg2-bin   # Ubuntu/Debian")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
