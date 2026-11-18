---
name: session-status
description: Use when the user asks about the current state of the session, such as "What's the status?", "What are you doing now?", "How far along are you?" or "What's left?", and when the user says the same thing in another language. Also use without being asked when reporting at a break in work that spans several tasks, when stopping to ask the user to decide, and when giving progress during long work. Report the session's situation as the current goal, the latest instruction, a task list with states, and the latest status. Add numbered decision questions if the user has something to decide. Keep it to the key points, but give enough background and intent to understand them. The report can also be shown as an HTML page on which the user chooses options for the decisions and copies the answers to paste back.
---

# Purpose

Write the answer so that the user, after reading it, knows what they are aiming for, how far the work has progressed, and what they need to decide, if anything. Check the situation against things that can be verified, such as files, command output and task states. Write the answer to match the facts now.

## How to write

Follow rule `writing-to-user.md` ("Write replies that someone who has not followed the session can understand") in the `writing-rules` skill.

## Structure of the reply

Write the sections in this order. Omit a section, including its heading, if there is nothing to put in it.

```markdown
## Current goal

<What the session as a whole is doing, and why>

## Latest instruction

<What you are working on for the last request: what, and why>

## Tasks

| # | Task | State | Background and notes |
|---|---|---|---|
| 1 | … | … | … |

## Latest status

<Where things stand now: what just finished, what is running, and what comes next>
```

If the user has something to decide, add a "## Decisions needed" section at the end. Write it in the form given in `asking.md` ("How to write a decision question") in the `writing-rules` skill. Decide what to ask by following the "Ask only what the user must decide, in a form they can answer without the history" section of `writing-to-user.md`.
Put what you chose and went ahead with in "Latest status", or in the background and notes of "Tasks". Do not put it in "Decisions needed".
If the request is finished, say so in "Latest status" and stop. Write points of caution that the results of the work brought to light as sentences, not as questions.

If there is only one thing to decide and nothing else to report, such as task progress, the reply may consist of the "Decisions needed" section alone.

The headings, column names, and state words in the template above and in the state table below are the English labels. Use them as written in a reply in English. In a reply in another language, use the names that the `conventions.md` of that language's pack defines. If that pack has no `conventions.md`, write the labels in the reply's language. Language packs are in `skills/writing-rules/lang/<code>/` (the `lang/` folder of the `writing-rules` skill).

## Notation of the task state

Write the state column as an emoji plus a state word. The seven states below are fixed. When one applies, use its emoji with its state word. In an English reply, use the exact pair from the table. The emoji are the same in every language. In a reply in another language, write the state word as described above.

| State column | When to use |
|---|---|
| ✅ Done | Finished, and the result is verified |
| 🚧 In progress | You are working on it now |
| ⏳ Waiting on a process | You are waiting for something that has left your hands to finish, such as a background process, a subagent or CI |
| 🙋 Waiting for your decision | You cannot proceed until the user decides. Add the number of the question in "Decisions needed", for example 🙋 Waiting for your decision (1) |
| 📝 Not started | The work is decided but not begun |
| ❗ Problem | It failed, or the result differs from what was expected and work has stopped. Write what happened in the background and notes |
| ⛔ Cancelled | It was decided not to do it. Write who decided in the background and notes |

If the user has asked you not to use emoji, write only the state word.

For a state that fits none of the seven, you may make a new pair of an emoji and a word that expresses the state. Do not use the seven emoji for any other meaning.

The emoji in the state column carry meaning, so keep them when polishing.

## Showing the report as a page

The report can also be shown as an HTML page, on which the user chooses options and writes messages for the decisions, then copies the answers to paste into the session. Make the page when the user asks to see the status as a page, or when the user's instructions say that what they look at should be shown as an artifact or a page. Make it only where you can publish a page or hand over an HTML file. The page shows the same report as the reply, so the same rules and the same polishing apply to its text. Before making the page, read `references/status-page.md`, which describes the steps, how to describe the report for the page, and what the reply that hands the page over contains.

## Check before sending

Polish the report following rule `polishing.md` ("Polish what you wrote before handing it over") in the `writing-rules` skill. Do not run an external reviewer skill on the report. Keep the table structure.
