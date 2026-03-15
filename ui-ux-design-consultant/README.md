# UI/UX Design Consultant

A Claude Code skill that transforms amateur websites into professional-grade designs through structured diagnosis, strategic planning, and code-level execution.

## What It Does

This skill acts as a senior Design Architect embedded in your codebase. It doesn't just suggest improvements — it analyzes your existing code, produces data-driven audits, proposes a structured plan, and then executes the redesign directly in your files.

**Key capabilities:**

- **Framework-agnostic analysis** — Works with React, Next.js, Vue, Nuxt, Svelte, SvelteKit, or plain HTML/CSS
- **Data-driven audits** — Automated scripts scan for spacing inconsistencies, color palette bloat, typography chaos, and accessibility issues
- **12-category scoring** — Comprehensive rubric covering everything from visual hierarchy to mobile responsiveness
- **Structured execution** — Establishes design tokens first, then systematically updates components and pages
- **Before/after tracking** — Generates detailed changelogs documenting every modification

## Installation

Copy the `ui-ux-design-consultant/` folder to your Claude Code skills directory:

```bash
# macOS/Linux
cp -r ui-ux-design-consultant ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse ui-ux-design-consultant $env:USERPROFILE\.claude\skills\

# Windows (Command Prompt)
xcopy /E /I ui-ux-design-consultant %USERPROFILE%\.claude\skills\ui-ux-design-consultant
```

## How It Works

The skill follows a 6-phase workflow:

### Phase 0 — Environment Detection
Automatically detects your stack (framework, styling approach, component libraries, design tokens) before analysis begins.

### Phase 1 — Discovery
Asks targeted questions about your product, audience, goals, and constraints. Understands what needs to stay unchanged.

### Phase 2 — Scoring Audit
Runs automated scripts and produces a 12-category scorecard with specific, actionable findings.

### Phase 3 — Improvement Strategy
Proposes design direction, color palettes, typography, and a tiered implementation plan.

### Phase 4 — Approval Gate
Presents the complete plan and requests explicit approval before modifying any code.

### Phase 5 — Execution
Makes changes following established patterns — tokens first, then components, then pages. Works in incremental or batch mode.

### Phase 6 — Changelog
Documents everything: score improvements, changes by section, files modified, before/after summaries.

## The 12-Category Scoring Rubric

Each category is scored 1-10 with specific justification:

| Category | What It Measures |
|----------|------------------|
| **Layout & Structure** | Grid system, content grouping, alignment |
| **Typography** | Font selection, scale consistency, hierarchy |
| **Color System** | Palette coherence, contrast, brand alignment |
| **Spacing & Rhythm** | Consistency, whitespace balance, scale system |
| **Component Design** | Buttons, cards, forms — consistency and quality |
| **Visual Hierarchy** | Eye flow, information priority, emphasis |
| **CTA & Conversion** | Button prominence, funnel flow, value proposition |
| **Accessibility** | Contrast, semantic HTML, keyboard nav, ARIA |
| **Branding & Identity** | Visual personality, memorability, consistency |
| **Overall Polish** | Attention to detail, edge cases, consistency |
| **Motion & Interaction** | Hover states, transitions, purposeful animation |
| **Responsive & Mobile** | Mobile layout, touch targets, content reflow |

## Supported Frameworks

| Framework | Styling Support |
|-----------|-----------------|
| React / Next.js | Tailwind, CSS Modules, Styled Components, Plain CSS |
| Vue / Nuxt | Tailwind, Scoped Styles, CSS Modules |
| Svelte / SvelteKit | Tailwind, Scoped Styles |
| Plain HTML | CSS, SCSS, Tailwind |

## Automated Audit Scripts

The skill includes Python/Bash scripts that provide objective data:

| Script | What It Analyzes |
|--------|------------------|
| `detect_stack.sh` | Framework, styling, component libraries, file structure |
| `audit_spacing.py` | Unique spacing values, scale adherence, magic numbers |
| `audit_colors.py` | Palette bloat, hardcoded vs tokenized, WCAG contrast |
| `audit_typography.py` | Font sizes, type scale detection, font families |
| `audit_accessibility.py` | Alt text, semantic HTML, headings, ARIA usage |
| `audit_responsive.py` | Breakpoints, touch targets, viewport meta |
| `generate_changelog.py` | Git diff to structured changelog |

## Example Usage

**Trigger phrases:**
- "Audit the design of this site"
- "This looks amateur, help me fix it"
- "Do a UI review and tell me what's wrong"
- "Redesign the frontend to look professional"
- "Make this look world-class"

**Example conversation:**

```
You: The landing page looks amateur. Can you audit it and fix the design?

Claude: I'll analyze your codebase. First, let me detect your stack...

[Phase 0: Detects Next.js + Tailwind]

Before I dive into the audit, I have a few questions:
1. What type of product is this?
2. Who is the target audience?
3. What's the primary conversion goal?
...

[Phase 1-2: Discovery + Audit with 12-category scorecard]

Based on the audit, here's my improvement plan:
- Design direction: Clean Minimal
- Establish base-8 spacing system
- Consolidate to 6 font sizes
...

Ready to proceed with the redesign?

You: Yes, go ahead in batch mode.

[Phase 5-6: Executes changes + generates changelog]
```

## File Structure

```
ui-ux-design-consultant/
├── SKILL.md                 # Main skill instructions
├── README.md                # This file
├── LICENSE                  # MIT License
├── CONTRIBUTING.md          # Contribution guidelines
├── .gitignore               # Git ignore patterns
├── references/
│   ├── scoring-rubric.md    # Full 12-category rubric
│   ├── design-principles.md # Spacing, typography, color guidelines
│   ├── design-archetypes.md # 6 design direction options
│   ├── framework-react.md   # React/Next.js patterns
│   ├── framework-vue.md     # Vue/Nuxt patterns
│   ├── framework-svelte.md  # Svelte/SvelteKit patterns
│   ├── framework-html.md    # Plain HTML/CSS patterns
│   ├── styling-tailwind.md  # Tailwind customization guide
│   ├── styling-css-modules.md
│   └── styling-plain-css.md
├── scripts/
│   ├── detect_stack.sh      # Stack detection
│   ├── audit_spacing.py     # Spacing analysis
│   ├── audit_colors.py      # Color analysis
│   ├── audit_typography.py  # Typography analysis
│   ├── audit_accessibility.py
│   ├── audit_responsive.py
│   └── generate_changelog.py
├── templates/
│   ├── audit-report.md      # Scorecard template
│   ├── improvement-plan.md  # Plan template
│   ├── changelog.md         # Changelog template
│   ├── design-tokens-tailwind.js  # Starter Tailwind config
│   └── design-tokens-css.css      # Starter CSS variables
└── evals/
    └── evals.json           # Test cases
```

## Requirements

- Python 3.8+ (for audit scripts)
- Bash (Git Bash on Windows, or native on macOS/Linux)
- jq (for JSON processing in bash scripts) - [Install jq](https://jqlang.github.io/jq/download/)
- Git (for changelog generation)

## Design Direction Options

When brand guidelines are missing, the skill proposes 2-3 of these archetypes:

| Archetype | Best For |
|-----------|----------|
| **Clean Minimal** | SaaS, developer tools, premium products |
| **Bold & Vibrant** | Consumer apps, creative agencies, startups |
| **Corporate Premium** | Enterprise SaaS, financial products, B2B |
| **Startup Fresh** | Early-stage products, productivity tools |
| **Editorial** | Blogs, publications, content platforms |
| **Dark & Technical** | Developer tools, dashboards, analytics |

## Behavioral Notes

- **Never deletes content** without explicit approval
- **Never changes copy/text** unless asked
- **Preserves all functionality** (handlers, routing, data flow)
- **Respects the existing stack** — doesn't introduce new dependencies
- **Requests approval** before any code modifications

## Contributing

Contributions welcome. Key areas for improvement:

- Additional framework support (Angular, Astro, etc.)
- More audit scripts (animation patterns, bundle size impact)
- Enhanced accessibility checks
- Component library-specific guides (MUI, Chakra, etc.)

## License

MIT
