#!/bin/sh
# セッションの開始・再開・/clear・/compact のたびに、規則と、返答のたびに使うリファレンスの本文を読み込ませる。
# Claude Code のプラグインは規則のファイルを読み込まないため、フックの出力で渡す。
# README の書き方と指示文の書き方は、その文書を書くときだけ使うので読み込ませず、場所だけを伝える。
set -eu

for r in writing-to-user writing-documents polishing; do
    cat "${CLAUDE_PLUGIN_ROOT}/rules/$r.md"
    printf '\n'
done
for f in styles asking; do
    cat "${CLAUDE_PLUGIN_ROOT}/references/$f.md"
    printf '\n'
done
sh "${CLAUDE_PLUGIN_ROOT}/scripts/terms-table"
printf '\n# wakariyasu のファイルの場所\n\n'
printf -- '- 規則: %s/rules/\n' "${CLAUDE_PLUGIN_ROOT}"
printf -- '- リファレンスと言い回しの一覧: %s/references/（readme.md と writing-instructions.md は読み込んでいないので、書くときに読む）\n' "${CLAUDE_PLUGIN_ROOT}"
printf -- '- ファイルに書いた文書の検査: sh "%s/scripts/check-terms" <ファイル>\n' "${CLAUDE_PLUGIN_ROOT}"
