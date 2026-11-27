---
name: compose-page
description: Use when creating or revising a single HTML page that shows content to people (a report, a summary of materials, a meeting or open issues, research results, and other pages that convey content, including pages published as Claude artifacts). Decide what the page carries, how it is structured, which words it uses, how readers tell things apart, and which figures it draws, so that readers who do not know how the page was made can read the conclusion, the state of things, and the differences between items from the screen. Use when asked to make something into a page or an artifact, to make a page easier to read, or to show something visually, and when told that a page you presented is hard to follow. Also use, without being asked, before you present a page you made for people. For a page that shows the diff of a change, use show-changes. For a page that another skill builds from its bundled template, follow that skill. Do not use for a page only its author will look at. Also applies when the user says the same thing in another language.
---

# Purpose of the skill

Make a single HTML page that people look at into one where readers can read the conclusion, the state of things, and the differences between items from the screen. An item is each thing the page lays out side by side: something the reader handles as distinct, such as a case, a work stage, a person or an option. Readers know neither the exchanges in which the page was made nor the numbers and nicknames that the authors (the agent making the page and the person who asked for it) used during the work. On a page that only moves prose onto the screen, readers cannot tell what was decided, what the problem is, or where things differ until they have read all of it. Decide what the page shows, in what order and in what form, by what the reader should take from the screen.

This skill does not cover the following.

- How to write and polish the text on the page. Text on a page is a document too, and follows rules `writing-documents.md` and `polishing.md` of the `writing-rules` skill.
- The look itself, such as an attractive palette or typeface. The skill uses color, placement and layering only as far as they help readers tell things apart and read the page.

If the environment, the user, the team or the project has rules for building pages, those rules come first, and this skill fills the places they leave open. When nothing sets the page's code, start from `references/single-file-page.md`, a single HTML file that runs without a build step.

When you use a timeline, a flow diagram, collapsible sections, badges (short words or phrases shown apart from headings and body text) or view switches, read in `references/page-techniques.md` the failures each technique tends to produce.

Put an element on the page (a summary, a description of the page, badges, a legend, controls) when readers would lose information without it. An element that carries no information buries the content readers use to decide.

## Readers and what the page carries

Before making the page, settle who the readers are, what they do not know, and what they will decide from the page. If the request and the materials do not identify the readers, add the readers you assumed to the reply in which you present the page.

- Group items the way readers group them in meetings and conversation, and call them by the readers' names. Take readers' names for things from the wording of the request and from materials the readers wrote or use.
- Show what readers can now do, what was decided, and what remains, rather than what the authors did. Include the work process when readers ask for it.
- On a page that sorts out open issues, let readers read separately what was decided, the premises, the wishes of the people involved, and what is still undecided. When these are mixed, readers cannot pick out what to discuss.
- An assessment such as whether something is late or has a problem looks more definite as a colored status than as a sentence, and moves readers' decisions directly. Show the basis (the planned date or the standard it was compared against) where readers can check it, and do not show a concern whose basis you have not checked as a definite delay or problem.

## Structure

- Make what readers need first, such as the conclusion, the overall situation and what is still undecided, readable on the first screen. Even on a page asked to cover every detail, a page of details alone does not let readers grasp the content.
- Let readers check what they treat as evidence, such as sources and how numbers were obtained, near the figure or field that uses it.
- Let readers copy the text they select, because readers carry parts of a page into their own notes and messages. The template in `references/single-file-page.md` has a copy button for this. When you build a page that does not start from the template, add a button that behaves the same way.
- Group information that differs by item so that readers can finish reading one item at a time. When you lay out items of the same kind, show the same information in the same place and form, so that readers can compare items. When an item has no content for some information, keep its slot and show that it is empty; dropping the slot shifts the places readers compare.

## Headings and words

- Keep information that is separate from what a heading names, such as the time unit, the role of a section or a date, out of the heading's wording and show it as a badge. In the title too, keep the subject's name and the point in time the content describes apart, so that readers can read each on its own.
- Use names that appear in source materials as the sources spell them, so that readers can match them against the sources. When sources spell a name differently, use the spelling in the source the readers use.
- Name what the page newly names (fields, controls, states) with words readers already use.

## Cues for telling things apart

Color, shape and badges are for letting readers tell differences apart at a glance. Added as decoration, every extra cue buries the differences further.

- People, categories and states are easier for readers to pick out and compare as badges than embedded in sentences. Assign status colors by a property readers use to decide, such as good or bad, whether attention or a decision is needed, or how far along something is, not one color per status name.
- Show the same person, the same state and the same item in the same color and shape everywhere on the page, so that readers can connect them across places.
- A badge that reads the same on every item tells nothing apart.
- Give a figure that conveys meaning only through color or line style a legend that explains the meaning.

## Settled and unsettled, options, and controls

- Show settled and unsettled information so that readers do not confuse them. In a list, a distinction made by wording alone is easily missed.
- On a page that asks readers to choose, lay out the options so that readers can answer by naming an option briefly. Show the work that comes after the choice apart from the options.
- Add a control that switches views when readers have a use for it, and name it so that the name says what operating it will show.
- Provide both a light and a dark appearance, and show the one that matches the display setting of the reader's device (the OS or browser setting).

## Figures and quantities

Stages, progress, quantities, proportions, composition, relationships and routes are easier to read as a figure than as prose. A table suits comparing rows. When the same content can take several forms, choose the one that needs the fewest operations and eye movements from readers. Do not make up values or dates that are not in the materials to fill a figure or a field. Where a value is missing, show that it is missing.
