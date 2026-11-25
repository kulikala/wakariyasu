---
description: When asked to write a document for people, the agent applies remove-meta-narrative before handing it over
tags: [trigger, ja, document]
runs: 3
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Agent, Write, Edit]
expected_outcome: Writes setup.md, applies remove-meta-narrative, and leaves no sentence about the document itself
---
新入社員向けに、Mac に Homebrew と Git を入れる短い手順書を setup.md としてこのフォルダに書いてください。600字程度で。
