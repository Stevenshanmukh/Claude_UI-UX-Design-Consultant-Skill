#!/usr/bin/env python3
"""
audit_typography.py - Scan for typography consistency

Analyzes:
- All font-size values used
- Whether they follow a modular scale
- Number of font families
- Line-height and letter-spacing consistency

Usage: python audit_typography.py [project_root]
"""

import os
import re
import sys
import json
import math
from pathlib import Path
from collections import defaultdict


# Common type scales (ratios)
TYPE_SCALES = {
    "minor-second": 1.067,
    "major-second": 1.125,
    "minor-third": 1.2,
    "major-third": 1.25,
    "perfect-fourth": 1.333,
    "augmented-fourth": 1.414,
    "perfect-fifth": 1.5,
    "golden-ratio": 1.618,
}

# Tailwind text sizes (in pixels)
TAILWIND_TEXT = {
    "xs": 12, "sm": 14, "base": 16, "lg": 18, "xl": 20,
    "2xl": 24, "3xl": 30, "4xl": 36, "5xl": 48, "6xl": 60,
    "7xl": 72, "8xl": 96, "9xl": 128,
}

# Common system fonts
SYSTEM_FONTS = [
    "system-ui", "-apple-system", "BlinkMacSystemFont", "Segoe UI",
    "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans",
    "Helvetica Neue", "Arial", "sans-serif", "serif", "monospace",
]


def find_style_files(project_root: str) -> list:
    """Find all CSS and component files."""
    extensions = [".css", ".scss", ".sass", ".less", ".tsx", ".jsx", ".vue", ".svelte", ".html"]
    files = []

    for ext in extensions:
        for path in Path(project_root).rglob(f"*{ext}"):
            if "node_modules" in str(path) or "dist" in str(path) or ".next" in str(path):
                continue
            files.append(path)

    return files


def extract_font_sizes(content: str) -> list:
    """Extract font-size values from CSS."""
    sizes = []

    # CSS font-size property
    pattern = r'font-size\s*:\s*([^;}\n]+)'
    matches = re.findall(pattern, content, re.IGNORECASE)

    for match in matches:
        value = match.strip()
        # Parse numeric value
        numeric_match = re.match(r'([\d.]+)(px|rem|em|%|vw|vh)?', value)
        if numeric_match:
            num = float(numeric_match.group(1))
            unit = numeric_match.group(2) or "px"

            # Convert to pixels
            px_value = num
            if unit == "rem":
                px_value = num * 16
            elif unit == "em":
                px_value = num * 16  # Approximate

            sizes.append({
                "raw": value,
                "value": num,
                "unit": unit,
                "px": px_value,
            })

    return sizes


def extract_tailwind_text(content: str) -> list:
    """Extract Tailwind text size classes."""
    sizes = []

    # Find class attributes
    class_pattern = r'class(?:Name)?=["\']([^"\']+)["\']|class(?:Name)?=\{[`"\']([^`"\']+)[`"\']\}'
    matches = re.findall(class_pattern, content)

    for match in matches:
        class_string = match[0] or match[1]
        classes = class_string.split()

        for cls in classes:
            base_class = cls.split(":")[-1]

            # Text size classes
            if base_class.startswith("text-"):
                size_part = base_class[5:]
                if size_part in TAILWIND_TEXT:
                    sizes.append({
                        "class": cls,
                        "size": size_part,
                        "px": TAILWIND_TEXT[size_part],
                    })
                # Arbitrary value
                elif size_part.startswith("[") and size_part.endswith("]"):
                    arbitrary = size_part[1:-1]
                    numeric_match = re.match(r'([\d.]+)(px|rem)?', arbitrary)
                    if numeric_match:
                        num = float(numeric_match.group(1))
                        unit = numeric_match.group(2) or "px"
                        px = num * 16 if unit == "rem" else num
                        sizes.append({
                            "class": cls,
                            "arbitrary": arbitrary,
                            "px": px,
                        })

    return sizes


def extract_font_families(content: str) -> list:
    """Extract font-family declarations."""
    families = []

    # CSS font-family
    pattern = r'font-family\s*:\s*([^;}\n]+)'
    matches = re.findall(pattern, content, re.IGNORECASE)

    for match in matches:
        # Split by comma and clean up
        fonts = [f.strip().strip("'\"") for f in match.split(",")]
        families.extend(fonts)

    return families


def extract_tailwind_fonts(content: str) -> list:
    """Extract Tailwind font family classes."""
    fonts = []

    class_pattern = r'class(?:Name)?=["\']([^"\']+)["\']'
    matches = re.findall(class_pattern, content)

    for match in matches:
        classes = match.split()
        for cls in classes:
            base_class = cls.split(":")[-1]
            if base_class.startswith("font-"):
                font_type = base_class[5:]
                if font_type in ["sans", "serif", "mono"]:
                    fonts.append(font_type)

    return fonts


def extract_line_heights(content: str) -> list:
    """Extract line-height values."""
    heights = []

    pattern = r'line-height\s*:\s*([^;}\n]+)'
    matches = re.findall(pattern, content, re.IGNORECASE)

    for match in matches:
        value = match.strip()
        numeric_match = re.match(r'([\d.]+)(px|rem|em|%)?', value)
        if numeric_match:
            heights.append({
                "raw": value,
                "value": float(numeric_match.group(1)),
                "unit": numeric_match.group(2) or "unitless",
            })

    return heights


def extract_letter_spacing(content: str) -> list:
    """Extract letter-spacing values."""
    spacings = []

    pattern = r'letter-spacing\s*:\s*([^;}\n]+)'
    matches = re.findall(pattern, content, re.IGNORECASE)

    for match in matches:
        value = match.strip()
        numeric_match = re.match(r'(-?[\d.]+)(px|rem|em)?', value)
        if numeric_match:
            spacings.append({
                "raw": value,
                "value": float(numeric_match.group(1)),
                "unit": numeric_match.group(2) or "em",
            })

    return spacings


def detect_type_scale(sizes_px: list) -> dict:
    """Detect if sizes follow a modular scale."""
    if len(sizes_px) < 3:
        return {"detected": False, "reason": "Not enough sizes to detect scale"}

    sorted_sizes = sorted(set(sizes_px))

    # Calculate ratios between consecutive sizes
    ratios = []
    for i in range(1, len(sorted_sizes)):
        if sorted_sizes[i - 1] > 0:
            ratio = sorted_sizes[i] / sorted_sizes[i - 1]
            ratios.append(ratio)

    if not ratios:
        return {"detected": False, "reason": "Could not calculate ratios"}

    # Find average ratio
    avg_ratio = sum(ratios) / len(ratios)

    # Check if ratios are consistent
    variance = sum((r - avg_ratio) ** 2 for r in ratios) / len(ratios)
    std_dev = math.sqrt(variance)

    # Match to known scales
    best_match = None
    best_diff = float("inf")

    for name, ratio in TYPE_SCALES.items():
        diff = abs(avg_ratio - ratio)
        if diff < best_diff:
            best_diff = diff
            best_match = name

    is_consistent = std_dev < 0.15  # Low variance indicates consistent scale

    return {
        "detected": is_consistent and best_diff < 0.1,
        "averageRatio": round(avg_ratio, 3),
        "standardDeviation": round(std_dev, 3),
        "closestScale": best_match,
        "closestScaleRatio": TYPE_SCALES.get(best_match),
        "isConsistent": is_consistent,
    }


def analyze_font_families(families: list) -> dict:
    """Analyze font family usage."""
    # Normalize and count
    normalized = defaultdict(int)
    custom_fonts = []

    for font in families:
        font_lower = font.lower()

        # Check if it's a system font
        is_system = any(sys_font.lower() in font_lower for sys_font in SYSTEM_FONTS)

        if is_system:
            normalized["system-fonts"] += 1
        else:
            normalized[font] += 1
            if font not in custom_fonts:
                custom_fonts.append(font)

    return {
        "customFonts": custom_fonts,
        "customFontCount": len(custom_fonts),
        "distribution": dict(normalized),
        "recommendation": (
            "Good - 2 or fewer custom fonts" if len(custom_fonts) <= 2
            else f"Consider reducing {len(custom_fonts)} custom fonts to 2-3 maximum"
        ),
    }


def main():
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."

    if not os.path.isdir(project_root):
        print(json.dumps({"error": f"Directory not found: {project_root}"}))
        sys.exit(1)

    files = find_style_files(project_root)

    all_font_sizes = []
    all_tailwind_text = []
    all_font_families = []
    all_tailwind_fonts = []
    all_line_heights = []
    all_letter_spacings = []
    files_analyzed = []

    for file_path in files:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")

            font_sizes = extract_font_sizes(content)
            tw_text = extract_tailwind_text(content)
            font_families = extract_font_families(content)
            tw_fonts = extract_tailwind_fonts(content)
            line_heights = extract_line_heights(content)
            letter_spacings = extract_letter_spacing(content)

            if font_sizes or tw_text or font_families:
                files_analyzed.append(str(file_path.relative_to(project_root)))

            all_font_sizes.extend(font_sizes)
            all_tailwind_text.extend(tw_text)
            all_font_families.extend(font_families)
            all_tailwind_fonts.extend(tw_fonts)
            all_line_heights.extend(line_heights)
            all_letter_spacings.extend(letter_spacings)

        except Exception:
            continue

    # Collect all pixel sizes
    all_px_sizes = [s["px"] for s in all_font_sizes]
    all_px_sizes.extend([s["px"] for s in all_tailwind_text])

    # Unique sizes
    unique_sizes = sorted(set(int(round(s)) for s in all_px_sizes))

    # Size frequency
    size_frequency = defaultdict(int)
    for s in all_px_sizes:
        size_frequency[int(round(s))] += 1

    # Detect type scale
    type_scale = detect_type_scale(unique_sizes)

    # Analyze font families
    family_analysis = analyze_font_families(all_font_families)

    # Tailwind font usage
    tw_font_counts = defaultdict(int)
    for f in all_tailwind_fonts:
        tw_font_counts[f] += 1

    # Line height analysis
    unique_line_heights = set(h["raw"] for h in all_line_heights)

    # Letter spacing analysis
    unique_letter_spacings = set(s["raw"] for s in all_letter_spacings)

    # Calculate consistency score
    consistency_score = 0

    # Fewer unique sizes is better (max 30 points)
    if len(unique_sizes) <= 8:
        consistency_score += 30
    elif len(unique_sizes) <= 12:
        consistency_score += 20
    elif len(unique_sizes) <= 16:
        consistency_score += 10

    # Type scale detected (max 30 points)
    if type_scale["detected"]:
        consistency_score += 30
    elif type_scale["isConsistent"]:
        consistency_score += 15

    # Font family discipline (max 20 points)
    if family_analysis["customFontCount"] <= 2:
        consistency_score += 20
    elif family_analysis["customFontCount"] <= 3:
        consistency_score += 10

    # Line height consistency (max 20 points)
    if len(unique_line_heights) <= 4:
        consistency_score += 20
    elif len(unique_line_heights) <= 6:
        consistency_score += 10

    # Rating
    if consistency_score >= 80:
        rating = "Excellent - Strong typographic system"
    elif consistency_score >= 60:
        rating = "Good - Mostly consistent typography"
    elif consistency_score >= 40:
        rating = "Fair - Some inconsistencies"
    else:
        rating = "Poor - Typography lacks system"

    result = {
        "projectRoot": project_root,
        "filesAnalyzed": len(files_analyzed),
        "summary": {
            "uniqueFontSizes": len(unique_sizes),
            "customFontFamilies": family_analysis["customFontCount"],
            "typeScaleDetected": type_scale["detected"],
            "consistencyScore": consistency_score,
            "rating": rating,
        },
        "fontSizes": {
            "uniqueValues": unique_sizes,
            "distribution": sorted(size_frequency.items(), key=lambda x: -x[1])[:15],
            "cssDeclarations": len(all_font_sizes),
            "tailwindClasses": len(all_tailwind_text),
        },
        "typeScale": type_scale,
        "fontFamilies": family_analysis,
        "tailwindFonts": dict(tw_font_counts),
        "lineHeight": {
            "uniqueValues": list(unique_line_heights),
            "count": len(all_line_heights),
        },
        "letterSpacing": {
            "uniqueValues": list(unique_letter_spacings),
            "count": len(all_letter_spacings),
        },
        "recommendations": [],
    }

    # Generate recommendations
    if len(unique_sizes) > 10:
        result["recommendations"].append(f"Consolidate {len(unique_sizes)} font sizes to 6-8 using a modular scale")
    if not type_scale["detected"]:
        result["recommendations"].append(f"Adopt a type scale (recommend {type_scale['closestScale']} - ratio {type_scale['closestScaleRatio']})")
    if family_analysis["customFontCount"] > 3:
        result["recommendations"].append(f"Reduce {family_analysis['customFontCount']} custom fonts to 2-3 maximum")
    if len(unique_line_heights) > 5:
        result["recommendations"].append("Standardize line-heights (recommend: 1.2 for headings, 1.5-1.7 for body)")

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
