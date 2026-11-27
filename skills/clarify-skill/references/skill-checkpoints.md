# Checkpoints: how to check and how to fix

For each checkpoint in the table in SKILL.md, this reference describes where to look to find a problem (how to check) and how to rewrite (how to fix). The fixes are suggestions. Choose according to the nature of the skill. When one place matches two or more checkpoints, record both numbers in the findings (for example, a copied command is over-constraining under 3 and misplaced under 8). For overlaps, use 4 for repeated sentences within one skill, 8 for where a fact is placed, and 10 for overlaps between skills.

## 1. Purpose and scope

### How to check

- Does the opening of SKILL.md show what the skill can do?
- Is the body only a numbered procedure? Does the procedure mix in other concerns (handing over deliverables, maintaining rule documents, preparing prerequisites)?
- In situations the procedure does not cover (only one target, redoing only a part, a missing prerequisite), can the agent decide how to behave from the purpose?
- For a skill that lists criteria instead of a procedure, is it clear which criteria apply in which situation?

### How to fix

- Write the purpose (what the skill is for and what it should achieve) and what the skill can do in the opening. For what the skill does not cover, write only the boundaries an agent reading it is likely to cross (a neighboring skill's work) and add the name of the skill that covers it.
- Keep a procedure only where the order matters. Rewrite the rest as policy (what to satisfy).
- If a skill is only a procedure that calls other skills in turn, write the overall purpose and what it hands to and receives from each skill, and leave the details of the order to the skills being called.
- Move other concerns to the skill or rule document that covers them, and only point to them from the original skill.

## 2. Generalization

### How to check

- Do specific names (people, meetings, organizations, cases, domain identifiers, dates, particular files) appear in the instruction sentences? An instruction written with specific names does not apply when the owner or counterpart changes, or when the same thing is done for another target.
- Are records of events (what happened, what the agent found during work) written as the reason for or an example of an instruction?
- Are records of origin written (when, and from whose feedback or decision a rule came; the original wording of feedback)?
- Are past remarks quoted in quotation marks as examples? An agent looks only for situations that resemble the quoted remark.
- Is there only one example, so that the wording fits only that example's situation?
- Does a skill used in several environments contain the placement, domain, or people examples of one team or project?

### How to fix

- From each event, extract what to avoid and what to achieve, and write that as a purpose sentence. Keep the content of the rule and drop its origin.
- Write people, meetings, and organizations as roles (the person who decides, the party who reviews the deliverable, the side that produces the deliverable). Put the mapping from roles to current owners in one place in the documents of the repository or project that holds the skill.
- Keep a specific name only where it is part of a calling convention: skill names, tool entries, and headings or naming rules that other people or tools read.
- Put records of events and origins outside the skill (change history, design documents, feedback records). Before deleting one, check whether the record exists outside; if not, move it out.
- Keep an example only where a general sentence is easy to misread, and write it so that it is clearly an example with specific names removed.
- For a skill used in several environments, move the parts specific to one team or project into that team's or project's skill or documents. In the multi-environment skill, make clear that the environment's rules apply when they exist.

## 3. Degree of constraint

### How to check

- Are command lines, options, resolutions, tool call forms, or executable paths written? (If the repository has a rule on where tool definitions are placed, follow it.) The repository may have a mechanical check for copied tool usage. If that check looks only at executable locations, look for copied options and call forms yourself.
- Are working folder names, the order of reading files, or the choice of tool fixed?
- Do numeric targets (counts, number of sentences, characters, repetitions) constrain the means? Keep a number only when removing it causes trouble, such as a format that other people or tools read. A number that keeps the agent from spending too much effort, such as a stopping point for a repeated task, can stay if its purpose is attached.
- Is the shape of output tables, columns, or headings fixed even though nobody reads it?
- Does the skill include instructions that constrain how its deliverables are written? A sentence that fixes where things go in a document, how it opens, or in what order things are arranged becomes a work instruction. It stops the agent from choosing the structure that suits each deliverable. Fixing the form is acceptable only when the user or the party requesting the skill has explicitly specified an output format, or when other people or tools read the deliverable in that format.
- Is a prohibition used where a purpose and policy would do? A prohibition is needed only for what must be avoided: what cannot be undone if broken, what involves other people's work or originals, or what a person's feedback prohibited. A prohibition does not say what to do outside the described situation. It also narrows behavior even around the prohibited words.
- Does the body re-explain rules that a tool computes and decides? (They will diverge when the tool changes.)
- Does the skill specify means (the command to use, the order of operations, how to identify the target) instead of purpose? Without the purpose, the agent cannot decide in situations where that means is unavailable or a better means exists.
- Is there concrete content that the agent could take as a model for its output or input files and copy as it is, or that narrows its behavior to match? Judge by what the content does, not by how it is marked: quoted phrases, sample data and sample output in a code block or a table, and quoted tool messages all count. Exact text is needed only when the exact characters carry meaning. That applies to words matched against input (terms defined in the rule documents), output that other people or tools read under that name (headings, column names), and wording whose exact match is itself a rule. For a format that others read, keep what defines its shape (the names, the values each may take, which are required); when the text already states the shape, a sample filled with values is a repetition that adds values and counts to copy. Quote a tool's message only when the agent has to match its wording; otherwise state what happens and what to do next. Check example phrasings of requests that fill in situations in a description under checkpoint 14.
- Are examples listed in parentheses or with "etc."? When examples are listed, the agent takes the listed items as all of the target and does not apply the rule to items not listed. List items only when the listed items cover the whole target and which items are included is itself the rule.
- Did you separate what must not be removed from fixed choices (the name and shape of output that other people, tools, and skills read, but not sample values; authoritative sources; pitfalls known to occur)?

### How to fix

- When the environment has a tool guide (a document that collects how to use tools in one place), point to the guide for how to use tools. For a tool with no entry in the guide, include adding an entry in the fix plan.
  - If you were asked to rewrite and the guide is in the repository you are responsible for rewriting, add the entry following the guide's style.
  - If the guide is in another repository, record a proposed addition in the findings. Treat it the same as referrers under checkpoint 15.
  - In an environment without a guide, include in the plan where to put tool usage, following the environment's documents.
  - Tools bundled with the skill (the skill's `scripts/`) also get an entry. The skill, including its references, does not copy their usage. When a reference of the skill is itself the guide to its bundled tools, it states what each tool does and what to do with its results, and leaves the exact messages to the tool.
- For a skill whose job is to run a tool, after moving tool usage out, keep in SKILL.md when and why to run the tool, the arguments that depend on the skill's domain, how to read the results (who gets what back for each warning), and what is decided outside the tool.
- For rules that a tool computes, treat the tool's entry or code as authoritative, and make the skill show only that the tool decides them.
- Keep the conditions that make the agent's work easier (the name and shape of fixed output, where authoritative sources are, pitfalls known to occur). For a pitfall, state which action leads to which result, together with what is to be avoided.
- Write what the agent should decide as a range of choices, or write only the state to satisfy.
- Rewrite a specified means as the purpose and state it should satisfy, and leave the means to the agent. Keep the facts needed to choose a means (what is shared, what can change) as material for judgment.
- Rewrite instructions that constrain how a deliverable is written as a policy about what the reader should be able to take away from it, and leave to the agent where to put what.
- For quoted phrases, write the intended meaning in plain sentences. Keep quotation marks where the exact characters carry meaning.
- Replace a list of examples with a description of the condition or property that items must satisfy.
- Replace numeric targets with a sentence about what to satisfy (an amount that does not leave the reader unsure, a length at which the point is clear).
- Rewrite a prohibition as the purpose the prohibition was meant to serve, stated as a policy of what to do. Keep prohibitions on what must be avoided, with the reason.

## 4. Needless sentences

### How to check

- For each sentence, ask whether the agent's behavior would change without it.
- Does it repeat what the environment's rules (instruction files, rules, user instructions, memory of the repository or project) already decide, such as whether to push, where temporary files go, working branches, or the language of replies?
- Does it turn what the agent does anyway (reading the whole file, reporting the result of what it checked) into an instruction?
- Is the same thing written in two or more places within the skill? Also check files that are loaded together (SKILL.md and references, skill and rules).
- Ask the same question of phrases within sentences. Are there decorative phrases, giving a reason or an evaluation, that would not change behavior if removed? A reason that changes a judgment (what it is meant to avoid) is a purpose, so keep it.

### How to fix

- Delete sentences and phrases that would not change behavior. Delete sentences that repeat environment rules, and keep only the exceptions specific to the skill.
- When a sentence would change behavior if removed but its purpose is already contained in another sentence, merge it into the other sentence.

## 5. Starting conditions

### How to check

- Do the first few steps of the procedure decide the target or produce a prerequisite deliverable?
- Does that work overlap with what another skill covers?
- Did you separate finding and reading materials as the skill's own job from preparing prerequisites? (For a skill that writes minutes, finding the transcript is part of the job. For a review skill, the absence of a deliverable to review is a missing prerequisite.)

### How to fix

- For a skill that needs prerequisites, state what should be in place (the target, prerequisite deliverables, permissions) as states. If one sentence elsewhere conveys the prerequisite, no section is needed. For a skill without prerequisites, write nothing.
- State the behavior when something is missing (return to the caller, name the skill that prepares it, proceed as far as what can be prepared and report what is missing, and so on).
- Keep the effort of checking that the conditions are met (checking is cheap, and proceeding without checking is costly). Leave the work of preparing them to the caller.

## 6. Choice of agents

### How to check

- Does the skill specify the kind of subagent, how to split work, the number, the model, or whether to use agents in another runtime?
- Did you tell apart whether a specification is a choice about the environment (how many, which model) or a quality rule (get two independent reviews, have someone other than the author look)?

### How to fix

- Write that the agent that makes the call decides how to split work, how many agents, which model, and whether to use agents in another runtime, based on the environment and the amount of work.
- Write only the criteria for choosing. The criteria cover the amount (number of targets, length of materials), whether an independent view is needed (review, verification), whether heavy reasoning is needed, the available runtime, and the usage quota.
- Keep quality rules and add what each is for (making a review that is not pulled along by the context in which the work was done, for example).
- Keep pitfalls known to occur (for example, an agent that runs in an environment where it cannot write files should return its result in the body of its reply).

## 7. Handing over context

### How to check

- Does the skill hand nothing to the agents it calls, so that each agent searches for the same materials again?
- Conversely, does it hand over the author's conclusion or the expected answer, which removes the point of checking independently?
- For a skill that does not call subagents, this checkpoint does not apply.

### How to fix

- Write what is handed over in two groups.
  - Shared items: the purpose, where the authoritative material is, the rules to apply, the list of targets, how to treat terms, where writing is allowed, and the form of output. Put them in one file and give each agent its location.
  - What is withheld: the author's judgment, earlier conclusions, expected findings, anything the called agent should find independently. Write why it is withheld.
- Hand over a checkpoint added in an earlier review as a checkpoint, not as a conclusion.

## 8. Guidance on behavior and environment

### How to check

- Are the folder structure, file naming rules, or a table of locations written in both SKILL.md and environment documents, or in two places within the same skill?
- How many of the sentences in SKILL.md explain the environment (what is where) instead of the agent's behavior (what to decide and what to make)?
- Do other skills also use a term defined within this skill? (If so, the environment's documents are a better place for the definition.)
- Are maintenance procedures for the maker (how to fix or rebuild a tool) mixed into instructions that are read every time the skill is used?
- Are repositories, tools, or documents named or given by path? When a name changes, someone has to search the skills and fix them.

### How to fix

- The following table shows where each kind of content goes.

  | What it describes | Where it goes |
  |---|---|
  | Behavior of the agent that uses the skill (purpose, scope, prerequisites, policy) | SKILL.md |
  | Detailed forms, checkpoints, and where examples are, needed only when using this skill | The skill's `references/` |
  | A rule that two or more skills treat as authoritative | One place in the `references/` of the skill that covers the deliverable the rule produces, with the others pointing to it. If no skill clearly covers it, the documents of the repository or project |
  | Environment rules (folders, names, order of production, definitions of terms of the team or project) | The documents of the repository or project that holds the skill |
  | Ways of writing and rules to keep in every session | A place loaded at the start of a session, such as the repository's rules or the project's instruction file |
  | How to use and call tools | The environment's tool guide entry if one exists (checkpoint 3); otherwise the environment's documents |
  | Tool code | `scripts/` (in the skill, or in the repository's `scripts/`) |
  | Maintenance procedures for the maker, decisions and their reasons, rejected options | A README or design document in the skill (a place not read when the skill is used) |
  | Origins of rules (the original wording and date of a person's feedback, how a rule was decided) and records of events | Records outside the skill (change history, design documents, feedback records) |

- After moving something, point to its destination from SKILL.md.
- When the content of the skill and the documents of the repository or project conflict, handle it as described in the "Preserving the rules" section of SKILL.md.
- Set up sections to fit the content of the skill. Create only sections that have something to write: a purpose section if there is a purpose, a starting conditions section if there are prerequisites. There is no need to follow a fixed template; a section or sentence created to fill a template matches checkpoint 4.
- Replace named references with references by role (the repository that holds the skill, the higher-level document that the repository follows, the environment's tool guide). A document in the same repository can be pointed to by relative location. Use a name only when the role does not lead to the target.

## 9. Freshness of facts

### How to check

- Check locations, file names, tool behavior, and the way of writing names that tools read, one by one, against the current folders, documents, and tool code. An outdated fact written in only one place will not be found by looking for overlaps.
- Does the body keep text about a transition period (since when it changed, how it used to be, what to do for old cases), one-time migration steps, or flows no longer used?
- In a skill with an old flow and a new flow side by side, is the flow mainly used now written as the body? (Check by the number of deliverables made and recent use.)
- Does a file pointed to as an example still exist at that path, and does it match current rules?
- Does the skill point to a tool that does not work or no longer exists?
- Does the body state the number of listed items or steps? When items are added or removed, only the number goes stale.

### How to fix

- Correct outdated facts to current facts, and record in the findings what you checked them against.
- Delete the number of listed items or steps and point to the list without a number. Keep a number only when the number itself is the rule, such as a limit or a count of times.
- Delete text about a migration that is finished. If the migration is in progress, make the current flow the body and move the old flow to references, limited to when old deliverables are handled.
- If an unused procedure is kept only for comparison, put it in a design document or at the end of a reference, in a form that shows it is not used.
- Point to the latest deliverable that matches current rules as the example, or point by how to find it (for example, the previous round of the same material).

## 10. Consistency between skills

### How to check

- Do several skills describe the same rule (how to judge completion, how to align question sentences, how to hand over)? If so, have they diverged through differences in wording?
- Among skills that divide work in order of production (where a repository document, such as a table, decides which skill produces what), does the earlier skill's output fit the later skill's prerequisites? Does any skill presuppose something produced later?
- Is the same way of calling a tool copied into several skills?

### How to fix

- Make one place authoritative for each rule and point to it from the others (placement follows the table under checkpoint 8).
- Handle conflicts as described in the "Preserving the rules" section of SKILL.md.
- If the order of dependency is reversed, record it in the findings and return to the caller which order to use.

## 11. Loading weight

### How to check

- The size of SKILL.md and the share of sentences needed in every situation. If it is larger than other skills, check whether situation-specific sentences are mixed in.
- Is a single references file so large that reading the part you need means reading all of it?
- Does the skill say which references to read in which situation?

### How to fix

- Move detail specific to a situation (criteria per kind of material, rules needed only when requesting a review) into references, and make SKILL.md show which to read in which situation.
- Split large references by situation or target, or put a table of contents and a reading guide at the top.

## 12. Execution environment

### How to check

- Does the skill work as written in every runtime it is meant for? Does it depend on a particular tool's name or on how it is loaded (a call form that exists only in one agent's tools)? (If the repository has rules for writing skills, follow them.)
- Does it use material that exists on only one PC (personal memory, settings of that PC only) as a source? Does it state values that belong to one PC only (connection targets, user paths, PC names)?
- Does it contain secrets?
- Do the folder name and `name` match the environment's rules for naming skills (if any)?

### How to fix

- Write paths relative to the skill's folder. Refer to other skills by name and do not describe how they are loaded.
- Move a rule that relies on personal material to a shared place, or remove it from the sources.

## 13. Irreversible operations

### How to check

- Do operations that delete, overwrite, or edit in place affect only the agent's own work? Could they affect originals, versions people edited, or other sessions' work?
- Does the skill decide its target by relying on shared things (such as a staging place that other sessions also use) that other work can change?
- Are safeguards written as means (the command or procedure to use) instead of purpose? (Checkpoint 3.)
- Are prohibitions and safeguards written as rules to keep, or are some missing?

### How to fix

- Write what must not be involved and the state to satisfy (handle only your own work; keep it reversible). Keep facts that lead to wrong judgment if unknown, such as that something is shared, and leave the specific method and the commands to use to the agent.
- Record missing safeguards in the findings. If a judgment about the skill's domain is needed, return it to the caller.

## 14. How the skill gets invoked

### How to check

- Does the description have the situations in which to use the skill (what the user wants to do, which deliverable it concerns), the situations in which not to, and the division of work with neighboring skills?
- Does it list only request sentences without describing situations? With only request sentences, the situations in which the skill is called narrow to fit the listed sentences, or requests are read as fitting those patterns. Example phrasings of requests help the agent choose the skill. Keep them if situations are described and the examples only fill the situations in. Deliverables or terms that the users or the project usually use can be written as words that express situations.
- Compare with the descriptions of other skills that could be called for the same request. Is it settled which one is called?
- Do the scope in the description and the scope in the body disagree? If the body was rewritten, was the description updated to match?
- Does the skill work whether the caller is a person, an automated mechanism, or another agent? Does an instruction from an automated mechanism override the skill's procedure by step number? Does an instruction to confirm with the user still make sense when the skill is called as a subagent?

### How to fix

- Rewrite the description from the purpose and scope in the body. Details and tool processing that are in the body need not be in the description; keep only what is needed to decide whether to call the skill.
- If only request examples are given and situations are not described, extract the situations from the examples and write them. Keep examples only as far as they fill in situations.
- Where an automated mechanism overrides the procedure, write the situation on the skill's side so that it still holds when step numbers change.
- Write the party to confirm with as a caller that is not necessarily a person.

## 15. Reference links

### How to check

- Referrers: search the related repository's documents, code (imports and path computations), evaluation scenarios, and automatically generated guides and indexes for the skill's name, section names and numbers, the names of files in references and `scripts/`, module and function names, and output names. Also check places where a table column holds section numbers (for example, a feedback record with a column that states which section a feedback matches).
- Referents: do the files, sections, examples, and tool output sentences that this skill points to still exist? Also list references that are already broken.
- Are the section names and numbers of a skill that other skills extend an agreement with the skills that extend it?

### How to fix

- If you change a name or number, fix the referrers in the same change.
- If a referrer is in the repository you are responsible for rewriting, fix it in the same work. If it is in another repository (including another team's), keep the original name and record a proposed fix in the findings.
- If a section name or number is an agreement, change it only together with its referrers.

## 16. Wording

### How to check and how to fix

- Attach a purpose to each instruction, and write the range of choices as a range (follow `references/writing-instructions.md` of the `writing-rules` skill, as in the division of work section of SKILL.md).
- If the environment's documents define words not to use or rewordings of their own, follow those rewordings and use words that express the content.
- Check whether names coined within the skill are used without being defined. If so, define them or replace them with words that express the content.
- Apply the section for clarify-skill in the `skills.md` of the language pack for the language the target is written in, if any. The language packs are in the `lang/` folder of the `writing-rules` skill. How to treat terms defined by the environment's documents is as in the "Handling terms" section of SKILL.md.
- Treat rules for how output is written (rules on style or form of documents the skill produces) as domain rules and keep them as they are.

## Re-reading after a rewrite

- To check that the skill can be read without the writer's understanding filling gaps, have an agent that does not have the context in which it was made read the rewritten skill, and fix the places where that agent was unsure. Hand over the purpose and the rewritten files. Do not hand over the files from before the rewrite or the reasons for the rewrite (knowing the reasons, the reader would fill in what the text does not say). The review-for-readers skill can be used.

## Delegating several skills

- Apply checkpoints 6 and 7 to your own delegation. Hand over shared items (listed in the fix for checkpoint 7) once, and do not hand over what the reviewer should find independently (the findings you expect, conclusions of an earlier review).
- If you delegate rewriting, split the files each agent is responsible for (writes to the same file would collide).
- Choose the number, kind, and model of reviewers by the criteria in checkpoint 6 (the number and length of skills, whether an independent view is needed, whether heavy reasoning is needed, the available runtime and usage quota).
