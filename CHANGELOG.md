# Changelog

English | [日本語](CHANGELOG.ja.md)

Version numbers follow [Semantic Versioning](https://semver.org/).
A change to how the rules or skills are written that changes the agent's behavior raises the minor version.

## [1.0.1] - 2026-11-28

### Added

- The `show-changes` page has an inline layout that reads like tracked changes in a word processor: the text after the change without diff marks, changed words colored, a narrow mark where text was removed, and the earlier text shown on hover.

### Changed

- `show-changes` and `session-status` pages are built from the same single-file page template as the pages of `compose-page`, with the same light and dark themes.
- With `--artifact`, both pages leave out the document skeleton that Claude artifacts add when publishing, so a published page no longer holds a document inside a document.
- `show-changes` builds pages with the utfpack packer (the part of utfpack that compresses the page data) downloaded from jsDelivr instead of a copy bundled with wakariyasu, and reuses the downloaded copy when the download fails. Building a page therefore needs a network connection the first time, and utfpack updates arrive without a wakariyasu update.

## [1.0.0] - 2026-11-27

### Added

- The skill `compose-page`, which builds a page for people to read (a report, a proposal, a comparison) starting from what the reader wants to know.
- The skill `extract-insights`, which turns meeting records and documents into insights others can use.
- The `session-status` report can also be an HTML page on which the user answers the questions and copies the answers back into the session.
- `show-changes` can show files in full, not only changes, for requests to show the whole of a skill or a document. Pages with full text can switch to the full text after the change, without the diff.
- On the `show-changes` page, Enter in the search field jumps to the next match and Shift+Enter to the previous one.
- Text selected on the `session-status` page, and on pages built from the `compose-page` template, can be copied with a button that appears next to the selected text.
- Language packs: each reply and document follows the conventions of its own language, chosen by the language of what is written. Japanese and English are included.

### Changed

- The agent asks for a decision only when the work cannot continue without it, and reports other findings as facts. It asks for the final conclusion, such as whether to publish or send, only when the work is finished and the request covers it.
- `show-changes` pages are about a third of their size in 0.11.0, because their data is compressed with utfpack. A page loads the decoder that unpacks its data from jsDelivr when it opens, so opening it needs a network connection; `build.py --embed-decoder` puts the decoder into the page instead.
- Replies that explain a mechanism or a change state the whole first.
- Instructions the agent writes, and the checks of `clarify-skill`, avoid sample data, sample output and quoted tool messages that the agent would copy.
- READMEs the agent writes fold details into collapsible blocks, use the Markdown GitHub renders, and write each language version for its own readers rather than translating it.
- Web pages, artifacts, slides and Office documents are finished before handover like other documents.
- The rules and skills are written in English. The README and the changelog are also in Japanese.
- The `show-changes` page is in English unless another language is requested for it.
- If you pasted `AGENTS.snippet.md`, replace it with the whole of the new one.

### Fixed

- In Claude Code, the rules loaded at the start of a session were cut short. They now reach the agent in full.

## [0.11.0] - 2026-11-11

### Added

- The agent chooses the notation of a document from its purpose and reader. The notation can be set in CLAUDE.md.

## [0.10.0] - 2026-11-09

### Added

- Skills can be installed for Codex, Cursor, GitHub Copilot and other agents with `npx skills add` and `npx openskills install` ([Installation](README.md#installation)).
- Dates take the form of the document's language and the reader's region.
- On the `show-changes` page, buttons explain what they do, and the search field can be cleared.

### Changed

- Changelogs the agent writes tell users what changed, not what was done.
- Documents and instructions the agent writes have fewer item counts, repetitions and unneeded asides.
- `summarize-session` leaves work records out of its documents unless asked.
- `AGENTS.snippet.md` is shorter. If you pasted it, replace it with the whole of the new one.
- The `show-changes` page keeps your place when a file is closed and hides controls that would do nothing.

## [0.9.0] - 2026-11-06

### Added

- The skill `summarize-session`, which turns a session into a document that people who were not there can use.

### Changed

- `show-changes` presents its page as an artifact where Claude runs.
- The agent finishes every document it hands over, drafts included, and says which finishing steps it took.
- Documents refer to files in a way the reader can find, not by paths on the writer's machine.
- Formats the user asked for are kept and respected by `clarify-skill`.

### Fixed

- `check-terms` failed on Linux with GNU sed and grep.

## [0.8.0] - 2026-11-06

### Added

- The skills `writing-rules` and `check-terms`, which hold the rules and the phrase lists. If you installed with `gh skill install`, reinstall with `--all`.
- The skill `show-changes`, which shows a diff across repositories and folders as one page.
- The skill `clarify-skill`, which checks a skill as instructions for an agent.

### Changed

- The agent finishes a document in the way that suits its kind (skill, README, changelog, commit message).
- `AGENTS.snippet.md` marks its pasted range, so that it can be replaced on update.

## [0.7.0] - 2026-11-04

### Changed

- Replies call the same thing by the same word and keep the conditions of a conclusion.
- Polishing removes metaphors and decoration that do not help the reader.

## [0.6.0] - 2026-11-04

### Added

- `check-terms` also marks phrases that may read better as another word, to check in context.
- `remove-meta-narrative` also finds leftover work-in-progress notes.

### Changed

- The agent asks the user only about intent and approvals, and decides the means itself.
- Documents name what they refer to instead of using words like "this" and "that".
- Less is loaded at the start of a session.

## [0.5.2] - 2026-10-30

### Changed

- The plugin can be installed in the Claude apps and Cowork. The README has the steps.

## [0.5.1] - 2026-10-27

### Fixed

- `check-terms` did not work in some Linux locales.

## [0.5.0] - 2026-10-27

### Added

- A guide for writing READMEs.
- A list of phrases to avoid, and `check-terms` to search documents for them.

### Changed

- A question for a decision states what the work aims for and what stopped it.

## [0.4.0] - 2026-10-25

### Added

- Questions for a decision take a fixed form: a numbered heading, the reason, and a table of options. `session-status` uses the same form.
- A guide for writing instructions for agents.

## [0.3.0] - 2026-10-23

### Changed

- Polishing is split into checks for every language and checks for each language.
- `session-status` and `explain-clearly` work in any language, and the report is in the language of the reply.

## [0.2.3] - 2026-10-22

### Changed

- yomiyasu is no longer in wakariyasu's marketplace. Install it from its author's.

## [0.2.2] - 2026-10-22

### Changed

- The README's yomiyasu section is shorter.

## [0.2.1] - 2026-10-22

### Changed

- The finishing steps say where yomiyasu is called.

## [0.2.0] - 2026-10-22

### Changed

- The agent polishes its own writing first, and calls yomiyasu only for documents handed to people.

## [0.1.0] - 2026-10-21

### Added

- The rules `writing-to-user`, `writing-documents` and `polishing`.
- The skills `session-status`, `explain-clearly`, `remove-meta-narrative` and `review-for-readers`.
- A hook that loads the rules at the start of a session, and `AGENTS.snippet.md` for other agents.

[1.0.1]: https://github.com/kulikala/wakariyasu/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/kulikala/wakariyasu/compare/v0.11.0...v1.0.0
[0.11.0]: https://github.com/kulikala/wakariyasu/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/kulikala/wakariyasu/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/kulikala/wakariyasu/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/kulikala/wakariyasu/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/kulikala/wakariyasu/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/kulikala/wakariyasu/compare/v0.5.2...v0.6.0
[0.5.2]: https://github.com/kulikala/wakariyasu/compare/v0.5.1...v0.5.2
[0.5.1]: https://github.com/kulikala/wakariyasu/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/kulikala/wakariyasu/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/kulikala/wakariyasu/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/kulikala/wakariyasu/compare/v0.2.3...v0.3.0
[0.2.3]: https://github.com/kulikala/wakariyasu/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/kulikala/wakariyasu/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/kulikala/wakariyasu/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/kulikala/wakariyasu/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/kulikala/wakariyasu/releases/tag/v0.1.0
