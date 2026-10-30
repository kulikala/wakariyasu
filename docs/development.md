# 開発の手引き

## フォルダの構成

```text
.claude-plugin/plugin.json       プラグインの定義（名前・バージョン・スキルの場所）
.claude-plugin/marketplace.json  プラグインの入手先（マーケットプレイス）の定義
rules/                           規則の本文（writing-to-user・writing-documents・polishing）
references/                      リファレンスの本文（日本語の表記・判断の問いかけ・指示文の書き方・README の書き方）と、
                                 日本語では使わない言い回しの一覧（terms.tsv）
skills/<名前>/SKILL.md           スキルの本文
skills/<名前>/references/        規則・リファレンス・一覧のコピー（dev/build が作る）
skills/<名前>/scripts/           check-terms のコピー（dev/build が作る）
scripts/check-terms              日本語では使わない言い回しを文書から探す
scripts/terms-table              一覧を、フックと AGENTS.snippet.md に入れる表にする
tests/terms-cases.txt            check-terms が当たる例と当たらない例
hooks/                           セッションの始めに規則を読み込ませるフック
AGENTS.snippet.md                Claude Code 以外のエージェントに貼る規則の本文（dev/build が作る）
dev/build                        rules/・references/・scripts/ の本文を、スキルの中と AGENTS.snippet.md にコピーする
dev/test                         リポジトリの決まりを検査する
evals/                           スキルが呼ばれるかを測る claude plugin eval のケース
docs/                            この手引き
CHANGELOG.md                     バージョンごとの変更
```

フック・`dev/build`・`scripts/` は `sh` と標準のコマンドだけで動きます。`dev/test` は、それに加えて `git` を使います。Python などのほかの処理系は要りません。

## 本文を直す

規則とリファレンスは、`rules/` と `references/` だけで直します。スキルの中の `references/` と
`AGENTS.snippet.md` はコピーなので、直接は直しません。直したら `dev/build` でコピーを作り直します。

```sh
dev/build
```

規則とスキルの本文は、2つの層に分けて書きます。

- どの言語の文章にも当てる項目。返答や文書の組み立て、指す先、判断の問いかけ方など。
- 日本語で書いたときに足す項目。表記の選び方、読点、日本語の文の確かめ方、yomiyasu など。
  見出しや前置きで「日本語で書いたとき」と分かるようにする。

本文は日本語で書きます。訳さずに、日本語として書き起こします。

## 検査する

```sh
dev/test
```

`dev/test` はモデルを呼ばずに、次を確かめます。GitHub Actions も push と pull request のたびに同じ検査を実行します。

- スキルの中のコピーと `AGENTS.snippet.md` が本文と一致している。
- バージョンが `plugin.json`・`marketplace.json`・`CHANGELOG.md` でそろっている。
- 入手先（`marketplace.json`）に載っているプラグインが1つだけ。
- スキルごとに、`SKILL.md` が frontmatter で始まり、フォルダ名と同じ `name` と、`description` がある。
- フックの出力に、規則3本と `references/` のリファレンスそれぞれの見出しの行と、日本語では使わない言い回しの表がある。
- 規則とスキルが「規則 `polishing` の「…」」と指す見出しが、`rules/polishing.md` にある。
- README が指すリポジトリ内のファイルがある。
- `check-terms` が `tests/terms-cases.txt` の例のとおりに当たり、当たらない。
- 規則・リファレンス・SKILL.md・README・手引きに、日本語では使わない言い回しが無い。
- 最上位に `bin/` が無い。`bin/` があると、claude.ai と Cowork はプラグイン全体を受け付けない。開発用のスクリプトは `dev/` に置く。
- 改行と空白が `.editorconfig` の決まりに合っている（git に登録済みのファイルが対象）。

プラグインの定義の書式は Claude Code の検査でも確かめます。

```sh
claude plugin validate .
```

## スキルが呼ばれるかを測る

`evals/` のケースは、決まった頼み方でスキルが呼ばれるかを、`claude plugin eval` で測ります。
モデルを呼ぶので、費用がかかります。手元で、必要なときに実行します。

```sh
claude plugin eval . --model sonnet --allow-tools Write Edit --no-publish --max-cost-usd 5
```

| ケース | 頼み方 | 確かめること |
|---|---|---|
| `status-ja` | 「現状は？」 | `session-status` が呼ばれる |
| `status-en` | "What's the status? What's done and what's left?" | `session-status` が呼ばれ、返答に日本語が混ざらない |
| `document-ja` | 手順書 `setup.md` を書かせる | `setup.md` ができ、`remove-meta-narrative` が呼ばれ、文書自身を語る文が残らない |

`document-ja` はファイルを書くので、`--allow-tools Write Edit` が要ります。日本語が混ざらないことは、かなと漢字の正規表現で確かめます。

既定では、プラグインを入れた場合と入れない場合の2通りを実行して比べます。1通りだけで
手早く確かめるなら、`--runs 1 --ablation none` を付けます。結果は `evals/results/` に出ます
（git には登録しません）。

## バージョンを上げて公開する

1. `CHANGELOG.md` に新しいバージョンの節を書く。エージェントの振る舞いが変わる変更はマイナーバージョン、
   README や検査だけの変更はパッチバージョンを上げる。
2. `.claude-plugin/plugin.json` と `.claude-plugin/marketplace.json` の `version` を同じ値にする。
3. `dev/test` と `claude plugin validate .` を通す。
4. コミットし、そのコミットに `v0.3.0` の形のタグを付けて push する。GitHub で同じタグのリリースを出し、
   本文に `CHANGELOG.md` のそのバージョンの節を載せる。

入れてある人は `/plugin marketplace update wakariyasu` のあとに
`/plugin update wakariyasu@wakariyasu` を実行すると、新しいバージョンに替わります。Claude Code は
プラグインをバージョンごとにコピーして読み込むので、バージョンを上げないと、直した本文は読み込まれません。
