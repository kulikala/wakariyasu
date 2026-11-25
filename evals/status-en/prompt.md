---
description: When asked for the status in English, session-status is invoked and the report contains no Japanese
tags: [trigger, en]
runs: 3
allowed_tools: [Read, Glob, Grep, Skill]
append_system_prompt: Always respond in English.
expected_outcome: Invokes the session-status skill and reports with English headings
---
What's the status? What's done and what's left?
