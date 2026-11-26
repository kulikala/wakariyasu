#!/bin/sh
# Print where wakariyasu's files are, which language packs exist, and how to choose a pack.
# Usage: lang-index.sh <writing-rules folder> <check-terms folder> <session-status folder>
set -eu
W="$1"; T="$2"; S="$3"
printf '# wakariyasu: file locations and language packs\n\n'
printf 'The text above holds the rules (writing-to-user.md, writing-documents.md, polishing.md) and asking.md. Do not read them again.\n\n'
printf '## Language packs\n\n'
printf 'Choose the pack for each thing you are about to write by the language of that thing, not by the language of the conversation. A user who writes to you in Japanese and asks for an English README gets a reply from the ja pack and a README from the en pack; one turn can need two packs. Read only the file for that kind of text in that language'"'"'s pack, unless its text is already in the conversation:\n\n'
printf -- '- reply.md: a reply to the user\n'
printf -- '- documents.md: a document (README, specification, SKILL.md, commit message, and so on)\n'
printf -- '- skills.md: what a wakariyasu skill adds in that language; read the section for the skill you are using\n\n'
printf 'A language that is not listed has no pack; follow the rules alone.\n\n'
for d in "$W"/lang/*/; do
    [ -d "$d" ] || continue
    code="$(basename "$d")"
    files="$(cd "$d" && ls *.md | grep -v '^asking-template.md$' | tr '\n' ' ' | sed 's/ $//; s/ /, /g')"
    printf -- '- %s: %s (%s)\n' "$code" "${d%/}/" "$files"
done
printf '\n## Fixed words\n\n'
printf 'Headings, column names and state words are filled in by tools. Do not translate or look them up one by one. For the markdown you write yourself, take the filled template for the language of the text and use its words as printed:\n\n'
printf -- '- Decision questions: lang/<code>/asking-template.md in the writing-rules folder\n'
printf -- '- Status reports: lang/<code>/reply-template.md in the session-status folder\n\n'
printf 'Templates exist for:'
for d in "$W"/lang/*/; do
    [ -e "${d}asking-template.md" ] && printf ' %s' "$(basename "$d")"
done
printf '.\n\n'
printf 'For a language that has no template, run `python3 -B %s/scripts/asking-skeleton --init <code> -o <file>` (and `python3 -B %s/scripts/skeleton.py --init <code> -o <file>` for a status report), translate the values in the file and keep the words in braces, then pass the file with `--labels` to the same script, or to `build.py` when you build a page. The script prints the template or builds the page, and stops on a missing key or a dropped word in braces.\n' "$W" "$S"
printf '\n## Other files\n\n'
printf -- '- Rules: %s/rules/\n' "$W"
printf -- '- References: %s/references/ (writing-instructions.md, readme.md and changelog.md are not loaded; the rule writing-documents.md says when to read them)\n' "$W"
printf -- '- check-terms skill (a checker, and phrase lists per language in lang/<code>/): %s/\n' "$T"
