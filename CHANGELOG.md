# Changelog

English | [日本語](CHANGELOG.ja.md)

Version numbers follow [Semantic Versioning](https://semver.org/).
A change to how the rules or skills are written that changes the agent's behavior raises the minor version.

## [0.12.0] - 2026-11-25

### Added

- Added the skill `compose-page`. It builds a page for people to read (a report, proposal, comparison and the like) starting from what the reader wants to know. Unless the environment or the project fixes the page's code, it starts from a single-HTML-file template that uses Vue 3, Tailwind CSS v4 and Lucide (`@lucide/vue`); the template leaves the icons and colors to the agent. The page has both a light and a dark display and follows the display setting of the reader's device.
- Added the skill `extract-insights`. From text such as meeting records and documents, it extracts insights, one at a time, that other people can use. Each insight is written as one sentence plus its kind, background, supplement, certainty and source.
- In the `session-status` page, http and https URLs in the text become links that open in a new tab.
- Added 「包み」 (a translation of "wrapper") and 「札」 (meaning a tag or label) to the list of phrases Japanese does not use.
- Language-specific additions can now be placed in `skills/writing-rules/lang/<language>/`. The agent chooses a pack for each thing it writes by the language of that thing, not by the language of the conversation, so a Japanese reply and an English README in one turn use the Japanese pack for the reply and the English pack for the README. Each pack has `reply.md` (replies), `documents.md` (documents) and `skills.md` (additions for skills), and the agent reads only the file for the kind of text it writes. No setting for switching languages is needed. Folders for Japanese (`ja`) and English (`en`) exist.
- Headings, column names, state words and the words of the pages are filled in by tools, not looked up by the agent. Each language folder holds them in `labels.json` (`skills/writing-rules/lang/<language>/` for decision questions, `skills/session-status/lang/<language>/` and `skills/show-changes/lang/<language>/` for the pages). `dev/build` prints the decision question template (`asking-template.md`) and the status report skeleton (`reply-template.md`) from them, and the agent writes into the template of the language of the reply. For a language without a folder, `build.py --init <code> -o <file>` (and `asking-skeleton --init`, `skeleton.py --init`) writes the English words to translate, and `--labels <file>` passes the translation to `build.py` and to the scripts that print the templates. The tools stop with a one-line message when a key is missing or unknown, or when a word in braces was dropped.
- In any language, before handing over a document for people, the agent passes it through a skill that refines prose in that language, if one is among the available skills. The rules no longer name a particular skill; the agent chooses one by its description.
- The `session-status` report can now also be a single HTML page (an artifact). On the page, the user can pick options for the points that need a decision, write a message, and copy all the answers to paste into the session. The page is made when the user says they want to see it as a page, or when instructions ask for an artifact or a page.

### Changed

- The agent asks the user for a decision only when the answer is needed to continue or finish the requested work. Matters outside the request are reported as facts and their impact, not asked as questions, even if the work's results revealed them. If the request is finished, `session-status` says it is finished and stops.
- When a reply to the user explains a mechanism or a change, it states the whole first, and also states the facts confirmed between the reasons and the conclusion. The meaning of a name the agent coined is added again in each reply, and the content of an earlier reply or another file is written out where it is used rather than only pointed to.
- Web pages, artifacts, slides and Office documents are now included in what gets finished before handover. The agent extracts the text a reader will see and finishes it.
- Skill descriptions are now in English only. A request in Japanese still invokes the skill as a request of the same meaning.
- The bodies of the rules and skills are now in English. The notation choices, phrasing checks and what to give a prose-refining skill when writing in Japanese moved to the Japanese folder.
- The rules are loaded by five SessionStart hook commands (one per rule file, `asking.md`, and the index), because Claude Code shows a hook command's output inline only up to 10,000 characters. `dev/test` fails if a command's output passes 9,500 characters.
- The rules say that the reply follows the language the user writes in unless asked otherwise, and that each document or file follows the language requested for it.
- What is loaded at the start of a session is now the rules, the way to write a question for a decision, and a short index: which language folders exist, how to choose one by the language of what is written, and where the filled templates are. The agent reads the file for the kind of text from the Japanese folder before writing Japanese.
- `AGENTS.snippet.md` now holds only the rules. Each language folder is in its own file, `AGENTS.snippet.<code>.md` (`AGENTS.snippet.ja.md` for Japanese), which holds the reply, document and skill additions, the decision question template with that language's words, and the phrase lists. People who pasted it replace the whole, and paste after it the file of each language the agent writes in; there can be more than one.
- README, CHANGELOG, the design documents and the plugin manifests are now in English. The Japanese README and changelog are `README.ja.md` and `CHANGELOG.ja.md`.
- The lists of phrases to avoid moved to `skills/check-terms/lang/<language>/`, one folder per language. `check-terms` takes `--lang <code>` to search one language; without it, it searches every language that has a list. Its notes are in English (`(check in context)`), and it stops with exit code 2 on an unknown option, a language without a list, or a file it cannot read.
- The `show-changes` page is in English by default. Given the language of the page being produced (`--lang <code>` for `show-changes`, `lang` in the report for `session-status`), both pages take their words from `lang/<code>/labels.json` of their skill; Japanese has them. The language of the page is not the language of the conversation.

## [0.11.0] - 2026-11-11

### Added

- When the agent writes a Japanese document, it chooses, from the document's purpose and reader, between standard notation, which leans toward neither native Japanese nor Sino-Japanese words, and Sino-Japanese notation, which centers on Sino-Japanese words as far as meaning and readability are not lost.
- Which notation to write in can be specified in CLAUDE.md.

## [0.10.0] - 2026-11-09

### Added

- Skills can now also be installed for agents such as Codex, Cursor and GitHub Copilot with `npx skills add` and `npx openskills install`. The steps are in the README's "[Installation](README.md#installation)" section.
- The dates and weekdays the agent writes take the form used in the document's language and the reader's region.
- Added 「入れ方」, 「入るもの」 and 「使うエージェント」 to the list of phrases Japanese does not use. In READMEs and the like, the agent uses a familiar term such as 「インストール方法」 (installation method) for explaining installation.
- On the `show-changes` page, hovering over a clickable element shows what pressing it will do.
- On the `show-changes` page, when the search field has text, it can be cleared with the ✕ button at the right end or the Esc key.

### Changed

- The CHANGELOG the agent writes becomes a guide to what changed for the people who use the software, not a work record. Entries are divided by kind of change (added, changed, fixed and so on).
- In the README the agent writes, the explanation of other tools used for installation is limited to the commands to run and the required options. Detailed usage of those tools is shown as a link to their own READMEs.
- In the list of phrases Japanese does not use, added 「推奨」 (recommended) as a candidate replacement for 「勧め」 (recommendation).
- `AGENTS.snippet.md`, pasted into the instruction file, became shorter. How to write READMEs, changelogs and instructions is now read from the skill `writing-rules` when needed, and descriptions that repeated the same thing within the rules were merged. People who pasted it replace it with the whole of the new `AGENTS.snippet.md` when updating.
- When the agent polishes writing, it checks each parenthetical supplement and each example in quotation brackets, removes it if unneeded, and if needed works it into the main text. The brackets and symbols themselves are shown in code format.
- In the documents and instructions the agent writes, there are fewer enumerated item counts, values at points the reader will not use, and repeated instructions. The check by the skill `clarify-skill` also looks at item counts and repetition.
- The documents, insights and feedback documents made by the skill `summarize-session` no longer include the state at that moment or a work record. If a record is wanted, it is included on request as a separate section or as a quotation. Log documents still include the work record and the time the state is as of.
- The insights document made by the skill `summarize-session` no longer includes a list of the procedures checked and of what was not confirmed. Certainty is shown as confirmed insight or estimate.
- The skill `remove-meta-narrative` also checks record sections inside design documents and READMEs. Only documents whose purpose is to record work, such as work records, are not checked.
- On the `show-changes` page, if you scroll partway through a file and then press its heading to close it, you no longer lose sight of the next file's heading. The next heading that was on screen before closing stays in the same position, and a next heading that was off screen comes to the top of the screen.
- On the `show-changes` page, the color of a selected button when the mouse hovers over it differs from the color of an unselected button. Right after pressing, you can tell that it was selected.
- On the `show-changes` page, the filter button does not appear when there is no file that would disappear by filtering, and the range switch does not appear when the page does not contain full text. The whitespace switch is named 「空白」 (whitespace).
- On the `show-changes` page, dates in the commit list take the Japanese date form.

## [0.9.0] - 2026-11-06

- Fixed a defect in environments that use GNU sed and grep (many Linux systems) in which `check-terms` printed "Invalid collation character" and finished the check with the exclusion of some phrases not working. The cause is that GNU sed and grep in the C.UTF-8 locale do not accept range specifications of full-width digits and kanji. The regular expressions in the phrase list were rewritten without range specifications. This defect did not occur on macOS.
- Added the skill `summarize-session`. It turns what the session examined, found, was told and did into a document that people or agents who were not in the session can read and use later. It infers from the request what the user wants and builds the document with the policy of the applicable mode among the following four. Document output raises the level of abstraction of what was examined and structures it as a document. Insight extraction composes understanding that holds in general. Feedback extraction organizes feedback into the point, the intent, the background and target, and the response policy. Log output keeps a work record. For a request that matches several modes, the documents are split by mode. For a request that matches none, the agent builds a structure using each mode's policy as a guide.
- In environments where Claude runs, the skill `show-changes` now presents the page it builds as an artifact (a page held on claude.ai that opens in a browser).
- Each time the agent hands or shows a document to a person or an agent, even a prototype or a draft, it now carries out the finishing steps (removing meta-narrative, reader review and polishing) and states in its reply which steps it carried out and which it did not.
- When the agent polishes writing itself, it now checks for missing subjects and objects by reading as if translating into English word by word. Words it supplies are written in natural Japanese and do not copy the words or word order of the translated English.
- Files and folders in a document are now shown in a form that can be referenced in the reader's environment (a relative location inside the repository, a role or name outside it), and locations that exist only on the writer's PC are not written.
- In instructions such as skills and rules, examples are no longer listed in parentheses or with "etc."; they are written as the conditions or properties that satisfy the item. How deliverables are written is also stated as a policy of what the reader should be able to take away, without fixing where to put what in a document or the order of items. A writing format is fixed only when the output format is clearly specified or when another person or tool reads that format. The skill `clarify-skill` also checks for example lists and for instructions that bind how a deliverable is written.
- A format the user specified is now kept in the record of constraints agreed with the user in the repository or project that holds the skill. The skill `clarify-skill` reads the record and does not flag constraints in it.
- When the agent polishes writing itself, it now checks whether a parenthetical supplement is really needed, and when it is, first considers whether the parentheses can be removed and the supplement worked into the sentence.
- Native Japanese words that are not in the phrase list are also checked for whether they can be replaced with Sino-Japanese words when they are used apart from their concrete everyday meaning.
- Added 「調べ」 (a noun meaning investigation, search or tally) to the list of phrases Japanese does not use. Added to the list of phrases to check in context: 「切る」 (with a noun as object, meaning to divide), 「渡すとき」, 「節」, 「材料」, 「届く」, 「広がり」, 「抜け」 (a noun meaning that something that should be there is missing), 「確かめる」 and 「当たる」 (meaning to apply). Added 「問い合わせる」, 「突き合わせる」 and 「実施する」 to the candidate words for 「当てる」.

## [0.8.0] - 2026-11-06

- Merged the rules and references into the new skill `writing-rules`, and the list of phrases Japanese does not use and the script `check-terms` that searches documents for them into the new skill `check-terms`. If you installed the skills with `gh skill install`, reinstall with `--all`.
- Added comments marking the pasted range to the first and last lines of `AGENTS.snippet.md`. When updating wakariyasu, replace what is between these two lines with the new whole.
- Added the skill `show-changes`. It shows the before-and-after diff, across repositories and folders, as one HTML page. When the agent finishes work that changes files, it makes and hands over the page without being asked. Whitespace differences are shown with symbols, and the display can be switched to treat lines that differ only in whitespace as unchanged lines. The file list can be narrowed to only added and changed files. Permission changes and symbolic links show the kind before and after. Building the page needs Python 3.9 or later; where it is missing, the agent says the page cannot be built.
- Added the skill `clarify-skill`. It checks a skill for whether an agent reading it can decide from the purpose, and plans how to fix it. On request it rewrites the skill. It is used without being asked after a skill is written.
- How the agent finishes a document after writing it is now chosen by the kind of document (skill, README, changelog, commit message and so on). A public changelog follows the reference "how to write a changelog" and states the changes that reach the people who use the software.
- Headings in documents the agent writes are now phrases that say what the section contains.
- Added 「確かめ」 (a noun meaning verification or confirmation) to the list of phrases Japanese does not use, and changed the replacement for 「直し」 (a noun meaning fix) to 「改修、修正、更新」. Added 「流す」, 「道具」, 「決めたこと」, 「例外は」, 「直す」, 「書く」 and 「決める」 to the list of phrases to check in context, and wrote 「直す」, 「書く」 and 「決める」 with Sino-Japanese words in the rule and skill bodies as well. Added 「選ぶ」 too, but since 「選ぶ」 is natural in many places, its replacement is only a reference.

## [0.7.0] - 2026-11-04

### Added

- Added to the list of phrases to check in context the words that liken machine processing to a person's actions or places (「拾う」, 「通る」, 「効く」, 「響く」, 「入口」, 「受け口」, 「渡し先」).

### Changed

- Made the heading of the section of the rule `writing-to-user` 「ユーザーに通じる用語と言い回しを選んで記述する」 (choose and write terms and phrasing that reach the user), and added that the word for the same object is not changed, and that an action is not folded into a noun in a way that erases who does what. Also added that conditions are not dropped when a conclusion is summarized briefly.
- In the rule `polishing`, metaphors, decorative words and promotional phrasing are removed if removing them does not change the reader's understanding.
- Added examples of questions for a decision and of documents to the README's "Before and after installing", and put what changes in the report example into a table.
- Added to the README a section, "Acknowledgments", that says yomiyasu was drawn on.

## [0.6.0] - 2026-11-04

### Added

- Added a list of phrases where another word may read more naturally depending on context (`references/terms-caution.tsv`). It contains 「当てる」, 「決まり」, 「落ちる」, 「引く」, 「順」, 「指す」, 「置き場所」, 「一般の文」, 「目」 and 「次の表」 with candidate words. The hook loads the list as a second table, and `check-terms` prints the places that match marked "(check in context)". They do not count toward the exit code. `--no-caution` turns the search off.
- Added a fifth group to the skill `remove-meta-narrative`, "work-in-progress output remains" (「〜は未達」, 「〜は不明であった」 and the like). Groups 3 to 5 are not applied to documents that record the work itself, such as work records and progress records. Also added a row for work records to the table in the rule `writing-documents`.

### Changed

- Added to the list of phrases Japanese does not use (`references/terms.tsv`): 「台」 (an environment for inspection or measurement), 「直し」 (a noun meaning fix), 「出す」 (to release software or a version), 「限り」 (a noun meaning what cannot be done, a limit) and 「回す」 (to run inspections or tests).
- In the rule `writing-to-user`, changed 「回した検査」 to 「実行した検査」 (the inspection that was run).
- In the rule `writing-to-user`, wrote that what the user decides is the intent that cannot be read from the request and the work that needs approval, that the agent decides and proceeds with the means, order and format within the scope of the request, and writes in the report what it chose. Also revised the opening sentence that could be read as assuming a reply always includes something to decide.
- Removed the "points that need a decision" section from the answer form of the skill `session-status` and made it a section added only when there is something for the user to decide. In `references/asking.md`, narrowed the examples of reasons the user decides, and wrote that if the recommended option does not change the request's purpose or constraints, the agent proceeds without asking.
- In the rules `writing-to-user` and `writing-documents`, wrote that demonstratives (words such as "this", "that", "here" in Japanese) are not used and the name of the object being pointed to is written. In `writing-documents`, wrote that words indicating a previous state, and 「だけ」, also state the object they point to.
- In the rule `polishing`, wrote that English phrases and names are not replaced word by word, and a Japanese expression that suits the context is chosen.
- Unified how rules and references are referred to into the form of the first-line heading plus the file name (the rule 「書いた文章は、渡す前に整える」 (`polishing.md`)). The guidance on which file to read when it is not loaded was unified into the same sentence.
- Removed demonstratives from the body of wakariyasu. Changed the heading of the rule `writing-documents` to 「エージェントが書く文書は、文書だけで通じるように書く」 (documents the agent writes are written to be understood from the document alone).
- In the body of wakariyasu, reworded phrases where another word reads more naturally depending on context (「当てる」 to 「適用する」, 「指す先」 to 「示す対象」 and 「参照先」, 「読み手の目で」 to 「読み手の視点で」 and so on). Changed the heading of the rule `writing-to-user` to 「語が示す対象を読み取れる書き方にする」 (write so that the object a word refers to can be read), and the heading of the skill `review-for-readers` to 「読み手の視点で読み直す」 (reread from the reader's viewpoint).
- In the rules, changed the guidance on which file to read when it is not loaded to the actual locations in `rules/` and `references/` of the plugin folder.
- Added an explanation of the hook to the rule `polishing`, and wrote, in the rule `polishing` and the skill `review-for-readers`, examples of the names of kinds of writing to pass to yomiyasu.
- Narrowed what the hook loads to the three rules, the notation table, the way to write a question for a decision, and the two phrase tables. How to write READMEs and instructions is pointed to at the end of the hook's output and read when writing the relevant document. The amount loaded went from about 11,100 characters to about 10,400 characters. The guidance in the rules on which file to read when it is not loaded was reduced to file names.
- In `references/asking.md`, moved the condition for proceeding with the recommended option to the top, and wrote that even for a question with a recommendation, it is the user who chooses the option.

## [0.5.2] - 2026-10-30

### Changed

- Moved the development scripts from `bin/` to `dev/` (`dev/build` and `dev/test`), because claude.ai and Cowork do not accept a plugin that has `bin/` at the top level. `dev/test` also checks that there is no `bin/` at the top level.
- Wrote in the README the steps for installing into the Claude apps (web, desktop, phone) and Cowork. Hooks are not loaded in chat, so to make the rules apply, paste them into "Instructions for Claude" in the settings or into the project's instructions.

## [0.5.1] - 2026-10-27

### Changed

- Made `scripts/check-terms` work in Linux UTF-8 locales as well (spellings such as `C.utf8`). Also changed the detection of 「要る〜」 so that it does not use the character-code range specification that Linux grep does not accept.

## [0.5.0] - 2026-10-27

### Added

- Added the reference "how to write a README" (`references/readme.md`). It is a policy for writing a Japanese README placed at the top level of a repository and published externally, with the section names, structure and wording familiar from Japanese READMEs that people maintain. It includes the purpose of each section, that each section holds only content that serves that section's purpose, and how to choose terms. It does not fix the order of sections.
- Made the rule `writing-documents` have the agent read this reference when writing or fixing a README that is placed at the top level of a repository and published externally.
- Added the list of phrases Japanese does not use (`references/terms.tsv`) and the script `scripts/check-terms` that searches documents for them. The list holds the phrase not to use, the word to use instead, and regular expressions for detection and exclusion. The hook loads the list as a table, and in "search for phrases Japanese does not use" in the rule `polishing`, `check-terms` is run before the document goes through yomiyasu.

### Changed

- In the reference "how to write a question for a decision", the paragraph of the question now states what the work is aiming for and what the work ran into that made a decision necessary. The columns of the table state what happens toward the work's purpose if chosen.
- Rephrased the phrases in the list (「問い」, 「要る〜」, 「版」 and so on) in the bodies of wakariyasu's rules, references and skills.

## [0.4.0] - 2026-10-25

### Changed

- Made the questions for a decision in the rule `writing-to-user` follow the reference "how to write a question for a decision" (`references/asking.md`). For each question, write a heading with a session-wide serial number, the reason the user decides, and a table of options in descending order of how strongly each is recommended. Option labels can be A, B, C... and, for two choices, Y and N.
- Removed from the rule `writing-to-user` the item that said to offer a candidate answer before asking, and to investigate rather than ask about what can be found out. When to ask is not fixed; only how to write a question is.
- Made the "points that need a decision" of the skill `session-status` take the same form as that reference.
- Made the rule `writing-documents` have the agent read the reference "how to write instructions for agents" (`references/writing-instructions.md`) when writing a skill, rule or prompt.

### Added

- The references `references/asking.md` and `references/writing-instructions.md`. They were also put into the hook, the copy in each skill, and `AGENTS.snippet.md`.

## [0.3.0] - 2026-10-23

### Changed

- Made the rule `polishing` 「書いた文章は、渡す前に整える」 (polish writing before handing it over), and split it into the items checked in any language and the items added when writing in Japanese (choice of notation, commas, yomiyasu).
- Changed how the rule `writing-to-user` checks what a word points to into how to write demonstratives in general, and separated the method of checking by translating literally into English as a procedure for Japanese sentences.
- `session-status` and `explain-clearly` are also used when asked something of the same meaning in another language. The headings and state words of `session-status` are written in the same language as the reply.
- Removed the English README and put an English description of the plugin at the top of the Japanese README.
- Also put the Japanese notation table (`references/styles.md`) into the hook and `AGENTS.snippet.md`.

### Added

- `.editorconfig`, `.gitattributes` and `.gitignore`.
- `bin/test`, which checks the repository's rules, and the GitHub Actions that run it.
- Cases for `claude plugin eval` that measure whether skills are called (`evals/`).
- The development guide (`docs/development.md`).

## [0.2.3] - 2026-10-22

### Changed

- Removed yomiyasu from wakariyasu's marketplace. yomiyasu is installed from its author's marketplace.

## [0.2.2] - 2026-10-22

### Changed

- Reduced the README's yomiyasu section to the fact that it is called if installed, and the guidance on how to install it.

## [0.2.1] - 2026-10-22

### Changed

- Wrote where yomiyasu is called, after the finishing steps in the rule `writing-documents` and after the reread in `review-for-readers`.

## [0.2.0] - 2026-10-22

### Changed

- Changed the polishing procedure to the order of polishing yourself first and running yomiyasu as well only for documents handed to people. yomiyasu is not called for replies to the user.
- Added to the items the agent checks itself: introductory phrases, commas that only create a pause, headings in question form, bulleted lists of bold text and a colon, sentences that negate and then restate, and consecutive identical sentence endings.

## [0.1.0] - 2026-10-21

### Added

- The rules `writing-to-user`, `writing-documents` and `polishing`, and the Japanese notation table.
- The skills `session-status`, `explain-clearly`, `remove-meta-narrative` and `review-for-readers`.
- A hook that loads the rules at the start of a session.
- `AGENTS.snippet.md`, to paste into agents other than Claude Code.

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
