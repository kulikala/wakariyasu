# Constraints agreed with the author

Some of wakariyasu's skills and rules contain constraints whose wording or format was settled with the author who maintains wakariyasu, rather than left to the agent's judgment. A review does not flag the constraints listed here as over-constraining or as lists of examples. To change a constraint, first agree on it with the author, and update this list to match.

## summarize-session

### The four items of feedback extraction

- Subject: the "Feedback extraction" section of `skills/summarize-session/SKILL.md`
- Constraint: for each piece of feedback summarized, write all four of the point, the intent, the background and target, and the response policy. None of the four is omitted.
- Agreement: on 2026-11-06, the author specified the four items as the structure of feedback extraction.

### Handling the source records a document was made from

- Subject: the "Structuring the document" section of `skills/summarize-session/SKILL.md`
- Constraint: what the document was made from is written only when the reader needs it, in a section separate from the body.
- Agreement: on 2026-11-06, the author specified that what a work record was extracted from is to be written in a separate section if necessary.

## extract-insights

### The form of one insight

- Subject: the "Writing an insight" section of `skills/extract-insights/SKILL.md`
- Constraint: write each insight as one sentence of insight plus its kind, background, supplement, certainty and source. None of them is omitted.
- Agreement: on 2026-11-25, the author specified this as the form of the insights document.

## compose-page

### Light and dark display

- Subject: the "Settled and unsettled, options, and controls" section of `skills/compose-page/SKILL.md`, and `skills/compose-page/references/single-file-page.md`
- Constraint: the page provides both a light and a dark display, and shows whichever the reader's device display setting selects.
- Agreement: on 2026-11-22, the author specified that the page support both light mode and dark mode and follow the device display setting.

### No instructions to check the display

- Subject: SKILL.md and the references of `skills/compose-page/`
- Constraint: do not write an instruction that has the agent check how the page it made displays, nor an instruction that has it write in the reply that it could not check. Whether to check is left to the agent.
- Agreement: on 2026-11-22, the author specified that no instruction for the agent to check is to be written, and whether to check is left to the agent.

### Starting point for a page built as one HTML file

- Subject: `skills/compose-page/references/single-file-page.md`
- Constraint: as the starting point for when the environment or project does not fix the page's code, include a single-HTML-file template that uses Vue 3, Tailwind CSS v4 and Lucide. The URLs in the template carry the same major-version specifiers as the author's template (`vue@3`, `@tailwindcss/browser@4`). No font is specified; the browser's default font is used. Lucide is loaded from `@lucide/vue`. The template's code names no particular icon and no color values; they are placeholders, and the agent chooses the icons and colors from the content of the page.
- Agreement: on 2026-11-25, the author specified that the author's own template be taken in as a reference, and also specified supporting the light and dark displays, separating how the `<head>` is handled for artifacts, dropping the Noto Sans JP specification, and dropping the Vue 3 and Tailwind 4 version specifiers. On the same day, having found that it does not work without them, the author specified returning to the template's major-version specifiers. Also on the same day, the author specified moving from `lucide-vue-next`, which is discontinued, to `@lucide/vue`, and pointed out that the template's icons and colors were too specific.
