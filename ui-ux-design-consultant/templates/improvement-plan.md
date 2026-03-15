# Design Improvement Plan — {{SITE_NAME}}

**Date:** {{DATE}}
**Design Direction:** {{DESIGN_ARCHETYPE}}
**Execution Mode:** {{EXECUTION_MODE}}

---

## Design Direction

### {{DESIGN_ARCHETYPE}}

{{ARCHETYPE_DESCRIPTION}}

**Why this direction:**
{{ARCHETYPE_RATIONALE}}

**Expected improvements:**
- {{IMPROVEMENT_1}}
- {{IMPROVEMENT_2}}
- {{IMPROVEMENT_3}}

---

## Brand Elements

### Color Palette

**Primary:** `{{PRIMARY_COLOR}}` — {{PRIMARY_ROLE}}
**Secondary:** `{{SECONDARY_COLOR}}` — {{SECONDARY_ROLE}}
**Accent:** `{{ACCENT_COLOR}}` — {{ACCENT_ROLE}}

**Neutral Scale:**
```
50:  {{NEUTRAL_50}}
100: {{NEUTRAL_100}}
200: {{NEUTRAL_200}}
300: {{NEUTRAL_300}}
400: {{NEUTRAL_400}}
500: {{NEUTRAL_500}}
600: {{NEUTRAL_600}}
700: {{NEUTRAL_700}}
800: {{NEUTRAL_800}}
900: {{NEUTRAL_900}}
950: {{NEUTRAL_950}}
```

**Semantic Colors:**
- Success: `{{SUCCESS_COLOR}}`
- Warning: `{{WARNING_COLOR}}`
- Error: `{{ERROR_COLOR}}`
- Info: `{{INFO_COLOR}}`

### Typography

**Heading Font:** {{HEADING_FONT}}
- Source: {{HEADING_SOURCE}}
- Weights: {{HEADING_WEIGHTS}}

**Body Font:** {{BODY_FONT}}
- Source: {{BODY_SOURCE}}
- Weights: {{BODY_WEIGHTS}}

**Type Scale:**
| Level | Size | Line Height | Use |
|-------|------|-------------|-----|
| xs | {{SIZE_XS}} | {{LH_XS}} | Captions, labels |
| sm | {{SIZE_SM}} | {{LH_SM}} | Secondary text |
| base | {{SIZE_BASE}} | {{LH_BASE}} | Body text |
| lg | {{SIZE_LG}} | {{LH_LG}} | Lead paragraphs |
| xl | {{SIZE_XL}} | {{LH_XL}} | H4 |
| 2xl | {{SIZE_2XL}} | {{LH_2XL}} | H3 |
| 3xl | {{SIZE_3XL}} | {{LH_3XL}} | H2 |
| 4xl | {{SIZE_4XL}} | {{LH_4XL}} | H1 |
| 5xl | {{SIZE_5XL}} | {{LH_5XL}} | Display |

### Spacing Scale

Using base-{{SPACING_BASE}} system:

| Token | Value | Use |
|-------|-------|-----|
| 1 | {{SPACE_1}} | Tight spacing |
| 2 | {{SPACE_2}} | Icon gaps |
| 3 | {{SPACE_3}} | Related elements |
| 4 | {{SPACE_4}} | Standard gaps |
| 6 | {{SPACE_6}} | Card padding |
| 8 | {{SPACE_8}} | Section gaps |
| 12 | {{SPACE_12}} | Section padding |
| 16 | {{SPACE_16}} | Major breaks |
| 24 | {{SPACE_24}} | Page sections |

---

## Implementation Tiers

### Tier 1 — Foundations
*Do first. Everything else builds on these.*

- [ ] **Design tokens setup**
  - Create/update {{TOKEN_LOCATION}}
  - Define color palette variables
  - Define spacing scale
  - Define typography tokens

- [ ] **Global styles**
  - Update base typography in {{GLOBAL_STYLES_LOCATION}}
  - Set body font, color, and background
  - Add font imports
  - Reset/normalize styles

### Tier 2 — Component Upgrades
*Apply the foundations to UI elements.*

- [ ] **Button hierarchy**
  - Primary button: {{PRIMARY_BUTTON_DESC}}
  - Secondary button: {{SECONDARY_BUTTON_DESC}}
  - Ghost/text button: {{GHOST_BUTTON_DESC}}
  - Sizes: sm, md, lg
  - States: hover, focus, disabled

- [ ] **Card standardization**
  - Padding: {{CARD_PADDING}}
  - Border radius: {{CARD_RADIUS}}
  - Shadow: {{CARD_SHADOW}}

- [ ] **Form elements**
  - Input styling consistent with buttons
  - Focus states with ring
  - Error states
  - Labels and help text

- [ ] **Navigation & header**
  - {{NAV_CHANGES}}

- [ ] **Footer**
  - {{FOOTER_CHANGES}}

### Tier 3 — Page-Level Improvements
*Apply components to layouts.*

{{#each PAGES}}
- [ ] **{{PAGE_NAME}}**
  - {{PAGE_CHANGE_1}}
  - {{PAGE_CHANGE_2}}
  - {{PAGE_CHANGE_3}}
{{/each}}

### Tier 4 — Polish & Delight
*Final layer of quality.*

- [ ] **Hover states and transitions**
  - Button hover: {{BUTTON_HOVER}}
  - Link hover: {{LINK_HOVER}}
  - Card hover: {{CARD_HOVER}}
  - Transition duration: {{TRANSITION_DURATION}}

- [ ] **Micro-interactions**
  - {{MICRO_1}}
  - {{MICRO_2}}

- [ ] **Edge cases**
  - Loading states
  - Empty states
  - Error states

- [ ] **Responsive refinements**
  - Mobile navigation
  - Touch target verification
  - Content reflow check

---

## Estimated Scope

| Category | Files | Changes |
|----------|-------|---------|
| Design tokens | {{TOKEN_FILES}} | {{TOKEN_CHANGES}} |
| Components | {{COMPONENT_FILES}} | {{COMPONENT_CHANGES}} |
| Pages | {{PAGE_FILES}} | {{PAGE_CHANGES}} |
| Global styles | {{GLOBAL_FILES}} | {{GLOBAL_CHANGES}} |
| **Total** | **{{TOTAL_FILES}}** | — |

---

## Approval Checklist

Before proceeding to execution:

- [ ] Design direction approved
- [ ] Color palette approved
- [ ] Typography approved
- [ ] Execution mode selected: {{EXECUTION_MODE}}
- [ ] Priority pages identified

**Ready to proceed?**
