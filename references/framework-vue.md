# Vue / Nuxt Design Implementation Guide

This reference covers how to apply design changes in Vue 3 and Nuxt codebases.

---

## File Structure Patterns

### Nuxt 3
```
├── app.vue                  # Root component
├── nuxt.config.ts           # Nuxt configuration
├── assets/
│   └── css/
│       └── main.css         # Global styles
├── components/
│   ├── ui/                  # Base components (UiButton, UiCard)
│   └── [feature]/           # Feature components
├── composables/             # Composition API utilities
├── layouts/
│   └── default.vue          # Default layout
├── pages/
│   └── index.vue
└── plugins/                 # Vue plugins
```

### Vue 3 (Vite)
```
src/
├── App.vue
├── main.ts
├── assets/
│   └── main.css             # Global styles
├── components/
├── composables/
├── views/                   # Page-level components
└── router/
```

---

## Where to Define Design Tokens

### With Tailwind CSS
Put tokens in `tailwind.config.js`:

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
        },
      },
      spacing: {
        '18': '4.5rem',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Cal Sans', 'sans-serif'],
      },
    },
  },
}
```

### With CSS Variables
In `assets/css/main.css` (imported in `nuxt.config.ts` or `main.ts`):

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
  --text-lg: 1.125rem;
}
```

**Nuxt config for global CSS:**
```ts
// nuxt.config.ts
export default defineNuxtConfig({
  css: ['~/assets/css/main.css'],
})
```

**Vue 3 Vite setup:**
```ts
// main.ts
import './assets/main.css'
```

---

## Component Modification Patterns

### Vue 3 Single File Component Structure

```vue
<script setup lang="ts">
// Script section (Composition API)
import { computed } from 'vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
})

const classes = computed(() => [
  'inline-flex items-center justify-center font-medium transition-colors',
  'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2',
  'disabled:pointer-events-none disabled:opacity-50',
  // Size
  {
    'h-8 px-3 text-sm rounded-md': props.size === 'sm',
    'h-10 px-4 text-sm rounded-lg': props.size === 'md',
    'h-12 px-6 text-base rounded-lg': props.size === 'lg',
  },
  // Variant
  {
    'bg-primary-600 text-white hover:bg-primary-700': props.variant === 'primary',
    'border border-gray-300 bg-white hover:bg-gray-50': props.variant === 'secondary',
    'hover:bg-gray-100': props.variant === 'ghost',
  },
])
</script>

<template>
  <button :class="classes">
    <slot />
  </button>
</template>
```

### Scoped Styles vs Global

**Scoped (default, component-specific):**
```vue
<style scoped>
.button {
  background-color: var(--color-primary-500);
}
</style>
```

**Global (affects all components):**
```vue
<style>
/* No scoped attribute = global */
.utility-class {
  margin-bottom: 1rem;
}
</style>
```

**Deep selector (style child components):**
```vue
<style scoped>
:deep(.child-class) {
  color: red;
}
</style>
```

---

## Working with Component Libraries

### Vuetify 3
Theme in `plugins/vuetify.ts`:

```ts
import { createVuetify } from 'vuetify'

export default createVuetify({
  theme: {
    themes: {
      light: {
        colors: {
          primary: '#3b82f6',
          secondary: '#64748b',
          accent: '#f59e0b',
          error: '#ef4444',
        },
      },
    },
  },
  defaults: {
    VBtn: {
      rounded: 'lg',
    },
    VCard: {
      rounded: 'lg',
    },
  },
})
```

### PrimeVue
Theme customization via CSS variables or presets:

```ts
// main.ts
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'

app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      prefix: 'p',
      darkModeSelector: '.dark',
    },
  },
})
```

### Nuxt UI
Customize in `app.config.ts`:

```ts
export default defineAppConfig({
  ui: {
    primary: 'blue',
    gray: 'slate',
    button: {
      rounded: 'rounded-lg',
      default: {
        size: 'md',
      },
    },
  },
})
```

---

## Vue-Specific Gotchas

### 1. Class binding syntax
```vue
<!-- Static + dynamic -->
<div class="static-class" :class="{ active: isActive }">

<!-- Array syntax -->
<div :class="[baseClass, isActive ? 'active' : '']">

<!-- Object in array -->
<div :class="[baseClass, { active: isActive }]">
```

### 2. Style binding
```vue
<!-- Object syntax -->
<div :style="{ color: textColor, fontSize: fontSize + 'px' }">

<!-- Array (merge multiple style objects) -->
<div :style="[baseStyles, overrideStyles]">
```

### 3. v-bind shorthand for CSS
Vue 3.2+ allows binding JS values directly in CSS:
```vue
<script setup>
const theme = {
  color: '#3b82f6',
}
</script>

<style scoped>
.button {
  color: v-bind('theme.color');
}
</style>
```

### 4. Auto-imported components (Nuxt)
Components in `/components` are auto-imported. Name them with prefixes for clarity:
```
components/
├── ui/
│   ├── UiButton.vue    → <UiButton />
│   └── UiCard.vue      → <UiCard />
```

### 5. CSS Modules in Vue
```vue
<template>
  <button :class="$style.button">Click me</button>
</template>

<style module>
.button {
  background: var(--color-primary-500);
}
</style>
```

### 6. Tailwind + Vue class binding
```vue
<!-- Use computed for complex class logic -->
<script setup>
const buttonClasses = computed(() =>
  cn('btn', props.variant === 'primary' && 'btn-primary')
)
</script>

<template>
  <button :class="buttonClasses">
    <slot />
  </button>
</template>
```

---

## Animation Patterns

### Vue Transitions
```vue
<template>
  <Transition name="fade">
    <div v-if="show">Content</div>
  </Transition>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
```

### TransitionGroup (lists)
```vue
<TransitionGroup name="list" tag="ul">
  <li v-for="item in items" :key="item.id">
    {{ item.text }}
  </li>
</TransitionGroup>
```

### Using @vueuse/motion
```vue
<script setup>
import { useMotion } from '@vueuse/motion'

const target = ref()
useMotion(target, {
  initial: { opacity: 0, y: 20 },
  enter: { opacity: 1, y: 0 },
})
</script>

<template>
  <div ref="target">Animated content</div>
</template>
```

---

## Responsive Patterns

### Tailwind in Vue
Same as React — mobile-first with breakpoint prefixes:
```vue
<div class="px-4 md:px-8 lg:px-16">
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
```

### Composable for responsive logic
```ts
// composables/useBreakpoints.ts
import { useMediaQuery } from '@vueuse/core'

export function useBreakpoints() {
  return {
    isMobile: useMediaQuery('(max-width: 767px)'),
    isTablet: useMediaQuery('(min-width: 768px) and (max-width: 1023px)'),
    isDesktop: useMediaQuery('(min-width: 1024px)'),
  }
}
```
