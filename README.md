# wakariyasu

English | [日本語](README.ja.md)

wakariyasu is a plugin for Claude Code and the Claude apps that adds rules and skills to an AI agent so that the Japanese it writes can be understood by someone who has not followed its work. This applies to the agent's reports and questions to the user, and to the documents the agent writes, such as READMEs, specs and commit messages.

When you hand an agent a long task, its reports and questions tend to be written in terms of names the agent coined along the way and assumptions it settled on midway. The person reading the report has to ask, "So what does that mean?" wakariyasu adds instructions that make the agent write in a form that a reader who does not know the history can follow.

## Before and after installing

Suppose a user asks an agent, "The product list screen is slow, please fix it," and steps away. When the user comes back, they read the agent's report and questions and the documents the agent wrote. Here they are before and after installing wakariyasu.

### Progress report

**Before installing**

> Went with plan B and moved the cache to v2. The screen is lighter now. Only the zero-stock problem is left.

**After installing**

> For the slow product list screen, I now keep product information in the server's memory for 5 minutes, so the screen no longer reads from the database on every display. The time to display the screen went from 2.1 seconds to 0.4 seconds.
>
> One issue remains: the screen layout breaks for products whose stock is 0.

For each term in the report before installing, here is what the user thinks and how the report after installing writes it.

| Term in the report before installing | What the user thinks | How the report after installing writes it |
|---|---|---|
| Plan B | What is plan A, and what is plan B? | States what was done |
| v2 | A name that came up during the work; no idea what it refers to | Drops the name and states the content |
| Lighter | How much faster is it? | States the display time before and after, in numbers |
| Zero-stock problem | What kind of problem is it? | States what the defect does |

### Questions for a decision

This is a moment before the report, partway through the work, when the agent needs the user to decide something.

**Before installing**

> Which TTL for the cache?

**After installing**

> **1. Whether to keep product information on the server for 5 minutes or 1 hour**
>
> While speeding up the product list screen, a decision came up on how long to keep product information on the server. How long a stock count may lag on screen depends on how the shop operates, so I need you to decide.
>
> | Option | Background and what happens if chosen |
> |---|---|
> | A (recommended) | 5 minutes. Stock counts are shown up to 5 minutes late. The screen displays in 0.4 seconds. The reason for recommending it: a product that has sold out keeps showing as in stock for no more than 5 minutes. |
> | B | 1 hour. The screen displays in 0.3 seconds, but stock counts lag by up to 1 hour. |

The question after installing states what is being decided, why the user is the one to decide, and what happens with each choice. The user can answer with only the question number (1) and the option letter in the table (A or B), such as "1 is A".

### Written documents

**Before installing** (a passage from a design document)

> Following the review comments, this chapter organizes the cache policy. Details below.

**After installing**

> Product information is kept in the server's memory for 5 minutes. Information older than 5 minutes is read again from the database the next time it is displayed.

The sentence before installing cannot be understood without reading the exchange in which it was written (the review comments) and another place in the document (below). The sentence after installing states the policy on its own.

## Rules and skills

wakariyasu is made of instructions to the agent, in two kinds.

- A **rule** is an instruction that states a writing policy. In Claude Code, rules are loaded at the start of every session and applied to every reply and document. You do not need to ask for them.
- A **skill** is an instruction that states a procedure for a particular situation. The agent chooses and uses a skill on its own when the user asks in words listed in the table in the "When each is used" section, or when the agent writes a report or finishes a document to hand over.

## When each is used

| Situation | Example words | Instruction used | What it does |
|---|---|---|---|
| Ordinary replies | (applies without being asked) | Rule [`writing-to-user.md`](skills/writing-rules/rules/writing-to-user.md) | Has the agent write replies in words and a form that someone who has not followed the work can understand |
| You want to know the status | "Where do things stand?" "What's left?" | Skill `session-status` | Has the agent report what it is aiming for and its tasks and their states in a fixed form, with a question attached if it needs you to decide something. The report can also be a page where you pick an option and copy your answers |
| A reply is unclear | "Explain it plainly" "So what does it mean?" "What is X?" "What is the difference between X and Y?" | Skill `explain-clearly` | Has the agent restate its previous reply, or a term in the reply that was unclear. For "briefly" it shortens; for "so a child could understand" it adds the background |
| Having the agent write a document | (applies without being asked) | Rule [`writing-documents.md`](skills/writing-rules/rules/writing-documents.md) | Has the agent write READMEs, specs, SKILL.md files, commit messages and the like so that they can be understood from the document alone |
| Removing meta-narrative from a document | "Remove the meta-narrative" | Skill `remove-meta-narrative` | Has the agent find and fix meta-narrative (sentences in which a document talks about itself or how it was made, such as "this chapter covers..." or "following your comment...") and the agent's work-in-progress output ("X was not reached" "X was unknown"). In work logs and progress records, the record of the work stays |
| Before handing a document to someone | "Check it before release" "Review it through a reader's eyes" | Skill `review-for-readers` | Has a separate agent (a subagent) that does not know the history read only the document, and has the agent fix the places where that reader got stuck. It starts a subagent, so it uses more time and tokens. An agent that cannot start subagents rereads the document itself and says so in its report |
| Showing changes to a person | "Show me the diff" "Make the changes into a page" (applies without being asked after work that changes files) | Skill `show-changes` | Has the agent turn the before-and-after diff, across repositories and folders, into one HTML page. In Claude's environment the page is presented as an artifact; where artifacts are unavailable it is saved as an HTML file |
| Making a page for people to read | "Make it a page" "Make it an artifact" "Make it easier to read" (applies without being asked when a page for people is made) | Skill `compose-page` | Has the agent build an HTML page that conveys content to people, such as a report or an organized set of material, so that a reader who does not know how it was made can read the conclusion, the state and the differences between items from the screen. It has the agent prepare both a light and a dark display |
| Making a skill clearer | "Check this skill" "Rewrite the skill" (applies without being asked after a skill is written) | Skill `clarify-skill` | Has the agent check a skill (SKILL.md and the references it reads) for whether an agent reading it can decide from the purpose, and plan how to fix it. On request it rewrites the skill |
| Leaving the session's content as a document | "Summarize this session" "Summarize what we found" "Extract the feedback" | Skill `summarize-session` | Has the agent turn what the session examined, found, was told and did into a document that someone who was not in the session can read and use. It has the agent infer from the request what the user wants and write in the applicable mode: structuring what was examined as a document, composing findings as insights, organizing feedback by intent and response, or keeping a work log. If several apply it splits the documents, and if none applies it builds a structure with the modes as a guide |
| Extracting insights from text | "Extract insights from this transcript" "Summarize what the minutes tell us" | Skill `extract-insights` | Has the agent extract, from text such as a meeting or interview transcript, a record of remarks or an article, insights that someone who was not there can later use for decisions. Each insight is one sentence, with its kind (confirmed fact, claim or decision) and its background, supplement, certainty and source. It has the agent write what can be said from the remarks, not a collection of quotes or a summary. `summarize-session` handles summarizing what was found in the current session |
| Checking Japanese phrasing | "Check the phrasing" (applies without being asked before handing over a Japanese document written to a file) | Skill `check-terms` | Has the agent search a document for phrases that Japanese does not use and for phrases where another word may read more naturally depending on context, and replace them with the alternative when they are used in the listed sense |

`show-changes` needs Python 3 to build its page. The other skills and the rules do not use Python.

There is one more rule, [`polishing.md`](skills/writing-rules/rules/polishing.md), which states how to polish a piece of writing before handing it over.

Rules and skills state in English the content that applies to writing in any language. Content added only when writing in Japanese (the "Choosing notation" section below, how to check phrasing, how to use yomiyasu and so on) is kept in a folder for each language, [`skills/writing-rules/lang/ja/`](skills/writing-rules/lang/ja/). There is no setting for switching languages. If a folder exists for the language of the reply or document being written, the agent reads and uses the files in that folder before writing. An English folder, [`skills/writing-rules/lang/en/`](skills/writing-rules/lang/en/), also exists.

The lists of phrasing are in the folder of the skill `check-terms`. The agent writes with the lists in view, and checks a document written to a file with the script `check-terms`, which searches the document for phrases from the lists (run it with `sh skills/check-terms/scripts/check-terms <file>`).

- [`terms.tsv`](skills/check-terms/lang/ja/terms.tsv): phrases Japanese does not use (translation-like words such as 「コマンドを打つ」「旗」「導入」, and words coined during the work), with the words to use instead. When `check-terms` finds one, the check fails (exit code 1).
- [`terms-caution.tsv`](skills/check-terms/lang/ja/terms-caution.tsv): phrases that are not wrong but where another word may read more naturally depending on context, with candidate words. For example, there are places where 「規則を適用する」 reads more naturally than 「規則を当てる」, and places where naming a table by its content (「料金の表」) is clearer than by its position (「次の表」). `check-terms` prints these marked "(check in context)" but does not fail the check.

The rules and references are in the folder of the skill `writing-rules`. The references cover how to write a question for a decision, how to write instructions (how to write documents that agents read, such as skills and rules), how to write a README (the sections of a public README) and how to write a changelog (what a public changelog states). In Claude Code and Cowork, the rules and the way to write a question for a decision are loaded once per session, together with the list of language folders. The files in each language folder (including the notation tables and the handling of phrasing) and the guides for writing instructions, READMEs and changelogs are read by the agent when needed.

## Choosing notation

How kana and kanji are used, how numbers are written, noun-ending sentences, and the plain and polite styles vary with the kind of writing. wakariyasu does not fix notation uniformly; it has the agent choose in this order.

1. The user's instructions (including instructions in CLAUDE.md or AGENTS.md)
2. The way already used in the same document or the same repository
3. The default wakariyasu sets for each kind of writing. For example, replies to the user are written in polite-style sentences, and the change lines of a commit or PR may end in a noun. The table for each kind is in [`styles.md`](skills/writing-rules/lang/ja/styles.md)

For word choice too, the agent picks per document between standard notation and Sino-Japanese notation. Standard notation does not lean toward native Japanese words or Sino-Japanese words but picks the words that suit the context and the reader. Sino-Japanese notation centers on Sino-Japanese words as far as meaning and readability are not lost. If the user's instructions and the existing style do not decide it, the agent picks whichever conveys the meaning better from the document's purpose and reader.

To fix a particular style, specify it in one line in CLAUDE.md. For example, specifying "Write numbers in Arabic numerals" or "Write the README in polite style" takes precedence over the defaults.

## Combining with yomiyasu

What wakariyasu's rules look at is words and content that someone who does not know the history can follow. yomiyasu finely corrects how Japanese sentences are written, such as unnatural metaphors and mismatched subjects and predicates. The agent first polishes the Japanese it writes with wakariyasu's rules. In an environment where [yomiyasu](https://github.com/nanaism/yomiyasu) (nanaism/yomiyasu, a Japanese proofreading skill) is installed, the agent calls the yomiyasu skill without being asked when it finishes a document for people, such as a README or a procedure. The situations in which it is called are in [`polishing.md`](skills/writing-rules/lang/ja/polishing.md) in the Japanese folder. It is not called for replies to the user. wakariyasu works without yomiyasu.

yomiyasu is a separate plugin from wakariyasu. To use them together, install it as its author's repository describes. In Claude Code, run these two.

```text
/plugin marketplace add nanaism/yomiyasu
/plugin install yomiyasu@yomiyasu
```

## Installation

In Claude Code, install with the method in "4. Claude Code plugin"; in claude.ai chat and Cowork, use "5. Claude apps and Cowork". For agents such as Codex, Cursor and GitHub Copilot, install the skills with one of methods 1 to 3, then paste the rules following "[Paste the rules into an instruction file](#paste-the-rules-into-an-instruction-file)". Methods 1 to 3 all install the same skills, so choose by the command you have at hand (1 and 3 use Node.js `npx`; 2 uses the GitHub CLI). The difference between rules and skills is in the "[Rules and skills](#rules-and-skills)" section.

### 1. `npx skills add`

Install the skills with the command of [skills](https://github.com/vercel-labs/skills).

```sh
# New installation
npx skills add kulikala/wakariyasu --skill '*' -g

# Update to the latest version
npx skills update -g
```

`--skill '*'` installs all of wakariyasu's skills. wakariyasu's skills read the rules from the folder of the skill `writing-rules`, so install all of them, not a subset. `-g` installs into the home directory so that the skills can be used in every folder. To choose the agents to install for, use the `-a` option.

After installing, paste the rules following "[Paste the rules into an instruction file](#paste-the-rules-into-an-instruction-file)".

### 2. `gh skill install`

Install the skills with the `gh skill` command of the GitHub CLI (a preview feature).

```sh
# New installation
gh skill install kulikala/wakariyasu --all --scope user

# Update to the latest version
gh skill update --all
```

`--all` installs all of wakariyasu's skills. `--scope user` installs into the home directory so that the skills can be used in every folder. To choose the agents to install for, use the `--agent` option.

After installing, paste the rules following "[Paste the rules into an instruction file](#paste-the-rules-into-an-instruction-file)".

### 3. `npx openskills install`

With [OpenSkills](https://github.com/numman-ali/openskills), install the skills into the repository you are working in and write the list of skills into the repository's AGENTS.md.

```sh
# New installation and writing to AGENTS.md
npx openskills install kulikala/wakariyasu -y
npx openskills sync -y

# Update to the latest version and write to AGENTS.md
npx openskills update
npx openskills sync -y
```

`-y` installs all of wakariyasu's skills without asking which skills to install. To install into the home directory, use the `--global` option.

After installing, paste the rules into the AGENTS.md that `sync` wrote, following "[Paste the rules into an instruction file](#paste-the-rules-into-an-instruction-file)".

### 4. Claude Code plugin

In Claude Code, install with this method. Both the rules and the skills are installed, and the rules are loaded automatically at the start of every session.

In Claude Code, run the following two commands. The first registers the wakariyasu repository as a place to get plugins from (a marketplace), and the second installs wakariyasu from it.

```text
/plugin marketplace add kulikala/wakariyasu
/plugin install wakariyasu@wakariyasu
```

To check that the installation worked, ask "Where do things stand?" in a new session. This phrase is handled by the skill `session-status`, so if a report with headings such as "Current goal" and "Tasks" comes back, it is installed. You can check the same way after installing with methods 1 to 3.

To update to the latest version, run the following two commands in a terminal and restart Claude Code.

```sh
# Refresh the marketplace information
claude plugin marketplace update wakariyasu

# Update the plugin to the latest version
claude plugin update wakariyasu@wakariyasu
```

### 5. Claude apps and Cowork

In claude.ai (web) or the desktop app, open **Customize > Plugins**, enter `kulikala/wakariyasu` under **Add > Add marketplace**, and install wakariyasu. The plugin is installed to your claude.ai account, so installing once in the web or desktop app makes it available in the phone app and in Cowork when you are signed in with the same account.

In Cowork, as in Claude Code, both the rules and the skills work.

In chat, the skills in the table of the "[When each is used](#when-each-is-used)" section can be used. To check that the installation worked, ask "Where do things stand?" in chat and see whether a report with headings comes back.

In chat, the rules are not loaded automatically. To make the rules apply to the "Ordinary replies" and "Having the agent write a document" situations in the table of the "When each is used" section, paste them as follows.

- Paste the whole of [`AGENTS.snippet.md`](AGENTS.snippet.md) into "Your Claude" > "Instructions" in the web or desktop app's settings (your name at the bottom left > Settings), or into the instructions of a claude.ai project.
- If it does not fit in the instructions field, paste only the section with the heading "Write replies that someone who has not followed the session can understand" in `AGENTS.snippet.md` (the rules for how to write replies). The rules for writing replies alone work for the "Ordinary replies" situation.
- When pasting only a section, also put the first and last lines of `AGENTS.snippet.md` (comments marking the pasted range) before and after the section. They show which range to replace when updating.

### Paste the rules into an instruction file

Methods 1 to 3 install only the skills. A skill reads the rules from the folder of the skill `writing-rules` each time it runs, so the rules apply in situations where a skill is used. To make the rules apply also in the "Ordinary replies" and "Having the agent write a document" situations, where no skill is used, paste the rules into an instruction file.

Paste the whole of [`AGENTS.snippet.md`](AGENTS.snippet.md), the file that gathers wakariyasu's rules (it is at the top level of the wakariyasu repository on GitHub), into the instruction file the agent reads every time (AGENTS.md for Codex, custom instructions for other agents). The first line of the whole, `<!-- wakariyasu:AGENTS.snippet.md -->`, and the last line, `<!-- /wakariyasu:AGENTS.snippet.md -->`, are comments that mark the pasted range.

The update commands of methods 1 to 3 do not update the pasted rules. After updating wakariyasu, replace the pasted range (the two comment lines and everything between them) with the whole of the latest `AGENTS.snippet.md` on GitHub.

## For people who modify wakariyasu

The folder layout, the steps after changing a rule, the repository checks (`dev/test`), the tests that measure whether skills are called (eval) and how to raise the version are in the [development guide](docs/development.md). The changes for each version are in [CHANGELOG.md](CHANGELOG.md).

## Acknowledgments

Some of wakariyasu's rules draw on the Japanese proofreading skill [yomiyasu](https://github.com/nanaism/yomiyasu) (nanaism/yomiyasu, MIT license).

## License

MIT
