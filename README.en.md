# wakariyasu

[日本語](README.md)

wakariyasu is a Claude Code plugin that makes an AI agent write Japanese that someone who has not followed the work can understand. It covers both the agent's reports and questions to you, and the documents the agent writes, such as READMEs, specs and commit messages. Its skills also work in other agents such as Codex and Cursor. The name comes from the Japanese わかりやすい (wakariyasui), "easy to understand."

**wakariyasu only affects Japanese output.** Its guidance deals with problems typical of Japanese text, such as omitted subjects, pointing words (これ, それ) whose referent is unclear, and style choices that only exist in Japanese. If your agent writes in English, wakariyasu will not help you.

## The problem it solves

When an agent works on a long task, its reports tend to use labels it coined along the way and assumptions it settled on mid-task. Someone reading the report later has to ask, "So what actually happened?"

Here is a report at the end of a web-app fix, translated from Japanese.

Without wakariyasu:

> Went with option A and moved the cache to v2. Only that error is left.

With wakariyasu:

> The product list page was slow because it read product data from the database on every view. It now keeps that data for five minutes. The page now loads in 0.4 seconds instead of 2.1. One bug is left: the page layout breaks for products that are out of stock.

The first report only makes sense to someone who watched the work ("option A", "v2", "that error"). The second says what was done, what changed and what is left, on its own.

## Rules and skills

wakariyasu is made of instructions for the agent, written in Markdown. There are two kinds.

- **Rules** are writing guidelines. In Claude Code they are loaded at the start of every session, through a hook (a script Claude Code runs automatically at set points), and the agent follows them in every reply and document. You do not need to ask.
- **Skills** are step-by-step procedures for specific situations. The agent uses one when you ask with phrases like those in the table below, and also picks one on its own when it writes a status report or finishes a document to hand over.

## What each part does

The phrases are what you would type in Japanese. Any wording with the same meaning works.

| Situation | What you might say | Part | What it does |
|---|---|---|---|
| Any reply | (always applies) | rule `writing-to-user` | The agent uses words and structure that a reader without the history can follow |
| You want to know where things stand | 「現状は？」 (where are we?), 「残タスクは？」 (what's left?) | skill `session-status` | The agent reports the goal, each task with its state, and the decisions it needs from you, in a fixed format |
| You did not understand a reply | 「分かりやすく」 (clearer, please), 「つまり？」 (so, in short?), 「〜とは？」 (what is …?) | skill `explain-clearly` | The agent restates its last reply or an unclear term. Ask for a brief version and you get a shorter answer; ask for it explained "so a child could understand" and you get more background |
| The agent writes a document | (always applies) | rule `writing-documents` | The agent writes READMEs, specs, SKILL.md files, commit messages and the like so that each one makes sense on its own |
| Removing meta narrative | 「メタ記述を除いて」 (remove the meta narrative) | skill `remove-meta-narrative` | The agent finds sentences in which a document talks about itself or about how it was made, such as "This chapter explains…" or "Following the review comments…", and rewrites them |
| Before sharing a document | 「公開前に見て」 (check it before publishing) | skill `review-for-readers` | The agent gives only the document to a separate agent (a subagent) that knows nothing of the work, and fixes whatever that reader stumbled on. Where subagents are not available, the agent rereads the document itself and says so |

There is one more rule, `polishing`. It covers how to tidy Japanese text before handing it over, and how to choose the writing style described below.

The three rules add about 4,000 Japanese characters (a few thousand tokens) to each session. `review-for-readers` starts a subagent, which costs extra time and tokens.

## Writing style

Some style choices in Japanese depend on the kind of text: kana or kanji for certain words, how numbers are written, ending a line with a bare noun phrase (体言止め, common in bullet points and commit messages), and plain or polite verb endings. wakariyasu does not fix these. It has the agent choose them in this order:

1. Your instructions, including those in CLAUDE.md (Claude Code's project instruction file) or AGENTS.md (the same kind of file for other agents)
2. The style already used in the same document or repository
3. wakariyasu's default for each kind of text, listed in [`references/styles.md`](references/styles.md)

To fix a style, add a line to CLAUDE.md, such as 「数字は算用数字で書く」 ("write numbers as Arabic numerals").

## Working with yomiyasu

The agent first polishes the Japanese it writes, following wakariyasu's rules. Some of the checks in those rules are based on those of [yomiyasu](https://github.com/nanaism/yomiyasu) (nanaism/yomiyasu, a Japanese polishing skill by a different author). Where yomiyasu is installed, the agent also calls it when finishing documents that people will read, such as READMEs and manuals. wakariyasu works without yomiyasu.

yomiyasu is a separate plugin from wakariyasu. To use both, install yomiyasu as its author's repository describes. In Claude Code, that is:

```text
/plugin marketplace add nanaism/yomiyasu
/plugin install yomiyasu@yomiyasu
```

## Installing

### As a Claude Code plugin (recommended)

In Claude Code, run the two commands below. The first registers this repository as a marketplace (a source of plugins). The second installs the plugin named wakariyasu from the marketplace named wakariyasu (the form is `plugin@marketplace`).

```text
/plugin marketplace add kulikala/wakariyasu
/plugin install wakariyasu@wakariyasu
```

This installs both the rules and the skills.

To check that it works, ask 「現状は？」 in a new session. A report with headings such as 「現在のゴール」 (current goal) and 「タスク」 (tasks) means wakariyasu is active.

### In other agents

For Codex, Cursor, GitHub Copilot and others, install the skills and the rules separately.

Install the skills with the `gh skill` command of the GitHub CLI (a preview feature):

```sh
gh skill install kulikala/wakariyasu --all --scope user --agent codex
```

`--all` installs all four skills (session-status, explain-clearly, remove-meta-narrative and review-for-readers). `--scope user` installs them in your home directory so they work in every folder. Set `--agent` to your agent (`codex`, `cursor`, `github-copilot` and so on).

For the rules, paste the contents of [`AGENTS.snippet.md`](AGENTS.snippet.md), which joins the three rules into one text, into the instruction file your agent reads every session, such as AGENTS.md for Codex, or your agent's custom instructions.

If you install only the skills and skip the rules, nothing applies to everyday replies or to documents the agent writes. The skills run only when you ask or when the agent picks them, and then each skill reads its own copy of the rules it needs.

## For contributors

```text
rules/                  the rules (writing-to-user, writing-documents, polishing)
references/styles.md    style defaults for each kind of text
skills/                 the skills (session-status, explain-clearly, remove-meta-narrative, review-for-readers)
hooks/                  the hook that loads the rules at session start when installed as a plugin
AGENTS.snippet.md       the rules as one text, for agents other than Claude Code
bin/build               copies rules/ and references/ into the skills, and builds AGENTS.snippet.md
```

Edit the rules and style defaults only in `rules/` and `references/`. Then run `bin/build` to refresh the copies inside the skills and `AGENTS.snippet.md`. `bin/build --check` fails if any copy differs from `rules/` or `references/`.

## License

MIT
