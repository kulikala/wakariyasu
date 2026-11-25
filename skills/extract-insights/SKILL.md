---
name: extract-insights
description: Extract insights from a text the user gives (a transcript of a meeting or interview, a record of remarks, a talk, or a written text such as an article or report) that people who were not there can use later to make decisions, and write a document that states each insight in one sentence with its kind, background, notes, certainty and source. Use when the user asks to extract insights or findings from such a text, or asks what can be learned from it, and when another skill calls it with a text and output instructions. Do not use it to make a collection of quotes, a summary, or minutes (a record of what was discussed and who does what). When the source is the current session with the agent, use the insight extraction mode of summarize-session.
---

# Purpose

What was learned in a meeting, interview, talk or article is buried in the flow of the original text, and people who were not there cannot read it out. Extract from the original text the understanding that still holds away from the place where the text was produced, and make it a document that readers without that context can use to make decisions.

The readers have not read the original text and were not there. If the request names the readers or the use, choose the insights that affect those readers' decisions. If it does not, take as the reader someone who will start working with what the original text is about (a business, a field, a system) and will decide something about it.

An insight document is not a collection of remarks. If you line up quotes, readers learn who said what, but they have to work out for themselves what follows from it. The most important step is to raise the facts, concepts and decisions you can read in the original text into one sentence that readers without the context understand. Raising is not rewording. It moves from individual remarks or statements up to the properties, causes, premises and rules they support.

## What the caller specifies

The caller is the person who asked for this skill, or the skill or system that called it. If the caller specifies where to save, the file name, how to refer to people, the output format, or the range to extract from, follow it. Decide everything the caller left open by the policy of this skill.

- If no place to save is given and the original text is a file, save the document in the same folder under a name that shows which original text it comes from. If the original text was pasted into the conversation, put the whole document in the reply.
- If a file with the same name exists, do not overwrite it. Save under another name, so that a document a person has edited is not lost.
- If the original text is empty, too short to extract any insight from, or still audio or images that are not text, do not make a document. Return the reason to the caller.

## Kinds of original text

How you judge the kind and certainty of an insight depends on who is talking to whom in the original text. Before you read, tell which of the following the original text is. If one text mixes several kinds, tell them apart part by part.

| Kind of original text | Basis for saying a fact was confirmed | Basis for saying something was decided |
|---|---|---|
| An exchange among several people (a record of a meeting, hearing or dialogue) | One side stated an understanding and the other side accepted or corrected it, or someone answered a question with what they themselves do or saw | The participants decided a policy or method there. This includes a policy stated as settled that the others then built on in what they said next. Silence alone is not enough |
| One person speaking (a record of a talk or dictation) | The speaker names the material, measurement or source the statement rests on | The speaker is in a position to decide and states it as their own decision |
| A written text (an article, report or letter) | The writer names the material, measurement or source the statement rests on | The writer states it as a decision of the writer or the writer's organization |

In one person's speech and in a written text, no other party confirms anything. Treat a statement the speaker or writer makes without a basis as a claim, however firmly it is put. A named basis is enough even when you cannot check the material yourself. Say in the certainty that the basis was named but not checked.

## Kinds of insight

An insight is content of one of the following kinds.

- Confirmed fact: a fact for which the table in the "Kinds of original text" section gives a basis for saying it was confirmed.
- Claim: a fact or concept the speaker or writer stresses without a basis for confirmation. Stress shows in how it is said: repeated, given with reasons or examples, or insisted on as a premise. An answer to a question that is the answerer's own view, or something they heard from someone else, is also a claim.
- Decision: a policy or method for which the table gives a basis for saying it was decided. Do not widen its scope (which objects or which period it covers) beyond what the original text states. Do not raise a decision to a more general statement. Put its reasons and premises in the notes. When a decision made outside the exchange the text records (including one the same group made at an earlier meeting) is only reported, it is not a decision. Name the person who decided in the source, and make it a confirmed fact if the listener accepted it, or a claim if not.

Do not make the following into insights, because they are wrong by the time the reader reads them or do not change the reader's decisions.

- The state at that moment (progress, outlook, current counts or the person in charge) and planned work or follow-up tasks. If a role or rule can be stated, make the role or rule the insight and put the person's name in the source.
- A decision about where and how to fix a particular deliverable. Make an insight of the fact that made the fix necessary, and of the policy for how deliverables are made.
- Remarks that are only agreement, impressions or wishes, and the running of the meeting.
- What readers already know or what is generally known.
- Matters that cannot be raised and would remain a list of details.

## Writing an insight

An insight consists of one sentence, plus its kind, background, notes, certainty and source. Aim for readers to understand the insight from the sentence alone when they skim, and to go on to the background and source when they need to. One way to do this is to make the sentence a heading and put the rest under it.

### The insight sentence

- Make the subject what the insight is about: a business, an object, data, a rule or a mechanism. A sentence with the speaker or writer as its subject, a reported-speech ending, or a quote only tells readers who said it, not what follows from it. Write who said it in the source.
- Make the sentence understandable without the context of the original text. Fill in demonstratives and omissions, and replace names used only in that setting with words readers know. In a transcript, correct misrecognized words that the surrounding text settles.
- Raise the sentence until it states a property, cause, premise or rule that also holds in other situations involving the same object, not an individual event in the original setting. Even so, keep the concrete facts (what, who, with what, when). If you raise it too far, readers cannot apply it to their own situation.
- If it does not fit in one sentence, check whether two insights are mixed, and split them. Also split parts that differ in certainty. Move conditions and exceptions to the notes.

### Background, notes, certainty and source

- Background: the question or situation the insight came from. Write only as much as readers need to understand the insight. Do not reproduce the flow of the conversation.
- Notes: the range in which the insight holds and its exceptions, how it affects the reader's decisions, and any other insight it presupposes.
- Certainty: kept separate from the kind, so a confirmed fact or a claim can also be hearsay or an inference. State whether the insight was confirmed, is one side's claim, is hearsay (a judgment or remark of someone not present, passed on by the speaker or writer), or is an inference (something the agent writing the insight inferred from the original text). Add any reservation the speaker or writer attached. Hearsay, inference and reservations cannot be read from the kind of insight, so write them for every insight they apply to. For an inference, add what it was inferred from.
- Source: the speaker or writer (and, for hearsay, the original person who judged), and a position in the original text, so that readers can go back to the original remark or statement. Show the position with the cues the original text has (clock time, elapsed time, headings, pages, lines). If it has none, quote a short phrase from the relevant place. If there are several original texts, also say which one.

## Structuring the document

- At the top, let readers see what setting and what text the insights come from. Give the name and date of the original text, and explain how the body refers to people if that needs explaining.
- Divide the body into sections by subject, not by the flow of the original text. Make each heading say what its section contains. If an insight presupposes another, let readers read from the premise onward.
- The number of insights follows from the content of the original text. A text that mostly reports status yields few. Do not add content that is not an insight to reach a count.

## How to proceed

Do not write insight sentences until you have read the whole original text. Later remarks or statements can change the meaning of earlier ones or withdraw a claim.

1. Read the whole original text and note candidate insights. For each candidate, note the position, the speaker or writer, the point and the kind, in a form you can look up later. Do not put the notes in the document.
2. Merge candidates that say the same thing, and split a remark or paragraph that contains several points. For a withdrawn claim, take what stands at the end of the text. Drop candidates that are not insights.
3. Make sections by subject, and write each insight sentence with its kind, background, notes, certainty and source.
4. Read the document again as a reader who does not know the original text. Check that each insight sentence can be understood alone, that no state or plan has crept in, and that each kind and certainty matches the basis in the table in the "Kinds of original text" section.

## Finishing

If the language pack has a `styles.md`, choose the kind of text from it. Language packs are in `skills/writing-rules/lang/<code>/` (the `lang/` folder of the `writing-rules` skill), and the language pack's `skills.md` may add points for this skill. For finishing, follow the "When you finish writing" section of `writing-documents.md`. If the caller says it will do the finishing, leave it to the caller.

In the reply that presents the document, state where it is saved, the number of insights by kind, how you told the kind of original text, which insights are inferences, and any place where a misrecognized word could not be corrected and the meaning stayed unclear.
