# Development guide

## Folder layout

```text
.claude-plugin/plugin.json       Plugin definition (name, version, skills location)
.claude-plugin/marketplace.json  Definition of the place to get the plugin from (the marketplace)
skills/<name>/SKILL.md           Body of a skill
skills/<name>/references/        References read only by that skill
skills/<name>/scripts/           Scripts that skill runs
skills/writing-rules/rules/      Rules (writing-to-user, writing-documents, polishing)
skills/writing-rules/references/ References the rules point to (questions for a decision, how to write instructions, how to write a README, how to write a changelog)
skills/writing-rules/lang/<language>/ Per-language additions (language packs; ja is Japanese, en is English)
skills/check-terms/lang/<code>/  For each language, the list of phrases the language does not use (terms.tsv) and the list of phrases to check in context (terms-caution.tsv)
skills/check-terms/scripts/      check-terms (searches documents for phrases) and terms-table (turns the lists into the table put into the hook and AGENTS.snippet.md)
tests/lang/<code>/terms-cases.txt   Examples that check-terms matches (deny) and examples it does not (allow)
tests/lang/<code>/caution-cases.txt Examples that check-terms prints marked "(check in context)" (flag) and examples it does not (allow)
tests/session-status-report.json A fictional report used by the test that builds the session-status page
hooks/                           Hooks that load the rules at the start of a session and tell where the language packs are (load-rules.sh, lang-index.sh)
AGENTS.snippet.md                The body of the rules to paste into agents other than Claude Code (made by dev/build)
dev/build                        Joins the rules, asking.md, the language packs and the phrase lists to make AGENTS.snippet.md
dev/test                         Checks the repository's rules
dev/test-show-changes.py         Test to run after changing build.py and template.html of show-changes (docs/show-changes.md)
dev/test-show-changes-page.mjs   Test that opens the show-changes page in a browser and tries operating it
dev/test-session-status.py       Test to run after changing build.py and template.html that build the session-status page, and the page wording in the Japanese language pack
.github/workflows/test.yml       GitHub Actions configuration that runs dev/test on every push and pull request
evals/                           Cases for claude plugin eval that measure whether skills are called
docs/                            Development guides
docs/agreements.md               Constraints agreed with the author (wording and formats a review does not flag)
CHANGELOG.md                     Changes for each version (CHANGELOG.ja.md is the Japanese version)
```

The hooks, `dev/build`, `check-terms` and `terms-table` run with only `sh` and standard commands. `dev/test` also uses `git`. No other runtime such as Python is needed.

`build.py`, which builds the page of the skill `show-changes`, runs on the Python 3 standard library. The test after changing `build.py` also uses node and Chrome. The steps for changing it are in [How to modify show-changes](show-changes.md).

`build.py`, which builds the page of the skill `session-status`, also runs on the Python 3 standard library. After changing `build.py`, `template.html` or the page wording in the Japanese language pack, run `python3 dev/test-session-status.py`.

## Changing the body

The rules and references are in the skill `writing-rules`, and the phrase lists and `check-terms` are in the skill `check-terms`; the other skills read from these two folders.
Even with a method that installs only the skill folders, such as `gh skill install`, `--all` installs all the skills side by side, so the other skills can read the two folders.

After changing a rule, a reference or a phrase list, rebuild `AGENTS.snippet.md` with `dev/build`.

```sh
dev/build
```

The bodies of the rules and skills are written in two layers.

- Content that applies to writing in any language (how replies and documents are put together, writing so that the reader can tell what a word refers to, how to ask a question for a decision and so on) is written in English in the bodies of the rules, references and skills. It is composed in English, not translated.
- Content added only when writing in one language (the choice of notation, commas, how to check sentences in that language, that language's proofreading skill and so on) is written in that language in the language pack `skills/writing-rules/lang/<language>/`. The language code is the two letters of ISO 639-1.

A language pack file has one of the following fixed names. A file with nothing to add is not created. The rules and skills refer to a language pack by these names.

| File | Contents |
|---|---|
| `polishing.md` | Checks added when polishing writing in that language. It also points to the list of phrases not to use and to external proofreading skills |
| `styles.md` | How to choose notation and style for each kind of writing |
| `conventions.md` | Names familiar to readers of that language (README section names, changelog subheadings, session-status headings and state words, column names of questions for a decision) |
| `skills.md` | What to add for each skill (written in a section named after the skill) |

There is no setting for the user to switch languages. The hook outputs only the bodies of the rules and `asking.md`, and the list of language packs (language codes and folder locations). If a language pack exists for the language of the reply or document being written, the agent reads the files in that folder before writing. To add a language, create a folder named with the language code under `lang/` and place files with the names above. The hooks, `dev/build` and `dev/test` count the folders under `lang/`, so they need no rewriting.

## Checking

```sh
dev/test
```

`dev/test` checks the following without calling a model.

- `AGENTS.snippet.md` matches the body, and no other skill has a file with the same name as a rule, a reference or a phrase list.
- The version is the same in `plugin.json`, `marketplace.json` and `CHANGELOG.md`.
- The marketplace (`marketplace.json`) lists only one plugin.
- For each skill, `SKILL.md` starts with frontmatter and has a `name` equal to the folder name and a `description`.
- The hook output contains the heading lines of the rules and `asking.md` and the folder location of each language pack, and does not contain the contents of the language packs.
- Language pack files have one of the fixed names.
- When a rule, reference, language pack or skill refers by name to a section of another rule or reference (in English bodies in the form ``the "<heading>" section of `x.md` ``, in Japanese bodies in the form ``（`x.md`）の「<見出し>」の節``), the named heading exists in the rule or reference it refers to.
- The files in the repository that the README links to exist.
- `check-terms` matches and does not match as the examples in `tests/lang/<code>/terms-cases.txt` say, for each language.
- `check-terms` prints marked "(check in context)" as the examples in `tests/lang/<code>/caution-cases.txt` say, for each language, and does not make the exit code 1.
- The Japanese language pack, the SKILL.md of `check-terms`, the README and the guide contain no phrases Japanese does not use.
- There is no `bin/` at the top level. With a `bin/`, claude.ai and Cowork (the feature of the Claude desktop app for handing over work in bulk) do not accept the whole plugin. Development scripts are placed in `dev/`.
- Line endings and whitespace match the `.editorconfig` settings (files registered in git are checked).

The format of the plugin definition is also checked by Claude Code's validation.

```sh
claude plugin validate .
```

## Measuring whether skills are called

The cases in `evals/` measure with `claude plugin eval` whether a skill is called for a given way of asking.
It calls a model, so it costs money. Run it locally when needed.

```sh
claude plugin eval . --model sonnet --allow-tools Write Edit --no-publish --max-cost-usd 5
```

| Case | How it asks | What it checks |
|---|---|---|
| `status-ja` | 「現状は？」 ("Where do things stand?") | `session-status` is called |
| `status-en` | "What's the status? What's done and what's left?" | `session-status` is called, and no Japanese is mixed into the reply |
| `document-ja` | Has the agent write a procedure `setup.md` | `setup.md` is created, `remove-meta-narrative` is called, and no sentence about the document itself remains |

That no Japanese is mixed in is checked with a regular expression of kana and kanji.

By default it runs two ways, with the plugin installed and without, and compares them. To check quickly with only one way, add `--runs 1 --ablation none`. Results go to `evals/results/` (not registered in git).

## Raising the version and publishing

1. Write a section for the new version in `CHANGELOG.md` (and in `CHANGELOG.ja.md`). A change that alters the agent's behavior raises the minor version; a change only to the README or checks raises the patch version.
2. Set `version` in `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` to the same value.
3. Pass `dev/test` and `claude plugin validate .`.
4. Commit, tag the commit in the form `v0.3.0`, and push. Create a release with the same tag on GitHub, and put the new version's section of `CHANGELOG.md` in its body.

People who have it installed run `/plugin marketplace update wakariyasu` and then `/plugin update wakariyasu@wakariyasu` to switch to the new version. Claude Code copies a plugin for each version and loads from that copy, so a changed body is not loaded unless the version is raised.
