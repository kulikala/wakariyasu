---
name: writing-rules
description: Holds the rules of the wakariyasu plugin (how to write replies to the user, how to write documents, and how to polish text before handing it over), the references the rules point to (how to write decision questions, instructions for agents, READMEs, and changelogs), and the language packs with what applies only when writing in a given language. Use it when you write a reply to the user or a document and the text of the rules is not in the conversation. Read the rules and references that apply to what you write. Other wakariyasu skills also open the rule, reference, and language pack files from this skill's folder. It also applies when the user says the same thing in another language.
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

Before you write a reply or a document in a language, read every file in that language's folder, unless the text of the file is already in the conversation. If the folder does not exist, only the rules apply.

Every file in a pack has one of the names in the table below. A pack holds only the files that language needs. When a file is missing, nothing is added for that language: skip the step that would use it, and use the English names given in the rules and skills.

| File | Holds |
|---|---|
| `polishing.md` | Checks to add when polishing text in that language, including phrases to avoid and any external reviewer skill |
| `styles.md` | How to choose register, notation, and formatting for each kind of text |
| `conventions.md` | Names readers expect in that language: README section names, changelog subheading names, fixed labels such as session-status headings, task-state words, and the column names of decision questions |
| `skills.md` | Additions for each skill, one section per skill name |

A pack may point to tools in other skills. The Japanese pack uses the `check-terms` skill.

## How to tell whether the files are already loaded

In Claude Code with the wakariyasu plugin installed, the text of the rules and of `asking.md` is loaded into the conversation at the start of the session, together with a list of the available language packs and their paths. The files of a language pack are not loaded at the start.

Every file starts with a heading on its first line. If the conversation contains that heading and the text of a file you need, you do not need to read the file again. If the text is not in the conversation (an environment where the plugin is not installed, or an agent other than Claude Code), read the file from the skill's folder before you write.
