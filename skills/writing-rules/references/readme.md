# How to write a README

A README sits at the top level of a repository and publishes a tool externally. Its readers are people deciding whether to try the tool, people installing it, and people starting to use it. They try to learn from the README alone what the tool is and how to set it up for use. Readers jump to the section they need by its name. Write the README with the section names, structure, and wording that human-maintained READMEs in the document's language use.

If the repository has a document that defines how to write its README, read it first and follow it. For the points it does not define, use the policy for each section below.
For section names and phrasing that the policy below does not cover, open several READMEs that people maintain in the document's language for tools in the same field, if you can read files or the web. Match the form those READMEs use.
Use the README part of the document language's `documents.md` when it defines README section names and wording.

## Versions in several languages

When the README has versions in several languages (README.md and README.ja.md, for example), write each version for readers of its own language, not as a translation of another version. A translated README carries the source language's sentence order, headings and examples, and its readers find it harder to read than a README written in their language. Keep the facts the same in every version: what the tool does, the commands, the requirements and the steps. Choose the section names, the order inside a section, the examples and the wording as a README written in that language would. After changing one version, apply the same change of facts to the others, in each one's own wording.

## Keeping it short to scan

Readers first scan a README to decide whether to read on, and then look only for the part that applies to them. Keep visible what every reader needs: what the tool does, an example of its output, and which installation method to choose. Fold the details that only some readers need into a `<details>` block whose `<summary>` names what is inside: the steps of each installation method, notes on options, long tables, and background on how the tool works. GitHub shows only the summary until the reader opens it, so the README reads short while the details stay on the same page and can be searched. Leave a blank line after `<summary>…</summary>` so that GitHub renders the Markdown inside the block.

## Markdown that GitHub renders

A README is read on GitHub more than anywhere else, so write it with the Markdown GitHub renders, and keep it readable where the same file is shown as plain Markdown.

- Mark a note, a tip or a warning the reader must not miss with GitHub's alert syntax (`> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]` or `> [!CAUTION]`, the keyword in capitals). GitHub shows it as a colored box, and other viewers show it as a quotation, which still reads. Keep alerts for what changes what the reader does; a page full of them hides the one that matters.
- Give every code block its language, so that GitHub colors it and the reader sees at once whether to run it in a shell or type it into the tool.
- When there are versions in several languages, link them to each other on the first lines, so that a reader who landed on the wrong one can switch.
- Show a badge only when it answers a question the reader has before reading on, such as the current version or the license. A row of badges reads as noise.
- Check the result with GitHub's own renderer before publishing (`gh api markdown -f mode=gfm -f context=<owner>/<repo> -F text=@README.md`, which returns the HTML GitHub shows): a block inside `<details>` or an alert that does not render appears in that HTML as its Markdown source rather than as HTML elements.

## Sections

Choose the order and the sections to fit the tool. Readers often proceed in this order: learn what the tool is, check that it works in their environment, install it, and start using it. An order that follows that sequence is easy to scan. Do not add a section that does not apply to the tool. Move long details to a separate document and link to it from the relevant README section.

Put in one section only the content that matches the section's purpose. Readers jump by section name and read only the section they jumped to. If content that belongs to another section is mixed in, they will not find it where they looked. They also cannot tell whether the section they read is complete.
When content belongs to another section, write it there and link to it.
When you have written a sentence, check which section's purpose it matches.

The purpose of each section is as follows.

- Opening description: state what the tool does and show an example of its output, so that readers can judge at once whether it fits their use.
- Features: if the tool has groups of functions that users can use separately (separate commands or modes), list each function's name and what it does. Put the list before the first section that uses the names. Without the meaning of the names, readers cannot follow the later sections.
- Strengths: state the properties that are reasons to choose the tool. Specifications such as output formats and options are looked up when using the tool, so put them in the usage section.
- Suitable uses: state what the tool covers and the uses it suits and does not suit. State the work users do before and after the tool as part of what the tool covers, and do not list that work among unsuitable uses. If you list it there, part of the flow of using the tool reads like an unsuitable use.
- Disclaimer: state how to treat the tool's output and whether there is a warranty. For a tool whose output can still contain errors, state what kinds of errors tend to remain and what users should check. Leave legal statements, such as disclaimers of damages, to the license.
- Supported environments: show them in a table so that readers can check what works in their environment. Add rows for environments that many people want to use but that are not supported, and mark them as unsupported. Readers look for their environment in the table. Without a row, they cannot tell whether the environment is supported.
- Required disk space and additional software: put what readers must check before installing in their own sections. Do not repeat that content in other sections; link to the relevant section.
- Installation: divide by environment so that readers read only the part for their environment, and state where to run each command. Make the part's name and its first lines show which environment the method is for. Give the comparison of methods and the reasons for the choice only as far as readers need them to choose a method.
- Usage: state the steps up to running it the first time and the commonly used operations.
- Developer guide and license: state the procedures for people who take part in development and the terms of use.

A README explains the tool the repository provides. For other tools used for installing or running (a package manager, an installer command), show only the command the reader runs and the options that command requires. Show an option that is not required with a one-phrase note of what it does, unless the place is for explaining options. Leave the conditions under which the other tool works, and its detailed usage, to that tool's README, and link to it. If you copy another tool's specification and that tool changes, only your README is out of date.

Do not include guidance for using old versions that are no longer maintained. Readers may mistake an old version's steps for the latest version's steps and start using a version whose bugs will not be fixed. If there are users moving from an old version, include only the steps for moving.

## Wording

Readers who meet phrasing that sounds translated, or unfamiliar words, trust the document less and may misread it. Choose wording that human-maintained technical documents in the document's language use.

- General words: for words for work and things, use words established in technical documents in the document's language. Avoid the phrases that the document language's `documents.md` points to, if it points to any. For words that are not on the list, use the same approach.
- The tool's words: readers compare the words that appear in the tool's commands, screens, and output with what they see on the screen. Use those words unchanged, and give their meaning where they first appear.
- The writer's coined names: a name the writer gave during the work does not carry meaning outside the tool. Do not use it. Replace it with a general word that states the content. After replacing, restate the replacement in another language, and check that it matches what the original name stands for.
- Section names: use names that READMEs in the document's language use. A name translated word for word from another language's heading is not seen in READMEs in the document's language.
- Names of work sections and subsections: name the sections and subsections where readers do things, such as installing and configuring, with the names readers are used to in READMEs in the document's language. Readers look for a familiar name and jump to it. With a reworded name, they do not notice that it is the section they are looking for. Use the same word in the body as in the heading.
