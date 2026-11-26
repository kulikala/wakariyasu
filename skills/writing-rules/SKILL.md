---
name: writing-rules
description: Holds the rules of the wakariyasu plugin (how to write replies to the user, how to write documents, and how to polish text before handing it over), the references the rules point to (how to write decision questions, instructions for agents, READMEs, and changelogs), and the language packs with what applies only when writing in a given language, chosen by the language of what you write. Use it when you write a reply to the user or a document and the text of the rules is not in the conversation. Read the rules and references that apply to what you write. Other wakariyasu skills also open the rule, reference, and language pack files from this skill's folder. It also applies when the user says the same thing in another language.
---

# Purpose of this skill

wakariyasu is a plugin that makes the replies and documents agents write understandable to people who did not follow the work: the user, and people and agents who read a document later. The rules, references, and language packs for that are in the folder that contains this SKILL.md (the "skill's folder" below).

## Rules

Follow the rules every time you write a reply or a document. They are in `rules/` of the skill's folder. Follow every rule that applies to what you write. A commit message is a document, so it follows `writing-documents.md` and `polishing.md`.

| File | When to follow it |
|---|---|
| `writing-to-user.md` | When you write a reply to the user (a report, a decision question, an answer to a question) |
| `writing-documents.md` | When you write a document other than a reply that people or agents read (a README, specification, SKILL.md, commit message, PR description, and so on) |
| `polishing.md` | When you polish a reply or document before you send it to the user or save it to a file to hand to people |

## References

Read a reference when a rule tells you to. They are in `references/` of the skill's folder.

| File | When to read it |
|---|---|
| `asking.md` | When you write a question that asks the user to decide |
| `writing-instructions.md` | When you write instructions that an agent reads, such as a skill, a rule, or a prompt |
| `readme.md` | When you write or revise the top-level README of a repository that publishes a tool externally. A README that is not published follows only `writing-documents.md` |
| `changelog.md` | When you write or revise the changelog of a published tool (CHANGELOG, release notes) |

## Language packs

A language pack holds what applies only when writing in one language. Packs are in `lang/<code>/` of the skill's folder, where `<code>` is the ISO 639-1 language code of the language.

Choose the pack for each thing you are about to write by the language of that thing, not by the language of the conversation. A user who writes in one language and asks for a document in another gets the reply in the user's language and the document in the requested one, so one turn can need two packs. For each thing, read only the pack file for its kind, unless the text of the file is already in the conversation. If the folder for the language does not exist, only the rules apply.

| File | Read it when you write | Holds |
|---|---|---|
| `reply.md` | A reply to the user | The register of replies and the checks to add when polishing a reply |
| `documents.md` | A document: a README, specification, SKILL.md, commit message, and so on | How to choose register and notation for each kind of text, the checks to add when polishing a document, and the names readers expect (README sections, changelog subheadings) |
| `skills.md` | Text for a wakariyasu skill | Additions for each skill, one section per skill name |

A pack holds only the files that language needs. When a file is missing, nothing is added for that language and kind of text. A pack may point to tools in other skills. The Japanese pack uses the `check-terms` skill.

The folder also holds files that tools read or print. Do not open them to look up words:

- `labels.json` holds the fixed words for tools (the column names of decision questions and "(recommended)").
- `asking-template.md` is the decision question template with those words filled in.

### Fixed words

Headings, column names and state words are filled in by tools. Do not translate them, and do not look them up in a table. For a decision question, take `lang/<code>/asking-template.md` for the language of the question, and use its words as printed. For a status report, the session-status skill gives its own filled template.

For a language that has no pack, run `scripts/asking-skeleton --init <code> -o <file>`. It writes the English words as a JSON file. Translate the values into the language, and keep the words in braces as they are. Then run `scripts/asking-skeleton --lang <code> --labels <file>`. It prints the template, and stops with a one-line message when a key is missing, a key is unknown, or a word in braces was dropped. Run the scripts with `python3 -B`.

## How to tell whether the files are already loaded

In Claude Code with the wakariyasu plugin installed, the text of the rules and of `asking.md` is loaded into the conversation at the start of the session, together with a list of the available language packs and their paths. The files of a language pack are not loaded at the start.

Every file starts with a heading on its first line. If the conversation contains that heading and the text of a file you need, you do not need to read the file again. If the text is not in the conversation (an environment where the plugin is not installed, or an agent other than Claude Code), read the file from the skill's folder before you write.
