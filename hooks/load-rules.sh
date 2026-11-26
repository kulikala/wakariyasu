#!/bin/sh
# At session start, resume, /clear and /compact, load the rules and asking.md into the conversation
# and give the index of language packs, one part per hook command.
# Claude Code shows a hook command's output inline only up to 10,000 characters (more is replaced by a short preview),
# so hooks/hooks.json runs this script once per part, and each part stays well under the limit (dev/test checks).
# Claude Code plugins do not load rule files, so the hook passes them through its output.
# Language pack files are not loaded here: the agent reads only the pack file it needs.
# Usage: load-rules.sh writing-to-user | writing-documents | polishing | asking | index
set -eu

W="${CLAUDE_PLUGIN_ROOT}/skills/writing-rules"
case "${1:-}" in
    writing-to-user | writing-documents | polishing)
        printf '<!-- %s -->\n\n' "$1.md"
        cat "$W/rules/$1.md"
        ;;
    asking)
        printf '<!-- asking.md -->\n\n'
        cat "$W/references/asking.md"
        ;;
    index)
        sh "${CLAUDE_PLUGIN_ROOT}/hooks/lang-index.sh" "$W" "${CLAUDE_PLUGIN_ROOT}/skills/check-terms" "${CLAUDE_PLUGIN_ROOT}/skills/session-status"
        ;;
    *)
        echo "usage: load-rules.sh writing-to-user | writing-documents | polishing | asking | index" >&2
        exit 2
        ;;
esac
