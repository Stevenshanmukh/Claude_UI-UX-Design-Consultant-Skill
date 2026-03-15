# UI/UX Scoring Rubric

This is the 12-category scoring system used in Phase 2 audits. Score each category 1-10 with a brief justification.

## Scoring Definitions

| Score | Meaning |
|-------|---------|
| **1-3** | Fundamentally broken. Major problems that actively harm the user experience. |
| **4-5** | Below average. Noticeable issues that make the product feel amateur or inconsistent. |
| **6-7** | Decent. Functional but generic, lacks polish or intentionality. |
| **8-9** | Strong. Professional quality with minor refinement opportunities. |
| **10** | Exceptional. Best-in-class execution that could serve as a reference example. |

---

## Category 1: Layout & Structure

**What to evaluate:** Grid system usage, section flow and content grouping, content hierarchy, alignment consistency, use of whitespace as a structural element, page-level composition.

- **Low scores (1-3):** No grid system, inconsistent alignment, sections feel disconnected, content floats without clear grouping.
- **High scores (8-10):** Clear grid with intentional breaks, logical content grouping, strong visual flow from section to section.

---

## Category 2: Typography

**What to evaluate:** Font selection quality, type scale consistency (how many distinct sizes and are they systematic), line-height and letter-spacing, heading hierarchy, body text readability, font pairing quality.

- **Low scores:** Too many font sizes with no system, poor readability, no clear heading hierarchy, generic or mismatched fonts.
- **High scores:** Systematic type scale (e.g., based on a modular ratio), excellent readability, clear hierarchy, distinctive and well-paired fonts.

---

## Category 3: Color System

**What to evaluate:** Palette coherence and harmony, contrast ratios, use of color for hierarchy and meaning, consistency of color application across components, brand alignment, light/dark considerations.

- **Low scores:** Random colors, poor contrast, color used inconsistently, no clear palette.
- **High scores:** Cohesive palette with clear primary/secondary/accent roles, excellent contrast, color reinforces hierarchy and brand.

---

## Category 4: Spacing & Rhythm

**What to evaluate:** Padding and margin consistency, vertical rhythm, spacing scale system, whitespace balance, breathing room between elements, section spacing consistency.

- **Low scores:** Random spacing values, cramped or uneven layouts, no consistent spacing scale.
- **High scores:** Systematic spacing scale (e.g., 4px/8px base), consistent rhythm, excellent whitespace management.

---

## Category 5: Component Design

**What to evaluate:** Button design and hierarchy (primary, secondary, ghost), card patterns, form elements, navigation components, footer, consistency across all components, visual quality of individual components.

- **Low scores:** Inconsistent button styles, mismatched component aesthetics, components feel like they're from different design systems.
- **High scores:** Unified component language, clear primary/secondary hierarchy, every component feels like it belongs to the same family.

---

## Category 6: Visual Hierarchy

**What to evaluate:** What draws the eye first, second, third on each page. Is the information priority correct? Are important elements emphasized and secondary elements subdued? Do headings, size, color, and weight work together to guide attention?

- **Low scores:** Everything competes for attention, important CTAs are buried, no clear reading path.
- **High scores:** Instant clarity about what matters most, natural eye flow, clear information layers.

---

## Category 7: CTA & Conversion

**What to evaluate:** Call-to-action button prominence and clarity, funnel flow (does the page guide users toward the goal?), value proposition visibility, trust signals, friction reduction, above-the-fold effectiveness.

- **Low scores:** CTAs blend into the page, unclear what action to take, value proposition buried.
- **High scores:** CTAs are unmissable and compelling, clear path to conversion, strong above-the-fold hook.

---

## Category 8: Accessibility

**What to evaluate:** Color contrast ratios (WCAG AA minimum), semantic HTML usage, keyboard navigation support, ARIA attributes where needed, focus indicators, alt text, touch target sizes on mobile.

- **Low scores:** Failing contrast ratios, div soup, no keyboard navigation, missing alt text.
- **High scores:** WCAG AA compliant, proper semantic structure, full keyboard support, ARIA where appropriate.

---

## Category 9: Branding & Identity

**What to evaluate:** Logo usage and placement, visual personality (does the site feel like the brand it represents?), consistency of brand expression, memorability, emotional tone alignment.

- **Low scores:** Generic, could be any brand, logo feels slapped on, no visual personality.
- **High scores:** Distinctive visual identity, brand personality comes through in every detail, memorable and cohesive.

---

## Category 10: Overall Polish

**What to evaluate:** Attention to detail, pixel-level refinement, edge cases (empty states, loading states, error states), consistency of quality across all pages, the "feel" of using the product.

- **Low scores:** Rough edges everywhere, inconsistent quality, feels like a prototype.
- **High scores:** Every detail is considered, consistent quality throughout, feels finished and intentional.

---

## Category 11: Motion & Interaction Design

**What to evaluate:** Hover states, transitions between states, page transitions, loading animations, micro-interactions, scroll-based animations, whether motion serves purpose or is gratuitous.

- **Low scores:** No interactive feedback, jarring state changes, either no animation or excessive meaningless animation.
- **High scores:** Purposeful motion that guides and delights, smooth transitions, meaningful micro-interactions, motion reinforces hierarchy.

---

## Category 12: Responsive & Mobile Design

**What to evaluate:** Mobile layout quality, breakpoint handling, touch targets, mobile navigation, content reflow, image handling across sizes, mobile-specific UX considerations.

- **Low scores:** Broken on mobile, elements overlap, tiny touch targets, desktop layout crammed into mobile.
- **High scores:** Mobile feels intentionally designed (not just responsive), appropriate content prioritization, excellent touch UX.

---

## Audit Output Format

Present the audit as a visual scorecard:

```
+--------------------------------------------------+
|          UI/UX DESIGN AUDIT - [Site Name]        |
+--------------------------------------------------+
|  Layout & Structure        ██████░░░░  6/10      |
|  Typography                ████░░░░░░  4/10      |
|  Color System              █████░░░░░  5/10      |
|  Spacing & Rhythm          ███░░░░░░░  3/10      |
|  Component Design          █████░░░░░  5/10      |
|  Visual Hierarchy          ██████░░░░  6/10      |
|  CTA & Conversion          ████░░░░░░  4/10      |
|  Accessibility             █████░░░░░  5/10      |
|  Branding & Identity       ██████░░░░  6/10      |
|  Overall Polish            ████░░░░░░  4/10      |
|  Motion & Interaction      ██░░░░░░░░  2/10      |
|  Responsive & Mobile       █████░░░░░  5/10      |
+--------------------------------------------------+
|  OVERALL SCORE                        4.6/10     |
+--------------------------------------------------+
```

After the scorecard, always provide:
1. **Top 3 Strengths** — What's already working well
2. **Top 5 Issues** — The most impactful problems, ranked by severity
3. **Quick Wins** — 2-3 things that would improve the feel immediately with minimal effort
