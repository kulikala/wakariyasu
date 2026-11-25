# Polish what you wrote before handing it over

Polish for readability. Do not change the claims, conditions, numbers, or the strength of assertions.

## Checks for every language

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

Apply the `polishing.md` in the language pack for the language of the text. If the pack has a `styles.md`, choose notation by it. The language packs are in `lang/<code>/` of the `writing-rules` skill's folder. A language with no pack gets only the checks for every language.

## Pass documents for people through a skill that refines prose, if one is available

Documents that people will read or that will be published (READMEs, manuals, specifications, proposals) go through a skill that refines prose in the document's language, after you polish them yourself, if such a skill is among the available skills. A skill of this kind audits and rewrites text that AI wrote, to remove the patterns of AI writing (unnatural metaphors, unclear links between subject and predicate, skewed sentence patterns, decoration and promotional tone) while keeping the meaning and conditions. Choose it by its description: the skill must name the language of the document. If the skill takes the kind of document or how much the readers know, give them. The language pack's `styles.md`, if any, names the kinds of document.

Check that the refined text keeps every claim, condition, number, and level of certainty of your text. Where the skill changed the meaning, restore your wording.

Do not pass replies to the user, work reports, commit messages, pull request descriptions, or code comments through such a skill. When a reply carries the full text of a document, treat only that full text as a document.

## Read it through at the end

Read the text through yourself from the start. If you went back to an earlier place while reading, fix the sentence that made you go back.
