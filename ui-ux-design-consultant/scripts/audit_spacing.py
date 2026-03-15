#!/usr/bin/env python3
"""
audit_spacing.py - Scan CSS/Tailwind files for spacing consistency

Analyzes:
- All unique spacing values used (margin, padding, gap)
- Whether they follow a consistent scale
- Count of "magic number" values vs systematic values
- Inconsistency score

Usage: python audit_spacing.py [project_root]
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict


# Common spacing scales (in pixels)
COMMON_SCALES = {
    "base-4": [0, 1, 2, 4, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32, 36, 40, 44, 48, 56, 64, 72, 80, 96],
    "base-8": [0, 4, 8, 12, 16, 24, 32, 40, 48, 64, 80, 96, 128],
    "tailwind": [0, 1, 2, 4, 5, 6, 8, 10, 11, 12, 14, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 72, 80, 96],
}

# Tailwind spacing classes
TAILWIND_SPACING = {
    "0": 0, "px": 1, "0.5": 2, "1": 4, "1.5": 6, "2": 8, "2.5": 10, "3": 12, "3.5": 14,
    "4": 16, "5": 20, "6": 24, "7": 28, "8": 32, "9": 36, "10": 40, "11": 44, "12": 48,
    "14": 56, "16": 64, "20": 80, "24": 96, "28": 112, "32": 128, "36": 144, "40": 160,
    "44": 176, "48": 192, "52": 208, "56": 224, "60": 240, "64": 256, "72": 288,
    "80": 320, "96": 384,
}

# CSS spacing properties
SPACING_PROPERTIES = [
    "margin", "margin-top", "margin-right", "margin-bottom", "margin-left",
    "padding", "padding-top", "padding-right", "padding-bottom", "padding-left",
    "gap", "row-gap", "column-gap", "grid-gap",
    "top", "right", "bottom", "left",
]

# Tailwind spacing prefixes
TAILWIND_PREFIXES = [
    "m-", "mx-", "my-", "mt-", "mr-", "mb-", "ml-",
    "p-", "px-", "py-", "pt-", "pr-", "pb-", "pl-",
    "gap-", "gap-x-", "gap-y-",
    "space-x-", "space-y-",
    "top-", "right-", "bottom-", "left-",
    "inset-", "inset-x-", "inset-y-",
]


def find_style_files(project_root: str) -> list:
    """Find all CSS, SCSS, and relevant style files."""
    extensions = [".css", ".scss", ".sass", ".less", ".tsx", ".jsx", ".vue", ".svelte", ".html"]
    files = []

    for ext in extensions:
        for path in Path(project_root).rglob(f"*{ext}"):
            # Skip node_modules and build directories
            if "node_modules" in str(path) or "dist" in str(path) or ".next" in str(path):
                continue
            files.append(path)

    return files


def extract_css_spacing(content: str) -> list:
    """Extract spacing values from CSS content."""
    values = []

    # Pattern for CSS property: value pairs
    for prop in SPACING_PROPERTIES:
        # Match property with various value formats
        pattern = rf'{prop}\s*:\s*([^;}}]+)'
        matches = re.findall(pattern, content, re.IGNORECASE)

        for match in matches:
            # Parse individual values (handles shorthand like "10px 20px")
            parts = match.strip().split()
            for part in parts:
                # Extract numeric value
                numeric_match = re.match(r'(-?\d+(?:\.\d+)?)(px|rem|em|%|vh|vw)?', part)
                if numeric_match:
                    value = float(numeric_match.group(1))
                    unit = numeric_match.group(2) or "px"

                    # Convert to pixels for comparison
                    if unit == "rem":
                        value *= 16
                    elif unit == "em":
                        value *= 16  # Approximate

                    values.append({
                        "raw": part,
                        "value": value,
                        "unit": unit,
                        "property": prop,
                    })

    return values


def extract_tailwind_spacing(content: str) -> list:
    """Extract Tailwind spacing classes from content."""
    values = []

    # Find class attributes
    class_pattern = r'class(?:Name)?=["\']([^"\']+)["\']|class(?:Name)?=\{[`"\']([^`"\']+)[`"\']\}'
    matches = re.findall(class_pattern, content)

    for match in matches:
        class_string = match[0] or match[1]
        classes = class_string.split()

        for cls in classes:
            # Check for spacing classes
            for prefix in TAILWIND_PREFIXES:
                if cls.startswith(prefix) or cls.startswith(f"-{prefix}"):
                    # Extract the value part
                    value_part = cls.replace(f"-{prefix}", "").replace(prefix, "")

                    # Handle responsive prefixes
                    if ":" in value_part:
                        value_part = value_part.split(":")[-1]

                    # Look up in Tailwind spacing scale
                    if value_part in TAILWIND_SPACING:
                        values.append({
                            "raw": cls,
                            "value": TAILWIND_SPACING[value_part],
                            "unit": "px",
                            "property": prefix.rstrip("-"),
                        })
                    # Handle arbitrary values like p-[20px]
                    elif value_part.startswith("[") and value_part.endswith("]"):
                        arbitrary = value_part[1:-1]
                        numeric_match = re.match(r'(-?\d+(?:\.\d+)?)(px|rem|em)?', arbitrary)
                        if numeric_match:
                            val = float(numeric_match.group(1))
                            unit = numeric_match.group(2) or "px"
                            if unit == "rem":
                                val *= 16
                            values.append({
                                "raw": cls,
                                "value": val,
                                "unit": unit,
                                "property": prefix.rstrip("-"),
                                "arbitrary": True,
                            })

    return values


def extract_css_variables(content: str) -> dict:
    """Extract CSS custom property definitions for spacing."""
    variables = {}

    # Pattern for --variable: value
    pattern = r'(--[\w-]+)\s*:\s*(\d+(?:\.\d+)?(?:px|rem|em)?)'
    matches = re.findall(pattern, content)

    for name, value in matches:
        if any(keyword in name.lower() for keyword in ["space", "margin", "padding", "gap", "size"]):
            numeric_match = re.match(r'(\d+(?:\.\d+)?)(px|rem|em)?', value)
            if numeric_match:
                val = float(numeric_match.group(1))
                unit = numeric_match.group(2) or "px"
                if unit == "rem":
                    val *= 16
                variables[name] = val

    return variables


def analyze_scale_adherence(values: list, scale_name: str = "base-8") -> dict:
    """Analyze how well values adhere to a spacing scale."""
    scale = COMMON_SCALES.get(scale_name, COMMON_SCALES["base-8"])

    on_scale = 0
    off_scale = 0
    off_scale_values = []

    unique_values = set()
    for v in values:
        px_value = int(round(v["value"]))
        unique_values.add(px_value)

        if px_value in scale or px_value == 0:
            on_scale += 1
        else:
            off_scale += 1
            off_scale_values.append(v["raw"])

    total = on_scale + off_scale
    adherence_rate = (on_scale / total * 100) if total > 0 else 100

    return {
        "scale": scale_name,
        "onScale": on_scale,
        "offScale": off_scale,
        "adherenceRate": round(adherence_rate, 1),
        "uniqueValues": len(unique_values),
        "offScaleExamples": list(set(off_scale_values))[:10],
    }


def calculate_inconsistency_score(values: list) -> dict:
    """Calculate an overall inconsistency score."""
    if not values:
        return {"score": 0, "rating": "No spacing values found"}

    unique_values = set(int(round(v["value"])) for v in values)
    total_values = len(values)

    # Factors affecting inconsistency:
    # 1. Number of unique values (more = worse)
    # 2. Scale adherence (lower = worse)
    # 3. Presence of arbitrary values

    arbitrary_count = sum(1 for v in values if v.get("arbitrary"))

    # Check adherence to common scales
    best_adherence = 0
    best_scale = "none"
    for scale_name in COMMON_SCALES:
        result = analyze_scale_adherence(values, scale_name)
        if result["adherenceRate"] > best_adherence:
            best_adherence = result["adherenceRate"]
            best_scale = scale_name

    # Calculate score (0-100, lower is better)
    unique_penalty = min(len(unique_values) * 2, 30)  # Max 30 points
    adherence_penalty = (100 - best_adherence) * 0.5  # Max 50 points
    arbitrary_penalty = min(arbitrary_count * 5, 20)  # Max 20 points

    score = unique_penalty + adherence_penalty + arbitrary_penalty
    score = min(max(score, 0), 100)  # Clamp to 0-100

    # Rating
    if score < 20:
        rating = "Excellent - Consistent spacing system"
    elif score < 40:
        rating = "Good - Minor inconsistencies"
    elif score < 60:
        rating = "Fair - Notable inconsistencies"
    elif score < 80:
        rating = "Poor - Many magic numbers"
    else:
        rating = "Critical - No apparent spacing system"

    return {
        "score": round(score, 1),
        "rating": rating,
        "bestMatchingScale": best_scale,
        "scaleAdherence": round(best_adherence, 1),
        "uniqueValueCount": len(unique_values),
        "arbitraryValueCount": arbitrary_count,
    }


def main():
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."

    if not os.path.isdir(project_root):
        print(json.dumps({"error": f"Directory not found: {project_root}"}))
        sys.exit(1)

    files = find_style_files(project_root)

    all_values = []
    css_variables = {}
    files_analyzed = []

    for file_path in files:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")

            # Extract CSS spacing
            css_values = extract_css_spacing(content)

            # Extract Tailwind spacing
            tw_values = extract_tailwind_spacing(content)

            # Extract CSS variables
            vars = extract_css_variables(content)
            css_variables.update(vars)

            if css_values or tw_values:
                files_analyzed.append(str(file_path.relative_to(project_root)))
                all_values.extend(css_values)
                all_values.extend(tw_values)
        except Exception as e:
            continue

    # Analyze results
    inconsistency = calculate_inconsistency_score(all_values)

    # Group values by pixel amount
    value_distribution = defaultdict(int)
    for v in all_values:
        px = int(round(v["value"]))
        value_distribution[px] += 1

    # Sort by frequency
    sorted_distribution = sorted(value_distribution.items(), key=lambda x: -x[1])[:20]

    result = {
        "projectRoot": project_root,
        "filesAnalyzed": len(files_analyzed),
        "totalSpacingValues": len(all_values),
        "uniqueValues": len(set(int(round(v["value"])) for v in all_values)),
        "inconsistencyScore": inconsistency,
        "valueDistribution": [{"px": k, "count": v} for k, v in sorted_distribution],
        "cssVariablesDefined": len(css_variables),
        "cssVariables": css_variables,
        "scaleAnalysis": {
            "base4": analyze_scale_adherence(all_values, "base-4"),
            "base8": analyze_scale_adherence(all_values, "base-8"),
            "tailwind": analyze_scale_adherence(all_values, "tailwind"),
        },
        "recommendations": [],
    }

    # Generate recommendations
    if inconsistency["score"] > 40:
        result["recommendations"].append("Establish a consistent spacing scale (recommend base-8: 4, 8, 16, 24, 32, 48, 64)")
    if inconsistency["arbitraryValueCount"] > 5:
        result["recommendations"].append(f"Replace {inconsistency['arbitraryValueCount']} arbitrary values with scale values")
    if len(css_variables) < 5 and len(all_values) > 20:
        result["recommendations"].append("Define CSS custom properties for spacing tokens")
    if inconsistency["uniqueValueCount"] > 15:
        result["recommendations"].append(f"Consolidate {inconsistency['uniqueValueCount']} unique values to reduce complexity")

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
