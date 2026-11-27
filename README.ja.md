# wakariyasu

[English](README.md) | 日本語

[![Release](https://img.shields.io/github/v/release/kulikala/wakariyasu)](https://github.com/kulikala/wakariyasu/releases/latest) [![License: MIT](https://img.shields.io/github/license/kulikala/wakariyasu)](LICENSE)

wakariyasu は、AI エージェントの書く文章を、作業の経緯を知らない人が読んでも分かるようにする、Claude Code と Claude のアプリ向けのプラグインです。エージェントからの報告や質問と、エージェントが書く文書（README・仕様書・コミットメッセージなど）の両方が対象です。

エージェントに長い作業を任せると、報告は、作業の途中で付けた呼び名や、黙って置いた前提のまま書かれがちです。読んだ人は「結局どういうこと？」と聞き返すことになります。wakariyasu は規則とスキルを足して、何をしたのかを読み手の知っている言葉で書かせます。

## 何が変わるか

「商品一覧の画面が遅いので直して」と頼んで席を外し、戻ってきたときの報告です。

**wakariyasu が無いとき**

> 案Bで進め、キャッシュは v2 に寄せました。表示は軽くなりました。残りは在庫ゼロ問題だけです。

**wakariyasu が有るとき**

> 商品一覧の画面が遅い件は、商品の情報をサーバーのメモリーに5分間残し、表示のたびにデータベースから読まない形にしました。表示にかかる時間は 2.1 秒から 0.4 秒になりました。
>
> 残っているのは、在庫が0の商品で画面の表示が崩れる不具合の1件です。

「案B」「v2」「在庫ゼロ問題」のような作業中の呼び名は、何をしたか・何が起きるかに置き換わり、「軽くなりました」は数字になります。

<details>
<summary>判断を求める問いかけ</summary>

**wakariyasu が無いとき**

> キャッシュの TTL、どっちにします？

**wakariyasu が有るとき**

> **1. 商品の情報をサーバーに残す時間を、5分と1時間のどちらにするか**
>
> 商品一覧の表示を速くする作業の途中で、商品の情報をサーバーに残す時間を決める必要が出ました。在庫の数が画面に遅れて出てもよい時間は、お店の運用で決まるので、判断をお願いします。
>
> | 案 | 背景・選ぶと起きること |
> |---|---|
> | A（お勧め） | 5分。在庫の数は最大5分遅れて表示されます。表示は 0.4 秒です。在庫切れの商品が在庫ありと出続けるのを5分以内に抑えられるので、お勧めです。 |
> | B | 1時間。表示は 0.3 秒になりますが、在庫の数は最大1時間遅れます。 |

問いかけの番号と案の記号だけで、「1 は A」のように答えられます。

</details>

<details>
<summary>エージェントが書く文書</summary>

**wakariyasu が無いとき**（設計書の一節）

> レビューの指摘を受けて、本章ではキャッシュの方針を整理する。詳細は後述。

**wakariyasu が有るとき**

> 商品の情報は、サーバーのメモリーに5分間残す。5分を過ぎた情報は、次に表示するときにデータベースから読み直す。

前の文は、レビューのやり取りを知っていて、後ろの章まで読んだ人にしか分かりません。後の文は、その一節だけで方針が分かります。

</details>

## 機能

wakariyasu は、エージェントへの指示文の集まりです。**規則**は、頼まなくても毎回の返答と文書に当てはまります。**スキル**は決まった仕事の手順で、表にある頼み方をしたときや、その仕事が来たときに、エージェントが選んで使います。

| 場面 | 頼み方の例 | 使われるもの | エージェントがすること |
|---|---|---|---|
| いつもの返答 | （頼まなくても） | 規則 [`writing-to-user.md`](skills/writing-rules/rules/writing-to-user.md) | 経緯を知らない人に通じる返答を書く |
| 文書を書く | （頼まなくても） | 規則 [`writing-documents.md`](skills/writing-rules/rules/writing-documents.md) | 文書だけで通じるように書く |
| 文章を渡す前 | （頼まなくても） | 規則 [`polishing.md`](skills/writing-rules/rules/polishing.md) | 書いた文章を整える |
| 状況を知りたい | 「現状は？」 | `session-status` | ゴール・タスクと状態を報告し、判断してほしいことを問いかける |
| 返答が分からない | 「つまり？」 | `explain-clearly` | 短く、または前提を足して言い直す |
| 文書が自分のことを語っている | 「メタ記述を除いて」 | `remove-meta-narrative` | 文書自身や作った経緯を語る文を直す |
| 文書を人に渡す前 | 「読み手の目でレビューして」 | `review-for-readers` | 経緯を知らない別のエージェントに読ませ、引っかかった箇所を直す |
| 変更を見たい | 「差分を見せて」 | `show-changes` | リポジトリをまたぐ差分も1つのページにする |
| 読ませるページが欲しい | 「ページにして」 | `compose-page` | 読み手が知りたいことから HTML のページを組み立てる |
| スキルを点検したい | 「このスキルを点検して」 | `clarify-skill` | エージェントへの指示文として点検し、頼めば書き直す |
| セッションを残したい | 「このセッションをまとめて」 | `summarize-session` | 分かったこと・決めたこと・受けた指摘を、居なかった人が使える文書にする |
| 文字起こしがある | 「知見を抜き出して」 | `extract-insights` | 会議の記録や文書から、ほかの人が使える知見を取り出す |
| 言い回しを確かめたい | 「言い回しを確かめて」 | `check-terms` | 文書の言語の一覧から、使わない言い回しを探して替える |

返答と文書は、それぞれ書く物の言語の慣習に従います。慣習は言語パック（[`skills/writing-rules/lang/`](skills/writing-rules/lang/)）にあり、日本語と英語を同梱しています。

## インストール方法

- **Claude Code:** 「Claude Code のプラグイン」でインストールします。
- **claude.ai のチャットと Cowork:** 「Claude のアプリと Cowork」でインストールします。
- **Codex・Cursor・GitHub Copilot などのエージェント:** `npx skills add`・`gh skill install`・`npx openskills install` のどれかでスキルをインストールし、規則を指示のファイルに貼ります。どれでも同じスキルが入るので、手元にあるコマンドで選んでください（`npx` は Node.js に付いていて、`gh` は GitHub CLI のコマンドです）。

インストールできたかは、新しいセッションで「現状は？」と聞いて確かめます。「現在のゴール」「タスク」のような見出しのある報告が返ってくれば、インストールできています。

<details>
<summary>1. Claude Code のプラグイン</summary>

Claude Code の中で次の2つを実行します。規則とスキルの両方が入り、規則はセッションを始めるたびに読み込まれます。

```text
/plugin marketplace add kulikala/wakariyasu
/plugin install wakariyasu@wakariyasu
```

アップデートは、ターミナルで次の2つを実行し、Claude Code を起動し直します。

```sh
claude plugin marketplace update wakariyasu
claude plugin update wakariyasu@wakariyasu
```

</details>

<details>
<summary>2. Claude のアプリと Cowork</summary>

claude.ai の Web かデスクトップアプリで **Customize > Plugins** を開き、**Add > Add marketplace** に `kulikala/wakariyasu` を入力して、wakariyasu をインストールします。アカウントにインストールされるので、同じアカウントのスマホのアプリと Cowork でも使えます。

Cowork では Claude Code と同じく規則が読み込まれます。チャットでは読み込まれないので、毎回の返答に規則を当てはめたいときは、[`AGENTS.snippet.md`](AGENTS.snippet.md) の全文を **Settings > Your Claude > Instructions** か、プロジェクトの指示に貼ります。欄に収まらなければ、節「Write replies that someone who has not followed the session can understand」だけを、最初と最後のコメントの行で挟んで貼ります。

</details>

<details>
<summary>3. <code>npx skills add</code></summary>

[skills](https://github.com/vercel-labs/skills) のコマンドで、スキルをインストールします。

```sh
# 新規インストール
npx skills add kulikala/wakariyasu --skill '*' -g

# 最新版へのアップデート
npx skills update -g
```

`--skill '*'` はすべてのスキルを入れる指定です。スキルは `writing-rules` の規則を共有するので、一部ではなくすべてを入れます。`-g` はホームディレクトリに入れて、どのフォルダでも使えるようにする指定です。入れるエージェントは `-a` で選べます。

続けて「[規則を貼る](#規則を貼る)」の手順で規則を貼ります。

</details>

<details>
<summary>4. <code>gh skill install</code></summary>

GitHub CLI の `gh skill`（プレビュー版の機能）で、スキルをインストールします。

```sh
# 新規インストール
gh skill install kulikala/wakariyasu --all --scope user

# 最新版へのアップデート
gh skill update --all
```

`--all` はすべてのスキルを入れる指定、`--scope user` はホームディレクトリに入れてどのフォルダでも使えるようにする指定です。入れるエージェントは `--agent` で選べます。

続けて「[規則を貼る](#規則を貼る)」の手順で規則を貼ります。

</details>

<details>
<summary>5. <code>npx openskills install</code></summary>

[OpenSkills](https://github.com/numman-ali/openskills) で、作業しているリポジトリにスキルを入れ、スキルの一覧をそのリポジトリの AGENTS.md に書き込みます。

```sh
# 新規インストールと AGENTS.md への反映
npx openskills install kulikala/wakariyasu -y
npx openskills sync -y

# 最新版へのアップデートと AGENTS.md への反映
npx openskills update
npx openskills sync -y
```

`install` の `-y` は確かめずにすべてのスキルを入れる指定、`sync` の `-y` は確かめずにすべてを AGENTS.md に書く指定です。ホームディレクトリに入れるときは `--global` を付けます。

続けて「[規則を貼る](#規則を貼る)」の手順で、`sync` が書いた AGENTS.md に規則を貼ります。

</details>

### 規則を貼る

3〜5 の方法で入るのはスキルだけです。スキルは動くときに規則を読みますが、毎回の返答と文書に規則を当てはめるには、[`AGENTS.snippet.md`](AGENTS.snippet.md) の全文を、エージェントが毎回読む指示のファイル（Codex なら AGENTS.md、ほかのエージェントならカスタム指示）に貼ります。言語パックは貼りません。エージェントが、インストールしたスキル `writing-rules` から読みます。

スキルをアップデートしても、貼った規則は変わりません。アップデートしたら、`<!-- wakariyasu:AGENTS.snippet.md -->` から `<!-- /wakariyasu:AGENTS.snippet.md -->` までを、最新の `AGENTS.snippet.md` に入れ替えます。

## 別途必要なソフトウェア

> [!NOTE]
> `show-changes` と `session-status` のページを作るとき、言語パック（1つの言語の慣習。「仕組み」を参照）の無い言語で雛形を出すときに、Python 3 を使います。規則とほかのスキルには要りません。

## 仕組み

<details>
<summary>言語パックと決まった語</summary>

規則とスキルは英語で書いてあり、どの言語の文章にも当てはまります。1つの言語だけに必要なことは、その言語のパック（[`skills/writing-rules/lang/<コード>/`](skills/writing-rules/lang/)）にあります。返答用の `reply.md`、文書用の `documents.md`、スキル用の `skills.md` です。言語を切り替える設定はありません。エージェントは、書く物1つずつについて、その物の言語でパックを選びます。日本語で英語の README を頼めば、返答は日本語のパックで、README は英語のパックで書きます。

見出し・列名・状態の語は、エージェントが打ち込むのではなく、ツールが入れます。語は各パックの `labels.json` にあります。パックの無い言語では、エージェントが `--init` で語の一覧を作って訳し、`--labels` でツールに渡します。

使わない言い回しの一覧は [`skills/check-terms/lang/`](skills/check-terms/lang/) にあり、`sh skills/check-terms/scripts/check-terms <ファイル>` で文書を確かめられます。

</details>

<details>
<summary>日本語の表記の選び方</summary>

かなと漢字の使い分け・数字の書き方・体言止め・常体と敬体は、次の順で決めます。

1. ユーザーの指示（CLAUDE.md や AGENTS.md の指示を含みます）
2. 同じ文書や同じリポジトリで、すでに使われている書き方
3. 文章の種類ごとの既定（表は [`documents.md`](skills/writing-rules/lang/ja/documents.md) にあります）

語の選び方も、和語と漢語のどちらにも寄せない標準表記か、漢語を中心にする漢語表記かを、文書の目的と読み手から選びます。決まった書き方にしたいときは、CLAUDE.md に「数字は算用数字で書く」「README は敬体で書く」のように1行で書いてください。既定より優先されます。

</details>

<details>
<summary>文章を推敲するスキルとの組み合わせ</summary>

wakariyasu が見るのは、経緯を知らない人に語と内容が通じるかです。文の書き方を細かく直すのは、文章を推敲するスキルの役目です。文書の言語を推敲するスキルが入っていれば、エージェントは、人に渡す文書を wakariyasu の規則で整えたあとに、そのスキルにも通します。返答は通しません。推敲のスキルが無くても、wakariyasu は動きます。

</details>

## 開発者ガイド

フォルダの構成・検査（`dev/test`）・リリースの手順は [開発ガイド](docs/development.md) にあります。バージョンごとの変更は [CHANGELOG.ja.md](CHANGELOG.ja.md) にあります。

## 謝辞

規則の一部は、日本語の推敲スキル [yomiyasu](https://github.com/nanaism/yomiyasu)（nanaism/yomiyasu、MIT ライセンス）を参考にしています。

## ライセンス

MIT
