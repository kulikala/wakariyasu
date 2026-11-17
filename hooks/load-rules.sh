#!/bin/sh
# At session start, resume, /clear and /compact, load the rules and asking.md into the conversation,
# and list the language packs so the agent can read the pack for the language it writes in.
# Claude Code plugins do not load rule files, so the hook passes them through its output.
# Language pack files are not loaded here: the agent reads only the pack it needs.
set -eu

W="${CLAUDE_PLUGIN_ROOT}/skills/writing-rules"
for r in writing-to-user writing-documents polishing; do
    printf '<!-- %s -->\n\n' "$r.md"
    cat "$W/rules/$r.md"
    printf '\n'
done
printf '<!-- asking.md -->\n\n'
cat "$W/references/asking.md"
printf '\n'
sh "${CLAUDE_PLUGIN_ROOT}/hooks/lang-index.sh" "$W" "${CLAUDE_PLUGIN_ROOT}/skills/check-terms"
