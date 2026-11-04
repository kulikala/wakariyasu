#!/bin/sh
# セッションの開始・再開・/clear・/compact のたびに、規則と、返答のたびに使うリファレンスの本文を読み込ませる。
# Claude Code のプラグインは規則のファイルを読み込まないため、フックの出力で渡す。
# README の書き方と指示文の書き方は、README や指示文を書くときだけ使うので読み込ませず、場所だけを伝える。
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
printf 'フックの出力に入っているのは、規則3本・styles.md・asking.md・言い回しの2つの一覧（terms.tsv・terms-caution.tsv）。\n'
printf '規則やリファレンスに「読み込まれていなければ〜を読む」とあっても、フックの出力に入っているものは読み直さなくてよい。\n\n'
printf -- '- 規則（writing-to-user.md・writing-documents.md・polishing.md）: %s/rules/\n' "${CLAUDE_PLUGIN_ROOT}"
printf -- '- リファレンスと言い回しの一覧: %s/references/\n' "${CLAUDE_PLUGIN_ROOT}"
printf -- '- フックの出力に入っていないリファレンス: readme.md は README を書く・直すとき、writing-instructions.md はスキル・規則・プロンプトを書くときに、references/ から読む\n'
printf -- '- ファイルに書いた文書の検査: sh "%s/scripts/check-terms" <ファイル>\n' "${CLAUDE_PLUGIN_ROOT}"
