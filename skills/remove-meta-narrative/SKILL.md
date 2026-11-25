---
name: remove-meta-narrative
description: Find meta-narrative in a document (README, specification, design document, proposal, procedure, rule, SKILL.md, prompt and so on), that is, sentences in which the document talks about itself or the history of how it was made, and rewrite them so the document talks about its subject itself. Also check that the agent's work log or intermediate output (such as "Not achieved" or "Unknown") has not been left in. Use when the user says things like "Remove the meta-narrative" or "Check for meta-narrative", and when the user says the same thing in another language. Also use without being asked after finishing a document that will be read on its own, before handing it over. Do not use it on replies to the user or reports of work. For a document whose purpose is to record work, such as a work log, do not check the history of how it was made, the work procedure or intermediate output (groups 3 to 5). For a document handed to people, use it before review-for-readers.
---

# Purpose

A document talks about its subject (the mechanism, the specification, the content of a proposal). It does not talk about the document itself, the history of how it was made, the act of writing, or a response to an instruction. The reader reads only the document as handed over.

Apply this skill to the body of a document. Do not apply it to replies to the user or reports of work, because their job is to say what was done.
The job of a commit message and of a PR description is to say what was changed and how. So do not apply the part of group 3 about differences from the earlier version. Apply only the part of group 3 about the order of what was tried and the difficulties met, and groups 4 and 5.
When the purpose of a document is to record work (a work log, a progress log, a verification record, minutes, a change history), do not apply groups 3 to 5. Apply only groups 1 and 2.
For a document whose purpose is not to record work (a design document, a specification, a README), apply groups 3 to 5 even to a section that holds a record. Keep a record only if it is needed to understand the content. In that case, put it in a separate section or in a quotation, so that the reader can tell the record from the content.

## Groups of meta-narrative and how to judge them

| Group | Common form | Question to tell them apart |
|---|---|---|
| 1. The document talks about itself | A sentence whose subject is the document, a chapter or a source, and which states what it covers, its premises, its position, or the criteria used in writing it | If you remove it, does the information about the subject decrease? |
| 2. The document refers to something outside | A phrase that points to another place in the document or to another source without saying where | Can a reader tell what is referred to from the document alone? |
| 3. The history of how it was made remains | A sentence that states the order of the work, a response to a comment received, a difference from the earlier version, or a response to the request | Does a reader who reads only the document as handed over need the sentence? |
| 4. The author's work (steps, reports, plans) remains | A sentence that states work the writer can proceed with, work the writer has finished, or work the writer plans next | Does the sentence still read naturally if you add "(the writer, in the course of the work)" at its start? |
| 5. Intermediate output of the work remains | A word or phrase such as not achieved, unknown, unconfirmed, needs checking or TODO that says how far the writer's work has progressed | Does it say how far the writer's work has progressed, rather than how the subject is? |

The fix is set for each group.

- Group 1: Rewrite the sentence so that its subject is the subject of the document, not the document. If a declaration of premises is a requirement of the subject (such as the permissions needed to use it), write it as a requirement.
- Group 2: First try removing the phrase. If the text still makes sense, remove it. If it does not, change the phrase to a form that can be identified within the document, such as a chapter number. If the content of what the phrase refers to is needed to understand the text, put the needed part in the body.
- Group 3: Keep only the conclusion. If you want to convey the difference from the earlier version, do so outside the document, in the reply when you send it or in a change history.
- Group 4: Remove the work steps and reports, and keep only the conditions, states and results. If you write what will be done next, write it as a promise agreed with the reader. If the document does not show whether the promise was agreed, do not fix the sentence. List it as "needs a decision".
- Group 5: If the reader needs the information as the state of the subject, write it as a state or constraint of the subject (turn "not achieved" into the state that the subject does not support the thing in question).
  - Turn something the writer merely could not verify into a state of the subject (such as "the value is not decided") only when you have verified the state of the subject. If you have not, do not fix the sentence. List it as "needs a decision".
  - If the sentence only says how far the writer's work has progressed, remove it and say it in the reply to the user.
  - For a "needs checking" or TODO mark: if what is to be checked is an undecided matter of the subject, write it as undecided. If it is work remaining for the writer, remove it.

Group 4 has no single recognizable sentence form, so it is hard to find. Sometimes a whole passage of the document is divided by the author's work (for example, into what you can proceed with yourself and what you wait for others on). Fixing individual sentences will not solve that. Reorganize the division along the subject's own axes (conditions, certainty, scope of impact).

## What is not meta-narrative

The following are used by the reader to read the body, so do not treat them as meta-narrative.

- Definitions of symbols and labels used in the body.
- The purpose of the subject the document covers. An explanation of how to use the document is still meta-narrative.
- Sources and dates.
- References within the document that can be identified, such as by chapter number.
- A difference from the earlier version's numbers that the reader needs for a decision (in an estimate, an actual or a target: how much it moved).
- A preface that draws the reader's attention. Fix it only when it clearly falls under another group.

If unsure, consider whether removing the sentence would change the reader's decision or understanding. If it would, keep it.

## Procedure

1. Read the document from the start, and check each sentence against the questions of the five groups. Read headings, table cells, list items and notes too.
2. Fix each sentence that matches, using the fix for its group.
3. After fixing, read it from the start again. Look for sentences whose referent the fix removed, and sentences that no longer connect.

How to write documents in general is in rule `writing-documents.md` ("Write documents that make sense on their own") in the `writing-rules` skill.

## Format of the result

- When asked to remove meta-narrative, return a list of "location / group / before -> after" and the full fixed text. Do not fix a sentence you cannot decide is meta-narrative or content; list it as "needs a decision".
- When you used this skill yourself before handing over a document, hand over the fixed document and say in the reply in one line that you used it. Give the list if the user asks for it.
