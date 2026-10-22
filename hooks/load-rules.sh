#!/bin/sh
# セッションの開始・再開・/clear・/compact のたびに、規則と表記の表の本文を読み込ませる。
# Claude Code のプラグインは規則のファイルを読み込まないため、フックの出力で渡す。
set -eu

for r in writing-to-user writing-documents polishing; do
    cat "${CLAUDE_PLUGIN_ROOT}/rules/$r.md"
    printf '\n'
done
cat "${CLAUDE_PLUGIN_ROOT}/references/styles.md"
