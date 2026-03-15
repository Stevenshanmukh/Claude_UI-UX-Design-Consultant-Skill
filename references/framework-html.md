# Plain HTML / CSS / JavaScript Design Implementation Guide

This reference covers how to apply design changes in static HTML sites and vanilla JavaScript projects.

---

## File Structure Patterns

### Basic Static Site
```
├── index.html
├── about.html
├── contact.html
├── css/
│   ├── main.css             # Main stylesheet
│   ├── variables.css        # Design tokens
│   └── components.css       # Component styles
├── js/
│   └── main.js
├── images/
└── fonts/
```

### With Build Tool (Vite/Parcel)
```
├── index.html
├── src/
│   ├── css/
│   │   ├── main.css
│   │   └── variables.css
│   ├── js/
│   │   └── main.js
│   └── components/          # HTML partials (if using includes)
├── public/
│   ├── images/
│   └── fonts/
└── vite.config.js
```

### Multi-page with Shared Components
```
├── pages/
│   ├── index.html
│   ├── about.html
│   └── contact.html
├── includes/                # Shared HTML snippets
│   ├── header.html
│   └── footer.html
├── css/
├── js/
└── images/
```

---

## Where to Define Design Tokens

### CSS Custom Properties (Recommended)
Create a dedicated `variables.css` or place at top of `main.css`:

```css
/* css/variables.css */
:root {
  /* ===== Colors ===== */
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

  /* Semantic colors */
  --color-text: #1f2937;
  --color-text-muted: #6b7280;
  --color-background: #ffffff;
  --color-surface: #f9fafb;
  --color-border: #e5e7eb;

  /* Status colors */
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;
  --color-info: #3b82f6;

  /* ===== Typography ===== */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-display: 'Cal Sans', var(--font-sans);
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* Type scale (1.25 ratio) */
  --text-xs: 0.75rem;      /* 12px */
  --text-sm: 0.875rem;     /* 14px */
  --text-base: 1rem;       /* 16px */
  --text-lg: 1.125rem;     /* 18px */
  --text-xl: 1.25rem;      /* 20px */
  --text-2xl: 1.5rem;      /* 24px */
  --text-3xl: 1.875rem;    /* 30px */
  --text-4xl: 2.25rem;     /* 36px */
  --text-5xl: 3rem;        /* 48px */
  --text-6xl: 3.75rem;     /* 60px */

  /* Line heights */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;

  /* ===== Spacing ===== */
  --space-1: 0.25rem;      /* 4px */
  --space-2: 0.5rem;       /* 8px */
  --space-3: 0.75rem;      /* 12px */
  --space-4: 1rem;         /* 16px */
  --space-5: 1.25rem;      /* 20px */
  --space-6: 1.5rem;       /* 24px */
  --space-8: 2rem;         /* 32px */
  --space-10: 2.5rem;      /* 40px */
  --space-12: 3rem;        /* 48px */
  --space-16: 4rem;        /* 64px */
  --space-20: 5rem;        /* 80px */
  --space-24: 6rem;        /* 96px */

  /* ===== Borders ===== */
  --radius-sm: 0.25rem;    /* 4px */
  --radius-md: 0.5rem;     /* 8px */
  --radius-lg: 0.75rem;    /* 12px */
  --radius-xl: 1rem;       /* 16px */
  --radius-full: 9999px;

  /* ===== Shadows ===== */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);

  /* ===== Transitions ===== */
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-text: #f9fafb;
    --color-text-muted: #9ca3af;
    --color-background: #111827;
    --color-surface: #1f2937;
    --color-border: #374151;
  }
}
```

**Link in HTML:**
```html
<head>
  <link rel="stylesheet" href="css/variables.css">
  <link rel="stylesheet" href="css/main.css">
</head>
```

---

## Component Patterns in CSS

### Button Component
```css
/* css/components.css */

/* Base button */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  font-family: var(--font-sans);
  font-size: var(--text-sm);
  font-weight: 500;
  line-height: var(--leading-normal);
  text-decoration: none;
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.btn:focus-visible {
  outline: 2px solid var(--color-primary-500);
  outline-offset: 2px;
}

.btn:disabled {
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

.btn-secondary {
  background-color: var(--color-surface);
  border-color: var(--color-border);
  color: var(--color-text);
}

.btn-secondary:hover {
  background-color: var(--color-border);
}

.btn-ghost {
  background-color: transparent;
  color: var(--color-text);
}

.btn-ghost:hover {
  background-color: var(--color-surface);
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
```

### Card Component
```css
.card {
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  box-shadow: var(--shadow-sm);
}

.card-header {
  margin-bottom: var(--space-4);
}

.card-title {
  font-size: var(--text-xl);
  font-weight: 600;
  color: var(--color-text);
}

.card-description {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  margin-top: var(--space-1);
}

.card-content {
  /* Content area */
}

.card-footer {
  margin-top: var(--space-4);
  padding-top: var(--space-4);
  border-top: 1px solid var(--color-border);
}
```

### Form Elements
```css
.form-group {
  margin-bottom: var(--space-4);
}

.form-label {
  display: block;
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--color-text);
  margin-bottom: var(--space-1);
}

.form-input {
  width: 100%;
  padding: var(--space-2) var(--space-3);
  font-family: var(--font-sans);
  font-size: var(--text-base);
  color: var(--color-text);
  background-color: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition: border-color var(--transition-fast), box-shadow var(--transition-fast);
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 3px rgb(59 130 246 / 0.2);
}

.form-input::placeholder {
  color: var(--color-text-muted);
}

.form-input:disabled {
  background-color: var(--color-surface);
  cursor: not-allowed;
}

/* Error state */
.form-input.error {
  border-color: var(--color-error);
}

.form-error {
  font-size: var(--text-sm);
  color: var(--color-error);
  margin-top: var(--space-1);
}
```

---

## Layout Patterns

### Container
```css
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
```

### Grid System
```css
.grid {
  display: grid;
  gap: var(--space-6);
}

.grid-cols-1 { grid-template-columns: repeat(1, 1fr); }
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }

@media (min-width: 768px) {
  .md\:grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
  .md\:grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
}

@media (min-width: 1024px) {
  .lg\:grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
  .lg\:grid-cols-4 { grid-template-columns: repeat(4, 1fr); }
}
```

### Flexbox Utilities
```css
.flex { display: flex; }
.flex-col { flex-direction: column; }
.flex-wrap { flex-wrap: wrap; }
.items-center { align-items: center; }
.items-start { align-items: flex-start; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.gap-2 { gap: var(--space-2); }
.gap-4 { gap: var(--space-4); }
.gap-6 { gap: var(--space-6); }
```

---

## HTML Patterns

### Semantic Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title</title>
  <link rel="stylesheet" href="css/variables.css">
  <link rel="stylesheet" href="css/main.css">
</head>
<body>
  <header class="site-header">
    <nav class="nav" aria-label="Main navigation">
      <a href="/" class="logo">Logo</a>
      <ul class="nav-list">
        <li><a href="/about">About</a></li>
        <li><a href="/contact">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <section class="hero" aria-labelledby="hero-heading">
      <h1 id="hero-heading">Main Heading</h1>
      <p>Supporting text</p>
      <a href="/signup" class="btn btn-primary">Get Started</a>
    </section>

    <section class="features" aria-labelledby="features-heading">
      <h2 id="features-heading">Features</h2>
      <!-- Feature cards -->
    </section>
  </main>

  <footer class="site-footer">
    <p>&copy; 2024 Company Name</p>
  </footer>

  <script src="js/main.js"></script>
</body>
</html>
```

---

## JavaScript Interaction Patterns

### Class Toggle
```js
// Toggle mobile menu
const menuButton = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('.mobile-nav');

menuButton?.addEventListener('click', () => {
  const isOpen = mobileNav.classList.toggle('is-open');
  menuButton.setAttribute('aria-expanded', isOpen);
});
```

### Smooth Scroll
```js
// Smooth scroll to anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    e.preventDefault();
    const target = document.querySelector(anchor.getAttribute('href'));
    target?.scrollIntoView({ behavior: 'smooth' });
  });
});
```

### Intersection Observer (scroll animations)
```js
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
      }
    });
  },
  { threshold: 0.1 }
);

document.querySelectorAll('.animate-on-scroll').forEach(el => {
  observer.observe(el);
});
```

```css
.animate-on-scroll {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.animate-on-scroll.is-visible {
  opacity: 1;
  transform: translateY(0);
}
```

---

## Responsive Patterns

### Mobile-First Media Queries
```css
/* Base (mobile) */
.hero-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
}

/* Tablet */
@media (min-width: 768px) {
  .hero-grid {
    flex-direction: row;
    align-items: center;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .hero-grid {
    gap: var(--space-16);
  }
}
```

### Common Breakpoints
```css
/* Mobile: default (< 640px) */
/* sm: 640px - Larger phones */
/* md: 768px - Tablets */
/* lg: 1024px - Small laptops */
/* xl: 1280px - Desktops */
/* 2xl: 1536px - Large screens */
```

---

## HTML-Specific Gotchas

### 1. Viewport Meta Tag (required for responsive)
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

### 2. Font Loading
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### 3. CSS Load Order
Load variables before main styles:
```html
<link rel="stylesheet" href="css/variables.css">
<link rel="stylesheet" href="css/main.css">
<link rel="stylesheet" href="css/components.css">
```

### 4. Cache Busting
Add version query strings during development:
```html
<link rel="stylesheet" href="css/main.css?v=1.0.1">
```

### 5. Accessibility Basics
- Always include `alt` on images
- Use semantic elements (`header`, `nav`, `main`, `section`, `footer`)
- Ensure sufficient color contrast
- Make all interactive elements keyboard-accessible
- Use `aria-label` for icon-only buttons
