---
name: show-changes
description: Turn the before and after of a change, across one or more targets (two commits of a git repository, two folders or files, or an existing unified diff), into a single HTML page so a person can check the whole change and its details in a browser. Use when asked to show the diff, show the changes, display what changed, put the changes on a page, or collect the diff for review; when showing changes to a person before review, approval, merge or replacement; and when showing changes that span several repositories or folders. Also use when asked to show the full text of files rather than a change, such as the whole of a skill or a document, so that the person reads it on the same kind of page. Also use, without being asked, when you finish work that changed files and show the user what you changed. Do not use when you only read a diff yourself or when you check whether a change is good. Also applies when the user says the same thing in another language.
---

# Purpose of the skill

Turn the before and after of a change into one HTML page that opens in a browser. The person viewing the page (a reviewer or approver, sometimes the user who asked) must be able to check two things in one place, across repositories and folders: how much changed (the whole) and how it changed (the details). The page shows the change. It does not judge whether the change is good. The caller is the user who asked for this skill, or the agent that invoked it.

Build the page with the bundled `scripts/build.py`. If Python 3.9 or later (`python3` or similar) is available, run `build.py`. If it is not available, tell the caller that the page cannot be built. Before building, read `references/usage.md`, which gives the invocation and the arguments. Paths inside the skill (`scripts/`, `references/`) are relative to the skill's folder.

## Specify what to compare

- Choose the kind of target to match the change the viewer needs to check. For changes managed by git, compare two commits. For files that git does not manage (a copy made before the change and the current version, or two versions of a folder), compare two folders. For a diff made by another tool, use that tool's unified diff. One page can mix kinds.
- To show a branch's changes, compare from the point where the branch diverged from the target branch to the tip of the branch (`--merge-base`). Changes added to the target branch later then stay out of the page.
- A comparison of two git commits covers only committed changes. The user decides whether to commit work in progress. To show uncommitted work, use one of two ways. One is to pass the output of `git diff HEAD` as a unified diff; new files not yet added to git are not included. The other is to compare a copy made before the change with the current files as two folders. A two-folder comparison also compares files that git ignores (dependencies, build output, files with credentials), so put only the files to show in the folders you compare.
- A unified diff holds only the line ranges it lists. To show the whole of a file, use another kind of target.
- When the person wants to read files rather than a change (the full text of a skill, a document or a folder), pass them as files to show (`--files`), read from disk when you build the page. Nothing is compared: the page holds each file's full text and opens on the range "after", the same view that shows the full text after a change without diff marks.
- Pass `--lang` with the language of the page you are producing, which is the language the viewer reads the page in. That can differ from the language you use in the conversation. The page's words then come from `lang/<code>/labels.json` of this skill (see `references/usage.md`, "The page language"); without `--lang` the page is in English.
- Give the page a title and a data version (`--data-version`, a string shown as is in the page header), so that the viewer can later say what they were looking at. Put what changed in the title. Put something that identifies the compared states (a commit, a date, a version name) in the data version.

## Decide whether to include full text

Full text lets the viewer read a change in the flow of the whole file, not only the lines around the changed lines. With full text, the page grows by the size of the changed files. With full text, the viewer can also switch to the text after the change alone, without the removed lines and the diff marks. Include full text when the request suggests the viewer needs the surrounding flow (a rewritten document, a partial change to a configuration file). Use the diff alone when the viewer only needs the amount or location of changes. If the request suggests neither, use the diff alone. When you hand over a diff-only page, say that a page with full text can also be built. A page of files to show (`--files`) always has full text.

## Hand over the page

Hand over the page in a form the viewer can open on the spot. If you only save an HTML file and point to its location or attachment, the viewer must fetch and open the file before seeing the page. In environments where Claude runs, present the page as an artifact by default.

- If a tool can publish a local HTML file as an artifact as it is, publish the file you built. Claude publishes artifacts by wrapping the page in a document skeleton (DOCTYPE, html, head, body). So add `--artifact` to `build.py` to write the page without the skeleton. The page holds all the diff data and can be large, so publish the file as it is and do not copy its contents.
- In environments that build an artifact from its contents (no tool publishes files, and the agent writes the artifact's contents), use the page `build.py` wrote, unmodified, as the artifact's contents. If you edit the page by hand, its diff no longer matches the actual change. If the page is too large to use as contents, build a page without full text.
- In environments without artifacts, save the HTML file and tell the caller where it is. If the caller named no location, save it where none of the compared repositories or folders contains it. `build.py` stops if the output is inside a compared target.
- If the publishing destination has a size limit and the page exceeds it, build a page without full text or hand over the HTML file.

- `build.py` overwrites a file of the same name at the output path without checking. Do not reuse the name of a page someone has open or has edited.
- A published page is stored on an external service. If a target is one the user treats as confidential, or likely holds information that its owner has not allowed outside, hand over the HTML file instead of publishing it, and leave the location to the caller. A diff-only page holds the changed lines, a few lines around them, and the commit subjects. A page with full text also holds all the unchanged parts of the changed files.
- When you hand over the page, add a short note of what was compared: the targets, the two states compared, and whether the comparison started from the divergence point. Also say whether full text is included. With the note, the viewer can judge whether any change is missing from the page.
