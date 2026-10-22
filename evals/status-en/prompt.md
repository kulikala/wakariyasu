---
description: 英語で状況を聞かれたときも session-status が呼ばれ、報告に日本語が混ざらない
tags: [trigger, en]
runs: 3
allowed_tools: [Read, Glob, Grep, Skill]
append_system_prompt: Always respond in English.
expected_outcome: session-status スキルを呼び、英語の見出しで報告する
---
What's the status? What's done and what's left?
