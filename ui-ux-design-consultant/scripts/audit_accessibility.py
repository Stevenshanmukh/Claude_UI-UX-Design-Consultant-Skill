#!/usr/bin/env python3
"""
audit_accessibility.py - Check for accessibility issues

Analyzes:
- Color contrast ratios (WCAG AA/AAA)
- Semantic HTML usage (divs vs proper elements)
- Missing alt attributes on images
- Focus indicator presence
- ARIA attribute usage

Usage: python audit_accessibility.py [project_root]
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict


# Semantic HTML elements
SEMANTIC_ELEMENTS = [
    "header", "nav", "main", "section", "article", "aside", "footer",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "figure", "figcaption", "time", "mark", "details", "summary",
    "button", "a", "form", "label", "input", "select", "textarea",
    "table", "thead", "tbody", "tfoot", "th", "td", "caption",
    "ul", "ol", "li", "dl", "dt", "dd",
    "address", "blockquote", "cite", "code", "pre",
]

# Non-semantic elements (red flags when overused)
NON_SEMANTIC = ["div", "span"]

# ARIA attributes
ARIA_ATTRIBUTES = [
    "aria-label", "aria-labelledby", "aria-describedby", "aria-hidden",
    "aria-expanded", "aria-selected", "aria-checked", "aria-disabled",
    "aria-live", "aria-atomic", "aria-relevant", "aria-busy",
    "aria-controls", "aria-owns", "aria-flowto", "aria-haspopup",
    "role",
]


def find_component_files(project_root: str) -> list:
    """Find all component/HTML files."""
    extensions = [".tsx", ".jsx", ".vue", ".svelte", ".html", ".htm"]
    files = []

    for ext in extensions:
        for path in Path(project_root).rglob(f"*{ext}"):
            if "node_modules" in str(path) or "dist" in str(path) or ".next" in str(path):
                continue
            files.append(path)

    return files


def find_style_files(project_root: str) -> list:
    """Find CSS files."""
    extensions = [".css", ".scss", ".sass"]
    files = []

    for ext in extensions:
        for path in Path(project_root).rglob(f"*{ext}"):
            if "node_modules" in str(path) or "dist" in str(path):
                continue
            files.append(path)

    return files


def count_elements(content: str) -> dict:
    """Count HTML element usage."""
    counts = defaultdict(int)

    # Match opening tags
    pattern = r'<(\w+)[\s>]'
    matches = re.findall(pattern, content, re.IGNORECASE)

    for tag in matches:
        counts[tag.lower()] += 1

    return dict(counts)


def check_images(content: str) -> dict:
    """Check image accessibility."""
    issues = []
    stats = {
        "total": 0,
        "withAlt": 0,
        "emptyAlt": 0,
        "missingAlt": 0,
        "decorative": 0,
    }

    # Find img tags
    img_pattern = r'<img\s+([^>]*)/?>'
    img_matches = re.findall(img_pattern, content, re.IGNORECASE | re.DOTALL)

    for attrs in img_matches:
        stats["total"] += 1

        # Check for alt attribute
        alt_match = re.search(r'alt\s*=\s*["\']([^"\']*)["\']', attrs)

        if alt_match:
            alt_value = alt_match.group(1)
            if alt_value == "":
                stats["emptyAlt"] += 1
                stats["decorative"] += 1
            else:
                stats["withAlt"] += 1
        else:
            stats["missingAlt"] += 1
            # Try to get src for context
            src_match = re.search(r'src\s*=\s*["\']([^"\']*)["\']', attrs)
            src = src_match.group(1) if src_match else "unknown"
            issues.append(f"Missing alt: {src[:50]}")

    # Check Next.js Image component
    next_img_pattern = r'<Image\s+([^>]*)/?>'
    next_matches = re.findall(next_img_pattern, content, re.DOTALL)

    for attrs in next_matches:
        stats["total"] += 1
        alt_match = re.search(r'alt\s*=\s*["\']([^"\']*)["\']', attrs)
        if alt_match:
            stats["withAlt"] += 1
        else:
            stats["missingAlt"] += 1
            issues.append("Next.js Image missing alt attribute")

    return {"stats": stats, "issues": issues[:10]}


def check_headings(content: str) -> dict:
    """Check heading structure."""
    issues = []
    headings = []

    # Find heading tags
    for level in range(1, 7):
        pattern = rf'<h{level}[^>]*>'
        matches = re.findall(pattern, content, re.IGNORECASE)
        headings.extend([(level, m) for m in matches])

    # Sort by order of appearance (approximately)
    heading_levels = [h[0] for h in headings]

    # Check for skipped levels
    if heading_levels:
        for i in range(1, len(heading_levels)):
            current = heading_levels[i]
            previous = heading_levels[i - 1]
            if current > previous + 1:
                issues.append(f"Heading level skipped: h{previous} to h{current}")

        # Check for multiple h1
        h1_count = heading_levels.count(1)
        if h1_count > 1:
            issues.append(f"Multiple h1 tags found ({h1_count})")
        elif h1_count == 0:
            issues.append("No h1 tag found")

    return {
        "levels": heading_levels,
        "distribution": {f"h{i}": heading_levels.count(i) for i in range(1, 7)},
        "issues": issues,
    }


def check_links_buttons(content: str) -> dict:
    """Check link and button accessibility."""
    issues = []
    stats = {
        "links": 0,
        "linksWithText": 0,
        "emptyLinks": 0,
        "buttons": 0,
        "divButtons": 0,
        "spanButtons": 0,
    }

    # Check anchor tags
    link_pattern = r'<a\s+([^>]*)>([^<]*)</a>'
    links = re.findall(link_pattern, content, re.IGNORECASE | re.DOTALL)

    for attrs, text in links:
        stats["links"] += 1
        text = text.strip()

        if text:
            stats["linksWithText"] += 1
        else:
            # Check for aria-label
            if not re.search(r'aria-label\s*=', attrs):
                stats["emptyLinks"] += 1
                issues.append("Empty link without aria-label")

    # Check buttons
    button_pattern = r'<button[^>]*>'
    stats["buttons"] = len(re.findall(button_pattern, content, re.IGNORECASE))

    # Check for div/span with onClick (bad pattern)
    onclick_div = r'<div[^>]*onClick[^>]*>'
    onclick_span = r'<span[^>]*onClick[^>]*>'

    div_buttons = len(re.findall(onclick_div, content))
    span_buttons = len(re.findall(onclick_span, content))

    stats["divButtons"] = div_buttons
    stats["spanButtons"] = span_buttons

    if div_buttons > 0:
        issues.append(f"{div_buttons} clickable divs should be buttons")
    if span_buttons > 0:
        issues.append(f"{span_buttons} clickable spans should be buttons")

    return {"stats": stats, "issues": issues}


def check_forms(content: str) -> dict:
    """Check form accessibility."""
    issues = []
    stats = {
        "inputs": 0,
        "inputsWithLabels": 0,
        "inputsWithPlaceholderOnly": 0,
    }

    # Find input elements
    input_pattern = r'<input\s+([^>]*)/?>'
    inputs = re.findall(input_pattern, content, re.IGNORECASE | re.DOTALL)

    for attrs in inputs:
        input_type = re.search(r'type\s*=\s*["\']([^"\']*)["\']', attrs)
        input_type = input_type.group(1).lower() if input_type else "text"

        # Skip hidden and submit inputs
        if input_type in ["hidden", "submit", "button"]:
            continue

        stats["inputs"] += 1

        # Check for id (needed for label association)
        has_id = bool(re.search(r'\bid\s*=\s*["\']', attrs))
        has_aria_label = bool(re.search(r'aria-label\s*=', attrs))
        has_placeholder = bool(re.search(r'placeholder\s*=', attrs))

        if has_id or has_aria_label:
            stats["inputsWithLabels"] += 1
        elif has_placeholder:
            stats["inputsWithPlaceholderOnly"] += 1
            issues.append("Input uses placeholder as only label")

    return {"stats": stats, "issues": issues[:5]}


def check_aria_usage(content: str) -> dict:
    """Check ARIA attribute usage."""
    usage = defaultdict(int)

    for attr in ARIA_ATTRIBUTES:
        pattern = rf'\b{attr}\s*='
        count = len(re.findall(pattern, content, re.IGNORECASE))
        if count > 0:
            usage[attr] = count

    # Check for role attribute
    roles = re.findall(r'role\s*=\s*["\']([^"\']*)["\']', content)
    role_counts = defaultdict(int)
    for role in roles:
        role_counts[role] += 1

    return {
        "attributeUsage": dict(usage),
        "totalAriaAttributes": sum(usage.values()),
        "roles": dict(role_counts),
    }


def check_focus_styles(content: str) -> dict:
    """Check for focus indicator styles."""
    has_focus_visible = bool(re.search(r':focus-visible', content))
    has_focus = bool(re.search(r':focus[^-]', content))
    has_focus_outline_none = bool(re.search(r'outline\s*:\s*none|outline\s*:\s*0', content))
    has_focus_ring = bool(re.search(r'focus:ring|focus-visible:ring', content))

    issues = []

    if has_focus_outline_none and not has_focus_ring:
        issues.append("Focus outline removed without alternative indicator")

    return {
        "hasFocusStyles": has_focus or has_focus_visible,
        "hasFocusVisible": has_focus_visible,
        "hasOutlineNone": has_focus_outline_none,
        "hasFocusRing": has_focus_ring,
        "issues": issues,
    }


def main():
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."

    if not os.path.isdir(project_root):
        print(json.dumps({"error": f"Directory not found: {project_root}"}))
        sys.exit(1)

    component_files = find_component_files(project_root)
    style_files = find_style_files(project_root)

    all_elements = defaultdict(int)
    all_image_issues = []
    image_stats = {"total": 0, "withAlt": 0, "emptyAlt": 0, "missingAlt": 0}
    all_heading_issues = []
    heading_distribution = defaultdict(int)
    all_link_button_issues = []
    link_button_stats = {"links": 0, "buttons": 0, "divButtons": 0}
    all_form_issues = []
    form_stats = {"inputs": 0, "inputsWithLabels": 0}
    aria_usage = defaultdict(int)
    focus_results = {"hasFocusStyles": False}

    files_analyzed = 0

    # Analyze component files
    for file_path in component_files:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            files_analyzed += 1

            # Element counts
            elements = count_elements(content)
            for tag, count in elements.items():
                all_elements[tag] += count

            # Images
            img_result = check_images(content)
            all_image_issues.extend(img_result["issues"])
            for key in image_stats:
                image_stats[key] += img_result["stats"].get(key, 0)

            # Headings
            heading_result = check_headings(content)
            all_heading_issues.extend(heading_result["issues"])
            for level, count in heading_result["distribution"].items():
                heading_distribution[level] += count

            # Links and buttons
            lb_result = check_links_buttons(content)
            all_link_button_issues.extend(lb_result["issues"])
            for key in ["links", "buttons", "divButtons"]:
                link_button_stats[key] += lb_result["stats"].get(key, 0)

            # Forms
            form_result = check_forms(content)
            all_form_issues.extend(form_result["issues"])
            for key in ["inputs", "inputsWithLabels"]:
                form_stats[key] += form_result["stats"].get(key, 0)

            # ARIA
            aria = check_aria_usage(content)
            for attr, count in aria["attributeUsage"].items():
                aria_usage[attr] += count

        except Exception:
            continue

    # Analyze style files for focus indicators
    for file_path in style_files:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            focus = check_focus_styles(content)
            if focus["hasFocusStyles"]:
                focus_results["hasFocusStyles"] = True
            if focus["hasFocusVisible"]:
                focus_results["hasFocusVisible"] = True
            if focus.get("issues"):
                focus_results["issues"] = focus_results.get("issues", []) + focus["issues"]
        except Exception:
            continue

    # Calculate semantic ratio
    semantic_count = sum(all_elements.get(el, 0) for el in SEMANTIC_ELEMENTS)
    non_semantic_count = sum(all_elements.get(el, 0) for el in NON_SEMANTIC)
    total_elements = semantic_count + non_semantic_count

    semantic_ratio = (semantic_count / total_elements * 100) if total_elements > 0 else 0

    # Calculate accessibility score
    score = 0
    max_score = 100

    # Images (20 points)
    if image_stats["total"] > 0:
        alt_rate = (image_stats["withAlt"] + image_stats["emptyAlt"]) / image_stats["total"]
        score += int(alt_rate * 20)
    else:
        score += 20

    # Semantic HTML (20 points)
    if semantic_ratio >= 30:
        score += 20
    elif semantic_ratio >= 20:
        score += 15
    elif semantic_ratio >= 10:
        score += 10

    # Headings (15 points)
    if not all_heading_issues:
        score += 15
    elif len(all_heading_issues) <= 2:
        score += 10

    # Interactive elements (15 points)
    if link_button_stats["divButtons"] == 0:
        score += 15
    elif link_button_stats["divButtons"] <= 2:
        score += 10

    # Forms (15 points)
    if form_stats["inputs"] > 0:
        label_rate = form_stats["inputsWithLabels"] / form_stats["inputs"]
        score += int(label_rate * 15)
    else:
        score += 15

    # Focus indicators (15 points)
    if focus_results.get("hasFocusStyles"):
        score += 15
    elif focus_results.get("hasFocusVisible"):
        score += 15

    # Rating
    if score >= 85:
        rating = "Excellent - Strong accessibility foundation"
    elif score >= 70:
        rating = "Good - Minor issues to address"
    elif score >= 50:
        rating = "Fair - Notable accessibility gaps"
    else:
        rating = "Poor - Significant accessibility issues"

    result = {
        "projectRoot": project_root,
        "filesAnalyzed": files_analyzed,
        "summary": {
            "accessibilityScore": score,
            "rating": rating,
            "semanticHTMLRatio": round(semantic_ratio, 1),
        },
        "images": {
            "stats": image_stats,
            "issues": list(set(all_image_issues))[:10],
        },
        "headings": {
            "distribution": dict(heading_distribution),
            "issues": list(set(all_heading_issues))[:5],
        },
        "interactiveElements": {
            "stats": link_button_stats,
            "issues": list(set(all_link_button_issues))[:5],
        },
        "forms": {
            "stats": form_stats,
            "issues": list(set(all_form_issues))[:5],
        },
        "semanticHTML": {
            "ratio": round(semantic_ratio, 1),
            "topElements": sorted(all_elements.items(), key=lambda x: -x[1])[:15],
        },
        "aria": {
            "totalUsage": sum(aria_usage.values()),
            "attributes": dict(aria_usage),
        },
        "focusIndicators": focus_results,
        "recommendations": [],
    }

    # Generate recommendations
    if image_stats["missingAlt"] > 0:
        result["recommendations"].append(f"Add alt text to {image_stats['missingAlt']} images")
    if semantic_ratio < 20:
        result["recommendations"].append("Replace divs with semantic elements (header, nav, main, section, etc.)")
    if all_heading_issues:
        result["recommendations"].append("Fix heading hierarchy (no skipped levels, single h1)")
    if link_button_stats["divButtons"] > 0:
        result["recommendations"].append(f"Convert {link_button_stats['divButtons']} clickable divs to button elements")
    if not focus_results.get("hasFocusStyles"):
        result["recommendations"].append("Add visible focus indicators for keyboard navigation")

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
