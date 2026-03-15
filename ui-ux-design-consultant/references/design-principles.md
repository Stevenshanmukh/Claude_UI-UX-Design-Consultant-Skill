# Design Principles Reference

Use these principles to guide and justify design decisions during audits and redesigns.

---

## Visual Hierarchy

- **Size, color, weight, and position** all contribute to hierarchy — use them consistently
- **Primary action** should be the most visually prominent element in any section
- **Maximum 3 levels** of visual importance per section (primary, secondary, tertiary)
- **F-pattern and Z-pattern** reading flows — place key content along these natural scan paths
- **Visual weight** increases with: larger size, bolder weight, saturated color, isolation (whitespace)

---

## Spacing System

- **Related elements closer together** (Gestalt Law of Proximity)
- **Consistent spacing creates rhythm** and professionalism
- **Base-8 system** recommended: 4, 8, 16, 24, 32, 48, 64, 96, 128px
- **Section spacing** should be 2-4x larger than element spacing
- **Breathing room** — elements need space to be individually perceived
- **Vertical rhythm** — maintain consistent line-height multiples

### Common Spacing Scale (8px base)
| Token | Value | Use Case |
|-------|-------|----------|
| xs | 4px | Tight inline spacing, icon gaps |
| sm | 8px | Related element gaps, small padding |
| md | 16px | Standard padding, form element gaps |
| lg | 24px | Card padding, section content spacing |
| xl | 32px | Component separation |
| 2xl | 48px | Section padding (mobile) |
| 3xl | 64px | Section padding (desktop) |
| 4xl | 96px | Major section breaks |

---

## Typography

- **Maximum 2 font families** (3 if one is monospace for code)
- **Type scale** should follow a ratio:
  - 1.125 (Major Second) — subtle, corporate
  - 1.25 (Major Third) — balanced, most common
  - 1.333 (Perfect Fourth) — expressive, editorial
  - 1.5 (Perfect Fifth) — dramatic, bold
- **Body text:** 16-18px minimum, line-height 1.5-1.7
- **Headings:** line-height 1.1-1.3 (tighter than body)
- **Measure (line length):** 45-75 characters optimal, 65ch ideal
- **Font weight hierarchy:** Regular (400) for body, Medium (500) for emphasis, Bold (700) for headings

### Type Scale Example (1.25 ratio, 16px base)
| Level | Size | Use |
|-------|------|-----|
| xs | 12px | Captions, labels |
| sm | 14px | Secondary text, metadata |
| base | 16px | Body text |
| lg | 20px | Lead paragraphs |
| xl | 25px | H4 |
| 2xl | 31px | H3 |
| 3xl | 39px | H2 |
| 4xl | 49px | H1 |
| 5xl | 61px | Display/Hero |

---

## Color System

- **60-30-10 rule:** 60% dominant (neutrals), 30% secondary (brand), 10% accent
- **Color reinforces hierarchy** — not decoration
- **Every color needs a clear role:** primary action, secondary action, success, warning, error, info
- **Neutral colors** do most of the work — accent colors create emphasis
- **Consistent saturation levels** across the palette for harmony

### Palette Structure
```
Primary    → Brand color, primary CTAs, key interactive elements
Secondary  → Supporting brand color, secondary actions
Accent     → Highlights, badges, special callouts (use sparingly)
Neutrals   → 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950
Success    → Confirmations, positive states (#22C55E family)
Warning    → Cautions, pending states (#F59E0B family)
Error      → Errors, destructive actions (#EF4444 family)
Info       → Informational, links (#3B82F6 family)
```

### Contrast Requirements (WCAG)
| Context | AA Minimum | AAA Target |
|---------|------------|------------|
| Normal text | 4.5:1 | 7:1 |
| Large text (18px+ bold, 24px+ regular) | 3:1 | 4.5:1 |
| UI components, graphical objects | 3:1 | — |

---

## Component Design

### Buttons
- **Clear hierarchy:** Primary (filled, high contrast), Secondary (outlined or muted), Tertiary (text/ghost)
- **Consistent sizing:** Match with form inputs (e.g., 40px, 44px, 48px heights)
- **Adequate padding:** Horizontal padding typically 1.5-2x vertical
- **Focus states:** Visible focus ring for accessibility
- **Disabled states:** Reduced opacity (50-60%), no hover effects

### Cards
- **Consistent border-radius** across all cards (typically 8px, 12px, or 16px)
- **Consistent padding** (16-24px typical)
- **Shadow or border** — pick one approach and stick with it
- **Content hierarchy** within cards should mirror page-level hierarchy

### Form Elements
- **Clear focus states** — ring or border change
- **Consistent sizing** with buttons
- **Visible labels** (not just placeholder text)
- **Error states** with clear visual indicator and message

---

## Responsive Design

- **Mobile is a different design**, not a smaller desktop
- **Content prioritization** — what matters most in limited viewport?
- **Touch targets:** minimum 44x44px (Apple HIG), 48x48px (Material)
- **Reduce visual complexity** on mobile — fewer columns, simpler layouts
- **Thumb zone** consideration for mobile navigation placement

### Common Breakpoints
| Name | Width | Use |
|------|-------|-----|
| sm | 640px | Large phones, small tablets |
| md | 768px | Tablets portrait |
| lg | 1024px | Tablets landscape, small laptops |
| xl | 1280px | Laptops, desktops |
| 2xl | 1536px | Large desktops |

---

## Motion & Animation

- **Purpose over decoration** — motion should guide, not distract
- **Duration guidelines:**
  - Micro-interactions: 100-200ms
  - State transitions: 200-300ms
  - Page transitions: 300-500ms
  - Complex animations: 500-1000ms
- **Easing:** Use ease-out for entrances, ease-in for exits, ease-in-out for continuous
- **Reduce motion** support — respect `prefers-reduced-motion` media query
- **Performance** — use transform and opacity for animations, avoid animating layout properties
