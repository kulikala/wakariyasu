# A single-file page with Vue, Tailwind CSS and Lucide

This is the starting point when nothing in the environment or the project sets the page's code. The page is one HTML file with no build step, so it opens directly in a browser and can be published as an artifact as it is. It uses Vue 3 for state (switching views, filtering, opening details), Tailwind CSS v4 for styling, and Lucide for icons, all loaded from jsDelivr.

The library URLs below carry no version, so the page loads the latest release of each library. Where the environment requires exact versions, see "Publishing as a Claude artifact".

## The file

```html
<!DOCTYPE html>
<html lang="{{language of the page}}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{name}}</title>
  <script type="importmap">
    {
      "imports": {
        "vue": "https://cdn.jsdelivr.net/npm/vue/dist/vue.esm-browser.js",
        "lucide-vue-next": "https://cdn.jsdelivr.net/npm/lucide-vue-next/+esm"
      }
    }
  </script>
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser"></script>
  <style type="text/tailwindcss">
    @theme {
      /* Light values of the page's colors. Use them as bg-surface, text-ink and so on. */
      --color-surface: #ffffff;
      --color-ink: #1f2328;
    }
    @layer base {
      :root { color-scheme: light; }
      @media (prefers-color-scheme: dark) {
        :root {
          /* Dark values of the same colors */
          --color-surface: #16181d;
          --color-ink: #e6e8eb;
          color-scheme: dark;
        }
      }
      body { @apply bg-surface text-ink; }
    }
  </style>
</head>
<body>
  <div id="app">
    <!-- Page content -->
  </div>

  <script type="module">
    import { createApp, ref, computed, reactive } from 'vue'

    const app = createApp({
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
- Define each color the page uses once in `@theme` with its light value, and redefine it with its dark value under `prefers-color-scheme: dark`. Utilities built from the token (`bg-surface`, `text-ink`) then follow the device's setting without a `dark:` variant on every element. Give `body` its background and text color from the tokens.

## Writing Lucide icons in the template

Vue reads the template from the HTML in the page, which the browser parses first. The browser lowercases tag names and does not treat a custom tag written as self-closing as closed.

- Import the icons you use from `lucide-vue-next` and register them in the app's `components`. In the template, write them in kebab-case (`<bell />` for `Bell`, `<chevron-down />` for `ChevronDown`), not in PascalCase.
- Put each icon inside its own element, such as a `<div>`. Otherwise the icon tag stays open and takes the elements after it as its children.

```html
<button>
  <div><bell /></div>
  <span>Notifications</span>
</button>
```

## Publishing as a Claude artifact

When the page is published as a Claude artifact, follow the environment's rules for artifacts (the instructions of the tool that publishes them); they take precedence over this file. The points below are where those rules touch this file.

- The publishing step wraps the page in the document skeleton (DOCTYPE, `html`, `head`, `body`). Leave out those four parts and start the file with the `<title>`, followed by the import map, the Tailwind script and the style. With no `html` element to carry `lang`, put `lang` on the element with the id `app`.
- Scripts load only from the hosts the environment allows (jsDelivr is one), and each URL must name an exact version. Before writing the URLs, look up the current release of each library that the environment's rules accept, and put that version in each URL.
- The viewer can force a theme by setting `data-theme="dark"` or `data-theme="light"` on the root element, while the default leaves it unset and follows the device. Apply the dark values under `:root[data-theme="dark"]` as well, and guard the media query with `:root:not([data-theme="light"])`, so the page follows whichever applies. Use this block in place of the `@layer base` block of the file.

```css
@layer base {
  :root { color-scheme: light; }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --color-surface: #16181d;
      --color-ink: #e6e8eb;
      color-scheme: dark;
    }
  }
  :root[data-theme="dark"] {
    --color-surface: #16181d;
    --color-ink: #e6e8eb;
    color-scheme: dark;
  }
  body { @apply bg-surface text-ink; }
}
```
