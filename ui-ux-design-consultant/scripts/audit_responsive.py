#!/usr/bin/env python3
"""
audit_responsive.py - Check responsive design implementation

Analyzes:
- Breakpoint coverage and consistency
- Touch target sizes (min 44x44px)
- Viewport meta tag presence
- Mobile-specific considerations

Usage: python audit_responsive.py [project_root]
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict


# Common breakpoints
COMMON_BREAKPOINTS = {
    "tailwind": {"sm": 640, "md": 768, "lg": 1024, "xl": 1280, "2xl": 1536},
    "bootstrap": {"sm": 576, "md": 768, "lg": 992, "xl": 1200, "xxl": 1400},
    "material": {"xs": 0, "sm": 600, "md": 960, "lg": 1280, "xl": 1920},
}

# Tailwind responsive prefixes
TAILWIND_BREAKPOINTS = ["sm:", "md:", "lg:", "xl:", "2xl:"]


def find_files(project_root: str, extensions: list) -> list:
    """Find files with given extensions."""
    files = []
    for ext in extensions:
        for path in Path(project_root).rglob(f"*{ext}"):
            if "node_modules" in str(path) or "dist" in str(path) or ".next" in str(path):
                continue
            files.append(path)
    return files


def check_viewport_meta(project_root: str) -> dict:
    """Check for viewport meta tag in HTML files."""
    html_files = find_files(project_root, [".html", ".htm"])

    # Also check for Next.js/React root layouts
    component_files = find_files(project_root, [".tsx", ".jsx"])

    found = False
    correct = False
    issues = []

    viewport_pattern = r'<meta[^>]*name\s*=\s*["\']viewport["\'][^>]*>'
    content_pattern = r'content\s*=\s*["\']([^"\']+)["\']'

    for file_path in html_files + component_files:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")

            match = re.search(viewport_pattern, content, re.IGNORECASE)
            if match:
                found = True
                viewport_tag = match.group(0)

                content_match = re.search(content_pattern, viewport_tag)
                if content_match:
                    viewport_content = content_match.group(1).lower()

                    if "width=device-width" in viewport_content:
                        correct = True
                    else:
                        issues.append("Viewport missing width=device-width")

                    if "maximum-scale=1" in viewport_content or "user-scalable=no" in viewport_content:
                        issues.append("Viewport restricts zoom - accessibility issue")

        except Exception:
            continue

    return {
        "found": found,
        "correct": correct,
        "issues": issues,
    }


def extract_media_queries(content: str) -> list:
    """Extract media query breakpoints from CSS."""
    queries = []

    # Match @media queries
    pattern = r'@media[^{]+\{|@media[^{]+'
    matches = re.findall(pattern, content)

    for match in matches:
        # Extract width values
        width_pattern = r'(min|max)-width\s*:\s*(\d+)(px|em|rem)?'
        width_matches = re.findall(width_pattern, match)

        for direction, value, unit in width_matches:
            px_value = int(value)
            if unit == "em" or unit == "rem":
                px_value = int(value) * 16

            queries.append({
                "type": direction,
                "value": px_value,
                "unit": unit or "px",
                "raw": match.strip(),
            })

    return queries


def extract_tailwind_responsive(content: str) -> dict:
    """Extract Tailwind responsive class usage."""
    breakpoint_usage = defaultdict(int)

    # Find class attributes
    class_pattern = r'class(?:Name)?=["\']([^"\']+)["\']'
    matches = re.findall(class_pattern, content)

    for class_string in matches:
        classes = class_string.split()
        for cls in classes:
            for bp in TAILWIND_BREAKPOINTS:
                if cls.startswith(bp):
                    breakpoint_usage[bp.rstrip(":")] += 1
                    break

    return dict(breakpoint_usage)


def check_touch_targets(content: str) -> dict:
    """Check for touch target size issues."""
    issues = []
    stats = {
        "potentialIssues": 0,
        "explicitSizing": 0,
    }

    # Check for small explicit sizes on interactive elements
    small_patterns = [
        r'(width|height)\s*:\s*(\d+)(px)',
        r'(w|h)-(\d+)',  # Tailwind
    ]

    # Find buttons, links with small dimensions
    interactive_pattern = r'<(button|a)[^>]*class(?:Name)?=["\']([^"\']+)["\'][^>]*>'
    matches = re.findall(interactive_pattern, content, re.IGNORECASE)

    for tag, classes in matches:
        # Check for small Tailwind classes
        for cls in classes.split():
            # Width classes
            w_match = re.match(r'^w-(\d+)$', cls)
            if w_match:
                # Convert Tailwind spacing to px (w-8 = 32px, w-10 = 40px)
                value = int(w_match.group(1))
                if value < 11:  # w-11 = 44px
                    stats["potentialIssues"] += 1
                    issues.append(f"Small touch target: {tag} with {cls}")

            # Height classes
            h_match = re.match(r'^h-(\d+)$', cls)
            if h_match:
                value = int(h_match.group(1))
                if value < 11:
                    stats["potentialIssues"] += 1

    return {"stats": stats, "issues": issues[:10]}


def analyze_breakpoint_consistency(media_queries: list, tailwind_usage: dict) -> dict:
    """Analyze breakpoint consistency."""
    # Group CSS breakpoints
    css_breakpoints = defaultdict(int)
    for query in media_queries:
        css_breakpoints[query["value"]] += 1

    # Detect which system is being used
    detected_system = None

    for system_name, breakpoints in COMMON_BREAKPOINTS.items():
        matches = sum(1 for bp in breakpoints.values() if bp in css_breakpoints)
        if matches >= 3:
            detected_system = system_name
            break

    # Check for custom breakpoints
    known_values = set()
    for system_breakpoints in COMMON_BREAKPOINTS.values():
        known_values.update(system_breakpoints.values())

    custom_breakpoints = [bp for bp in css_breakpoints.keys() if bp not in known_values]

    return {
        "detectedSystem": detected_system,
        "cssBreakpoints": dict(css_breakpoints),
        "tailwindUsage": tailwind_usage,
        "customBreakpoints": custom_breakpoints,
        "isConsistent": len(custom_breakpoints) <= 2,
    }


def check_container_queries(content: str) -> bool:
    """Check if container queries are being used."""
    return bool(re.search(r'@container|container-type', content))


def check_responsive_images(content: str) -> dict:
    """Check for responsive image patterns."""
    stats = {
        "srcset": 0,
        "sizes": 0,
        "picture": 0,
        "nextImage": 0,
        "regularImg": 0,
    }

    # srcset attribute
    stats["srcset"] = len(re.findall(r'srcset\s*=', content, re.IGNORECASE))

    # sizes attribute
    stats["sizes"] = len(re.findall(r'sizes\s*=', content, re.IGNORECASE))

    # picture element
    stats["picture"] = len(re.findall(r'<picture', content, re.IGNORECASE))

    # Next.js Image
    stats["nextImage"] = len(re.findall(r'<Image\s', content))

    # Regular img
    stats["regularImg"] = len(re.findall(r'<img\s', content, re.IGNORECASE))

    return stats


def check_mobile_patterns(content: str) -> dict:
    """Check for mobile-specific patterns."""
    patterns = {
        "hiddenOnMobile": 0,
        "hiddenOnDesktop": 0,
        "mobileNav": 0,
        "hamburgerMenu": 0,
    }

    # Tailwind hidden patterns
    patterns["hiddenOnMobile"] = len(re.findall(r'hidden\s+(?:sm:|md:|lg:)(?:block|flex|grid|inline)', content))
    patterns["hiddenOnDesktop"] = len(re.findall(r'(?:sm:|md:|lg:|xl:)hidden', content))

    # Mobile nav indicators
    patterns["mobileNav"] = len(re.findall(r'mobile[-_]?nav|nav[-_]?mobile', content, re.IGNORECASE))

    # Hamburger menu
    patterns["hamburgerMenu"] = len(re.findall(r'hamburger|menu[-_]?icon|burger[-_]?menu', content, re.IGNORECASE))

    return patterns


def main():
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."

    if not os.path.isdir(project_root):
        print(json.dumps({"error": f"Directory not found: {project_root}"}))
        sys.exit(1)

    style_files = find_files(project_root, [".css", ".scss", ".sass"])
    component_files = find_files(project_root, [".tsx", ".jsx", ".vue", ".svelte", ".html"])

    all_media_queries = []
    all_tailwind_usage = defaultdict(int)
    all_touch_issues = []
    touch_stats = {"potentialIssues": 0}
    responsive_images = {"srcset": 0, "sizes": 0, "picture": 0, "nextImage": 0, "regularImg": 0}
    mobile_patterns = {"hiddenOnMobile": 0, "hiddenOnDesktop": 0}
    uses_container_queries = False

    files_analyzed = 0

    # Analyze style files
    for file_path in style_files:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            files_analyzed += 1

            media_queries = extract_media_queries(content)
            all_media_queries.extend(media_queries)

            if check_container_queries(content):
                uses_container_queries = True

        except Exception:
            continue

    # Analyze component files
    for file_path in component_files:
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            files_analyzed += 1

            # Tailwind responsive
            tw_usage = extract_tailwind_responsive(content)
            for bp, count in tw_usage.items():
                all_tailwind_usage[bp] += count

            # Touch targets
            touch_result = check_touch_targets(content)
            all_touch_issues.extend(touch_result["issues"])
            touch_stats["potentialIssues"] += touch_result["stats"]["potentialIssues"]

            # Responsive images
            img_stats = check_responsive_images(content)
            for key in responsive_images:
                responsive_images[key] += img_stats[key]

            # Mobile patterns
            mob_patterns = check_mobile_patterns(content)
            for key in mobile_patterns:
                mobile_patterns[key] += mob_patterns.get(key, 0)

        except Exception:
            continue

    # Check viewport
    viewport_result = check_viewport_meta(project_root)

    # Analyze breakpoint consistency
    breakpoint_analysis = analyze_breakpoint_consistency(
        all_media_queries,
        dict(all_tailwind_usage)
    )

    # Calculate responsive score
    score = 0

    # Viewport (20 points)
    if viewport_result["found"] and viewport_result["correct"]:
        score += 20
    elif viewport_result["found"]:
        score += 10

    # Breakpoint consistency (20 points)
    if breakpoint_analysis["isConsistent"]:
        score += 20
    elif breakpoint_analysis["detectedSystem"]:
        score += 15

    # Responsive images (20 points)
    total_images = responsive_images["regularImg"] + responsive_images["nextImage"]
    responsive_count = responsive_images["srcset"] + responsive_images["nextImage"] + responsive_images["picture"]
    if total_images > 0:
        img_ratio = min(responsive_count / total_images, 1)
        score += int(img_ratio * 20)
    else:
        score += 20

    # Touch targets (20 points)
    if touch_stats["potentialIssues"] == 0:
        score += 20
    elif touch_stats["potentialIssues"] <= 3:
        score += 15
    elif touch_stats["potentialIssues"] <= 5:
        score += 10

    # Mobile patterns (20 points)
    has_mobile_nav = mobile_patterns["mobileNav"] > 0 or mobile_patterns["hamburgerMenu"] > 0
    has_responsive_visibility = mobile_patterns["hiddenOnMobile"] > 0 or mobile_patterns["hiddenOnDesktop"] > 0

    if has_mobile_nav:
        score += 10
    if has_responsive_visibility:
        score += 10

    # Rating
    if score >= 85:
        rating = "Excellent - Strong responsive implementation"
    elif score >= 70:
        rating = "Good - Solid responsive patterns"
    elif score >= 50:
        rating = "Fair - Responsive gaps to address"
    else:
        rating = "Poor - Major responsive issues"

    result = {
        "projectRoot": project_root,
        "filesAnalyzed": files_analyzed,
        "summary": {
            "responsiveScore": score,
            "rating": rating,
        },
        "viewport": viewport_result,
        "breakpoints": breakpoint_analysis,
        "mediaQueries": {
            "total": len(all_media_queries),
            "uniqueBreakpoints": len(set(q["value"] for q in all_media_queries)),
        },
        "tailwindResponsive": dict(all_tailwind_usage),
        "touchTargets": {
            "potentialIssues": touch_stats["potentialIssues"],
            "issues": list(set(all_touch_issues))[:10],
        },
        "responsiveImages": responsive_images,
        "mobilePatterns": mobile_patterns,
        "containerQueries": uses_container_queries,
        "recommendations": [],
    }

    # Generate recommendations
    if not viewport_result["found"]:
        result["recommendations"].append("Add viewport meta tag: <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">")
    if viewport_result["issues"]:
        result["recommendations"].extend(viewport_result["issues"])
    if not breakpoint_analysis["isConsistent"]:
        result["recommendations"].append("Standardize breakpoints to a consistent system (Tailwind, Bootstrap, or custom)")
    if touch_stats["potentialIssues"] > 0:
        result["recommendations"].append(f"Increase touch target sizes ({touch_stats['potentialIssues']} elements may be too small)")
    if responsive_images["regularImg"] > responsive_images["srcset"] + responsive_images["nextImage"]:
        result["recommendations"].append("Use responsive images (srcset, Next.js Image, or picture element)")
    if not has_mobile_nav and files_analyzed > 10:
        result["recommendations"].append("Consider adding a mobile navigation pattern")

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
