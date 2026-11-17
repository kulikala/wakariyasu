---
name: review-for-readers
description: Reread a document that will be handed over, sent or published (README, specification, procedure, proposal, rule, SKILL.md and so on) from the viewpoint of a reader who does not know the history of how it was written, and fix the places where that reader gets stuck. Use when the user says things like "Review it with a reader's eyes", "Look at it before we publish" or "Check whether someone reading it for the first time can follow it", and when the user says the same thing in another language. Also use without being asked after finishing a document that will be handed over, before handing it over. Have a separate agent, given only the document and not the history, read it, fix the places it raises, and have it read the document again.
---

# Purpose

The writer of a document remembers the exchanges during the writing, so the writer can fill in what the document does not state.
Have a reader who does not know the history read only the document, and fix the places where that reader gets stuck.

## 1. Prepare the reader

Start a separate agent (a subagent) that has no history, and give it only these two things.

- The text of the document (a file path or the full text).
- The assumed reader in one line: what that reader knows and does not know about the subject of the document.

Do not give it the history of the work, the intent of the writing, or the places you fixed. If you do, the reader can fill in what the document leaves unsaid, as the writer can.
Ask the reader not to open any file other than the document you gave it, such as instruction files in the same repository.

If you cannot start a separate agent, reread the document yourself once from the start. Fix it using the points in "2. What to ask the reader". The writer remembers the earlier version, so rereading many times is never a substitute for a reader.
Reread only once, and state in your report that the writer reread the document instead of a separate reader.

## 2. What to ask the reader

Ask the reader to read the document from the start, in order, without going back. Then ask the reader to list the places that match the following, each with its location and the reason. Do not ask for suggested fixes.

- Words whose meaning is not settled: coined names, abbreviations without an explanation, abstract words with no definite content.
- Words whose referent is unclear: pronouns and demonstratives, and general words with no "of what" or "of whom".
- Sentences that need a premise the document does not state: matters decided in a conversation, the content of another document.
- Places the reader went back to reread, with the reason they went back.
- Questions the reader is left with after finishing and cannot answer: what the subject of the document can do, what the reader should do, and so on.

Then apply the language pack's `skills.md` section for review-for-readers, if any, to what you ask the reader. Language packs are in `skills/writing-rules/lang/<code>/` (the `lang/` folder of the `writing-rules` skill).

## 3. Fix and reread

Fix the places the reader raised. Follow rule `writing-documents.md` ("Write documents that make sense on their own") in the `writing-rules` skill.
If you find sentences about the history of the writing or about the document itself, fix them with the `remove-meta-narrative` skill. Finally, polish the document following rule `polishing.md` ("Polish what you wrote before handing it over") in the `writing-rules` skill.

After fixing, have a different reader, again one who does not know the history, read the document once more. The same reader remembers the earlier version.
Repeat until the reader raises nothing that hinders understanding. As a rough guide, expect two or three rounds.

When the reader no longer raises anything, apply the language pack's `skills.md` section for review-for-readers, if any, to the finished document.

## 4. What to report

- How many times you had the document read, and from which points the reader read it.
- The places the reader raised and how you fixed each. For a place you did not fix, the reason.
- What you have not verified (for example: a translation was not read, the actual procedure was not run).
