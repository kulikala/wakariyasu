# wakariyasu

[日本語](README.md)

wakariyasu is a plugin that makes the Japanese an AI agent writes understandable to someone who has not followed the work.

When an agent works on a long task, its reports and questions tend to carry the names and assumptions it made up along the way. The person reading them ends up asking, "So what does this actually mean?" wakariyasu shapes both the agent's replies to the user and the documents the agent writes so that a reader without that history can follow them.

wakariyasu is written for Japanese text. Its rules and skills are in Japanese.

## When it helps

| Situation | What you might say | Handled by | What it does |
|---|---|---|---|
| Every reply | (applies without asking) | rule `writing-to-user` | Has the agent write replies in words and shapes a reader without the history can follow |
| You want to know where things stand | 「現状は？」 (where are we?), 「残タスクは？」 (what's left?) | skill `session-status` | Has the agent report the goal, the tasks and their states, and the decisions it needs from you, in a fixed format |
| You did not understand a reply | 「分かりやすく」 (make it clearer), 「つまり？」 (in short?), 「〜とは？」 (what is …?) | skill `explain-clearly` | Has the agent restate the last reply or the unclear term, shorter or with more background depending on what you asked |
| The agent writes a document | (applies without asking) | rule `writing-documents` | Has the agent write READMEs, specs, SKILL.md files, commit messages and the like so each one stands on its own |
| Removing traces of the work from a document | 「メタ記述を除いて」 (remove the meta narrative) | skill `remove-meta-narrative` | Finds and fixes sentences in which a document talks about itself or about how it was made, such as "This chapter explains…" or "Following the review comments…" |
| Before handing a document to someone | 「公開前に見て」 (check before publishing) | skill `review-for-readers` | Gives the document alone to a separate agent that has no history of the work, and fixes the places where that reader got stuck |

In Claude Code, the rules are loaded at the start of every session and apply to every reply and document. The skills run when you ask with words like those above, and when the agent decides it is reporting status or handing over a document.

## Choosing the writing style

Choices such as kana or kanji, numerals, ending a line with a noun, and plain or polite form differ by kind of text. wakariyasu does not fix them. The agent chooses them in this order:

1. The user's instructions, including those in CLAUDE.md or AGENTS.md
2. The style already used in the same document or repository
3. A default for the kind of text (reply to the user, commit and PR, README, rules and specs, and so on)

To fix a style, add one line to CLAUDE.md, for example 「数字は算用数字で書く」 (write numbers in Arabic numerals).

## Working with yomiyasu

[yomiyasu](https://github.com/nanaism/yomiyasu) (nanaism/yomiyasu) is a skill that fixes unnatural metaphors, mismatched subjects and predicates, and similar problems in Japanese written by AI. When yomiyasu is installed, wakariyasu has the agent run long replies and documents through yomiyasu, passing the kind of text, before handing them over.

wakariyasu works without yomiyasu. In that case the agent checks sentence length, the distance between subject and predicate, decorative wording, and sentences that only announce what comes next, and fixes them itself.

## Installing

### Claude Code (as a plugin)

```text
/plugin marketplace add kulikala/wakariyasu
/plugin install wakariyasu@wakariyasu
```

This installs both the rules and the skills. yomiyasu is available from the same marketplace:

```text
/plugin install yomiyasu@wakariyasu
```

### Skills only

The skills also work with other agents such as Codex, Cursor and GitHub Copilot.

```sh
gh skill install kulikala/wakariyasu --all --scope user --agent claude-code
```

Choose your agent with `--agent`. When only the skills are installed, the rules are not loaded on their own, but each skill reads its own copy of the rules in its `references/` folder.

### The rules in agents other than Claude Code

[`AGENTS.snippet.md`](AGENTS.snippet.md) contains the four rules joined into one text. Paste it into a file your agent reads every time, such as AGENTS.md.

## Contents

```text
rules/                  rules loaded every session (4)
  writing-to-user.md    how to write replies to the user
  writing-documents.md  how to write documents
  polishing.md          how to polish Japanese before handing it over, and how to choose the style
  session-status.md     when to use session-status for reports
skills/                 skills (4)
references/styles.md    style defaults for each kind of text
hooks/                  hook that loads the rules when installed as a plugin
AGENTS.snippet.md       the rules as one text, for agents other than Claude Code
bin/build               builds the skills' copies and AGENTS.snippet.md from rules/ and references/
```

Edit the rules and style defaults in `rules/` and `references/`, then run `bin/build` to rebuild the copies. `bin/build --check` fails if any copy differs from its source.

## License

MIT
