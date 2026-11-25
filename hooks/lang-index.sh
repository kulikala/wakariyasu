#!/bin/sh
# Print where wakariyasu's files are and which language packs exist.
# Usage: lang-index.sh <writing-rules folder> <check-terms folder>
set -eu
W="$1"; T="$2"
printf '# wakariyasu: file locations and language packs\n\n'
printf 'The text above holds the rules (writing-to-user.md, writing-documents.md, polishing.md) and asking.md. Do not read them again.\n\n'
printf '## Language packs\n\n'
printf 'Before you write a reply or a document in one of the languages below, read every file in that language'"'"'s folder, unless the file'"'"'s text is already in the conversation. A language that is not listed has no pack; follow the rules alone.\n\n'
for d in "$W"/lang/*/; do
    [ -d "$d" ] || continue
    code="$(basename "$d")"
    files="$(cd "$d" && ls *.md | tr '\n' ' ' | sed 's/ $//; s/ /, /g')"
    printf -- '- %s: %s (%s)\n' "$code" "${d%/}/" "$files"
done
printf '\n## Other files\n\n'
printf -- '- Rules: %s/rules/\n' "$W"
printf -- '- References: %s/references/ (writing-instructions.md, readme.md and changelog.md are not loaded; the rule writing-documents.md says when to read them)\n' "$W"
printf -- '- check-terms skill (a checker, and phrase lists per language in lang/<code>/): %s/\n' "$T"
