# wakariyasu

English | [日本語](README.ja.md)

[![Release](https://img.shields.io/github/v/release/kulikala/wakariyasu)](https://github.com/kulikala/wakariyasu/releases/latest) [![License: MIT](https://img.shields.io/github/license/kulikala/wakariyasu)](LICENSE)

wakariyasu is a plugin for Claude Code and the Claude apps that makes an AI agent write for someone who hasn't followed its work. It covers the agent's reports and questions to you, and the documents it writes: READMEs, specs, commit messages and the like.

Give an agent a long task and its reports fill up with names it made up along the way and assumptions it settled on without telling you. You end up asking, "So what does that mean?" wakariyasu adds rules and skills that make the agent say what it did, in words you already know.

## What changes

You ask an agent to fix a slow product list screen and step away. When you come back, this is the report waiting for you.

**Without wakariyasu**

> Went with plan B and moved the cache to v2. The screen is lighter now. Only the zero-stock problem is left.

**With wakariyasu**

> For the slow product list screen, I now keep product information in the server's memory for 5 minutes, so the screen no longer reads from the database on every display. The time to display the screen went from 2.1 seconds to 0.4 seconds.
>
> One issue remains: the screen layout breaks for products whose stock is 0.

"Plan B", "v2" and "the zero-stock problem" are gone, replaced by what was done and what is wrong, and "lighter" became a number.

<details>
<summary>Questions that need your decision</summary>

**Without wakariyasu**

> Which TTL for the cache?

**With wakariyasu**

> **1. Whether to keep product information on the server for 5 minutes or 1 hour**
>
> While speeding up the product list screen, I need to decide how long to keep product information on the server. How long a stock count may lag on screen depends on how the shop operates, so this is your call.
>
> | Option | Background and what happens if chosen |
> |---|---|
> | A (recommended) | 5 minutes. Stock counts are shown up to 5 minutes late. The screen displays in 0.4 seconds. Recommended because a sold-out product shows as in stock for 5 minutes at most. |
> | B | 1 hour. The screen displays in 0.3 seconds, but stock counts lag by up to 1 hour. |

You can answer with just the number and the letter: "1 is A".

</details>

<details>
<summary>Documents the agent writes</summary>

**Without wakariyasu** (from a design document)

> Following the review comments, this chapter organizes the cache policy. Details below.

**With wakariyasu**

> Product information is kept in the server's memory for 5 minutes. Information older than 5 minutes is read again from the database the next time it is displayed.

The first version only makes sense to someone who saw the review and reads further down. The second states the policy on its own.

</details>

## What's included

wakariyasu is a set of instructions for the agent. **Rules** apply to every reply and document without being asked. **Skills** handle particular jobs; the agent picks one when you ask in words like the examples below, or when the job comes up.

| When | Say, for example | Used | What the agent does |
|---|---|---|---|
| Every reply | (always) | Rule [`writing-to-user.md`](skills/writing-rules/rules/writing-to-user.md) | Writes replies someone who hasn't followed the work can understand |
| Every document | (always) | Rule [`writing-documents.md`](skills/writing-rules/rules/writing-documents.md) | Writes documents that make sense on their own |
| Before handing over text | (always) | Rule [`polishing.md`](skills/writing-rules/rules/polishing.md) | Polishes what it wrote |
| You want the status | "Where do things stand?" | `session-status` | Reports the goal, the tasks and their state, and asks what it needs you to decide |
| A reply is unclear | "So what does that mean?" | `explain-clearly` | Says it again in plainer words, shorter or with more background |
| A document talks about itself | "Remove the meta-narrative" | `remove-meta-narrative` | Removes sentences about the document or how it was made |
| Before you share a document | "Review it as a reader" | `review-for-readers` | Has a fresh agent read only the document, and fixes where it got stuck |
| You want to see changes | "Show me the diff" | `show-changes` | Turns a diff, across repositories if needed, into one page |
| You want a page to read | "Make it a page" | `compose-page` | Builds an HTML page around what the reader wants to know |
| A skill needs checking | "Check this skill" | `clarify-skill` | Checks a skill as instructions for an agent, and rewrites it on request |
| You want the session written up | "Summarize this session" | `summarize-session` | Writes what the session found, decided or was told, for people who weren't there |
| You have a transcript | "Pull out the insights" | `extract-insights` | Turns meeting records and documents into insights others can use |
| Checking phrasing | "Check the phrasing" | `check-terms` | Finds phrases to avoid from the lists for the document's language |

Each reply and document follows the conventions of its own language, from the language packs in [`skills/writing-rules/lang/`](skills/writing-rules/lang/). Japanese and English are included.

## Installation

- **Claude Code:** use the Claude Code plugin.
- **claude.ai chat and Cowork:** use the Claude apps.
- **Codex, Cursor, GitHub Copilot and other agents:** install the skills with `npx skills add`, `gh skill install` or `npx openskills install`, then paste the rules into the agent's instruction file. All three install the same skills; use whichever command you have (`npx` comes with Node.js, `gh` is the GitHub CLI).

To check the installation, start a new session and ask "Where do things stand?". A report with headings such as "Current goal" and "Tasks" means it worked.

<details>
<summary>1. Claude Code plugin</summary>

Run these in Claude Code. The rules and the skills are both installed, and the rules load at the start of every session.

```text
/plugin marketplace add kulikala/wakariyasu
/plugin install wakariyasu@wakariyasu
```

To update, run these in a terminal and restart Claude Code.

```sh
claude plugin marketplace update wakariyasu
claude plugin update wakariyasu@wakariyasu
```

</details>

<details>
<summary>2. Claude apps and Cowork</summary>

In claude.ai on the web or in the desktop app, open **Customize > Plugins**, enter `kulikala/wakariyasu` under **Add > Add marketplace**, and install wakariyasu. It is installed to your account, so it also works in the phone app and in Cowork.

Cowork loads the rules like Claude Code. Chat does not: to apply them to every reply there, paste the whole of [`AGENTS.snippet.md`](AGENTS.snippet.md) into **Settings > Your Claude > Instructions**, or into a project's instructions. If it does not fit, paste only its section "Write replies that someone who has not followed the session can understand", keeping the first and last comment lines around it.

</details>

<details>
<summary>3. <code>npx skills add</code></summary>

Install the skills with [skills](https://github.com/vercel-labs/skills).

```sh
# Install
npx skills add kulikala/wakariyasu --skill '*' -g

# Update
npx skills update -g
```

`--skill '*'` installs every skill; install all of them, since they share the rules in `writing-rules`. `-g` installs into your home directory so that the skills work in every folder. `-a` chooses the agents to install for.

Then [paste the rules](#paste-the-rules).

</details>

<details>
<summary>4. <code>gh skill install</code></summary>

Install the skills with the GitHub CLI's `gh skill` (a preview feature).

```sh
# Install
gh skill install kulikala/wakariyasu --all --scope user

# Update
gh skill update --all
```

`--all` installs every skill. `--scope user` installs into your home directory so that the skills work in every folder. `--agent` chooses the agents to install for.

Then [paste the rules](#paste-the-rules).

</details>

<details>
<summary>5. <code>npx openskills install</code></summary>

Install the skills into the repository you work in with [OpenSkills](https://github.com/numman-ali/openskills), and list them in its AGENTS.md.

```sh
# Install
npx openskills install kulikala/wakariyasu -y
npx openskills sync -y

# Update
npx openskills update
npx openskills sync -y
```

`-y` on `install` installs every skill without asking; on `sync` it writes them all to AGENTS.md without asking. `--global` installs into your home directory instead.

Then [paste the rules](#paste-the-rules) into the AGENTS.md that `sync` wrote.

</details>

### Paste the rules

Methods 3 to 5 install only the skills. Skills read the rules when they run, but for the rules to shape every reply and document, paste the whole of [`AGENTS.snippet.md`](AGENTS.snippet.md) into the instruction file the agent always reads (AGENTS.md for Codex, custom instructions elsewhere). The language packs are not pasted; the agent reads them from the installed `writing-rules` skill.

Updating the skills does not update what you pasted. After an update, replace everything from `<!-- wakariyasu:AGENTS.snippet.md -->` to `<!-- /wakariyasu:AGENTS.snippet.md -->` with the latest `AGENTS.snippet.md`.

## Requirements

> [!NOTE]
> Python 3 is needed to build the pages of `show-changes` and `session-status`, and to print the templates for a language without a language pack. The rules and the other skills need nothing else.

## How it works

<details>
<summary>Language packs and fixed words</summary>

The rules and skills are written in English and apply to writing in any language. What only one language needs lives in its pack, [`skills/writing-rules/lang/<code>/`](skills/writing-rules/lang/): `reply.md` for replies, `documents.md` for documents and `skills.md` for the skills. There is no language setting. The agent picks the pack for each thing it writes by that thing's language, so a request in Japanese for an English README gets a reply written with the Japanese pack and a README written with the English one.

Headings, column names and state words are not typed by the agent. Each pack keeps them in `labels.json`, and the tools fill them in. For a language without a pack, the agent creates the list of words with `--init`, translates it, and passes it with `--labels`.

The lists of phrases to avoid are in [`skills/check-terms/lang/`](skills/check-terms/lang/); `sh skills/check-terms/scripts/check-terms <file>` checks a document against them.

</details>

<details>
<summary>Working with a prose-refining skill</summary>

wakariyasu looks at whether a reader without the history can follow the words and content. A prose-refining skill fixes how sentences are written. If one for the document's language is installed, the agent runs documents for people through it after applying wakariyasu's rules. Replies are not. wakariyasu works without one.

</details>

## Contributing

The folder layout, the checks (`dev/test`) and the release steps are in the [development guide](docs/development.md). Changes by version are in [CHANGELOG.md](CHANGELOG.md).

## Acknowledgments

Some rules draw on the Japanese proofreading skill [yomiyasu](https://github.com/nanaism/yomiyasu) (nanaism/yomiyasu, MIT license).

## License

MIT
