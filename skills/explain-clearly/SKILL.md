---
name: explain-clearly
description: Use when the user says they do not understand your last reply, or a word or explanation in it. This covers requests like "Explain it more clearly", "So what does that mean?", "Shorter please", "What do you mean?", "In other words?", "Explain it simply", "Explain it so a child could understand", "What is X?" about a term that appeared in your reply, and "What is the difference between X and Y?" about things your reply listed. Also use it when the user says the same thing in another language. Restate in words that someone who has not followed the session understands, and choose from the user's wording whether to shorten or to add background. Answer a general question unrelated to your reply (such as "What is REST?") as usual. For questions about how the session is going, use session-status. Requests in Japanese that trigger it include 「分かりやすく」「つまり？」「簡潔に」「どういうこと？」「言い換えると？」「平易に言うと？」「小学生でも分かるように」「〜とは？」「〜と〜の違いは？」.
---

# Purpose

Restate what the user did not understand in words the user understands. Keep the content. Change how you say it.

## Identify what was unclear

Before restating, decide what the user got stuck on.

- **A word** ("What is X?"): Often a name you kept using during the work, or a term from tool output.
- **A connection** ("What do you mean?"): Each sentence is readable, but the user cannot follow what is the reason for what, or what is being compared with what.
- **A conclusion** ("So what does that mean?"): The user could read the explanation, but does not know what it means for them or what they should decide.
- **A difference** ("What is the difference between X and Y?"): The user does not know where listed items differ, or what changes depending on the choice.
- **The whole reply** ("Explain it more clearly"): The cause is not one of the above. Read your last reply from the start as someone who has not followed the session, and list every place where they would get stuck.

If the user's words do not tell you which of these applies, look in your last reply for words the user has not used in the session and for words whose referent is not stated in the sentences that contain them. Start the restatement from those words.

## Choose the length of the explanation

| What the user said | Direction |
|---|---|
| "So what?", "Shorter", "In a word" | Shorten. State the conclusion in one to three sentences and keep only the conditions that matter |
| "What do you mean?", "Explain it so a child could understand", "Simply" | Add background. Before the conclusion, put the short background that is needed to read it |
| "In other words?", "Explain it more clearly" | Do not change the length much. Change the words and how the sentences are built |
| "What is X?" | Give the meaning of the word in one or two sentences, and add what it refers to in the current discussion |
| "What is the difference between X and Y?" | List only the points that differ. Include what happens depending on the choice |

When the user's words match no row of the table, use the row closest in meaning.

## How to restate

- State the conclusion first.
- Replace names, abbreviations and terms from files that came up during the work with words the user used or words that are generally understood. Keep exact proper names, such as file names and command names, and add what each is for.
- Do not add causes or connections that the original explanation did not have. Do not join two separately decided things with a connective that implies a reason. If you do not know how they connect, write them in separate sentences.
- Use at most one analogy, and state which part of the analogy corresponds to which part of the subject.
- Do not drop the conditions, exceptions and degree of certainty (inferred or verified) from the earlier explanation to make it shorter. If you drop any, say that you did.
- Start with the restatement itself. Do not open with an explanation of what was unclear in the earlier explanation or with an apology.

Follow rule `writing-to-user.md` ("Write replies that someone who has not followed the session can understand") in the `writing-rules` skill.

## Check before sending

- Read the restated text from the start, in order, as someone who has not read your last reply. If you had to go back and reread any part, fix it.
- Polish it following rule `polishing.md` ("Polish what you wrote before handing it over") in the `writing-rules` skill. If you are unsure about notation or register and the language pack has a `styles.md`, read it. Language packs are in `skills/writing-rules/lang/<code>/` (the `lang/` folder of the `writing-rules` skill).
