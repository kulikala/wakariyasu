# A single-file page with Vue, Tailwind CSS and Lucide

This is the starting point when nothing in the environment or the project sets the page's code. The page is one HTML file with no build step, so it opens directly in a browser and can be published as an artifact as it is. It uses Vue 3 for state (switching views, filtering, opening details), Tailwind CSS v4 for styling, and Lucide for icons, all loaded from jsDelivr.

The URLs name only the major versions of Vue (3) and Tailwind CSS (4), so the page loads the latest release within each major version. The Lucide URL names no version and loads the latest release.

Vue is loaded from jsDelivr's `+esm` build of the bundler file, which includes the template compiler. Lucide's `+esm` bundle imports Vue's runtime from jsDelivr in the same form, so the page and the icons share one Vue runtime. When they run on separate copies of Vue, icons fail to render and the console shows an error from inside the Lucide bundle.

## The file

```html
<!DOCTYPE html>
<html lang="{{language code of the page}}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{name}}</title>
  <script type="importmap">
    {
      "imports": {
        "vue": "https://cdn.jsdelivr.net/npm/vue@3/dist/vue.esm-bundler.js/+esm",
        "@lucide/vue": "https://cdn.jsdelivr.net/npm/@lucide/vue/+esm"
      }
    }
  </script>
  <script type="module" src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  <style type="text/tailwindcss">
    @theme {
      /* One line per color role the page uses, with its light value */
      --color-{{role}}: {{light value}};
    }
    @layer base {
      :root { color-scheme: light; }
      @media (prefers-color-scheme: dark) {
        :root {
          /* The same roles with their dark values */
          --color-{{role}}: {{dark value}};
          color-scheme: dark;
        }
      }
      body { @apply bg-{{background role}} text-{{text role}}; }
    }
  </style>
</head>
<body>
  <div id="app">
    <!-- Page content -->
  </div>

  <script type="module">
    import { createApp, ref, computed, reactive } from 'vue'
    // Import each icon the page uses by its Lucide component name, and list the same names in components
    import { {{IconName}} } from '@lucide/vue'

    const app = createApp({
      components: { {{IconName}} },
      setup () {
        // Composition API state for the page
        return {}
      }
    })
    app.mount('#app')
  </script>
</body>
</html>
```

- Set `lang` to the language the page is written in. Browsers choose the default font from it, so a page with the wrong `lang` can show text in a typeface meant for another language.
- The page specifies no font and uses the browser's default.
- Decide the color roles and their values from what the page shows and what its cues must tell apart. The roles include one for the page background and one for the body text. A role's name becomes part of Tailwind class names, so use a name that is valid there. Define each role once in `@theme` with its light value, and redefine it with its dark value under `prefers-color-scheme: dark`. Utilities built from a token (`bg-{{role}}`, `text-{{role}}`) then follow the device's setting without a `dark:` variant on every element. Give `body` its background and text color from the tokens.

## Writing Lucide icons in the template

Vue reads the template from the HTML in the page, which the browser parses first. The browser lowercases tag names and does not treat a custom tag written as self-closing as closed.

- Import the icons you use from `@lucide/vue` and register them in the app's `components`. In the template, write each one as the kebab-case form of its component name, not in PascalCase.
- Put each icon inside its own element, such as a `<div>`. Otherwise the icon tag stays open and takes the elements after it as its children.

```html
<div><{{icon-name}} /></div>
```

## Publishing as a Claude artifact

When the page is published as a Claude artifact, follow the environment's rules for artifacts (the instructions of the tool that publishes them); they take precedence over this file. The points below are where those rules touch this file.

- The publishing step wraps the page in the document skeleton (DOCTYPE, `html`, `head`, `body`). Leave out those four parts and start the file with the `<title>`, followed by the import map, the Tailwind script, the Tailwind style and the color-switching style described below, then the element with the id `app` and the module script. With no `html` element to carry `lang`, put `lang` on the element with the id `app`.
- Scripts load only from the hosts the environment allows. jsDelivr, which the file uses, is one of them.
- The viewer can force a theme by setting `data-theme="dark"` or `data-theme="light"` on the root element, while the default leaves it unset and follows the device. The publishing skeleton also sets `color-scheme: light` on `:root` outside any CSS layer, and a rule outside a layer wins over Tailwind's layered rules, so `color-scheme: dark` inside `@layer base` has no effect and form controls and scrollbars stay light. Remove the `:root` rule and the media query from the `@layer base` block, leaving only the `body` rule there, and put the color switching in a plain `<style>` element (without `type="text/tailwindcss"`) after the Tailwind style, guarded so that the page follows whichever applies.

```html
<style>
  /* The light values stay in @theme */
  :root { color-scheme: light; }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --color-{{role}}: {{dark value}};
      color-scheme: dark;
    }
  }
  :root[data-theme="dark"] {
    --color-{{role}}: {{dark value}};
    color-scheme: dark;
  }
</style>
```
