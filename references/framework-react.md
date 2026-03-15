# React / Next.js Design Implementation Guide

This reference covers how to apply design changes in React and Next.js codebases.

---

## File Structure Patterns

### Next.js App Router (v13+)
```
src/
├── app/
│   ├── layout.tsx          # Root layout, global providers
│   ├── page.tsx             # Home page
│   ├── globals.css          # Global styles, CSS variables
│   └── [section]/
│       └── page.tsx
├── components/
│   ├── ui/                  # Base components (Button, Card, Input)
│   └── [feature]/           # Feature-specific components
├── lib/
│   └── utils.ts             # Utility functions (cn, classnames)
└── styles/                  # Additional stylesheets if needed
```

### Next.js Pages Router (legacy)
```
src/
├── pages/
│   ├── _app.tsx             # App wrapper
│   ├── _document.tsx        # HTML document structure
│   └── index.tsx
├── components/
├── styles/
│   └── globals.css
```

### Standard React (Vite/CRA)
```
src/
├── App.tsx
├── main.tsx
├── index.css                # Global styles
├── components/
└── styles/                  # Component styles if CSS Modules
```

---

## Where to Define Design Tokens

### With Tailwind CSS
Put tokens in `tailwind.config.js` or `tailwind.config.ts`:

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          // ... full scale
        },
        // Custom semantic colors
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
      },
      spacing: {
        // Extend or override spacing scale
        '18': '4.5rem',
        '88': '22rem',
      },
      fontSize: {
        // Custom type scale
        'display': ['3.5rem', { lineHeight: '1.1', fontWeight: '700' }],
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
      },
    },
  },
}
```

### With CSS Variables
Define in `globals.css` or `index.css`:

```css
:root {
  /* Colors */
  --color-primary-500: #3b82f6;
  --color-primary-600: #2563eb;

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-display: 'Cal Sans', sans-serif;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.dark {
  --color-primary-500: #60a5fa;
  /* Dark mode overrides */
}
```

---

## Component Modification Patterns

### Modifying a Component with Tailwind

**Before:**
```tsx
function Button({ children }) {
  return (
    <button className="bg-blue-500 text-white px-3 py-1 rounded">
      {children}
    </button>
  );
}
```

**After (with design system):**
```tsx
import { cn } from '@/lib/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
}

function Button({
  children,
  variant = 'primary',
  size = 'md',
  className,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(
        // Base styles
        'inline-flex items-center justify-center font-medium transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
        'disabled:pointer-events-none disabled:opacity-50',
        // Size variants
        {
          'h-8 px-3 text-sm rounded-md': size === 'sm',
          'h-10 px-4 text-sm rounded-lg': size === 'md',
          'h-12 px-6 text-base rounded-lg': size === 'lg',
        },
        // Color variants
        {
          'bg-primary-600 text-white hover:bg-primary-700': variant === 'primary',
          'border border-gray-300 bg-white hover:bg-gray-50': variant === 'secondary',
          'hover:bg-gray-100': variant === 'ghost',
        },
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
}
```

### The cn() Utility
Most React projects use a classname merge utility. If it doesn't exist, create it:

```ts
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

Install dependencies: `npm install clsx tailwind-merge`

---

## Working with Component Libraries

### shadcn/ui
Components are in `components/ui/`. Modify directly — they're meant to be customized.

**Customizing theme:** Edit `tailwind.config.js` and CSS variables in `globals.css`.

**Adding variants:** Edit the component file directly, using the existing `cva` patterns.

### MUI (Material UI)
Theme in `theme.ts` or `ThemeProvider`:

```tsx
import { createTheme, ThemeProvider } from '@mui/material';

const theme = createTheme({
  palette: {
    primary: {
      main: '#3b82f6',
      light: '#60a5fa',
      dark: '#2563eb',
    },
  },
  typography: {
    fontFamily: '"Inter", "Helvetica", "Arial", sans-serif',
    h1: { fontSize: '2.5rem', fontWeight: 700 },
  },
  spacing: 8, // Base unit
  shape: {
    borderRadius: 8,
  },
});
```

### Chakra UI
Theme in `theme.ts`:

```tsx
import { extendTheme } from '@chakra-ui/react';

const theme = extendTheme({
  colors: {
    brand: {
      50: '#eff6ff',
      500: '#3b82f6',
      600: '#2563eb',
    },
  },
  fonts: {
    heading: '"Cal Sans", sans-serif',
    body: '"Inter", sans-serif',
  },
});
```

---

## Common React-Specific Gotchas

### 1. className vs class
React uses `className`, not `class`. This is automatic but worth noting when copying CSS examples.

### 2. Inline styles use camelCase
```tsx
// Wrong
<div style={{ background-color: 'red' }}>

// Correct
<div style={{ backgroundColor: 'red' }}>
```

### 3. CSS Modules naming
CSS Modules convert kebab-case to camelCase:
```css
/* styles.module.css */
.my-button { ... }
```
```tsx
import styles from './styles.module.css';
<button className={styles.myButton}> // or styles['my-button']
```

### 4. Conditional classes
Don't concatenate strings manually:
```tsx
// Bad
<div className={`btn ${isActive ? 'btn-active' : ''}`}>

// Good (use clsx or cn)
<div className={cn('btn', isActive && 'btn-active')}>
```

### 5. Tailwind purging
Ensure dynamic classes are complete strings, not constructed:
```tsx
// Bad (won't be included in production)
<div className={`text-${color}-500`}>

// Good
const colorClasses = {
  blue: 'text-blue-500',
  red: 'text-red-500',
};
<div className={colorClasses[color]}>
```

### 6. Server Components (Next.js App Router)
By default, components are Server Components. If you add interactivity (onClick, useState), add `'use client'` at the top.

---

## Animation Patterns

### CSS Transitions
```tsx
<button className="transition-colors duration-200 hover:bg-primary-600">
```

### Framer Motion
```tsx
import { motion } from 'framer-motion';

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
  Content
</motion.div>
```

### CSS @keyframes
Define in `globals.css`, use via Tailwind `animate-*` or direct className:
```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}
```

---

## Responsive Patterns

### Tailwind
Mobile-first: `md:` prefix for tablet+, `lg:` for desktop+.
```tsx
<div className="px-4 md:px-8 lg:px-16">
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
```

### CSS Variables with Media Queries
```css
:root {
  --section-padding: 2rem;
}

@media (min-width: 768px) {
  :root {
    --section-padding: 4rem;
  }
}
```
