# How to modify show-changes

The page of the skill `show-changes` is built by `build.py` in `skills/show-changes/scripts/` (the script that collects the diff and builds the page), which embeds the data into `template.html` (the page template).

The page's fixed words are not in the template. `template.html` holds an empty `/*__LABELS__*/{}/*__LABELS_END__*/` block, and `build.py` fills it with the English words of `lang/en/labels.json` of the skill; the words of another language are stored in the page's data under `labels`. To add or change a word, change `lang/en/labels.json` and the `labels.json` of every other language (the test checks that the keys and the words in braces agree), and use the word in the template as `T('<key>')`.

## Testing after a change

```sh
python3 -B dev/test-show-changes.py --repo <name> <location> <BASE> <TARGET> [--merge-base <name>] [--sample-dir <folder to save to>]
```

From two commits of the repository passed with `--repo`, `dev/test-show-changes.py` builds a diff-only page, a page that includes full text, and a page built with `--artifact`, and checks the HTML text of each (an artifact page starts with `<title>` and has none of the DOCTYPE, html, head and body tags or the charset and viewport metas, a plain page is a complete document, and in both the parts come in the order title, import map, decoder, data script, Tailwind script, Tailwind style, color-switching style, `#app`, module script; the utfpack decoder tag with its `integrity` value, the data script, and a packed string that holds neither `</script` nor `<!--`). It also verifies the following.

- Data does not change when written out to JSON and read back.
- Mistakes fixed in the past have not happened again (the list of mistakes is `regressions`, which `dev/test-show-changes.py` prints).
- The state of the compared repository is the same before and after the test.
- A page can be built that mixes two-folder targets with unified diff targets (the forms `git diff`, `--no-prefix` and `diff -ru`). Targets containing bytes that cannot be read as UTF-8 and symbolic links can also be built.

The built page is received on standard output, and the two-folder targets are created in a temporary folder. The built page is saved only when `--sample-dir` (an existing writable folder) is passed. Building a page downloads utfpack's packer from jsDelivr (or uses the cache), so the test needs a network connection the first time.

The test does not open a page in a browser. After changing `template.html`, build pages (diff only, with full text, with `--artifact`, and of `--files` targets) and open them by hand in any browser to check how they behave.

## Decisions and reasons

- The display is a single Vue 3 file and uses no build system. Libraries are loaded from a CDN. `template.html` holds the parts of the page (title, import map, styles, then the marker `<!--__BODY__-->`, then `#app`, the loading message and the module script); `build.py` puts them into a complete document for a plain file, or leaves them as parts for `--artifact`, without removing anything afterwards. This is so that `build.py` runs on the Python standard library alone and the page can be handed over as one file.
- Libraries are imported as ESM through the import map, which follows `skills/compose-page/references/single-file-page.md`.
- No external stylesheets are loaded other than Google Fonts. Depending on where it is displayed (such as Claude artifacts), stylesheets other than Google Fonts are blocked. highlight.js is loaded as ESM with only the core and the languages used, and colors are applied with Tailwind classes.
- Vue is loaded from `vue@3/dist/vue.esm-bundler.js/+esm`, the same Vue runtime that @lucide/vue imports on jsDelivr, so the page and the icons share one Vue. This build includes the template compiler. Because templates are compiled at runtime, the page does not work where the display site forbids `unsafe-eval` in its CSP. It works in Claude artifacts.
- The import map names major versions only (Vue 3, Tailwind CSS 4, highlight.js 11) and no version for @lucide/vue.
- The page data is packed with utfpack, which makes a page about a third of the size of the same data as plain JSON. `build.py` does not bundle the packer. When it builds a page (`-o`; not for `--json-out` alone or `--init`), it downloads `https://cdn.jsdelivr.net/npm/utfpack@0/python/utfpack_pack.py` (the [utfpack repository](https://github.com/kulikala/utfpack)'s `python/utfpack_pack.py`, major version 0, so fixes and features of utfpack 0.x are picked up without a change here). The resolved version comes from the response header `x-jsd-version` (the module's `VERSION` when the header is absent), and the file is cached as `wakariyasu/utfpack/<version>/utfpack_pack.py` under `XDG_CACHE_HOME` or `~/.cache` (`LOCALAPPDATA` on Windows). When the download fails, the newest cached version is used; with no cache, `build.py` stops with exit code 2. The decoder's URL and `integrity` on the page come from the loaded packer (`VERSION` and `decoder_sri('utfpack')`), and the decoder is loaded from jsDelivr.
- Only jsDelivr is used as the CDN. It is among the sources Claude artifacts allow loading from.
- Opening and closing is done with buttons and the page's own state, not `<details>` or in-page links (`#...`). Scripts that the display site injects can break the behavior of `<details>` and in-page links.
- File headings and `@@` lines are made sticky inside the scroll frame so that they stay at the top. The corners of a file's frame are rounded with `overflow: clip`, and `overflow: hidden` is not used, because `hidden` creates a scroll container and sticky stops working. For the same reason, the padding of the scroll frame (`#main`) is put on an inner element.
- The diff is made by git if git is available (`git diff --no-index` for two-folder targets), and by Python's difflib only when git is unavailable. difflib is slow on large files with many identical lines.
- Bytes that cannot be read as UTF-8 are kept in the form `\xNN`, not as the replacement character. With the replacement character, different bytes look like the same character, and a changed line would look unchanged.
- Search is not applied to the patch heading, the `@@` lines or the marks at the start of lines. What viewers look for is file names and the text of lines.
- Whitespace symbols are drawn with CSS (background and pseudo-elements), and the page's text is left as the original, because copying and searching then handle the original characters, not the symbols.
- Symbols are attached only to the changed range within a line, to a leading indent that differs from the paired line, to trailing whitespace on a changed line, and to zero-width characters that appear on any line (ZWSP and BOM). Marking all whitespace would fill even unchanged indentation with symbols. A trailing CR gets a symbol only when it changed, to avoid symbols on every changed line in CRLF files.
- "Ignore" under 「空白」 (whitespace) follows the same idea as `git diff -w`: lines that become identical when whitespace (including full-width spaces, tabs and a trailing CR) is removed are shown as unchanged lines. Added and deleted blank lines are kept. The diff is rebuilt inside the page, so only one set of data is needed.
- "Only added and changed files" keeps only files whose state is added or changed and whose content has a diff (including binary files). Permission-only changes, moves, copies, deletions, symbolic links and submodules are excluded because they are not targets whose file contents are read. Moves and copies are excluded even if their contents changed. On a page where every file would remain, the button is not shown, because a button that changes nothing when pressed confuses viewers.
- When the mouse is over a selected button, the selected button's color is made darker. If it were the same as the color over an unselected button, the appearance would not change after pressing until the mouse is released, and viewers would think they had not pressed it and press again.
- When a file is closed by pressing its heading, the next file's heading is scrolled to match the position the viewer was looking at. If you had scrolled partway through the closed file, staying at the same position after closing would show the middle of a later file. When the top of the closed file is on screen, no scrolling is done.
