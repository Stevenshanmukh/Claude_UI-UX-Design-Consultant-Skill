#!/usr/bin/env python3
"""
audit_colors.py - Scan for color usage and consistency

Analyzes:
- All color values (hex, rgb, hsl, CSS vars, Tailwind classes)
- Whether colors are tokenized (CSS variables) or hardcoded
- WCAG contrast ratio checking for text/background combos
- Number of unique colors (palette bloat detection)

Usage: python audit_colors.py [project_root]
"""

import os
import re
import sys
import json
import math
from pathlib import Path
from collections import defaultdict


# Tailwind color palette (subset for detection)
TAILWIND_COLORS = [
    "slate", "gray", "zinc", "neutral", "stone",
    "red", "orange", "amber", "yellow", "lime",
    "green", "emerald", "teal", "cyan", "sky",
    "blue", "indigo", "violet", "purple", "fuchsia",
    "pink", "rose", "black", "white", "transparent",
]

TAILWIND_SHADES = ["50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950"]


def find_style_files(project_root: str) -> list:
    """Find all CSS, SCSS, and relevant style files."""
    extensions = [".css", ".scss", ".sass", ".less", ".tsx", ".jsx", ".vue", ".svelte", ".html", ".js", ".ts"]
    files = []

    for ext in extensions:
        for path in Path(project_root).rglob(f"*{ext}"):
            if "node_modules" in str(path) or "dist" in str(path) or ".next" in str(path):
                continue
            files.append(path)

    return files


def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip("#")

    # Handle shorthand hex
    if len(hex_color) == 3:
        hex_color = "".join([c * 2 for c in hex_color])

    if len(hex_color) == 6:
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    return None


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB to hex."""
    return f"#{r:02x}{g:02x}{b:02x}"


def parse_rgb(rgb_string: str) -> tuple:
    """Parse rgb() or rgba() string to RGB tuple."""
    match = re.search(r'rgba?\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', rgb_string)
    if match:
        return tuple(int(x) for x in match.groups())
    return None


def parse_hsl(hsl_string: str) -> tuple:
    """Parse hsl() or hsla() string and convert to RGB."""
    match = re.search(r'hsla?\s*\(\s*([\d.]+)\s*,\s*([\d.]+)%?\s*,\s*([\d.]+)%?', hsl_string)
    if match:
        h = float(match.group(1)) / 360
        s = float(match.group(2)) / 100
        l = float(match.group(3)) / 100

        # HSL to RGB conversion
        if s == 0:
            r = g = b = l
        else:
            def hue_to_rgb(p, q, t):
                if t < 0:
                    t += 1
                if t > 1:
                    t -= 1
                if t < 1 / 6:
                    return p + (q - p) * 6 * t
                if t < 1 / 2:
                    return q
                if t < 2 / 3:
                    return p + (q - p) * (2 / 3 - t) * 6
                return p

            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r = hue_to_rgb(p, q, h + 1 / 3)
            g = hue_to_rgb(p, q, h)
            b = hue_to_rgb(p, q, h - 1 / 3)

        return (int(r * 255), int(g * 255), int(b * 255))

    return None


def get_relative_luminance(rgb: tuple) -> float:
    """Calculate relative luminance for WCAG contrast calculation."""
    def adjust(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = rgb
    return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)


def calculate_contrast_ratio(color1: tuple, color2: tuple) -> float:
    """Calculate WCAG contrast ratio between two colors."""
    l1 = get_relative_luminance(color1)
    l2 = get_relative_luminance(color2)

    lighter = max(l1, l2)
    darker = min(l1, l2)

    return (lighter + 0.05) / (darker + 0.05)


def extract_hex_colors(content: str) -> list:
    """Extract hex color values."""
    # Match #RGB, #RRGGBB, #RGBA, #RRGGBBAA
    pattern = r'#(?:[0-9a-fA-F]{3,4}){1,2}\b'
    matches = re.findall(pattern, content)
    return [m.lower() for m in matches]


def extract_rgb_colors(content: str) -> list:
    """Extract rgb() and rgba() color values."""
    pattern = r'rgba?\s*\(\s*\d+\s*,\s*\d+\s*,\s*\d+(?:\s*,\s*[\d.]+)?\s*\)'
    return re.findall(pattern, content, re.IGNORECASE)


def extract_hsl_colors(content: str) -> list:
    """Extract hsl() and hsla() color values."""
    pattern = r'hsla?\s*\(\s*[\d.]+\s*,\s*[\d.]+%?\s*,\s*[\d.]+%?(?:\s*,\s*[\d.]+)?\s*\)'
    return re.findall(pattern, content, re.IGNORECASE)


def extract_css_variables(content: str) -> dict:
    """Extract CSS custom property definitions for colors."""
    variables = {}

    # Match --variable: #hex or --variable: rgb() or --variable: hsl()
    patterns = [
        (r'(--[\w-]+)\s*:\s*(#(?:[0-9a-fA-F]{3,4}){1,2})', "hex"),
        (r'(--[\w-]+)\s*:\s*(rgba?\s*\([^)]+\))', "rgb"),
        (r'(--[\w-]+)\s*:\s*(hsla?\s*\([^)]+\))', "hsl"),
    ]

    for pattern, color_type in patterns:
        matches = re.findall(pattern, content)
        for name, value in matches:
            if any(keyword in name.lower() for keyword in ["color", "bg", "text", "border", "fill", "stroke", "primary", "secondary", "accent", "gray", "neutral"]):
                variables[name] = {"value": value, "type": color_type}

    return variables


def extract_tailwind_colors(content: str) -> list:
    """Extract Tailwind color classes."""
    colors = []

    # Color prefixes in Tailwind
    prefixes = [
        "bg-", "text-", "border-", "ring-", "fill-", "stroke-",
        "outline-", "decoration-", "accent-", "caret-",
        "divide-", "placeholder-", "from-", "via-", "to-",
    ]

    # Find class attributes
    class_pattern = r'class(?:Name)?=["\']([^"\']+)["\']|class(?:Name)?=\{[`"\']([^`"\']+)[`"\']\}'
    matches = re.findall(class_pattern, content)

    for match in matches:
        class_string = match[0] or match[1]
        classes = class_string.split()

        for cls in classes:
            # Remove responsive/state prefixes
            base_class = cls.split(":")[-1]

            for prefix in prefixes:
                if base_class.startswith(prefix):
                    color_part = base_class[len(prefix):]

                    # Check if it's a Tailwind color
                    for color in TAILWIND_COLORS:
                        if color_part.startswith(color):
                            colors.append({
                                "class": cls,
                                "color": color,
                                "prefix": prefix.rstrip("-"),
                            })
                            break

                    # Check for arbitrary colors
                    if color_part.startswith("[") and color_part.endswith("]"):
                        colors.append({
                            "class": cls,
                            "arbitrary": color_part[1:-1],
                            "prefix": prefix.rstrip("-"),
                        })

    return colors


def normalize_color(color_value: str) -> tuple:
    """Normalize any color format to RGB tuple."""
    color_value = color_value.strip().lower()

    if color_value.startswith("#"):
        return hex_to_rgb(color_value)
    elif color_value.startswith("rgb"):
        return parse_rgb(color_value)
    elif color_value.startswith("hsl"):
        return parse_hsl(color_value)

    return None


def analyze_palette_coherence(colors: list) -> dict:
    """Analyze if colors form a coherent palette."""
    # Group colors by hue
    hue_groups = defaultdict(list)

    for color in colors:
        rgb = normalize_color(color)
        if not rgb:
            continue

        r, g, b = rgb
        max_c = max(r, g, b)
        min_c = min(r, g, b)

        if max_c == min_c:
            hue = 0  # Gray
        elif max_c == r:
            hue = 60 * (((g - b) / (max_c - min_c)) % 6)
        elif max_c == g:
            hue = 60 * (((b - r) / (max_c - min_c)) + 2)
        else:
            hue = 60 * (((r - g) / (max_c - min_c)) + 4)

        # Group into 30-degree hue buckets
        bucket = int(hue // 30) * 30
        hue_groups[bucket].append(color)

    return {
        "hueGroupCount": len(hue_groups),
        "distribution": {str(k): len(v) for k, v in sorted(hue_groups.items())},
        "coherent": len(hue_groups) <= 5,  # Coherent if 5 or fewer hue groups
    }


def check_common_contrasts(colors: list) -> list:
    """Check contrast ratios for common color pairs."""
    results = []

    # Find likely text colors (darker) and background colors (lighter)
    color_rgbs = []
    for color in set(colors):
        rgb = normalize_color(color)
        if rgb:
            luminance = get_relative_luminance(rgb)
            color_rgbs.append((color, rgb, luminance))

    # Sort by luminance
    color_rgbs.sort(key=lambda x: x[2])

    # Check contrasts between light and dark colors
    dark_colors = [c for c in color_rgbs if c[2] < 0.3][:3]
    light_colors = [c for c in color_rgbs if c[2] > 0.7][:3]

    for dark in dark_colors:
        for light in light_colors:
            ratio = calculate_contrast_ratio(dark[1], light[1])
            wcag_aa = ratio >= 4.5
            wcag_aaa = ratio >= 7.0

            results.append({
                "foreground": dark[0],
                "background": light[0],
                "ratio": round(ratio, 2),
                "wcagAA": wcag_aa,
                "wcagAAA": wcag_aaa,
            })

    return results[:10]  # Return top 10 combinations


def main():
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."

    if not os.path.isdir(project_root):
        print(json.dumps({"error": f"Directory not found: {project_root}"}))
        sys.exit(1)

    files = find_style_files(project_root)

    all_hex_colors = []
    all_rgb_colors = []
    all_hsl_colors = []
    all_tailwind_colors = []
    css_variables = {}
    files_analyzed = []

    for file_path in files:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")

            hex_colors = extract_hex_colors(content)
            rgb_colors = extract_rgb_colors(content)
            hsl_colors = extract_hsl_colors(content)
            tw_colors = extract_tailwind_colors(content)
            vars = extract_css_variables(content)

            if hex_colors or rgb_colors or hsl_colors or tw_colors:
                files_analyzed.append(str(file_path.relative_to(project_root)))

            all_hex_colors.extend(hex_colors)
            all_rgb_colors.extend(rgb_colors)
            all_hsl_colors.extend(hsl_colors)
            all_tailwind_colors.extend(tw_colors)
            css_variables.update(vars)

        except Exception:
            continue

    # Normalize all colors
    all_colors = all_hex_colors + all_rgb_colors + all_hsl_colors

    # Count unique colors
    unique_colors = set()
    for color in all_colors:
        rgb = normalize_color(color)
        if rgb:
            unique_colors.add(rgb_to_hex(*rgb))

    # Color frequency
    color_frequency = defaultdict(int)
    for color in all_hex_colors:
        normalized = color.lower()
        if len(normalized) == 4:  # Expand shorthand
            normalized = f"#{normalized[1]*2}{normalized[2]*2}{normalized[3]*2}"
        color_frequency[normalized] += 1

    # Tailwind color usage
    tw_color_frequency = defaultdict(int)
    for tc in all_tailwind_colors:
        if "color" in tc:
            tw_color_frequency[tc["color"]] += 1

    # Analyze hardcoded vs tokenized
    hardcoded_count = len(all_hex_colors) + len(all_rgb_colors) + len(all_hsl_colors)
    tokenized_count = len(css_variables)

    # Palette coherence
    coherence = analyze_palette_coherence(list(unique_colors))

    # Contrast checks
    contrast_results = check_common_contrasts(list(unique_colors))

    # Calculate bloat score
    bloat_score = 0
    if len(unique_colors) > 50:
        bloat_score = 100
    elif len(unique_colors) > 30:
        bloat_score = 75
    elif len(unique_colors) > 20:
        bloat_score = 50
    elif len(unique_colors) > 10:
        bloat_score = 25

    # Rating
    if bloat_score < 25:
        rating = "Excellent - Well-constrained palette"
    elif bloat_score < 50:
        rating = "Good - Slightly expanded palette"
    elif bloat_score < 75:
        rating = "Fair - Consider consolidating colors"
    else:
        rating = "Poor - Significant palette bloat"

    result = {
        "projectRoot": project_root,
        "filesAnalyzed": len(files_analyzed),
        "summary": {
            "uniqueColors": len(unique_colors),
            "hardcodedValues": hardcoded_count,
            "cssVariablesDefined": tokenized_count,
            "tailwindColorsUsed": len(set(tc.get("color") for tc in all_tailwind_colors if tc.get("color"))),
            "bloatScore": bloat_score,
            "rating": rating,
        },
        "colorUsage": {
            "hex": len(all_hex_colors),
            "rgb": len(all_rgb_colors),
            "hsl": len(all_hsl_colors),
            "tailwind": len(all_tailwind_colors),
        },
        "topColors": sorted(color_frequency.items(), key=lambda x: -x[1])[:15],
        "topTailwindColors": sorted(tw_color_frequency.items(), key=lambda x: -x[1])[:10],
        "cssVariables": css_variables,
        "paletteCoherence": coherence,
        "contrastChecks": contrast_results,
        "recommendations": [],
    }

    # Generate recommendations
    if hardcoded_count > tokenized_count * 3:
        result["recommendations"].append("Tokenize colors using CSS custom properties")
    if len(unique_colors) > 20:
        result["recommendations"].append(f"Consolidate {len(unique_colors)} unique colors to a defined palette")
    if not coherence["coherent"]:
        result["recommendations"].append("Colors span too many hues - consider a more focused palette")
    failing_contrasts = [c for c in contrast_results if not c["wcagAA"]]
    if failing_contrasts:
        result["recommendations"].append(f"{len(failing_contrasts)} color combinations fail WCAG AA contrast requirements")

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
