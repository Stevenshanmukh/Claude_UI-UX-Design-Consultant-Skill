# CSS Modules Design Implementation Guide

This reference covers how to apply design changes in projects using CSS Modules.

---

## How CSS Modules Work

CSS Modules scope class names locally by default. When you import a CSS Module, you get an object where keys are class names and values are generated unique identifiers.

```css
/* Button.module.css */
.button {
  background: blue;
}
```

```jsx
import styles from './Button.module.css';

// styles.button → "Button_button__abc123"
<button className={styles.button}>Click</button>
```

---

## File Naming Conventions

- `Component.module.css` — Component-specific styles
- `Component.module.scss` — With SCSS features
- `styles.module.css` — Generic module name

**Location patterns:**
```
# Co-located with component
components/
├── Button/
│   ├── Button.tsx
│   └── Button.module.css

# Separate styles folder
src/
├── components/
│   └── Button.tsx
└── styles/
    └── Button.module.css
```

---

## Design Token Integration

### Option 1: CSS Variables (Recommended)

Define tokens globally, use them in modules:

```css
/* styles/variables.css - NOT a module */
:root {
  --color-primary-500: #3b82f6;
  --color-primary-600: #2563eb;
  --space-4: 1rem;
  --radius-md: 0.5rem;
  --font-sans: 'Inter', sans-serif;
}
```

```css
/* Button.module.css */
.button {
  background-color: var(--color-primary-500);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  font-family: var(--font-sans);
}

.button:hover {
  background-color: var(--color-primary-600);
}
```

### Option 2: SCSS Variables

With SCSS modules, you can use variables within the module:

```scss
/* _variables.scss */
$color-primary-500: #3b82f6;
$color-primary-600: #2563eb;
$space-4: 1rem;
```

```scss
/* Button.module.scss */
@use '../styles/variables' as *;

.button {
  background-color: $color-primary-500;
  padding: $space-4;

  &:hover {
    background-color: $color-primary-600;
  }
}
```

---

## Class Composition

### composes Keyword

Import styles from another module:

```css
/* base.module.css */
.flexCenter {
  display: flex;
  align-items: center;
  justify-content: center;
}
```

```css
/* Button.module.css */
.button {
  composes: flexCenter from './base.module.css';
  background-color: var(--color-primary-500);
}
```

### Composing from Global

```css
.button {
  composes: globalClassName from global;
}
```

---

## Component Patterns

### Basic Component with Variants

```css
/* Button.module.css */
.base {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: var(--radius-md);
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.base:focus-visible {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 2px;
}

.base:disabled {
  opacity: 0.5;
  pointer-events: none;
}

/* Variants */
.primary {
  composes: base;
  background-color: var(--color-primary-600);
  color: white;
}

.primary:hover {
  background-color: var(--color-primary-700);
}

.secondary {
  composes: base;
  background-color: var(--color-surface);
  border: 1px solid var(--color-border);
  color: var(--color-text);
}

.secondary:hover {
  background-color: var(--color-border);
}

.ghost {
  composes: base;
  background-color: transparent;
  color: var(--color-text);
}

.ghost:hover {
  background-color: var(--color-surface);
}

/* Sizes */
.sm {
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
}

.lg {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
}
```

```tsx
import styles from './Button.module.css';

function Button({ variant = 'primary', size = 'md', children }) {
  const variantClass = styles[variant];
  const sizeClass = size !== 'md' ? styles[size] : '';

  return (
    <button className={`${variantClass} ${sizeClass}`.trim()}>
      {children}
    </button>
  );
}
```

### Card Component

```css
/* Card.module.css */
.card {
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.header {
  padding: var(--space-4) var(--space-6);
  border-bottom: 1px solid var(--color-border);
}

.title {
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--color-text);
  margin: 0;
}

.description {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  margin-top: var(--space-1);
}

.content {
  padding: var(--space-6);
}

.footer {
  padding: var(--space-4) var(--space-6);
  border-top: 1px solid var(--color-border);
  background-color: var(--color-surface);
}
```

---

## Handling Class Names

### Using clsx or classnames

```tsx
import clsx from 'clsx';
import styles from './Button.module.css';

function Button({ variant, size, className, disabled }) {
  return (
    <button
      className={clsx(
        styles.base,
        styles[variant],
        size && styles[size],
        disabled && styles.disabled,
        className
      )}
    >
      {children}
    </button>
  );
}
```

### Multiple Classes

```tsx
// Concatenation
<div className={`${styles.container} ${styles.centered}`}>

// Template literal
<div className={`${styles.button} ${isActive ? styles.active : ''}`}>

// With clsx
<div className={clsx(styles.container, styles.centered)}>
```

---

## Global Styles

### :global Selector

Apply styles globally from within a module:

```css
/* Component.module.css */
:global(.external-library-class) {
  /* Styles applied to global class */
  color: var(--color-primary-500);
}

/* Multiple global selectors */
:global {
  .prose h2 {
    color: var(--color-text);
  }

  .prose p {
    line-height: 1.7;
  }
}
```

### Global stylesheet

Non-module CSS files are global:

```css
/* globals.css - NOT a module */
body {
  font-family: var(--font-sans);
  color: var(--color-text);
}
```

---

## Responsive Styles

Media queries work normally within modules:

```css
/* Card.module.css */
.grid {
  display: grid;
  gap: var(--space-4);
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-6);
  }
}
```

---

## Animation Patterns

```css
/* Component.module.css */
.fadeIn {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.button {
  transition: background-color 0.2s ease, transform 0.1s ease;
}

.button:hover {
  transform: translateY(-1px);
}

.button:active {
  transform: translateY(0);
}
```

---

## CSS Modules Gotchas

### 1. Kebab-case Class Names

CSS Modules convert kebab-case to bracket notation:

```css
.my-button { ... }
```

```tsx
// Access via bracket notation
<button className={styles['my-button']}>

// Or use camelCase in CSS
.myButton { ... }
<button className={styles.myButton}>
```

### 2. TypeScript Support

Add type declarations for better IntelliSense:

```ts
// css-modules.d.ts
declare module '*.module.css' {
  const classes: { [key: string]: string };
  export default classes;
}

declare module '*.module.scss' {
  const classes: { [key: string]: string };
  export default classes;
}
```

For typed CSS Modules (exact class names):
```bash
npm install -D typescript-plugin-css-modules
```

### 3. Class Name Collisions

Module scoping prevents collisions, but be careful with `:global`:

```css
/* Avoid this - pollutes global namespace */
:global(.button) { ... }

/* Better - scoped wrapper */
.wrapper :global(.external-class) { ... }
```

### 4. Dynamic Class Names

CSS Modules don't support dynamic class names:

```tsx
// Won't work
<div className={styles[`color-${dynamicColor}`]}>

// Do this instead
const colorClasses = {
  blue: styles.colorBlue,
  red: styles.colorRed,
};
<div className={colorClasses[dynamicColor]}>
```

### 5. Order of Imported Styles

Import order affects cascade. Import base styles first:

```tsx
import './reset.css';           // Global reset first
import './variables.css';       // Variables second
import styles from './Component.module.css'; // Component styles last
```

---

## Project Structure Recommendation

```
src/
├── styles/
│   ├── variables.css       # CSS custom properties (global)
│   ├── reset.css           # CSS reset (global)
│   ├── typography.css      # Base typography (global)
│   └── utilities.module.css # Shared utility classes
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   └── Button.module.css
│   └── Card/
│       ├── Card.tsx
│       └── Card.module.css
```
