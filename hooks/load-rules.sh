#!/bin/sh
# セッションの開始・再開・/clear・/compact のたびに、規則の本文を読み込ませる。
# Claude Code のプラグインは規則のファイルを読み込まないため、フックの出力で渡す。
set -eu

for f in "${CLAUDE_PLUGIN_ROOT}"/rules/*.md; do
    cat "$f"
    printf '\n'
done
