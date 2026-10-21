# wakariyasu

[日本語](README.md)

wakariyasu is a Claude Code plugin for people who work with AI agents in Japanese. It makes the agent write Japanese that someone who has not followed the work can understand. Its skills also work in other agents such as Codex and Cursor.

**wakariyasu is for Japanese text only.** Its rules and skills are written in Japanese, and they shape Japanese output. If your agent writes in English, wakariyasu will not help you.

The name is the Japanese わかりやすい (wakariyasui), "easy to understand."

## The problem it solves

When an agent works on a long task, its reports and questions tend to use labels it coined along the way and assumptions it settled on mid-task. Someone reading the report later has to ask, "So what actually happened?"

For example, a report like this (translated from Japanese):

> Went with option B, injecting via the hook, and dropped the dependencies.

becomes, with wakariyasu:

> The rules are now loaded at session start by the plugin's hook (a script that runs automatically at set points). I removed the declared dependency on yomiyasu, because with the declaration in place, wakariyasu fails to load at all in environments where yomiyasu is not installed.

wakariyasu applies this both to the agent's replies to you and to the documents the agent writes, such as READMEs, specs and commit messages.

## Rules and skills

wakariyasu has two kinds of parts.

- **Rules** are writing guidelines. Claude Code loads them at the start of every session, and they apply to every reply and document. You do not need to ask for them.
- **Skills** are procedures for specific situations. The agent uses one when you ask with phrases like those in the table below, or when it judges that it is reporting status or handing over a document.

## What each part does

| Situation | What you might say | Part | What it does |
|---|---|---|---|
| Any reply | (always applies) | rule `writing-to-user` | Makes the agent use words and structure that a reader without the history can follow |
| You want to know where things stand | 「現状は？」 (where are we?), 「残タスクは？」 (what's left?) | skill `session-status` | Makes the agent report the goal, each task with its state, and the decisions it needs from you, in a fixed format |
| You did not understand a reply | 「分かりやすく」 (clearer, please), 「つまり？」 (so, in short?), 「〜とは？」 (what is …?) | skill `explain-clearly` | Makes the agent restate its last reply or an unclear term. "Briefly" gets a shorter answer; "so a child could understand" gets more background |
| The agent writes a document | (always applies) | rule `writing-documents` | Makes the agent write READMEs, specs, SKILL.md files, commit messages and the like so that each one makes sense on its own |
| Removing meta narrative | 「メタ記述を除いて」 (remove the meta narrative) | skill `remove-meta-narrative` | Finds sentences in which a document talks about itself or about how it was made, such as "This chapter explains…" or "Following the review comments…", and rewrites them |
| Before sharing a document | 「公開前に見て」 (check it before publishing) | skill `review-for-readers` | Has the agent start a subagent, give it only the document with none of the history, and fix whatever that reader stumbled on |

Two more rules: `polishing` covers how to tidy Japanese text before handing it over and how to choose its writing style, and `session-status` says when to use the `session-status` skill.

## Writing style

Some style choices in Japanese depend on the kind of text: kana versus kanji for certain words, how numbers are written, ending a line with a bare noun phrase (体言止め, common in bullet points and commit messages), and plain versus polite verb endings. wakariyasu does not fix these. It has the agent choose them in this order:

1. Your instructions, including those in CLAUDE.md or AGENTS.md
2. The style already used in the same document or repository
3. A default for each kind of text, listed in [`references/styles.md`](references/styles.md)

To fix a style, add a line to CLAUDE.md, such as 「数字は算用数字で書く」 ("write numbers as Arabic numerals").

## Working with yomiyasu

[yomiyasu](https://github.com/nanaism/yomiyasu) (by nanaism, a separate project) is a skill that fixes unnatural metaphors, mismatched subjects and predicates, and similar problems in AI-written Japanese.

If yomiyasu is installed in your agent, wakariyasu has the agent run long replies and documents through it before handing them over, and tell yomiyasu what kind of text it is.

wakariyasu also works without yomiyasu. The agent then checks for overlong sentences, subjects far from their predicates, empty decorative words, and sentences that only announce what comes next, and fixes them itself.

## Installing

### As a Claude Code plugin

In Claude Code, run the two commands below. The first registers this repository as a marketplace (a source of plugins). The second installs wakariyasu from it.

```text
/plugin marketplace add kulikala/wakariyasu
/plugin install wakariyasu@wakariyasu
```

This installs both the rules and the skills. yomiyasu is available from the same marketplace:

```text
/plugin install yomiyasu@wakariyasu
```

To check that it works, ask 「現状は？」 in a new session. A report with headings such as 「現在のゴール」 (current goal) and 「タスク」 (tasks) means wakariyasu is active.

### Skills only, for any agent

Use the `gh skill` command of the GitHub CLI (a preview feature):

```sh
gh skill install kulikala/wakariyasu --all --scope user --agent claude-code
```

Set `--agent` to your agent (`codex`, `cursor`, `github-copilot` and so on). `--scope user` installs into your home directory so the skills work in every folder.

With only the skills installed, the rules are not loaded at session start. Each skill still carries its own copy of the rules it needs and reads it when it runs.

### The rules in agents other than Claude Code

[`AGENTS.snippet.md`](AGENTS.snippet.md) contains all four rules as one text. Paste it into a file your agent reads every session, such as AGENTS.md.

## For contributors

```text
rules/                  the four rules
references/styles.md    style defaults for each kind of text
skills/                 the skills (session-status, explain-clearly, remove-meta-narrative, review-for-readers)
hooks/                  the hook that loads the rules at session start when installed as a plugin
AGENTS.snippet.md       the rules as one text, for agents other than Claude Code
bin/build               copies rules/ and references/ into the skills, and builds AGENTS.snippet.md
```

Edit the rules and style defaults only in `rules/` and `references/`. Then run `bin/build` to refresh the copies inside the skills and `AGENTS.snippet.md`. `bin/build --check` fails if any copy differs from `rules/` or `references/`.

## License

MIT
