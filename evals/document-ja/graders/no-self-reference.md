---
type: regex
pattern: "本書では|本章では|この手順書では|このドキュメントでは|この文書では|ご依頼"
match: not_contains
target: { source: file, path: setup.md }
---
