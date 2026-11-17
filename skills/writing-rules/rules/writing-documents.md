# Write documents that make sense on their own

A document such as a README, specification, design document, procedure, rule, SKILL.md, or prompt is read by people who were not part of the exchange in which it was written. Write it so that a reader can understand it from the document alone.

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
| Any other document | Finishing steps 1 to 3 |
