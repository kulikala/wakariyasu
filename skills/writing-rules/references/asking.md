# How to write a decision question

Write each point the user must decide in a reply as a decision question, one question per answer the user returns, in the form below.
Number the heading even when there is only one question, so that the user can answer with only the question number and the option letter.
Number questions continuously across what you know of the session, and do not reuse the number of a question that has been answered.

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
- The column names in the template and "(recommended)" are the English labels. Use them as written in an English reply. In a reply in another language, use the names that the language pack's `conventions.md` defines for that language. If the pack has no `conventions.md`, write the labels in the reply's language. Language packs are in `skills/writing-rules/lang/<code>/` (the `lang/` folder of the `writing-rules` skill).
- When there are several questions, put first the question whose answer changes the later work the most.
- Even for a question with a recommendation, the user decides which option to choose. You list what happens for each option.
