#!/bin/sh
# セッションの開始・再開・/clear・/compact のたびに、規則とリファレンスの本文を読み込ませる。
# Claude Code のプラグインは規則のファイルを読み込まないため、フックの出力で渡す。
set -eu

for r in writing-to-user writing-documents polishing; do
    cat "${CLAUDE_PLUGIN_ROOT}/rules/$r.md"
    printf '\n'
done
for f in styles asking writing-instructions readme; do
    cat "${CLAUDE_PLUGIN_ROOT}/references/$f.md"
    printf '\n'
done
