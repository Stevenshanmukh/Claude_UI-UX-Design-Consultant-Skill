#!/usr/bin/env python3
"""
generate_changelog.py - Generate structured changelog from git diff

After redesign execution, generates a structured changelog showing what changed,
in what files, organized by section.

Usage: python generate_changelog.py [project_root] [--from-commit COMMIT] [--format FORMAT]

Arguments:
  project_root    Path to the project (default: current directory)
  --from-commit   Compare against this commit (default: HEAD~1)
  --format        Output format: json or markdown (default: json)
"""

import os
import re
import sys
import json
import subprocess
import argparse
from pathlib import Path
from collections import defaultdict
from datetime import datetime


# File categories for organization
FILE_CATEGORIES = {
    "design-tokens": [
        "tailwind.config", "theme", "variables", "tokens",
        "globals.css", "index.css", "app.css",
    ],
    "components": [
        "components/", "ui/", "Button", "Card", "Input", "Modal",
        "Header", "Footer", "Nav", "Sidebar",
    ],
    "pages": [
        "pages/", "app/", "routes/", "views/",
    ],
    "styles": [
        ".css", ".scss", ".sass", ".less",
    ],
}


def run_git_command(cmd: list, cwd: str) -> tuple:
    """Run a git command and return output."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return result.stdout, result.returncode
    except subprocess.TimeoutExpired:
        return "", 1
    except Exception as e:
        return str(e), 1


def get_changed_files(project_root: str, from_commit: str) -> list:
    """Get list of changed files with their status."""
    cmd = ["git", "diff", "--name-status", from_commit, "HEAD"]
    output, code = run_git_command(cmd, project_root)

    if code != 0:
        # Try against working directory instead
        cmd = ["git", "diff", "--name-status", from_commit]
        output, code = run_git_command(cmd, project_root)

    if code != 0:
        return []

    files = []
    for line in output.strip().split("\n"):
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) >= 2:
            status = parts[0][0]  # M, A, D, R, etc.
            filepath = parts[-1]  # Handle renames
            files.append({"status": status, "path": filepath})

    return files


def get_file_diff_stats(project_root: str, filepath: str, from_commit: str) -> dict:
    """Get diff statistics for a file."""
    cmd = ["git", "diff", "--numstat", from_commit, "HEAD", "--", filepath]
    output, code = run_git_command(cmd, project_root)

    if code != 0 or not output.strip():
        cmd = ["git", "diff", "--numstat", from_commit, "--", filepath]
        output, code = run_git_command(cmd, project_root)

    if code != 0 or not output.strip():
        return {"additions": 0, "deletions": 0}

    parts = output.strip().split()
    if len(parts) >= 2:
        try:
            return {
                "additions": int(parts[0]) if parts[0] != "-" else 0,
                "deletions": int(parts[1]) if parts[1] != "-" else 0,
            }
        except ValueError:
            pass

    return {"additions": 0, "deletions": 0}


def get_file_diff(project_root: str, filepath: str, from_commit: str) -> str:
    """Get the actual diff content for a file."""
    cmd = ["git", "diff", from_commit, "HEAD", "--", filepath]
    output, code = run_git_command(cmd, project_root)

    if code != 0:
        cmd = ["git", "diff", from_commit, "--", filepath]
        output, code = run_git_command(cmd, project_root)

    return output if code == 0 else ""


def categorize_file(filepath: str) -> str:
    """Categorize a file based on its path."""
    filepath_lower = filepath.lower()

    for category, patterns in FILE_CATEGORIES.items():
        for pattern in patterns:
            if pattern.lower() in filepath_lower:
                return category

    return "other"


def analyze_css_changes(diff_content: str) -> list:
    """Analyze CSS-specific changes in a diff."""
    changes = []

    # Look for property changes
    property_patterns = [
        (r'\+.*color\s*:', "Color change"),
        (r'\+.*background', "Background change"),
        (r'\+.*font', "Typography change"),
        (r'\+.*margin|padding|gap', "Spacing change"),
        (r'\+.*border-radius', "Border radius change"),
        (r'\+.*box-shadow', "Shadow change"),
        (r'\+.*transition|animation', "Animation change"),
        (r'\+.*--[\w-]+\s*:', "CSS variable change"),
    ]

    for pattern, description in property_patterns:
        if re.search(pattern, diff_content, re.IGNORECASE):
            changes.append(description)

    return list(set(changes))


def analyze_component_changes(diff_content: str) -> list:
    """Analyze component-specific changes in a diff."""
    changes = []

    patterns = [
        (r'\+.*className', "Style class changes"),
        (r'\+.*style\s*=', "Inline style changes"),
        (r'\+.*tailwind', "Tailwind utility changes"),
        (r'\+.*<Button|<button', "Button modifications"),
        (r'\+.*<Card|<div.*card', "Card modifications"),
        (r'\+.*<Input|<input', "Input modifications"),
        (r'\+.*<Header|<header', "Header modifications"),
        (r'\+.*<Footer|<footer', "Footer modifications"),
        (r'\+.*<Nav|<nav', "Navigation modifications"),
    ]

    for pattern, description in patterns:
        if re.search(pattern, diff_content, re.IGNORECASE):
            changes.append(description)

    return list(set(changes))


def extract_tailwind_changes(diff_content: str) -> dict:
    """Extract Tailwind class changes from diff."""
    added_classes = []
    removed_classes = []

    # Find added lines with className
    added_lines = re.findall(r'^\+.*class(?:Name)?=["\']([^"\']+)["\']', diff_content, re.MULTILINE)
    removed_lines = re.findall(r'^-.*class(?:Name)?=["\']([^"\']+)["\']', diff_content, re.MULTILINE)

    for line in added_lines:
        added_classes.extend(line.split())

    for line in removed_lines:
        removed_classes.extend(line.split())

    # Find unique additions and removals
    new_classes = set(added_classes) - set(removed_classes)
    old_classes = set(removed_classes) - set(added_classes)

    return {
        "added": list(new_classes)[:20],
        "removed": list(old_classes)[:20],
    }


def generate_summary(changes_by_category: dict) -> dict:
    """Generate a summary of all changes."""
    summary = {
        "totalFiles": sum(len(files) for files in changes_by_category.values()),
        "totalAdditions": 0,
        "totalDeletions": 0,
        "categoryCounts": {},
    }

    for category, files in changes_by_category.items():
        summary["categoryCounts"][category] = len(files)
        for file_info in files:
            summary["totalAdditions"] += file_info.get("additions", 0)
            summary["totalDeletions"] += file_info.get("deletions", 0)

    return summary


def format_as_markdown(changelog: dict) -> str:
    """Format changelog as markdown."""
    lines = []

    lines.append(f"# Design Changelog")
    lines.append("")
    lines.append(f"Generated: {changelog['timestamp']}")
    lines.append("")

    # Summary
    summary = changelog["summary"]
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Files modified:** {summary['totalFiles']}")
    lines.append(f"- **Lines added:** {summary['totalAdditions']}")
    lines.append(f"- **Lines removed:** {summary['totalDeletions']}")
    lines.append("")

    # Changes by category
    for category, files in changelog["changesByCategory"].items():
        if not files:
            continue

        category_title = category.replace("-", " ").title()
        lines.append(f"## {category_title}")
        lines.append("")

        for file_info in files:
            status_icon = {
                "M": "Modified",
                "A": "Added",
                "D": "Deleted",
                "R": "Renamed",
            }.get(file_info["status"], "Changed")

            lines.append(f"### `{file_info['path']}`")
            lines.append(f"*{status_icon}* (+{file_info['additions']} / -{file_info['deletions']})")
            lines.append("")

            if file_info.get("analysisNotes"):
                for note in file_info["analysisNotes"]:
                    lines.append(f"- {note}")
                lines.append("")

    # File list
    lines.append("## All Modified Files")
    lines.append("")
    for category, files in changelog["changesByCategory"].items():
        for file_info in files:
            lines.append(f"- `{file_info['path']}`")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate changelog from git diff")
    parser.add_argument("project_root", nargs="?", default=".", help="Project root directory")
    parser.add_argument("--from-commit", default="HEAD~1", help="Compare against this commit")
    parser.add_argument("--format", choices=["json", "markdown"], default="json", help="Output format")

    args = parser.parse_args()
    project_root = args.project_root

    if not os.path.isdir(project_root):
        print(json.dumps({"error": f"Directory not found: {project_root}"}))
        sys.exit(1)

    # Check if it's a git repo
    git_check, code = run_git_command(["git", "status"], project_root)
    if code != 0:
        print(json.dumps({"error": "Not a git repository"}))
        sys.exit(1)

    # Get changed files
    changed_files = get_changed_files(project_root, args.from_commit)

    if not changed_files:
        output = {
            "timestamp": datetime.now().isoformat(),
            "fromCommit": args.from_commit,
            "summary": {"totalFiles": 0, "totalAdditions": 0, "totalDeletions": 0},
            "changesByCategory": {},
            "message": "No changes detected",
        }
        if args.format == "markdown":
            print("# Design Changelog\n\nNo changes detected.")
        else:
            print(json.dumps(output, indent=2))
        return

    # Organize changes by category
    changes_by_category = defaultdict(list)

    for file_info in changed_files:
        filepath = file_info["path"]
        category = categorize_file(filepath)

        # Get diff stats
        stats = get_file_diff_stats(project_root, filepath, args.from_commit)
        file_info.update(stats)

        # Get diff content for analysis
        diff_content = get_file_diff(project_root, filepath, args.from_commit)

        # Analyze changes based on file type
        analysis_notes = []

        if filepath.endswith((".css", ".scss", ".sass")):
            analysis_notes.extend(analyze_css_changes(diff_content))
        elif filepath.endswith((".tsx", ".jsx", ".vue", ".svelte")):
            analysis_notes.extend(analyze_component_changes(diff_content))

            # Extract Tailwind changes
            tw_changes = extract_tailwind_changes(diff_content)
            if tw_changes["added"]:
                analysis_notes.append(f"Added Tailwind classes: {', '.join(tw_changes['added'][:5])}")
            if tw_changes["removed"]:
                analysis_notes.append(f"Removed Tailwind classes: {', '.join(tw_changes['removed'][:5])}")

        file_info["analysisNotes"] = analysis_notes
        changes_by_category[category].append(file_info)

    # Generate summary
    summary = generate_summary(changes_by_category)

    changelog = {
        "timestamp": datetime.now().isoformat(),
        "projectRoot": project_root,
        "fromCommit": args.from_commit,
        "summary": summary,
        "changesByCategory": dict(changes_by_category),
    }

    # Output
    if args.format == "markdown":
        print(format_as_markdown(changelog))
    else:
        print(json.dumps(changelog, indent=2))


if __name__ == "__main__":
    main()
