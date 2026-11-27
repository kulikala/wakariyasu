---
name: clarify-skill
description: Review a finished skill (SKILL.md, references, and the guidance for bundled tools) as instructions for agents, and plan how to fix it (rewrite it when asked). Checks whether an agent reading it can decide from its purpose, whether it over-constrains or contains needless sentences, and whether each piece sits in the right place. Use it when asked to review a skill, generalize it, rewrite a skill that has turned into a procedure, or review several skills. It does not create new skills. Also use it, without being asked, after writing or changing a skill, before remove-meta-narrative and review-for-readers. To polish a SKILL.md only as a general document from the reader's viewpoint, use review-for-readers. To remove only meta-narrative, use remove-meta-narrative. Also applies when the user says the same thing in another language.
---

# Purpose of the review

A skill takes up the agent's context every time it is loaded, and it decides how that agent behaves. The purpose of the review is that an agent reading the skill understands its purpose and scope, and can make choices that fit the purpose in situations the skill does not describe. When a skill spells out procedures, tools, events, and numbers in detail, behavior is undefined outside the situations it describes. Stale instructions also remain when tools or the environment change.

This skill changes only how instructions are written and where they are placed. Domain rules written in the skill (what counts as authoritative, what was decided after a person's feedback) are kept intact or moved to the right place.

The caller is the user who asked for this skill or the agent that invoked it.

The rules to apply are in the repository's or project's instruction files and development documents (where skills, tools, and rules are placed and how they are written). They are also in the higher-level documents that the repository follows (rules shared by the organization or team). When no rules for writing skills can be found, use the guidance in `references/writing-instructions.md` of the `writing-rules` skill and the "Condition to meet" column of the checkpoint table below.

If the repository or project holding the skill has a record of constraints agreed with the user, read it. Do not flag a constraint in the record even when it matches a checkpoint, so that a format the user agreed to is not removed as over-constraining. When you agree a new constraint with the user during a review or rewrite, add it to the record. If no record exists, include in the fix plan where to put one.

## Division of work with review-for-readers and remove-meta-narrative

review-for-readers rereads a document meant for people from the viewpoint of a reader who did not follow its history. remove-meta-narrative removes sentences in which a document talks about itself or how it was made. This skill reads the skill as instructions for agents. It checks whether the purpose comes across, whether the skill over-constrains, and whether each piece is in the right place.

- Checkpoints 3, 4, and 16 overlap with `writing-instructions.md`. Follow `writing-instructions.md` for the purpose of each instruction, the range of choices left open, and removing sentences that change nothing when dropped.
- The records of events and origins in checkpoint 2, and the writer's coined names in checkpoint 16, also overlap with meta-narrative and with places where the reader gets stuck. Fix meta-narrative with remove-meta-narrative. Fix places where the reader gets stuck with review-for-readers.
- This skill covers what readability checks do not find: the skill's purpose, scope, placement, execution environment, and how it gets invoked.

## Checkpoints

Apply every checkpoint. For a checkpoint that does not fit the target, state that it does not apply and why. How to check and how to fix each checkpoint is in `references/skill-checkpoints.md`. Checks specific to a language are in the `skills.md` of the pack for the language of the target (see checkpoint 16).

| # | Checkpoint | Condition to meet |
|---|---|---|
| 1 | Purpose and scope | The opening shows what the skill is for and what it can do. If there is a boundary that is easy to cross, the opening also shows what the skill does not cover. In situations the procedure does not cover, the agent can choose behavior from the purpose |
| 2 | Generalization | The skill works outside the situations it describes. It has no specific names, events, or records of origin. Its sentences state purposes drawn from events. People, meetings, and organizations are written as roles. The mapping from roles to current owners is in the repository's or project's documents. Records of origin and events are outside the skill |
| 3 | Degree of constraint | Conditions that make the agent's work easier remain: the name and shape of output that others read, the authoritative sources, and pitfalls known to occur. What the agent should decide is left to it: tool choice and options, working folder names, reading order, counts and lengths. The skill states purposes and the state to satisfy, not means. The skill states how its deliverables are written as a policy about what the reader should be able to take away. The exceptions are an explicitly specified output format and output that others read. Concrete content the agent could copy (quoted phrases, sample data or output in a code block or a table, quoted tool messages) appears only where the exact characters matter, and none is a template to copy. For output that others read, the shape is fixed, not sample values. A prohibition does not repeat what a purpose and policy already convey. Prohibitions are used only for what must be avoided |
| 4 | Needless sentences | Without any sentence or phrase, behavior would change. The skill does not repeat what the environment already decides (instruction files, rules, user instructions) or what agents do anyway |
| 5 | Starting conditions | A skill that needs prerequisites states them as conditions. The work of preparing them is not in the procedure. The behavior when a prerequisite is missing is clear |
| 6 | Choice of agents | The skill does not specify the type, number, or model of subagents or agents in other runtimes. It states criteria for choosing. Quality rules such as getting an independent review stay, together with their purpose |
| 7 | Handing over context | What is shared with the agents the skill calls is separated from what is withheld so that those agents find it independently. Shared items are handed over once |
| 8 | Guidance on behavior and environment | SKILL.md describes behavior. It points to environment documents for environment rules. For how to use tools, it points to the environment's tool guide (a document that collects how to use tools in one place) if one exists. Other repositories, tools, and documents are referred to by role, not by name. The same fact does not appear twice within the skill or between the skill and environment documents |
| 9 | Freshness of facts | The environment facts the skill states (locations, tool behavior, file names, paths of examples) match the current documents, tools, code, and folders. The body has no text about a transition period or a flow that is no longer used |
| 10 | Consistency between skills | Several skills do not copy the same rule. One place is authoritative and the others point to it. For skills that run in sequence, the prerequisites and outputs fit together |
| 11 | Loading weight | SKILL.md, which is read every time, holds only what every situation needs. Details needed only in some situations are in references, and the skill says when to read each reference |
| 12 | Execution environment | The skill works as written in every runtime it is meant for. It does not depend on a specific tool's name, on how the skill is loaded, or on material that exists only on one PC. It has no secrets |
| 13 | Irreversible operations | Operations that delete, overwrite, or edit in place affect only the agent's own work. They do not affect shared things (a staging place that other sessions also use, originals, files that people edited) |
| 14 | How the skill gets invoked | The description states, as situations, when to use the skill, when not to use it, and how it divides work with neighboring skills. It does not contradict the body. Example phrasings of requests are added only as far as they help choose the skill by filling in situations. The skill works whether the caller is a person, an automated mechanism, or another agent |
| 15 | Reference links | After a rewrite, both the places that refer to this skill (referrers) and the places this skill refers to (referents) still connect. The links include documents, code imports and paths, column numbers in tables, and evaluation scenarios |
| 16 | Wording | Each sentence has one point. Each instruction has its purpose. The skill has no names coined by the writer |

## Preserving the rules

Before a rewrite, sort each of the original rules into keep, move (with the destination), or delete (with the reason), so that you can show that no rule is lost. After the rewrite, check against the original. For a review only, do not sort. Return the rules that must not be dropped when generalizing, with proposed destinations. Delete only sentences that match checkpoint 4, sentences whose same content already exists at the destination, and facts that no longer match the current tools or folders. When unsure whether to delete, keep the sentence.

When rules conflict, a later decision (a newer instruction or agreement) or a primary source (the original document that set the rule) may settle the conflict. If neither can settle it, do not decide which rule is authoritative. Return both rules to the caller, side by side. When a later decision can settle the conflict, follow the newer decision and record in the findings what you used to decide. Following a newer decision does not change the content of the rule.

## Rewriting and delegation

When you have rewritten a skill, or when you delegate several skills, read "Re-reading after a rewrite" and "Delegating several skills" at the end of `references/skill-checkpoints.md`.

## What to return

- The verdict (no fix needed / partial fix / rebuild), findings per checkpoint (the reason for each checkpoint that does not apply), and the fix plan
- The rules to keep (conditions, criteria, and exceptions that must not be lost when generalizing) and where each original rule goes
- Reference links (referrers and referents)
- What the caller must decide (such as conflicts between rules that cannot be settled)
- Candidate checkpoints: a checkpoint that is not in the table and seems to apply to other skills too. Report it when you notice it during the review
- After a rewrite: the rewritten skill and the changes at the destinations, what you verified, and what you did not verify

## Handling terms

When a term seems worth rewording but the environment's documents define it and people use it, keep it as it is. Then it matches the section names that other documents refer to and the way people call it.
