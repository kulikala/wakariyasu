<!-- wakariyasu:AGENTS.snippet.en.md -->

# wakariyasu: the language pack for en

Use this pack, together with the rules in AGENTS.snippet.md, for what you write in this language, whatever language the conversation is in: reply.md for a reply to the user, documents.md for a document, skills.md for a wakariyasu skill. Each file starts after a comment line with its name.

<!-- lang/en/reply.md -->

# Checks to add when replying in English

Read this when the user writes in English and you reply in English. If the user writes in another language, reply in that language and do not read this file. Apply these checks in addition to the "Checks for every language" section of `polishing.md`.

## Prefer plain words

Use the common word when it carries the same meaning as the formal one. Readers who use English as a second language, and readers outside the field, misread rare words and idioms. Keep a technical term when it is the name readers will search for, and give its meaning the first time it appears.

<!-- lang/en/documents.md -->

# Checks to add when writing a document in English

Read this when you write a document in English. It is about documents only and does not decide the language of your reply to the user: that follows the language the user writes in (rule `writing-to-user.md`). Apply these checks in addition to the "Checks for every language" section of `polishing.md`.

## Prefer plain words

Use the common word when it carries the same meaning as the formal one. Readers who use English as a second language, and readers outside the field, misread rare words and idioms. Keep a technical term when it is the name readers will search for, and give its meaning the first time it appears.

<!-- session-status/lang/en/reply-template.md -->

Write a status report in this language in this form, with these headings, column names and state words as printed (see "Status report" in AGENTS.snippet.md).

## Current goal

…

## Latest instruction

…

## Tasks

| # | Task | State | Background and notes |
|---|---|---|---|
| 1 | … | ✅ Done | … |
| 2 | … | 🚧 In progress | … |
| 3 | … | ⏳ Waiting on a process | … |
| 4 | … | 🙋 Waiting for your decision (1) | … |
| 5 | … | 📝 Not started | … |
| 6 | … | ❗ Problem | … |
| 7 | … | ⛔ Cancelled | … |

<!-- The emoji and state words stay as printed. For a language without a template, translate only the words. -->

## Latest status

…

## Decisions needed

### 1. …

…

| Option | Background and what happens if chosen |
|---|---|
| A (recommended) | … |
| B | … |

<!-- lang/en/asking-template.md -->

Write a decision question in this form in this language, with these column names and this mark as printed.

### 1. …

…

| Option | Background and what happens if chosen |
|---|---|
| A (recommended) | … |
| B | … |

<!-- /wakariyasu:AGENTS.snippet.en.md -->
