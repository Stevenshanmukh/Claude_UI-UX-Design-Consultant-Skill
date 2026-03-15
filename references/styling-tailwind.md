# Tailwind CSS Design Implementation Guide

This reference covers how to customize and extend Tailwind CSS for design system changes.

---

## Config File Location

Tailwind config is typically at the project root:
- `tailwind.config.js` (CommonJS)
- `tailwind.config.ts` (TypeScript)
- `tailwind.config.mjs` (ESM)

---

## Extending the Theme

Use `theme.extend` to add to defaults without replacing them:

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      // Additions go here
    },
  },
}
```

Use `theme` directly (without `.extend`) to replace defaults entirely:

```js
module.exports = {
  theme: {
    // This REPLACES the default colors entirely
    colors: {
      primary: '#3b82f6',
      // All default colors like 'gray', 'red', etc. are now gone
    },
  },
}
```

**Rule:** Always use `extend` unless you intentionally want to remove all defaults.

---

## Customizing Colors

### Adding a Brand Palette

```js
theme: {
  extend: {
    colors: {
      // Full scale for primary brand color
      primary: {
        50: '#eff6ff',
        100: '#dbeafe',
        200: '#bfdbfe',
        300: '#93c5fd',
        400: '#60a5fa',
        500: '#3b82f6',
        600: '#2563eb',
        700: '#1d4ed8',
        800: '#1e40af',
        900: '#1e3a8a',
        950: '#172554',
      },
      // Secondary and accent
      secondary: {
        // ... same structure
      },
      accent: {
        // ... same structure
      },
    },
  },
}
```

**Usage:** `bg-primary-500`, `text-primary-600`, `border-primary-200`

### Using CSS Variables (recommended for dark mode)

```js
theme: {
  extend: {
    colors: {
      background: 'hsl(var(--background))',
      foreground: 'hsl(var(--foreground))',
      primary: {
        DEFAULT: 'hsl(var(--primary))',
        foreground: 'hsl(var(--primary-foreground))',
      },
      muted: {
        DEFAULT: 'hsl(var(--muted))',
        foreground: 'hsl(var(--muted-foreground))',
      },
    },
  },
}
```

Then define in CSS:
```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 221.2 83.2% 53.3%;
  --primary-foreground: 210 40% 98%;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  --primary: 217.2 91.2% 59.8%;
  --primary-foreground: 222.2 84% 4.9%;
}
```

---

## Customizing Spacing

### Extending the Scale

```js
theme: {
  extend: {
    spacing: {
      '18': '4.5rem',    // 72px
      '88': '22rem',     // 352px
      '128': '32rem',    // 512px
    },
  },
}
```

**Usage:** `p-18`, `mt-88`, `gap-128`

### Custom Section Spacing

```js
theme: {
  extend: {
    spacing: {
      'section': '6rem',        // For section padding
      'section-lg': '8rem',
    },
  },
}
```

---

## Customizing Typography

### Font Families

```js
theme: {
  extend: {
    fontFamily: {
      sans: ['Inter', 'system-ui', 'sans-serif'],
      display: ['Cal Sans', 'Inter', 'sans-serif'],
      mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
    },
  },
}
```

**Usage:** `font-sans`, `font-display`, `font-mono`

### Font Sizes with Line Height

```js
theme: {
  extend: {
    fontSize: {
      'display-lg': ['4.5rem', { lineHeight: '1.1', fontWeight: '700' }],
      'display': ['3.75rem', { lineHeight: '1.1', fontWeight: '700' }],
      'display-sm': ['3rem', { lineHeight: '1.2', fontWeight: '600' }],
    },
  },
}
```

**Usage:** `text-display-lg`

---

## Customizing Border Radius

```js
theme: {
  extend: {
    borderRadius: {
      'sm': '0.25rem',   // 4px
      'DEFAULT': '0.5rem', // 8px
      'md': '0.5rem',
      'lg': '0.75rem',   // 12px
      'xl': '1rem',      // 16px
      '2xl': '1.5rem',   // 24px
    },
  },
}
```

---

## Customizing Shadows

```js
theme: {
  extend: {
    boxShadow: {
      'sm': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
      'DEFAULT': '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
      'md': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
      'lg': '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
      'xl': '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
      // Custom elevation
      'card': '0 2px 8px -2px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.06)',
      'button': '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    },
  },
}
```

---

## Customizing Transitions

```js
theme: {
  extend: {
    transitionDuration: {
      '400': '400ms',
    },
    transitionTimingFunction: {
      'bounce-in': 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
    },
  },
}
```

---

## Adding Custom Utilities

### Using @layer

In your CSS file:

```css
@layer utilities {
  .text-balance {
    text-wrap: balance;
  }

  .animate-fade-in {
    animation: fadeIn 0.5s ease-out;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
}
```

### Using Plugins

```js
// tailwind.config.js
const plugin = require('tailwindcss/plugin')

module.exports = {
  plugins: [
    plugin(function({ addUtilities }) {
      addUtilities({
        '.text-balance': {
          'text-wrap': 'balance',
        },
        '.scrollbar-hide': {
          '-ms-overflow-style': 'none',
          'scrollbar-width': 'none',
          '&::-webkit-scrollbar': {
            display: 'none',
          },
        },
      })
    }),
  ],
}
```

---

## Component Classes with @apply

Create reusable component classes:

```css
@layer components {
  .btn {
    @apply inline-flex items-center justify-center px-4 py-2 font-medium
           text-sm rounded-lg transition-colors focus-visible:outline-none
           focus-visible:ring-2 focus-visible:ring-offset-2
           disabled:pointer-events-none disabled:opacity-50;
  }

  .btn-primary {
    @apply bg-primary-600 text-white hover:bg-primary-700
           focus-visible:ring-primary-500;
  }

  .btn-secondary {
    @apply bg-white border border-gray-300 text-gray-700
           hover:bg-gray-50 focus-visible:ring-gray-500;
  }

  .card {
    @apply bg-white rounded-xl border border-gray-200 p-6 shadow-sm;
  }

  .input {
    @apply w-full px-3 py-2 text-base border border-gray-300 rounded-lg
           focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
           placeholder:text-gray-400 disabled:bg-gray-50 disabled:cursor-not-allowed;
  }
}
```

**Warning:** `@apply` is controversial. Prefer utility classes in HTML when possible. Use `@apply` for:
- Design tokens in component libraries
- Reducing repetition in very common patterns
- Third-party styling that requires class names

---

## Common Tailwind Patterns

### Responsive Breakpoints
```html
<!-- Mobile-first: base → sm → md → lg → xl → 2xl -->
<div class="px-4 md:px-8 lg:px-16">
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
```

### Hover, Focus, Active States
```html
<button class="bg-primary-600 hover:bg-primary-700 active:bg-primary-800
               focus-visible:ring-2 focus-visible:ring-offset-2">
```

### Dark Mode
```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
```

### Group Hover
```html
<div class="group">
  <span class="group-hover:text-primary-500">Text</span>
  <svg class="group-hover:translate-x-1 transition-transform">...</svg>
</div>
```

### Arbitrary Values
```html
<div class="top-[117px] grid-cols-[1fr_2fr_1fr] bg-[#1da1f2]">
```

---

## Tailwind Gotchas

### 1. Dynamic Classes Don't Work
```html
<!-- BAD: Won't be included in production -->
<div class={`text-${color}-500`}>

<!-- GOOD: Use complete class names -->
<div class={color === 'blue' ? 'text-blue-500' : 'text-red-500'}>
```

### 2. Content Configuration
Ensure all files with Tailwind classes are in the content config:

```js
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx}',
    './app/**/*.{js,ts,jsx,tsx}',
  ],
}
```

### 3. Class Order Matters
Use a consistent order. Install `prettier-plugin-tailwindcss` for auto-sorting:

```bash
npm install -D prettier prettier-plugin-tailwindcss
```

### 4. Conflicting Classes
Use `tailwind-merge` to handle conflicts:

```js
import { twMerge } from 'tailwind-merge'

// Later class wins
twMerge('px-4 py-2', 'px-8') // → 'py-2 px-8'
```

### 5. Safelist for Dynamic Classes
If you must use dynamic classes:

```js
module.exports = {
  safelist: [
    'bg-red-500',
    'bg-blue-500',
    'bg-green-500',
    { pattern: /^text-(red|blue|green)-/ },
  ],
}
```

---

## Recommended Plugins

```js
module.exports = {
  plugins: [
    require('@tailwindcss/typography'),    // Prose styling
    require('@tailwindcss/forms'),          // Form reset
    require('@tailwindcss/aspect-ratio'),   // Aspect ratios
    require('@tailwindcss/container-queries'), // Container queries
  ],
}
```
