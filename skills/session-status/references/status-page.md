# The status page

The status page shows a session-status report as one HTML page: the current goal, the latest instruction, the tasks with their states, the latest status, and the decisions needed. On the page the user can choose an option for each decision, write a message for each decision and for the whole report, and press the copy button to copy all answers as one text. The user pastes that text into the session. The text repeats each question with its number, so you can match every answer to its question without the page.

You describe the report in a JSON file, and `scripts/build.py` turns it into the page by filling `scripts/template.html`. Paths that start with `scripts/` or `references/` are relative to the folder of the `session-status` skill; run the commands below from that folder, or give the full path of `build.py`.

## Steps

1. Write the report as `SKILL.md` describes, including the polishing in "Check before sending".
2. Put the same report into a JSON file (see "The JSON report" below). Copy the text of each section and each decision as written in the report, not a shorter version, because the user may read only the page.
3. Run `python3 -B scripts/build.py <report>.json --check`. It only validates the JSON and writes nothing: it prints `ok`, or a message naming the key that is wrong and exits with 2. Fix the JSON until it prints `ok`.
4. Build the page and hand it over (see "Build and hand over the page" below).
5. In the reply, give the link or the file location, the key points of the latest status, and the decisions section as usual, so that the user can also answer in the session without opening the page. The first time in a session, add one sentence saying that the user can choose options and write messages on the page, press the copy button, and paste the copied text into the session.

The page needs Python 3.9 or later to build. Where Python is not available, do not make the page; write the report in the reply only, and tell the user that the page could not be built.

## The JSON report

The file has this structure; the table below says what each key holds.

```json
{
  "title": "…", "lang": "…", "asOf": "…",
  "goal": "…", "instruction": "…", "status": "…",
  "tasks": [ { "task": "…", "state": "…", "decision": 0, "notes": "…" } ],
  "decisions": [
    { "number": 0, "question": "…", "context": "…",
      "options": [ { "letter": "…", "label": "…", "recommended": true, "text": "…" } ] }
  ]
}
```

| Key | Content |
|---|---|
| `title` | Required. The page title, shown at the top of the page and in the browser tab. Name what the session works on. |
| `lang` | The language code of the report: the language of the page being produced. It marks the language of the page's text, and `build.py` takes the page's words from `lang/<code>/labels.json` (see "Words on the page"). |
| `asOf` | When the report was written, in the form the user reads dates. |
| `goal`, `instruction`, `status` | The text of the goal, the latest instruction and the latest status sections. Leave out the key of a section that the report leaves out; the page then leaves out the section too. |
| `tasks` | The rows of the task table, in order. `task` is required. `state` is one of `done`, `in_progress`, `waiting_process`, `waiting_decision`, `not_started`, `problem` and `cancelled`, which stand for the seven states in the state table of `SKILL.md`, from ✅ to ⛔ in table order. For a state you made up under the rules of `SKILL.md`, give `{ "emoji": …, "label": … }`. `decision` is the number of the decision the task waits for, and goes only with `waiting_decision`; the page then shows the state as a link to that decision. |
| `decisions` | The decision questions, in the order of the reply. `number` is the number of the question in the reply. `question` is the question sentence, and `context` is the paragraph under it. Each option has the answer `letter`, an optional short `label` that names the option, and `text`, which is the background-and-effects column of that row. Mark at most one option `recommended`. The reply already puts the recommended option in the first row with letter A, so keep the options in the order of the reply. For a question without options, leave out `options`; the page then shows a box for a written answer. |

Text fields are plain text. A blank line starts a new paragraph, lines that start with `- ` make a list, text between backticks is shown as code, and an http or https URL becomes a link that opens in a new tab. Write the full URL of an artifact or page the user should open to decide. Any other markup is shown as written.

## Words on the page

The page's fixed words (the section headings, the column names, the state words, the buttons, and the words of the copied text) come from `lang/<code>/labels.json` of this skill, where `<code>` is the report's `lang`. `lang/en/labels.json` holds the English words, and without `lang` the page is in English. Do not open `scripts/template.html` and do not fill in words yourself. The `build.py` command puts them into the page.

For a language without `lang/<code>/labels.json`, `build.py` stops and names the `--init` command to run. That command writes the English words as a JSON file. Translate the values into the language of the report and keep the words in braces as they are; the page fills them in. Then pass the file with `--labels <file>`. The script stops on an unknown key, a missing key, or a dropped word in braces, and says which. The same file prints the matching reply skeleton (`scripts/skeleton.py --lang <code> --labels <file>`), so the reply and the page use the same words.

With a language that has a pack, `--labels <file>` changes single words: the file holds only those keys.

## Build and hand over the page

Run one of these two commands:

```
python3 -B scripts/build.py <report>.json --artifact -o <page>.html   # to publish on a host such as Claude artifacts
python3 -B scripts/build.py <report>.json -o <page>.html              # to hand over an HTML file
```

- Add `--labels <file>` to either command for a language without a pack (see "Words on the page").
- Use `--artifact` when you publish the page on a host that wraps what it publishes in its own document skeleton, as Claude artifacts do. Leave it out when you hand over an HTML file, which then opens in a browser as is.
- Where you can publish the page, publish it and give the link. Otherwise save the HTML file and give its location.
- The page loads its scripts from jsDelivr when it opens, so the user needs a network connection, and a host must allow jsDelivr.
- Where the host refuses the clipboard, the page asks the user to select the text in the box under the decisions and copy it by hand.

The page keeps the user's unsent answers in the user's browser, under the page's `title` and `asOf`. A rebuilt page with the same `title` and `asOf` shows those answers again; a page with a new `asOf` starts empty. Give each new report the time it was written as `asOf`, so that answers to an older report do not appear on a newer one. Nothing the user enters reaches you until the user pastes it into the session.

## When the answers arrive

Treat each numbered answer as the answer to the question with that number, and a message as part of the answer it follows. A question marked with the no-answer word (the `copyNoAnswer` label) is still open. If an answer names a letter that is not an option of its question, or the text does not match the questions you asked, ask the user what they meant instead of guessing.
