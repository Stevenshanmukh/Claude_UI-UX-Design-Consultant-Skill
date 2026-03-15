# Plain CSS / SCSS Design Implementation Guide

This reference covers design implementation patterns for vanilla CSS and SCSS projects.

---

## File Organization

### Basic Structure
```
css/
├── variables.css       # Design tokens
├── reset.css           # CSS reset/normalize
├── base.css            # Base typography, body styles
├── utilities.css       # Utility classes
├── components/
│   ├── buttons.css
│   ├── cards.css
│   ├── forms.css
│   └── navigation.css
├── layouts/
│   ├── grid.css
│   ├── header.css
│   └── footer.css
└── main.css            # Imports all files
```

### SCSS Structure
```
scss/
├── _variables.scss     # Tokens and variables
├── _mixins.scss        # Reusable mixins
├── _functions.scss     # SCSS functions
├── _reset.scss         # Reset styles
├── base/
│   ├── _typography.scss
│   └── _global.scss
├── components/
│   ├── _buttons.scss
│   ├── _cards.scss
│   └── _forms.scss
├── layouts/
│   ├── _grid.scss
│   └── _sections.scss
└── main.scss           # Main entry point
```

---

## Design Token System

### CSS Custom Properties

```css
/* variables.css */
:root {
  /* ===== Colors ===== */
  /* Primary palette */
  --color-primary-50: #eff6ff;
  --color-primary-100: #dbeafe;
  --color-primary-200: #bfdbfe;
  --color-primary-300: #93c5fd;
  --color-primary-400: #60a5fa;
  --color-primary-500: #3b82f6;
  --color-primary-600: #2563eb;
  --color-primary-700: #1d4ed8;
  --color-primary-800: #1e40af;
  --color-primary-900: #1e3a8a;
  --color-primary-950: #172554;

  /* Neutral palette */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-300: #d1d5db;
  --color-gray-400: #9ca3af;
  --color-gray-500: #6b7280;
  --color-gray-600: #4b5563;
  --color-gray-700: #374151;
  --color-gray-800: #1f2937;
  --color-gray-900: #111827;
  --color-gray-950: #030712;

  /* Semantic colors */
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;

  /* Functional aliases */
  --color-text: var(--color-gray-900);
  --color-text-muted: var(--color-gray-500);
  --color-background: #ffffff;
  --color-surface: var(--color-gray-50);
  --color-border: var(--color-gray-200);

  /* ===== Typography ===== */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-display: 'Cal Sans', var(--font-sans);
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* Type scale (1.25 ratio) */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;
  --text-4xl: 2.25rem;
  --text-5xl: 3rem;
  --text-6xl: 3.75rem;

  /* Font weights */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;

  /* Line heights */
  --leading-none: 1;
  --leading-tight: 1.25;
  --leading-snug: 1.375;
  --leading-normal: 1.5;
  --leading-relaxed: 1.625;
  --leading-loose: 2;

  /* ===== Spacing ===== */
  --space-px: 1px;
  --space-0: 0;
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-5: 1.25rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-10: 2.5rem;
  --space-12: 3rem;
  --space-16: 4rem;
  --space-20: 5rem;
  --space-24: 6rem;
  --space-32: 8rem;

  /* ===== Border Radius ===== */
  --radius-none: 0;
  --radius-sm: 0.125rem;
  --radius-default: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-2xl: 1rem;
  --radius-3xl: 1.5rem;
  --radius-full: 9999px;

  /* ===== Shadows ===== */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-default: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  --shadow-2xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);
  --shadow-inner: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);

  /* ===== Transitions ===== */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
  --transition-slower: 500ms ease;

  /* ===== Z-Index Scale ===== */
  --z-dropdown: 1000;
  --z-sticky: 1020;
  --z-fixed: 1030;
  --z-modal-backdrop: 1040;
  --z-modal: 1050;
  --z-popover: 1060;
  --z-tooltip: 1070;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-text: var(--color-gray-100);
    --color-text-muted: var(--color-gray-400);
    --color-background: var(--color-gray-950);
    --color-surface: var(--color-gray-900);
    --color-border: var(--color-gray-800);
  }
}

/* Manual dark mode toggle */
.dark {
  --color-text: var(--color-gray-100);
  --color-text-muted: var(--color-gray-400);
  --color-background: var(--color-gray-950);
  --color-surface: var(--color-gray-900);
  --color-border: var(--color-gray-800);
}
```

### SCSS Variables

```scss
/* _variables.scss */

// Colors
$colors: (
  'primary': (
    50: #eff6ff,
    100: #dbeafe,
    500: #3b82f6,
    600: #2563eb,
    700: #1d4ed8,
  ),
  'gray': (
    50: #f9fafb,
    100: #f3f4f6,
    // ... etc
  ),
);

// Spacing
$spacing: (
  1: 0.25rem,
  2: 0.5rem,
  3: 0.75rem,
  4: 1rem,
  6: 1.5rem,
  8: 2rem,
  12: 3rem,
  16: 4rem,
);

// Typography
$font-sans: 'Inter', system-ui, sans-serif;
$font-display: 'Cal Sans', $font-sans;

$font-sizes: (
  'xs': 0.75rem,
  'sm': 0.875rem,
  'base': 1rem,
  'lg': 1.125rem,
  'xl': 1.25rem,
  '2xl': 1.5rem,
  '3xl': 1.875rem,
  '4xl': 2.25rem,
);

// Helper functions
@function color($name, $shade: 500) {
  @return map-get(map-get($colors, $name), $shade);
}

@function space($size) {
  @return map-get($spacing, $size);
}
```

---

## Component Patterns

### Button Component

```css
/* components/buttons.css */

/* Base button */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  line-height: var(--leading-normal);
  text-decoration: none;
  border: 1px solid transparent;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn:focus-visible {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 2px;
}

.btn:disabled,
.btn[disabled] {
  opacity: 0.5;
  pointer-events: none;
}

/* Variants */
.btn-primary {
  background-color: var(--color-primary-600);
  color: white;
}

.btn-primary:hover {
  background-color: var(--color-primary-700);
}

.btn-primary:active {
  background-color: var(--color-primary-800);
}

.btn-secondary {
  background-color: var(--color-surface);
  border-color: var(--color-border);
  color: var(--color-text);
}

.btn-secondary:hover {
  background-color: var(--color-gray-100);
}

.btn-ghost {
  background-color: transparent;
  color: var(--color-text);
}

.btn-ghost:hover {
  background-color: var(--color-surface);
}

.btn-danger {
  background-color: var(--color-error);
  color: white;
}

.btn-danger:hover {
  background-color: #dc2626;
}

/* Sizes */
.btn-sm {
  padding: var(--space-1) var(--space-3);
  font-size: var(--text-xs);
}

.btn-lg {
  padding: var(--space-3) var(--space-6);
  font-size: var(--text-base);
}

/* Full width */
.btn-full {
  width: 100%;
}

/* Icon button */
.btn-icon {
  padding: var(--space-2);
}

.btn-icon.btn-sm {
  padding: var(--space-1);
}

.btn-icon.btn-lg {
  padding: var(--space-3);
}
```

### Card Component

```css
/* components/cards.css */

.card {
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
}

.card-shadow {
  box-shadow: var(--shadow-md);
  border: none;
}

.card-header {
  padding: var(--space-4) var(--space-6);
}

.card-header-bordered {
  border-bottom: 1px solid var(--color-border);
}

.card-title {
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--color-text);
  margin: 0;
}

.card-description {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  margin-top: var(--space-1);
}

.card-content {
  padding: var(--space-6);
}

.card-content:first-child {
  padding-top: var(--space-6);
}

.card-footer {
  padding: var(--space-4) var(--space-6);
  background-color: var(--color-surface);
  border-top: 1px solid var(--color-border);
}

/* Card variants */
.card-interactive {
  cursor: pointer;
  transition: all var(--transition-base);
}

.card-interactive:hover {
  border-color: var(--color-primary-300);
  box-shadow: var(--shadow-lg);
}
```

### Form Elements

```css
/* components/forms.css */

.form-group {
  margin-bottom: var(--space-4);
}

.form-label {
  display: block;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-text);
  margin-bottom: var(--space-1);
}

.form-label-required::after {
  content: ' *';
  color: var(--color-error);
}

.form-input,
.form-textarea,
.form-select {
  width: 100%;
  padding: var(--space-2) var(--space-3);
  font-family: var(--font-sans);
  font-size: var(--text-base);
  color: var(--color-text);
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.form-input:focus,
.form-textarea:focus,
.form-select:focus {
  outline: none;
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: var(--color-text-muted);
}

.form-input:disabled,
.form-textarea:disabled,
.form-select:disabled {
  background-color: var(--color-surface);
  cursor: not-allowed;
  opacity: 0.7;
}

/* Error state */
.form-input-error {
  border-color: var(--color-error);
}

.form-input-error:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15);
}

.form-error-message {
  font-size: var(--text-sm);
  color: var(--color-error);
  margin-top: var(--space-1);
}

.form-help-text {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  margin-top: var(--space-1);
}

/* Textarea */
.form-textarea {
  min-height: 100px;
  resize: vertical;
}

/* Checkbox and Radio */
.form-checkbox,
.form-radio {
  width: 1rem;
  height: 1rem;
  accent-color: var(--color-primary-600);
}

.form-checkbox-label,
.form-radio-label {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: var(--text-sm);
  cursor: pointer;
}
```

---

## Layout Utilities

```css
/* utilities.css */

/* Container */
.container {
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--space-4);
  padding-right: var(--space-4);
}

@media (min-width: 768px) {
  .container {
    padding-left: var(--space-8);
    padding-right: var(--space-8);
  }
}

/* Flexbox */
.flex { display: flex; }
.inline-flex { display: inline-flex; }
.flex-col { flex-direction: column; }
.flex-row { flex-direction: row; }
.flex-wrap { flex-wrap: wrap; }
.items-center { align-items: center; }
.items-start { align-items: flex-start; }
.items-end { align-items: flex-end; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.justify-end { justify-content: flex-end; }
.flex-1 { flex: 1; }
.flex-none { flex: none; }

/* Grid */
.grid { display: grid; }
.grid-cols-1 { grid-template-columns: repeat(1, 1fr); }
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }

/* Gaps */
.gap-1 { gap: var(--space-1); }
.gap-2 { gap: var(--space-2); }
.gap-4 { gap: var(--space-4); }
.gap-6 { gap: var(--space-6); }
.gap-8 { gap: var(--space-8); }

/* Spacing */
.m-0 { margin: 0; }
.m-auto { margin: auto; }
.mx-auto { margin-left: auto; margin-right: auto; }
.my-4 { margin-top: var(--space-4); margin-bottom: var(--space-4); }
.mt-4 { margin-top: var(--space-4); }
.mb-4 { margin-bottom: var(--space-4); }
.p-4 { padding: var(--space-4); }
.px-4 { padding-left: var(--space-4); padding-right: var(--space-4); }
.py-4 { padding-top: var(--space-4); padding-bottom: var(--space-4); }

/* Text */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }
.font-medium { font-weight: var(--font-medium); }
.font-semibold { font-weight: var(--font-semibold); }
.font-bold { font-weight: var(--font-bold); }

/* Visibility */
.hidden { display: none; }
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Responsive utilities */
@media (min-width: 768px) {
  .md\:flex { display: flex; }
  .md\:hidden { display: none; }
  .md\:grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
  .md\:grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
}

@media (min-width: 1024px) {
  .lg\:flex { display: flex; }
  .lg\:hidden { display: none; }
  .lg\:grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
  .lg\:grid-cols-4 { grid-template-columns: repeat(4, 1fr); }
}
```

---

## SCSS Mixins

```scss
/* _mixins.scss */

// Responsive breakpoints
$breakpoints: (
  'sm': 640px,
  'md': 768px,
  'lg': 1024px,
  'xl': 1280px,
  '2xl': 1536px,
);

@mixin respond-to($breakpoint) {
  @if map-has-key($breakpoints, $breakpoint) {
    @media (min-width: map-get($breakpoints, $breakpoint)) {
      @content;
    }
  }
}

// Usage: @include respond-to('md') { ... }

// Truncate text
@mixin truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

// Line clamp
@mixin line-clamp($lines) {
  display: -webkit-box;
  -webkit-line-clamp: $lines;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

// Focus ring
@mixin focus-ring($color: var(--color-primary-500)) {
  &:focus-visible {
    outline: 2px solid $color;
    outline-offset: 2px;
  }
}

// Visually hidden (screen reader only)
@mixin sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

// Button base
@mixin button-base {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-fast);
  @include focus-ring;

  &:disabled {
    opacity: 0.5;
    pointer-events: none;
  }
}
```

---

## Main Entry Point

```css
/* main.css */
@import 'variables.css';
@import 'reset.css';
@import 'base.css';
@import 'utilities.css';
@import 'components/buttons.css';
@import 'components/cards.css';
@import 'components/forms.css';
@import 'components/navigation.css';
@import 'layouts/grid.css';
@import 'layouts/header.css';
@import 'layouts/footer.css';
```

Or with SCSS:

```scss
/* main.scss */
@use 'variables';
@use 'mixins';
@use 'reset';
@use 'base/typography';
@use 'base/global';
@use 'components/buttons';
@use 'components/cards';
@use 'components/forms';
@use 'layouts/grid';
@use 'layouts/sections';
```
