#!/usr/bin/env bash
# detect_stack.sh - Detect framework, styling approach, component library, and file structure
# Usage: ./detect_stack.sh [project_root]

set -e

PROJECT_ROOT="${1:-.}"

# Initialize result object
result='{}'

# Helper function to check if file exists
file_exists() {
    [[ -f "$PROJECT_ROOT/$1" ]]
}

# Helper function to check if directory exists
dir_exists() {
    [[ -d "$PROJECT_ROOT/$1" ]]
}

# Helper function to check if package.json has dependency
has_dependency() {
    if file_exists "package.json"; then
        grep -q "\"$1\"" "$PROJECT_ROOT/package.json" 2>/dev/null
    else
        return 1
    fi
}

# Detect Framework
detect_framework() {
    local framework="unknown"
    local framework_version=""

    # Next.js
    if file_exists "next.config.js" || file_exists "next.config.mjs" || file_exists "next.config.ts"; then
        framework="nextjs"
        if has_dependency "next"; then
            framework_version=$(grep -o '"next": *"[^"]*"' "$PROJECT_ROOT/package.json" | head -1 | cut -d'"' -f4)
        fi
    # Nuxt
    elif file_exists "nuxt.config.js" || file_exists "nuxt.config.ts"; then
        framework="nuxt"
        if has_dependency "nuxt"; then
            framework_version=$(grep -o '"nuxt": *"[^"]*"' "$PROJECT_ROOT/package.json" | head -1 | cut -d'"' -f4)
        fi
    # SvelteKit
    elif file_exists "svelte.config.js" || file_exists "svelte.config.ts"; then
        framework="sveltekit"
    # Astro
    elif file_exists "astro.config.mjs" || file_exists "astro.config.ts"; then
        framework="astro"
    # Gatsby
    elif file_exists "gatsby-config.js" || file_exists "gatsby-config.ts"; then
        framework="gatsby"
    # Angular
    elif file_exists "angular.json"; then
        framework="angular"
    # Vue (Vite or Vue CLI)
    elif has_dependency "vue"; then
        if file_exists "vite.config.js" || file_exists "vite.config.ts"; then
            framework="vue-vite"
        else
            framework="vue"
        fi
    # React (Vite or CRA)
    elif has_dependency "react"; then
        if file_exists "vite.config.js" || file_exists "vite.config.ts"; then
            framework="react-vite"
        else
            framework="react"
        fi
    # Svelte (standalone)
    elif has_dependency "svelte"; then
        framework="svelte"
    # Plain HTML
    elif file_exists "index.html" && ! file_exists "package.json"; then
        framework="html"
    # Has package.json but unknown framework
    elif file_exists "package.json"; then
        framework="unknown-node"
    fi

    echo "{\"name\": \"$framework\", \"version\": \"$framework_version\"}"
}

# Detect Styling Approach
detect_styling() {
    local styles=()

    # Tailwind CSS
    if file_exists "tailwind.config.js" || file_exists "tailwind.config.ts" || file_exists "tailwind.config.mjs"; then
        styles+=("tailwind")
    fi

    # CSS Modules (check for .module.css files)
    if find "$PROJECT_ROOT" -name "*.module.css" -o -name "*.module.scss" 2>/dev/null | head -1 | grep -q .; then
        styles+=("css-modules")
    fi

    # Styled Components
    if has_dependency "styled-components"; then
        styles+=("styled-components")
    fi

    # Emotion
    if has_dependency "@emotion/react" || has_dependency "@emotion/styled"; then
        styles+=("emotion")
    fi

    # SCSS/Sass
    if has_dependency "sass" || has_dependency "node-sass"; then
        styles+=("scss")
    elif find "$PROJECT_ROOT" -name "*.scss" -o -name "*.sass" 2>/dev/null | head -1 | grep -q .; then
        styles+=("scss")
    fi

    # LESS
    if has_dependency "less" || find "$PROJECT_ROOT" -name "*.less" 2>/dev/null | head -1 | grep -q .; then
        styles+=("less")
    fi

    # Plain CSS (fallback)
    if [[ ${#styles[@]} -eq 0 ]]; then
        if find "$PROJECT_ROOT" -name "*.css" 2>/dev/null | head -1 | grep -q .; then
            styles+=("plain-css")
        fi
    fi

    # Convert array to JSON
    printf '%s\n' "${styles[@]}" | jq -R . | jq -s .
}

# Detect Component Library
detect_component_library() {
    local libraries=()

    # shadcn/ui (check for components/ui directory with specific files)
    if dir_exists "components/ui" || dir_exists "src/components/ui"; then
        if find "$PROJECT_ROOT" -path "*/components/ui/*" -name "*.tsx" 2>/dev/null | head -1 | grep -q .; then
            libraries+=("shadcn-ui")
        fi
    fi

    # Material UI
    if has_dependency "@mui/material" || has_dependency "@material-ui/core"; then
        libraries+=("material-ui")
    fi

    # Chakra UI
    if has_dependency "@chakra-ui/react"; then
        libraries+=("chakra-ui")
    fi

    # Ant Design
    if has_dependency "antd"; then
        libraries+=("ant-design")
    fi

    # Radix UI
    if has_dependency "@radix-ui/react-dialog" || has_dependency "@radix-ui/themes"; then
        libraries+=("radix-ui")
    fi

    # Headless UI
    if has_dependency "@headlessui/react" || has_dependency "@headlessui/vue"; then
        libraries+=("headless-ui")
    fi

    # Bootstrap
    if has_dependency "bootstrap" || has_dependency "react-bootstrap"; then
        libraries+=("bootstrap")
    fi

    # Vuetify
    if has_dependency "vuetify"; then
        libraries+=("vuetify")
    fi

    # PrimeVue / PrimeReact
    if has_dependency "primevue" || has_dependency "primereact"; then
        libraries+=("primevue")
    fi

    # Mantine
    if has_dependency "@mantine/core"; then
        libraries+=("mantine")
    fi

    # Convert array to JSON
    if [[ ${#libraries[@]} -eq 0 ]]; then
        echo "[]"
    else
        printf '%s\n' "${libraries[@]}" | jq -R . | jq -s .
    fi
}

# Detect Design Tokens
detect_design_tokens() {
    local tokens=()

    # Tailwind config with theme extension
    if file_exists "tailwind.config.js" || file_exists "tailwind.config.ts"; then
        if grep -q "theme" "$PROJECT_ROOT/tailwind.config."* 2>/dev/null; then
            tokens+=("tailwind-theme")
        fi
    fi

    # CSS Custom Properties
    if find "$PROJECT_ROOT" -name "*.css" -exec grep -l -- '--' {} \; 2>/dev/null | head -1 | grep -q .; then
        tokens+=("css-variables")
    fi

    # Theme files
    if file_exists "theme.js" || file_exists "theme.ts" || file_exists "src/theme.js" || file_exists "src/theme.ts"; then
        tokens+=("theme-file")
    fi

    # Design tokens JSON
    if file_exists "tokens.json" || file_exists "design-tokens.json"; then
        tokens+=("tokens-json")
    fi

    # Convert array to JSON
    if [[ ${#tokens[@]} -eq 0 ]]; then
        echo "[]"
    else
        printf '%s\n' "${tokens[@]}" | jq -R . | jq -s .
    fi
}

# Detect File Structure
detect_file_structure() {
    local structure='{}'

    # Components directory
    if dir_exists "src/components"; then
        structure=$(echo "$structure" | jq '.components = "src/components"')
    elif dir_exists "components"; then
        structure=$(echo "$structure" | jq '.components = "components"')
    elif dir_exists "app/components"; then
        structure=$(echo "$structure" | jq '.components = "app/components"')
    fi

    # Pages/Routes directory
    if dir_exists "src/app"; then
        structure=$(echo "$structure" | jq '.pages = "src/app (App Router)"')
    elif dir_exists "app"; then
        structure=$(echo "$structure" | jq '.pages = "app"')
    elif dir_exists "src/pages"; then
        structure=$(echo "$structure" | jq '.pages = "src/pages"')
    elif dir_exists "pages"; then
        structure=$(echo "$structure" | jq '.pages = "pages"')
    elif dir_exists "src/routes"; then
        structure=$(echo "$structure" | jq '.pages = "src/routes"')
    elif dir_exists "src/views"; then
        structure=$(echo "$structure" | jq '.pages = "src/views"')
    fi

    # Styles directory
    if dir_exists "src/styles"; then
        structure=$(echo "$structure" | jq '.styles = "src/styles"')
    elif dir_exists "styles"; then
        structure=$(echo "$structure" | jq '.styles = "styles"')
    elif dir_exists "src/css"; then
        structure=$(echo "$structure" | jq '.styles = "src/css"')
    elif dir_exists "css"; then
        structure=$(echo "$structure" | jq '.styles = "css"')
    fi

    # Global styles file
    if file_exists "src/app/globals.css"; then
        structure=$(echo "$structure" | jq '.globalStyles = "src/app/globals.css"')
    elif file_exists "src/index.css"; then
        structure=$(echo "$structure" | jq '.globalStyles = "src/index.css"')
    elif file_exists "src/styles/globals.css"; then
        structure=$(echo "$structure" | jq '.globalStyles = "src/styles/globals.css"')
    elif file_exists "styles/globals.css"; then
        structure=$(echo "$structure" | jq '.globalStyles = "styles/globals.css"')
    elif file_exists "src/App.css"; then
        structure=$(echo "$structure" | jq '.globalStyles = "src/App.css"')
    fi

    # Assets directory
    if dir_exists "public"; then
        structure=$(echo "$structure" | jq '.assets = "public"')
    elif dir_exists "static"; then
        structure=$(echo "$structure" | jq '.assets = "static"')
    elif dir_exists "assets"; then
        structure=$(echo "$structure" | jq '.assets = "assets"')
    fi

    echo "$structure"
}

# Count files by extension
count_files() {
    local counts='{}'

    # Count various file types
    local tsx_count=$(find "$PROJECT_ROOT" -name "*.tsx" 2>/dev/null | wc -l | tr -d ' ')
    local jsx_count=$(find "$PROJECT_ROOT" -name "*.jsx" 2>/dev/null | wc -l | tr -d ' ')
    local vue_count=$(find "$PROJECT_ROOT" -name "*.vue" 2>/dev/null | wc -l | tr -d ' ')
    local svelte_count=$(find "$PROJECT_ROOT" -name "*.svelte" 2>/dev/null | wc -l | tr -d ' ')
    local css_count=$(find "$PROJECT_ROOT" -name "*.css" 2>/dev/null | wc -l | tr -d ' ')
    local scss_count=$(find "$PROJECT_ROOT" -name "*.scss" 2>/dev/null | wc -l | tr -d ' ')
    local html_count=$(find "$PROJECT_ROOT" -name "*.html" 2>/dev/null | wc -l | tr -d ' ')

    echo "{\"tsx\": $tsx_count, \"jsx\": $jsx_count, \"vue\": $vue_count, \"svelte\": $svelte_count, \"css\": $css_count, \"scss\": $scss_count, \"html\": $html_count}"
}

# Build final JSON output
framework=$(detect_framework)
styling=$(detect_styling)
componentLibrary=$(detect_component_library)
designTokens=$(detect_design_tokens)
fileStructure=$(detect_file_structure)
fileCounts=$(count_files)

# Combine all results
jq -n \
    --argjson framework "$framework" \
    --argjson styling "$styling" \
    --argjson componentLibrary "$componentLibrary" \
    --argjson designTokens "$designTokens" \
    --argjson fileStructure "$fileStructure" \
    --argjson fileCounts "$fileCounts" \
    --arg projectRoot "$PROJECT_ROOT" \
    '{
        projectRoot: $projectRoot,
        framework: $framework,
        styling: $styling,
        componentLibrary: $componentLibrary,
        designTokens: $designTokens,
        fileStructure: $fileStructure,
        fileCounts: $fileCounts
    }'
