---
name: summarize-session
description: Turn what the current session covered into a document that people or agents who were not in the session can read later and use. Use when the user says things like "Summarize this session", "Summarize what we found" or "Extract my feedback", and when the user says the same thing in another language. Infer from the request what the user wants, and build the document with the policy of the matching mode. Document output structures the matters the user asked about as a document. Insight extraction organizes what was learned as general insights. Feedback extraction organizes the user's feedback by finding, intent, background and target, and response policy. Log output keeps a record of the work. If several modes apply, make a separate document for each mode. If no mode applies, build a structure using the modes' policies as a reference. Do not use it for a short summary inside a reply. To extract insights from a text that is not the session (a transcript, a record of remarks, an article), use extract-insights. For questions about how the session is going, use session-status. When the user says they do not understand your last reply, use explain-clearly.
---

# Purpose

What the session examined, learned and was told is buried in the conversation record once the session ends. Put the content of the session into a form that someone who did not follow it can read and use from the document alone, so that it can be handed outside the session.

The readers of the document are people and agents who were not in the session. If the request names the reader or where the document will go, fit that reader.

## Choose the mode

Infer from the request what the user wants. If the words of the request do not settle it, infer from the conversation before and after the request and from what the session covered. If what the user wants matches one of the modes below, build the document with that mode's policy.

| Mode | What the user wants |
|---|---|
| Document output | The matters examined and decided in the session, structured as a document |
| Insight extraction | Understanding that holds outside the session, derived from facts confirmed in the session |
| Feedback extraction | The feedback the user gave the agent, with a response policy for each item |
| Log output | A record of the work the agent did |

- If what the user wants matches several modes, make a separate document for each mode. Each mode has different readers and uses, and combining them puts chapters in the document that no reader needs.
- If no mode applies, build a structure that fits what the user wants. Use the parts of each mode's policy that fit.
- If the request narrows the target to part of the session, narrow to that. If not, the target is the goal of the whole session.

## Decide whether the content changes over time

Before you start the document, decide from the user's request which of the following the document is. Readers read the document after the session. A value that changes over time can be wrong by the time it is read.

- A document whose content does not change over time: Build it only from content that holds after the session ends, such as purposes, policies, decisions and their reasons, and insights. Do not write the state at that point (progress, the current value of a count or size, the published version) or a work log.
  - Write a work log only when the user asks for one in the request. Even then, do not change the kind of document. Put the work log in a separate section or in a quotation, so that the reader can tell the work log from the content.
- A document that contains states that change: The purpose of the document is to keep the state or the course of the work at that point. Write the work log too. Add the time to which each state applies.

For document output, insight extraction and feedback extraction, make a document whose content does not change over time unless the request asks for the state to be kept as the purpose of the document. Log output is a document that contains states that change.

A work log is a kind of content. It states what the agent did, and how many times it tried what in which environment (which PC, which settings). If the content is of this kind, reordering it by content instead of by time does not stop it from being a work log. The range in which an insight or a decision holds (the tool it concerns, or the conditions it assumes) is part of the insight or decision, not a work log.

## Records to base the document on

Base the document on records you can verify. Look at the conversation record, the changed files, commits and command output, and match the facts at the end of the session.

- A session whose conversation continues from a summary has lost detail and wording in the summary. If you can read the file of the original conversation record, read it. If the record is large, read the user's statements together with the agent's proposal or question just before each. The user's approval or choice cannot be understood without the proposal just before it. For feedback extraction, rely on the original record in particular, because a summary does not show whether something is feedback or an instruction, or whether feedback was repeated.
- If you cannot read the original record, base the document on the summary left in the conversation, and on files and commits.
- Use only what is valid at the end of the session. Ignore options withdrawn midway, facts found to be wrong, and policies replaced by the user's later instructions. Mention a withdrawal only when it is needed to explain what is valid, and then state it as part of the reason for a decision. Do not state the order of what was tried before the withdrawal.
- Do not write what you cannot confirm from the records. If you estimate, write it so that it is clear it is an estimate.
- The document goes outside the session, so do not copy information that its owner has not allowed to be shared externally. Write only that the information exists. When you quote the user's words, hide only the part that contains it.

## Structuring the document

In every mode, let the reader tell what the document is about as soon as they start reading. Show the subject with sentences that talk about the subject itself, not sentences in which the document explains itself. Say what the document was made from only when the reader needs it, in a section separate from the body.

For a document whose content does not change over time, do not write a work log unless the user asked for one. The reader wants to know what to aim for, what was decided and what to keep in mind, not what the agent did.

- Divide the whole into chapters and sections by the axes of the content, not in time order.
- Make each heading say what is in the section, so that it can be understood from the heading alone. Avoid headings that are only the name of a category, because the reader cannot tell the content until they open the section.
- Let the reader read the overall purpose, the outline of the policy and the intent before the detail. Keep detail only when a reader outside the session would decide or act wrongly without it.
- Keep the amount to what the reader needs to understand the purpose and policy. When items multiply, group them under a higher-level policy and do not keep listing small items.

### Document output

The most important point in document output is to structure the material as a document. With a plain list of matters, the reader has to rebuild how the matters relate and which one is the higher-level policy.

Decide what to put in the document by inferring from the request what the user wants. The target is the matter the request named, and what the session examined and decided about it.

- Raise the level of abstraction of the target, from individual tasks and statements to purposes, policies, and decisions with their reasons.
- Keep the purpose of the whole document in mind. Build a hierarchy of chapters that support the purpose and sections that support each chapter. Let the reader see which part of the document's purpose each chapter and section carries.
- Write how the parts relate, and arrange them so that the reader can understand from the premises onward.
- Write what was decided separately from what was not decided. Then the reader knows where to start judging for themselves. Limit undecided matters to those that were raised in the session as questions and left unanswered. Write what is undecided and what is needed to decide it, as a state of the subject.
- Add a reason to each decision. With the reason, the reader can judge by the same policy in situations the document does not cover. If the reason depends on the result of a verification, write only what the result supports. Do not write the procedure, the number of trials, or the environment.
- Write procedures in the general form, not with the values of a specific version. The reader applies the procedure to the version in use when they read the document.

### Insight extraction

Insight extraction works from the current session (the record of the conversation with the agent). To extract insights from a text the user gives that is not the session, use the `extract-insights` skill, which tells claims from confirmed facts for each speaker or writer.

An insight is general understanding that holds outside the session. Build it by generalizing from facts, so that the reader does not misjudge the next time they face the same kind of environment, tool or problem.

The writer is tempted to report when and what was found. The reader needs what can be said in general. Leave the agent's work record out of an insight document. Add short background only when it is needed to understand an insight.

- Combine individual facts into the properties, tendencies, causes and premises they support, and make sections with the insight as the subject. Write facts only as far as they are needed as the basis of an insight.
- Drop any matter that cannot be generalized into an insight and would remain only a list of details.
- Organize the insights so that their relations are clear. If an insight presupposes another, let the reader understand from the premise insight onward.
- For each insight, write the range in which it holds (the tool concerned, or the conditions it assumes) and how it affects the reader's judgment.
- Write an inferred insight so that it is clear it is inferred. Show how certain an insight is by distinguishing confirmed from inferred. Do not show it by how many times, by what method, or why it was not confirmed. The number of times and the method belong to a work log.
- Do not write the procedure used to verify an insight (how the experiment went) or a list of what was not confirmed. The procedure is a work log, and what was not confirmed is remaining work. Neither is an insight. Write them as a record only when the user asks.

### Feedback extraction

Feedback is the user's statement that the agent's behavior or deliverable differs from what they expected. An instruction is different: it is a request for what to do from now on. An instruction decides the content of a task, and feedback changes the policy of behavior. If you list instructions as feedback, a one-off task request looks like a policy to keep following, so do not mix them.

Do not just list the points that were raised. Read from the feedback what the user is aiming for, and organize it as a policy toward that aim. The purpose is for the reader to change their behavior before they receive the same feedback.

- Do not list repeated feedback, or feedback that comes from the same aim, one by one. Raise it to the shared aim and combine it into one item of feedback. That it was repeated is itself evidence that the policy matters.
- For each combined item of feedback, write four things: the finding, the intent, the background and target, and the response policy. Do not omit any of the four, so that the reader can read the intent of each item of feedback together with the response.
  - The finding is what differed from the user's expectation.
  - The intent is what the user is aiming for with the feedback.
  - The background and target are the situation in which the feedback was given, and the agent behavior or deliverable it was aimed at.
  - The response policy is how the agent will behave.
- When there is a lot of feedback, group feedback with similar intent into chapters by the viewpoint they share. Set the viewpoints from the session's feedback.
- Quote the user's words only when needed as evidence for the intent, and keep quotations short. Do not rewrite quotations.
- Include the ways of working the user approved as policies to keep following.
- When feedback on the same point changed, use the policy that is valid at the end of the session.

### Log output

Log output is a document that records the work itself, so it may be in time order. Group a series of work into sections. For each section, let the reader see first what the work was for and what the result was. Write what the work was for in sentences fitted to the content of the work, not in an opening that is the same for every section. Keep attempts that failed along the way and what was not understood. Write the remaining work and what is waiting for the user's decision, so that a reader who finishes the record knows what is needed next.

## Finishing

If the `documents.md` of the document language's pack has a table of kinds of text, choose the kind of text from it. Except for log output, use `article` if none of the kinds fits. Language packs are in `skills/writing-rules/lang/<code>/` (the `lang/` folder of the `writing-rules` skill). For finishing, follow the "When you finish writing" section of `writing-documents.md`. Treat log output as a work log under the "How the history of the work is handled depends on the kind of text" section of `writing-documents.md`.

In the reply that presents the document, state the mode you chose and the result of deciding whether the content changes over time. If no mode applied and you built a structure, say so and state the structure you built. Also state the records you based it on, so that the user can tell whether you read the original conversation record or took from a summary.
