---
description: 人に渡す文書を書かせると、remove-meta-narrative を当ててから渡す
tags: [trigger, ja, document]
runs: 3
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Agent, Write, Edit]
expected_outcome: setup.md を書き、remove-meta-narrative を当て、文書自身を語る文を残さない
---
新入社員向けに、Mac に Homebrew と Git を入れる短い手順書を setup.md としてこのフォルダに書いてください。600字程度で。
