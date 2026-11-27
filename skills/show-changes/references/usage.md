# How to use build.py

Read this when you build or rebuild a page.

## Requirements

- Python 3.9 or later. Only the standard library is used. When building a page (`-o`), `build.py` downloads the packer of utfpack (a library that compresses data into a string a page can carry) from jsDelivr and keeps a copy. Building a page therefore needs network access, except that a copy from an earlier build is used when the download fails; with neither, `build.py` stops and says so. `--json-out` alone and `--init` need no network.
- When the page opens, it loads its libraries (Vue, Tailwind CSS, Lucide, highlight.js) and utfpack's decoder, which turns that string back into the data, from the CDN jsDelivr. The viewer needs a network connection, and the place that shows the page (a browser, or a host such as Claude artifacts) must allow jsDelivr. `--embed-decoder` puts the decoder into the page; the libraries still load from jsDelivr.
- git is required to collect a git two-commit target (`--repo`). Other targets and `--data` work without git. When git is available, the diff of a two-folder target is also built with git, which is fast even for large files.

## Build a page

```
python3 -B scripts/build.py --repo <name> <repository path> <BASE> <TARGET> --data-version '<version>' -o <output>.html
python3 -B scripts/build.py --repo <name> <path> main <branch> --merge-base <name> --data-version '<version>' -o <output>.html
python3 -B scripts/build.py --dirs <name> <before> <after> --data-version '<version>' -o <output>.html
python3 -B scripts/build.py --diff <name> <diff file> --data-version '<version>' -o <output>.html
python3 -B scripts/build.py --files <name> <file or folder>... --data-version '<version>' -o <output>.html
```

| Argument | Meaning |
|---|---|
| `--repo NAME PATH BASE TARGET` | A target made of two git commits. `PATH` can be anywhere inside the repository. `BASE` is the before state and `TARGET` is the after state; pass each as a branch, commit or tag. |
| `--dirs NAME BEFORE AFTER` | A target made of two ordinary folders or two files. It does not look inside `.git`, but it compares files that git ignores. It does not follow symbolic links and compares the link target paths. A change between a regular file and a symbolic link appears as a type change (T). |
| `--diff NAME FILE` | A target made of an existing unified diff. The format can be the `git diff` form (including the `--no-prefix` form without prefixes) or the `diff -u` / `diff -ru` form with only `---` and `+++`. |
| `--files NAME PATH...` | Files to show in full, not a change. Each path is a file or a folder, read from disk when the page is built; nothing is compared. The page holds the full text of each file and opens on the range "after", which shows the text without diff marks. A file's path on the page is its path inside the folder that was passed (a file passed alone shows its name); with several paths, each path on the page also starts with the last part of the path that was passed. |
| `--merge-base NAME` | Compare the target whose `--repo` name is `NAME` from the divergence point of `BASE` and `TARGET` to `TARGET` (the same range as `git diff BASE...TARGET`). |
| `--data-version` | The data version, shown as is in the header. Any form. Required when collecting new data. |
| `--title` | The page title. If omitted, the title is "Diff review" (or the `defaultTitle` word of the page's language). |
| `--group-depth N` | The directory depth at which the file list is grouped. Default 2; 0 means no grouping. |
| `--full-text` | Also include the full text of changed files. |
| `--lang CODE` | The language of the page you are producing. It sets the `lang` of the page and takes the page's words from `lang/CODE/labels.json` (see "The page language"). |
| `--labels FILE` | A JSON file of the page's words (buttons, headings, tooltips, notices and dates). For a language that has no `lang/CODE/labels.json`, it holds every word; for a language that has one, it holds only the words to change. An unknown key, a missing key and a dropped word in braces stop the build. |
| `--init CODE` | With `-o FILE`: write the English words as a JSON file to translate for the language `CODE`, then stop. |
| `--artifact` | Build the page for a destination that wraps what it publishes in its own document skeleton, as Claude artifacts do: the page then leaves out its own skeleton (DOCTYPE, html, head and body, and the charset and viewport meta), so the published page holds no document inside a document. Without it, the output is a complete HTML file that opens as is. |
| `--embed-decoder` | Put the utfpack decoder into the page instead of loading it from jsDelivr (see "Requirements"). |
| `-o` / `--output` | The HTML output path. `-` writes to standard output. |
| `--json-out` | Write the diff data as JSON. `-` writes to standard output. Can be used together with `-o`. |
| `--data <JSON>` | Build the page from a previously written JSON without collecting again. `-` reads standard input. |
| `--template` | Replace the template used for display. The default is `scripts/template.html`. |

- `--repo`, `--dirs`, `--diff` and `--files` can be mixed and repeated. Target names become the choices of the page's filter, so give names that do not overlap.
- The compared targets are never written to (git is only read). The script stops if the output path is inside a compared target.
- The exit code is 0 when the page was built and 2 for an error in arguments, git, input or JSON. Bytes that are not valid UTF-8 do not stop the build. They are shown in the form `\xNN`, and the file gets a notice. Errors go to standard error (git errors are git's own messages).
- Neither the HTML nor the JSON contains the location of the compared targets on this computer. The page can be handed to people as is.

## Rebuild from JSON

If you write the collected data to JSON, you can change the title or the display template and rebuild the page without collecting again.

```
python3 -B scripts/build.py --repo <name> <path> <BASE> <TARGET> --data-version '<version>' --json-out <output>.json
python3 -B scripts/build.py --data <output>.json --title '<title>' -o <output2>.html
```

- The title, data version, grouping depth, language and labels keep the JSON's values unless passed as arguments (`--lang`, `--labels`). Whether full text is included is decided by the JSON.
- `--data` cannot be combined with the collecting arguments (`--repo`, `--dirs`, `--diff`, `--files`, `--merge-base`, `--full-text`).
- Put the output where no git repository manages it (outside any repository, or in a work folder the repository ignores). The JSON does not hold the location of the compared targets, so the script cannot check whether the output is inside one. It therefore stops for output in a managed location and for output inside `.git`.
- The JSON format is in `references/data-format.md`. Read it only when you write or read JSON yourself.

## What the viewer can do on the page

Use this to tell the viewer how to use the page when handing it over. The page's own text (buttons, labels) is in English unless `--lang` was given (see "The page language").

- Select a target, and filter by file name or by the text of lines (the filter does not match `@@` lines or the leading `+` and `-`). Enter moves to the next matching line across all shown files, from the last back to the first, and Shift+Enter to the previous one, opening a closed file when needed; the count of matches is shown beside the input. Clear the entered text with the ✕ button at the right end of the input or with the Esc key.
- Open and close each file, and open all or close all. If the viewer scrolls partway into a file and closes it by its heading, the page scrolls so that the next file's heading is visible.
- A button next to a file name copies the file's path to the clipboard.
- When the viewer selects text, a small button appears above the selection, and pressing it copies the selected text.
- Layout (before and after stacked vertically, side by side, or inline: the text after the change read as one text, with changed words colored and a mark at each removal that shows the earlier text on hover or focus), range (diff, full text, or the text after the change alone without removed lines and diff marks; the last two are shown only when the data has full text) and color scheme (light, dark, or mixed, where the surroundings are dark and only the diff part is light). The color scheme starts from the OS or browser setting.
- The commit list (only for git two-commit targets; newest first, grouped by day).
- On wide screens, dragging the boundary between the file list and the diff changes the list's width (double-click restores it), and the button at the left end of the control bar hides the list. The width and the hidden state are kept in the viewer's browser.
- On smartphone widths, choosing from the file list moves to the diff screen, and the back button returns to the list.

## The page language

The page is in English by default. Pass `--lang <code>` with the language of the page you are producing, which is the language the viewer reads. It is not the language of your conversation with the person who asked. The script takes the page's words from `lang/<code>/labels.json` of this skill.

For a language without `lang/<code>/labels.json`, the script stops and names the `--init` command to run. That command writes the English words as a JSON file. Translate the values into the language of the page and keep the words in braces as they are; the page fills them in. Then pass the file:

```
python3 -B scripts/build.py --init <code> -o <labels>.json
python3 -B scripts/build.py --repo <name> <path> <BASE> <TARGET> --data-version '<version>' --lang <code> --labels <labels>.json -o <output>.html
```

The script stops on an unknown key, a missing key and a dropped word in braces, and says which. Do not open `scripts/template.html` to look for the words. With a language that has a pack, `--labels <file>` changes single words, and the file holds only those keys. The diff itself (file paths, lines, commit subjects) is shown as it is. The language and the words are stored in the JSON that `--json-out` writes, so a rebuild with `--data` keeps them.

## Page size

A diff-only page grows with the number of diff lines. A page with full text grows with the total size of the changed files. The page renders files nearest the screen first, so even a large page opens in about the same time.
