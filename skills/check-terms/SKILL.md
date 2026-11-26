---
name: check-terms
description: Find phrases that writers of a language do not use (translationese, or words coined during the work) and phrases for which another word is often more natural, using per-language phrase lists, and replace them. Use when asked to check the wording of a document or to look for phrases to avoid, and, even if not asked, before handing over a document the agent wrote to a file in a language that has phrase lists. The wakariyasu rules, language packs and other skills also use the phrase lists and the checker from this skill's folder.
---

# Purpose

When a document keeps phrases that writers of its language do not use, readers misread it and trust it less. Find the listed phrases in a document, and replace the places that use a phrase in the sense the list describes.

Whether you may rewrite the document depends on who wrote it.

- If you wrote it yourself (including a user's document you rewrote as asked), find and replace the phrases before you hand it over.
- If you are asked to check a document written by the user, another person or another agent, do not rewrite it. Find the phrases with the steps below, and return a list of the places, the phrases and the words to use instead. Replace them only when asked to fix them.

## This skill's folder

The lists and scripts are in the folder that holds this SKILL.md (below, "this skill's folder"). If the location was given when the skill was invoked, use it. Otherwise look for `check-terms/SKILL.md` and use its folder.

## Phrase lists

Phrase lists are kept per language in `lang/<code>/` of this skill's folder, where `<code>` is the two-letter ISO 639-1 code of the language. Each language can have two lists. Both are tab-separated, one phrase per line.

- The first column is the phrase, followed by the sense in which it is to be replaced. Only places that use the phrase in that sense are to be replaced.
- The second column is what to use instead. The third and fourth columns are the regular expressions the script uses to find the phrase, so you need not read them.
- `terms.tsv` holds phrases to avoid. Always replace a phrase used in the listed sense.
- `terms-caution.tsv` holds phrases that are not wrong, but for which another word is often more natural. Its second column gives candidate words. Replace a phrase only when, in its context, a candidate word is clearer to the reader. When in doubt, keep the phrase.

When you write a document yourself, read the first two columns of the lists for its language before you write, and avoid the phrases from the start. The `documents.md` and `reply.md` of the language pack of the `writing-rules` skill (`lang/<code>/` of that skill's folder) may say more about using the lists for its language. In environments that load wakariyasu's language snippet for a language (AGENTS.snippet.<code>.md), the lists for that language appear there as tables. If those tables are in the conversation, you need not read the lists again. When you use this skill after writing, start from the steps below.

## Find and replace

Find the phrases with `scripts/check-terms` in this skill's folder. It runs with sh and standard commands only.

```sh
sh <this skill's folder>/scripts/check-terms --lang <code> <file>...
```

The script's options, output and exit code are as follows.

- `--lang <code>` uses only the lists of that language. Without it, the script uses the lists of every language that has them.
- The script prints each match on its own line, as `file:line: matched text -> second column`. It does not print the whole line or the sense from the first column, so open the line to judge the sense. A match from `terms-caution.tsv` ends with `(check in context)`.
- The script exits 1 if it finds any phrase from `terms.tsv`. It exits 0 when it finds nothing, and when it finds only phrases from `terms-caution.tsv`.
- It blanks out code blocks fenced with ```, and the text inside 「」 quotes. It replaces each inline code span with the word `CODE`, so a phrase written as inline code is not found, but a pattern can still match the span as a whole (for example, a command written as code followed by a listed verb). To mention a phrase itself, put it in 「」 quotes or inline code.
- With no file, or with `-`, it reads standard input. When asked to check text that is not in a file, such as a reply to the user, pass the text on standard input.
- `--no-caution` searches only the phrases in `terms.tsv`.

The script searches with regular expressions, so a match is not always used in the listed sense. For each match, check in context whether it is used in the sense given in the first column, and handle it as the "Phrase lists" section above says. If it is used in another sense, keep it.

The lists collect phrases that have been found. They do not hold every phrase that should be replaced. The `documents.md` of the language pack of the `writing-rules` skill may say how to check words that are not in the lists. Some uses cannot be found with regular expressions. If you notice a listed phrase while rereading the document, replace it when it is used in the listed sense, even if the script did not report it.

After replacing, run the script again. Keep the places you already checked and decided to keep (a phrase from `terms.tsv` used in another sense, and a phrase from `terms-caution.tsv` you decided not to replace), even if the script reports them again. Line numbers shift as you replace, so tell the reported places apart by the content of the line. Stop when the script reports nothing except the places you decided to keep. If you kept a phrase from `terms.tsv`, the exit code stays 1, so decide that you are done by the reported places, not by the exit code.

## When the script cannot run

In an environment that cannot run sh (for example, one without a tool to run commands), read the first two columns of the lists, read the document from the start, and look for places that use a listed phrase in the listed sense. Exit code 1 means a phrase was found, not that the script failed. When the script fails, it prints an error on standard error and exits 2, for example for an unknown option, a language without lists, or a file it cannot read.
