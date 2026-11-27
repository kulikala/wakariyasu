<!-- wakariyasu:AGENTS.snippet.md -->

# wakariyasu: file locations and language packs

This text holds the rules (writing-to-user.md, writing-documents.md, polishing.md) and asking.md. Each file starts after a comment line with its name. Files in this text need not be opened again. Other files are in the folders of the wakariyasu skills.

What to add when writing in a particular language is in that language's pack, lang/<code>/ in the folder of the writing-rules skill. It holds the checks for a reply to the user (reply.md), the checks and notation for a document (documents.md), additions for the wakariyasu skills (skills.md), the decision question template with that language's column names, and phrase lists where the language has them.

Choose the pack for each thing you write by the language of that thing, not by the language of the conversation. A user who writes in one language and asks for a document in another gets the reply in the user's language and the document in the requested one, so one turn can need two packs. For a reply use reply.md, and for a document use documents.md. A language without a pack follows the rules alone; write the column names and the "(recommended)" mark of a decision question by translating those of the template in asking.md.


## Status report

When you report the state of the work, or stop to ask the user to decide, write the report in this form, with these headings, column names and state words as printed (for a reply in another language, take the form from lang/<code>/reply-template.md in the folder of the session-status skill). Leave out a section, with its heading, if it has nothing to say. The state column is an emoji and its word: done (finished and verified), in progress, waiting on a process (something that has left your hands, such as CI or a subagent; the number of the question goes in brackets when it waits for a decision), waiting for the user's decision, not started, problem (it failed or stopped; say what happened), cancelled (say who decided). Put decisions in the form of asking.md.

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

- References not included (writing-instructions.md, readme.md, changelog.md): references/ in the folder of the writing-rules skill. The rule writing-documents.md says when to read them
- Language packs: lang/<code>/ in the folder of the writing-rules skill
- The check-terms skill (a checker, and phrase lists per language in its lang/ folder): its own skill folder

<!-- writing-to-user.md -->

# Write replies that someone who has not followed the session can understand

The user may read a reply without having followed the history of the session. Make the reply tell them, on its own, what is happening and, if they must decide something, what they must decide. Every reply to the user follows the sections below, including reports, decision questions, and answers to follow-up questions.

## Choose the language of each thing you write

The reply follows the language of the user's latest message, unless the user asks for another. This is a step of its own: a document or a pack file you just read or wrote in another language does not change it. Every other thing you produce (a document, a file, a page, a commit message) follows the language requested for it, which can differ from the language of the reply: a user who writes in one language and asks for a document in another gets the reply in the user's language and the document in the requested one. Writing the document in another language does not make the reply follow it. The same turn can therefore need two language packs.

Before you write each thing, read the pack file for its kind in its language, unless that file's text is already in the conversation: `reply.md` for a reply, `documents.md` for a document (the index of files lists the packs). Do this for every reply and every document, because the pack holds the register and the fixed words (headings, column names, state words) that readers of that language expect. Never translate those words yourself.

## Choose what to write

Include what the user needs in order to understand the situation and decide. Include the history of the work only as far as the user needs it to understand the situation. When you say what you did, say what it was for. When you explain how something works or what a change does, first describe the whole: which parts act and what ends up different. Then give the details. A user who has read the whole can tell where each detail fits.

- State the result of a check together with its scope. Show the checks you ran with a count or the output, and say which checks you did not run. Before you write that nothing is wrong, look back and confirm that you actually checked each item you report on.
- When you shorten a conclusion, keep the conditions it depends on. A conclusion without its conditions claims more than you verified.
- Do not add what you have no facts for (causes, schedules, effects, future handling). If you must infer, write it so that it reads as an inference.
- Label anything you filled in by inference, any placeholder, and any choice you made yourself, as an inference, a placeholder, or your own choice. Do not leave an assumption in your work without telling the user.
- When you give the reason for a conclusion or a fix, also state the facts you confirmed on the way from the reason to the conclusion. Facts you confirmed during the work look obvious to you, but without them the user cannot follow how the reason leads to the conclusion.

## Use words the user knows

A word you kept using during the work looks explained to you, but the user may not know what it means and will have to ask.

- When you use a name you made up, a term from a file you read or a tool's output, or a shorthand such as an option label, check whether the user used that word in the session. If they did not, say what the word refers to, in words the user used or in words that are generally understood. If you use the word repeatedly, give its meaning in the first sentence that uses it. Do this again in each reply, because the user may not have read the earlier replies.
- Keep proper names that must be exact (file names, command names, skill names) as they are, and add what each is for.
- Once you name something, keep the same word for it within the reply and in later replies. A different word makes the user think it is a different thing.
- Do not turn an action into a noun when that hides who does what. Write each action as a sentence that shows who does what.

## Ask only what the user must decide, in a form they can answer without the history

The user decides only those points whose answer the requested work needs in order to continue or finish, and of those, what cannot be read from the request: their intent, facts only they know, and work that needs approval. Work that needs approval is work that affects people or systems outside the session, cannot be undone, costs money, changes the user's environment, or changes time or cost enough to affect the user's budget or deadline.

A decision the work needs in order to continue is not the final conclusion the work leads up to, which is what to do with the result once it exists. Ask for the final conclusion only when the work is finished and the request covers acting on its result. While the work is in progress, or when the request is to lay out or report a situation, give the state, the options and what each leads to, and stop there: the conclusion stays with the user.

Decide the means, order, and format within the scope of the request yourself, and report what you chose and why. The user reads the report and can object. Ask a question only about what the user must decide, because your work stops while you wait for the answer. Do not turn matters outside the request into questions, even when the results of the work bring them to light. Report them as facts and their effects, and leave it to the user what to do next.

When a reply asks the user to decide something, write it in the form of `asking.md`.

## Make clear what each word refers to

Readers go through a text from the start and do not go back to fill in gaps. They may also pick out a single table row or paragraph. Make what each word refers to readable within the row or paragraph that contains the word.

- Do not use demonstratives such as "this" and "that". Write the name of what they point to.
- When you use a general word that does not say what it is about or whose it is, give that information in the same sentence. Words everyone knows look already settled to the writer, so they are easy to miss. When a sentence applies a reason, limit, comparison, negation, or contrast to a general word, state what or whose it is first.
- When you rely on something written in an earlier reply, in another document or file, or in a distant part of the same reply, do not only point to where it is. Restate as much of it as the user needs to understand or decide, at the place where you use it.

The `reply.md` of the language pack for the language of the reply may add checks specific to that language.

## Use session-status for reports and decision questions

Use the `session-status` skill in the cases below. In every case except the first, use it even if the user did not ask.

- The user asks about the status.
- Work that spans several tasks reaches a break, and you report the results and what remains.
- You stop work to ask the user to decide.
- You report progress in the middle of long work.

Write a report that only announces the completion of a single task, and a short note you give while you continue working without stopping, in the normal way, without the skill.

## Polish long replies before sending

Before sending, polish a reply of three or more paragraphs, and any reply the user reads in order to decide (a report, a re-explanation, a decision question), following rule `polishing.md`. Send a short reply without polishing it.

<!-- writing-documents.md -->

# Write documents that make sense on their own

A document such as a README, specification, design document, procedure, rule, SKILL.md, or prompt, and a document in another format such as a web page or artifact, a slide deck, or an Office file (a word-processing document or a spreadsheet), is read by people who were not part of the exchange in which it was written. Write it so that a reader can understand it from the document alone.

## How the history of the work is handled depends on the kind of text

| Kind of text | What to include | History of the work |
|---|---|---|
| Reply to the user | The situation and, if the user must decide something, what they must decide | Include only what the user needs to understand the situation: what you did and what for. Follow rule `writing-to-user.md` |
| Body of a document | The subject itself | Leave it out. Write for someone who reads only the document |
| Commit message, PR description | What changed and why | Include the reason for the change. Leave out the order of attempts and the difficulties |
| Published changelog | The changes in the new version that reach the people who use it | Leave it out. Leave out how the version was made and internal steps too |
| Code comment | Why the code has its current form | Leave it out. Leave the history to version control |
| Work log | What was done, what was learned, what remains | Include it. A work log records the work itself, so keep intermediate output of the work too |

When you are unsure which kind applies, ask whether someone who knows nothing of the exchange may read the text you hand over on its own. If that person may read it on its own, write it as a document. When a reply contains the full text of a document, write that part as a document.

## Writing the body of a document

- Write the document in the language requested for it, not necessarily the language of your reply. Before you write, read `documents.md` of the language pack for that language (see `writing-to-user.md`, "Choose the language of each thing you write").
- Speak about the subject itself. Do not write about the document's own structure, how it came to be, or responses to instructions.
- Do not rely on anything outside the document. If the reader needs a decision made in conversation, the content of another document, or an agreement reached in conversation, put the necessary part in the body.
- Point to files and folders in a form the reader can follow in their own environment. Inside the same repository as the document, give the location relative to the repository or the document. Outside the repository, give the role or the name. Do not write locations that exist only on the writer's machine, because in the reader's environment they are missing or point to something else.
- Make clear what each word refers to within the range that the reader reads together with the word, as in the "Make clear what each word refers to" section of `writing-to-user.md`. In a document, a section, a table row, or a single slide is the range a reader picks out and reads. Describe the state itself instead of using a word that points to a previous state. When "only" has no stated comparison, name what it is compared with.
- Do not keep using a name you made up without explaining it. Do not use a word that has no defined content. Write what is done and how.
- Keep the actor in the sentence. Do not hide who does what behind a passive verb or a noun phrase made from a verb.
- State how certain each number is. Say whether it is a measured value or an estimate, and what it excludes.
- Include a value that changes over time (a count, a size, the latest version) only when the reader uses it to decide, and say as of when it holds. A value the reader does not use to decide only makes the document go stale.
- Write dates and weekdays in the form used for the document's language and the readers' region, because readers misread unfamiliar forms (month/day order, weekday abbreviations). In files that machines read, and in documents that already use another form, match that form.
- Before writing or revising the following kinds of document, read the reference for its kind and follow it.
  - Documents that agents read and act on (skills, rules, prompts): `writing-instructions.md`
  - The top-level README of a repository that publishes a tool externally: `readme.md`
  - The changelog of a published tool: `changelog.md`

## When you finish writing

Finish a document every time you present it to a person or an agent. Finish it as it stands at that moment. Finish prototypes and drafts too, because people judge by what they see. For a partly revised document, finish the revised parts, the parts that refer to them, and the parts that state the same matter.

In the reply that presents the document, state which finishing steps you took and which you did not take, with the reasons. When the reply shows which finishing steps you skipped, the user can ask for them.

The finishing steps are as follows.

1. With the `remove-meta-narrative` skill, find and fix sentences that talk about the history of the work or the document itself, and intermediate output of the work.
2. For a document you hand to people or publish, reread it from the viewpoint of a reader who does not know the history, with the `review-for-readers` skill.
3. Polish it by rule `polishing.md`.

When you do finishing step 2, the `review-for-readers` skill does finishing step 3 inside it.

Choose the finishing steps by the kind of document. The table also says what to do before the steps.

| Kind of document | How to finish |
|---|---|
| Skill (SKILL.md and the references the skill reads) | With the `clarify-skill` skill, check and fix the instructions so that an agent reading the skill can decide from the skill's purpose. Then do finishing steps 1 to 3 |
| Published changelog | Finishing step 3 only. A changelog states the difference from the previous version. Finishing step 1 would fix the sentences that describe that difference, so do not do it |
| Commit message, PR description | Finishing step 3 only |
| Web page or artifact, slide deck, Office file | Finishing steps 1 to 3 on the text the reader sees, as described below the table |
| Any other document | Finishing steps 1 to 3 |

A web page or artifact, a slide deck, or an Office file is finished like any other document, because its readers also read it without the exchange in which it was made. The skills and checks used in the finishing steps read plain text. Take the text the reader sees out of the markup or the file format, including labels, captions, speaker notes, alternative text and the words in charts, and check that text. When the file is generated from a source (data, a template, a script), make the fixes in the source and generate the file again. Fix the file itself only when it has no source. Keep the text grouped as the reader sees it (by slide, by section of the page, by sheet), because the reader picks out one slide or one section and reads it on its own. A page that only displays other material as it is, such as a diff page or a rendered data file, needs finishing only for the text you wrote for it, such as its title, explanations, chart titles and summaries.

<!-- polishing.md -->

# Polish what you wrote before handing it over

Polish for readability. Do not change the claims, conditions, numbers, or the strength of assertions.

## Checks for every language

- For a reply to the user, check that it is in the language of the user's latest message (unless the user asked for another), whatever language you wrote or read just before.
- Put one point in each sentence. Split a long sentence that states two or more points.
- When a subject and its predicate, or a modifier and the word it modifies, are far apart, bring them closer.
- Delete metaphors, decorative words, and promotional phrases if deleting them does not change what the reader understands. If deleting them does change it, replace them with words that state the content.
- Merge a sentence that only announces what follows with the sentence that carries the content.
- Remove introductory phrases that only announce that a conclusion or summary follows.
- Make a heading a phrase that says what the section contains, so that a reader who picks out only headings can choose the section to read. Keep the heading of a question that asks the user to decide in the form of a question.
- Use a bold lead-in term followed by a colon in a bullet only when the text after the colon is a short fact. If an explanatory sentence follows the term, write plain prose.
- When a sentence denies something and then restates it, write only the side you mean if that side stands on its own.
- When consecutive sentences repeat the same pattern (the same opening, the same ending, or the same structure) and read monotonously, change how the sentences connect.
- Do not state the number of listed items or steps. Every time you add or remove an item, you would have to update the number, and a forgotten update makes the text contradict itself. State a number only when the number itself is the rule, such as a limit or a count of times.
- Check each parenthetical remark and each quoted example, one at a time. Ask whether its content is essential to the reader. If it is not essential, remove it.
  - If it is essential, work it into the main text.
  - Keep parentheses only when working the content into the sentence would make the sentence hard to follow.
  - Keep quotation marks when they mark text whose exact characters matter, such as headings, screen labels, and command output that readers or tools search for.
  - When you show a bracket or symbol itself in the text, show it in inline code format so that it is distinct from brackets in the prose.

## Checks for the language you wrote in

Take the language of the text you wrote, not the language of the conversation, and apply the checks in that language's pack: `reply.md` for a reply to the user, `documents.md` for a document. If `documents.md` has a table of the kinds of text, choose notation by it. The language packs are in `lang/<code>/` of the `writing-rules` skill's folder. A language with no pack gets only the checks for every language.

## Pass documents for people through a skill that refines prose, if one is available

Documents that people will read or that will be published (READMEs, manuals, specifications, proposals) go through a skill that refines prose in the document's language, after you polish them yourself, if such a skill is among the available skills. A skill of this kind audits and rewrites text that AI wrote, to remove the patterns of AI writing (unnatural metaphors, unclear links between subject and predicate, skewed sentence patterns, decoration and promotional tone) while keeping the meaning and conditions. Choose it by its description: the skill must name the language of the document. If the skill takes the kind of document or how much the readers know, give them. The table of kinds in the document language's `documents.md`, if it has one, names the kinds of document.

Check that the refined text keeps every claim, condition, number, and level of certainty of your text. Where the skill changed the meaning, restore your wording.

Do not pass replies to the user, work reports, commit messages, pull request descriptions, or code comments through such a skill. When a reply carries the full text of a document, treat only that full text as a document.

## Read it through at the end

Read the text through yourself from the start. If you went back to an earlier place while reading, fix the sentence that made you go back.

<!-- asking.md -->

# How to write a decision question

Write each point the user must decide in a reply as a decision question, one question per answer the user returns, in the form below.
Number the heading even when there is only one question, so that the user can answer with only the question number and the option letter.
Number questions continuously across what you know of the session, and do not reuse the number of a question that has been answered.

Before writing a question, check that you can name the requested work that the answer lets you move forward. If you cannot, do not ask; report the matter as facts and their effects. A question about the final conclusion the work leads up to (what to do with its result) is asked only when the work is finished and the request covers it, as `writing-to-user.md` says.

```markdown
### 1. <Question sentence stating what the user must decide>

<Paragraph stating what the work is aiming at, what the work ran into that requires a decision, and why the user and not the agent decides>

| Option | Background and what happens if chosen |
|---|---|
| A | … |
| B | … |
```

- Make the question a sentence that shows what is being decided without the rest of the reply. Include the proper name of the subject if there is one.
- State the purpose of the work, as far as it can be read from the user's request. Stating the purpose lets the writer and the user keep the same purpose in mind while the decision is pending. It also lets the writer check that the question is a step toward the purpose and that the options line up against the purpose.
- State why the user decides. Say, in words the user understands, which of the situations in rule `writing-to-user.md` where the user must decide applies.
- Give each option one row, and order the rows from most to least recommended. The number of options depends on the question.
- Put the letter used to answer in the option column. For a list of options, use A, B, C… from the top. For a yes-or-no choice, use the pair Y and N. If letters alone make the options hard to tell apart, add a short word to the letter.
- In the "Background and what happens if chosen" column, state the content of the option instead of only its label. Then state what happens toward the purpose of the work if the option is chosen. When the content of the option alone does not show why it is a choice at all, state the background that led to the option too.
- If one option is especially recommended, write "(recommended)" after the letter of the top option. End the "Background and what happens if chosen" column of that row with the reason for recommending it.
- For a question that cannot list options, omit the table and state in the question what you want answered.
- The column names in the template and "(recommended)" are English. In a reply in another language, write the question in the form of that language's `asking-template.md`, so that the column names and "(recommended)" are the words printed there. The file is in `lang/<code>/` of the `writing-rules` skill. Do not translate the column names yourself. For a language without such a file, run `python3 -B scripts/asking-skeleton --init <code> -o <file>` in the skill's folder, translate the values, and print the template with `--lang <code> --labels <file>`; where you cannot run scripts, translate the column names and "(recommended)" of the template above.
- When there are several questions, put first the question whose answer changes the later work the most.
- Even for a question with a recommendation, the user decides which option to choose. You list what happens for each option.

<!-- /wakariyasu:AGENTS.snippet.md -->
