# wakariyasu

[English](README.en.md)

wakariyasu は、AI エージェントが書く日本語を、作業の経緯を知らない人が読んでも分かるようにするプラグインです。

エージェントに長い作業を任せると、報告や質問が、作業の途中で生まれた呼び名や前提のまま書かれがちです。読む人は「結局どういうこと？」と聞き返すことになります。wakariyasu は、エージェントがユーザーに返す文と、エージェントが書く文書の両方を、経緯を知らない読み手に通じる形に整えます。

## 使う場面

| 場面 | 言葉の例 | 受け持つもの | すること |
|---|---|---|---|
| いつもの返答 | （言わなくても効きます） | 規則 `writing-to-user` | 返答を、経緯を知らない人に通じる語と形で書かせます |
| 状況を知りたい | 「現状は？」「残タスクは？」 | スキル `session-status` | 目指していること・タスクと状態・判断を求めることを、決まった形で報告させます |
| 返答が分からない | 「分かりやすく」「つまり？」「〜とは？」「〜の違いは？」 | スキル `explain-clearly` | 直前の返答や分からなかった語を、言われた言葉に合わせて短く、または前提を足して言い直させます |
| 文書を書かせる | （言わなくても効きます） | 規則 `writing-documents` | README・仕様書・SKILL.md・コミットメッセージなどを、その文書だけで通じるように書かせます |
| 文書から作業の跡を除く | 「メタ記述を除いて」 | スキル `remove-meta-narrative` | 「本章では〜」「ご指摘を受けて〜」のように、文書が自分自身や作った経緯を語る文を見つけて直させます |
| 文書を人に渡す前 | 「公開前に見て」「読み手の目でレビューして」 | スキル `review-for-readers` | 経緯を渡さない別のエージェントに文書だけを読ませ、引っかかった箇所を直させます |

規則は、Claude Code のセッションが始まるたびに読み込まれ、毎回の返答と文書に効きます。スキルは、上の言葉で頼んだときと、エージェントが報告や文書の受け渡しの場面で必要と判断したときに動きます。

## 表記の選び方

かなと漢字の使い分け・数字の書き方・体言止め・常体と敬体は、文章の種類によって変わります。wakariyasu はこれらを一律に決めず、次の順で選ばせます。

1. ユーザーの指示（CLAUDE.md や AGENTS.md に書いた指示を含みます）
2. 同じ文書や同じリポジトリで、すでに使われている書き方
3. 文章の種類ごとの既定（ユーザーへの返答・コミットと PR・README・規則と仕様書など）

決まった書き方にしたいときは、CLAUDE.md に1行で書いてください。たとえば「数字は算用数字で書く」「README は敬体で書く」と書けば、そちらが優先されます。

## yomiyasu との組み合わせ

[yomiyasu](https://github.com/nanaism/yomiyasu)（nanaism/yomiyasu）は、AI が書いた日本語の不自然な比喩や主語と述語のずれを整えるスキルです。yomiyasu が入っていれば、wakariyasu は長い返答や文書を渡す前に、文章の種類を添えて yomiyasu で整えさせます。

yomiyasu が入っていなくても、wakariyasu はそのまま動きます。そのときは、文の長さ・主語と述語の距離・飾りの語・予告だけの文を、エージェント自身に確かめさせて整えます。

## 入れ方

### Claude Code（プラグインとして）

```text
/plugin marketplace add kulikala/wakariyasu
/plugin install wakariyasu@wakariyasu
```

規則とスキルの両方が入ります。yomiyasu も同じマーケットプレイスから入れられます。

```text
/plugin install yomiyasu@wakariyasu
```

### スキルだけを入れる

ほかのエージェント（Codex・Cursor・GitHub Copilot など）でも使えます。

```sh
gh skill install kulikala/wakariyasu --all --scope user --agent claude-code
```

`--agent` で、使うエージェントを選びます。スキルだけを入れた場合、規則は読み込まれません。それでも、スキルは自分の `references/` にある規則の写しを読んで動きます。

### 規則を Claude Code 以外で使う

[`AGENTS.snippet.md`](AGENTS.snippet.md) は、4本の規則をつなげた本文です。AGENTS.md など、エージェントが毎回読む指示のファイルに貼ってください。

## 中身

```text
rules/                  毎回読み込む規則（4本）
  writing-to-user.md    ユーザーへの返答の書き方
  writing-documents.md  エージェントが書く文書の書き方
  polishing.md          書いた日本語を渡す前に整える方法と、表記の選び方
  session-status.md     状況報告に session-status を使う場面
skills/                 スキル（4本）
references/styles.md    文章の種類ごとの表記の既定
hooks/                  プラグインとして入れたときに、規則を読み込ませるフック
AGENTS.snippet.md       Claude Code 以外のエージェントに貼る規則の本文
bin/build               rules/ と references/ から、スキルの写しと AGENTS.snippet.md を作る
```

規則と表記の既定は `rules/` と `references/` で直し、`bin/build` で写しを作り直してください。`bin/build --check` は、写しが本文と食い違っていれば失敗します。

## ライセンス

MIT
