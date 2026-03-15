# Svelte / SvelteKit Design Implementation Guide

This reference covers how to apply design changes in Svelte and SvelteKit codebases.

---

## File Structure Patterns

### SvelteKit
```
src/
├── app.html                 # HTML template
├── app.css                  # Global styles
├── lib/
│   ├── components/
│   │   └── ui/              # Base components
│   └── styles/
│       └── variables.css    # Design tokens
├── routes/
│   ├── +layout.svelte       # Root layout
│   ├── +page.svelte         # Home page
│   └── [section]/
│       └── +page.svelte
└── hooks.server.ts
```

### Standalone Svelte (Vite)
```
src/
├── App.svelte
├── main.ts
├── app.css                  # Global styles
├── lib/
│   └── components/
└── vite-env.d.ts
```

---

## Where to Define Design Tokens

### With Tailwind CSS
Put tokens in `tailwind.config.js`:

```js
// tailwind.config.js
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
}
```

**Import in app.css:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### With CSS Variables
Define in `app.css` or a dedicated `variables.css`:

```css
:root {
  /* Colors */
  --color-primary-500: #3b82f6;
  --color-primary-600: #2563eb;

  /* Spacing */
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --text-base: 1rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
}
```

**Import in +layout.svelte:**
```svelte
<script>
  import '../app.css';
</script>
```

---

## Component Modification Patterns

### Svelte Component Structure

```svelte
<script lang="ts">
  // Props with TypeScript
  interface $$Props {
    variant?: 'primary' | 'secondary' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    class?: string;
  }

  export let variant: $$Props['variant'] = 'primary';
  export let size: $$Props['size'] = 'md';
  let className: $$Props['class'] = '';
  export { className as class };

  // Reactive class computation
  $: classes = [
    'inline-flex items-center justify-center font-medium transition-colors',
    'focus-visible:outline-none focus-visible:ring-2',
    'disabled:pointer-events-none disabled:opacity-50',
    // Size
    size === 'sm' && 'h-8 px-3 text-sm rounded-md',
    size === 'md' && 'h-10 px-4 text-sm rounded-lg',
    size === 'lg' && 'h-12 px-6 text-base rounded-lg',
    // Variant
    variant === 'primary' && 'bg-primary-600 text-white hover:bg-primary-700',
    variant === 'secondary' && 'border border-gray-300 bg-white hover:bg-gray-50',
    variant === 'ghost' && 'hover:bg-gray-100',
    className,
  ].filter(Boolean).join(' ');
</script>

<button class={classes} on:click {...$$restProps}>
  <slot />
</button>
```

### Svelte 5 (Runes) Component Pattern

```svelte
<script lang="ts">
  interface Props {
    variant?: 'primary' | 'secondary' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    class?: string;
  }

  let { variant = 'primary', size = 'md', class: className = '', ...restProps }: Props = $props();

  const classes = $derived([
    'btn',
    `btn-${variant}`,
    `btn-${size}`,
    className,
  ].filter(Boolean).join(' '));
</script>

<button class={classes} {...restProps}>
  {@render children?.()}
</button>
```

---

## Styling Approaches in Svelte

### Scoped Styles (default)
Styles in `<style>` are scoped to the component automatically:

```svelte
<style>
  button {
    /* Only affects buttons in this component */
    background: var(--color-primary-500);
    padding: 0.5rem 1rem;
  }
</style>
```

### Global Styles
Use `:global()` selector:

```svelte
<style>
  :global(body) {
    font-family: var(--font-sans);
  }

  /* All .btn classes anywhere */
  :global(.btn) {
    border-radius: 0.5rem;
  }

  /* .btn only inside this component's descendants */
  .wrapper :global(.btn) {
    margin-bottom: 1rem;
  }
</style>
```

### Using CSS Modules
Svelte doesn't have built-in CSS Modules, but you can use standard imports:

```svelte
<script>
  import styles from './Button.module.css';
</script>

<button class={styles.button}>Click</button>
```

---

## Working with Component Libraries

### Skeleton UI
Customize via Tailwind config and theme:

```js
// tailwind.config.js
import { skeleton } from '@skeletonlabs/tw-plugin';

export default {
  plugins: [
    skeleton({
      themes: {
        custom: {
          name: 'custom-theme',
          properties: {
            '--theme-color-primary-500': '#3b82f6',
            // ...
          },
        },
      },
    }),
  ],
}
```

### Melt UI (headless)
Style the underlying elements directly:

```svelte
<script>
  import { createDialog } from '@melt-ui/svelte';

  const { trigger, content, overlay } = createDialog();
</script>

<button use:trigger class="btn btn-primary">Open</button>

<div use:overlay class="fixed inset-0 bg-black/50" />
<div use:content class="dialog-panel">
  Content
</div>
```

### shadcn-svelte
Components are in `$lib/components/ui/`. Modify directly:

```svelte
<!-- $lib/components/ui/button.svelte -->
<script>
  import { cn } from '$lib/utils';
  // ... customize as needed
</script>
```

---

## Svelte-Specific Gotchas

### 1. class is a reserved word
Use `class:` directive or rename the prop:

```svelte
<!-- class directive for conditional -->
<div class:active={isActive}>

<!-- Spread class prop -->
<script>
  let className = '';
  export { className as class };
</script>
<div class={className}>
```

### 2. Reactive declarations
Use `$:` for computed values:

```svelte
<script>
  export let variant = 'primary';

  $: variantClass = variant === 'primary' ? 'bg-blue-500' : 'bg-gray-500';
</script>

<div class={variantClass}>
```

### 3. Style props (CSS custom properties)
Pass CSS variables as props:

```svelte
<!-- Parent -->
<Button --btn-bg="red" --btn-color="white" />

<!-- Button.svelte -->
<button style:--btn-bg style:--btn-color>
  <slot />
</button>

<style>
  button {
    background: var(--btn-bg, blue);
    color: var(--btn-color, white);
  }
</style>
```

### 4. Forwarding events
Use `on:click` without a handler to forward:

```svelte
<button on:click on:focus on:blur>
  <slot />
</button>
```

### 5. Spread props
Use `$$restProps` for remaining props or `$$props` for all:

```svelte
<button class="btn" {...$$restProps}>
```

---

## Animation Patterns

### Svelte Transitions
Built-in transitions:

```svelte
<script>
  import { fade, fly, slide, scale } from 'svelte/transition';
  import { quintOut } from 'svelte/easing';

  let visible = true;
</script>

{#if visible}
  <div transition:fade={{ duration: 300 }}>
    Fades in/out
  </div>

  <div in:fly={{ y: 20, duration: 300 }} out:fade>
    Different in/out
  </div>
{/if}
```

### Custom Transitions
```svelte
<script>
  function typewriter(node, { speed = 1 }) {
    const text = node.textContent;
    const duration = text.length / (speed * 0.01);

    return {
      duration,
      tick: t => {
        const i = Math.trunc(text.length * t);
        node.textContent = text.slice(0, i);
      }
    };
  }
</script>

<p transition:typewriter>
  Hello world
</p>
```

### Animate Directive (keyed lists)
```svelte
<script>
  import { flip } from 'svelte/animate';
</script>

{#each items as item (item.id)}
  <div animate:flip={{ duration: 300 }}>
    {item.name}
  </div>
{/each}
```

---

## Responsive Patterns

### Tailwind in Svelte
Same mobile-first approach:

```svelte
<div class="px-4 md:px-8 lg:px-16">
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
```

### Reactive Media Queries
```svelte
<script>
  import { readable } from 'svelte/store';

  const isMobile = readable(false, set => {
    const query = window.matchMedia('(max-width: 767px)');
    set(query.matches);

    const handler = (e) => set(e.matches);
    query.addEventListener('change', handler);
    return () => query.removeEventListener('change', handler);
  });
</script>

{#if $isMobile}
  <MobileNav />
{:else}
  <DesktopNav />
{/if}
```
