# 変更履歴

[English](CHANGELOG.md) | 日本語

バージョンの番号は [セマンティック バージョニング](https://semver.org/lang/ja/) に従います。
規則やスキルの書き方が変わり、エージェントの振る舞いが変わる変更は、マイナーバージョンを上げます。

## [1.0.1] - 2026-11-28

### 追加

- `show-changes` のページに、ワープロの変更履歴のように読めるインラインの配置を足した。差分の記号を付けずに変更後の文章を並べ、変わった語に色を付け、削除された所に幅の狭い印を置き、マウスを載せると前の文章を出す。

### 変更

- `show-changes` と `session-status` のページを、`compose-page` のページと同じ1ファイルの雛形で作るようにした。明るい表示と暗い表示も同じ形になる。
- `--artifact` を付けたとき、どちらのページも Claude のアーティファクトが公開時に付ける文書の骨組みを含めずに出すようにした。公開したページの中に、もう一つの文書が入れ子になることがなくなる。
- `show-changes` は、ページのデータを圧縮する utfpack の packer として、wakariyasu に同梱したコピーではなく、ページを作るときに jsDelivr から取ったものを使うようにした。取れなかったときは前に取ったものを使う。初めてページを作るときはネットワークへの接続が要り、utfpack の更新は wakariyasu の更新を待たずに入る。

## [1.0.0] - 2026-11-27

### 追加

- スキル `compose-page`。人に読ませるページ（報告・提案・比較）を、読み手が知りたいことから組み立てる。
- スキル `extract-insights`。会議の記録や文書から、ほかの人が使える知見を取り出す。
- `session-status` の報告を HTML のページにもできる。ユーザーはページで問いかけに答え、答えをコピーしてセッションに貼れる。
- `show-changes` で、変更だけでなくファイルの全文も見せられる。スキルや文書の全文を見せるよう頼まれたときにも使う。全文を入れたページは、変更後の全文だけの表示に切り替えられる。
- `show-changes` のページで、検索欄の Enter で次の該当箇所へ、Shift+Enter で前の該当箇所へ移る。
- `session-status` のページと、`compose-page` の雛形から作るページで、選んだ文字をその横に出るボタンでコピーできる。
- 言語パック。返答と文書は、それぞれ書く物の言語の慣習に従う。日本語と英語を同梱した。

### 変更

- エージェントがユーザーに判断を求めるのは、答えが無いと作業を続けられないときだけになった。ほかに見つけたことは事実として報告する。公開するか・送るかのような最終結論は、作業が済み、依頼がそこまで含むときにだけ求める。
- `show-changes` のページは、データを utfpack で圧縮したので、0.11.0 の約3分の1の大きさになった。ページは開くときに、データを戻すデコーダを jsDelivr から読むので、開くにはネットワークへの接続が要る。`build.py --embed-decoder` を付けると、デコーダをページに入れる。
- 仕組みや変更を説明する返答は、全体から述べる。
- エージェントが書く指示文と `clarify-skill` の点検で、エージェントが写してしまうサンプルのデータ・出力・ツールのメッセージの引用を避ける。
- エージェントが書く README は、細かい内容を折りたたみ、GitHub が描画する Markdown で書き、言語ごとの版を訳さずにその言語の読み手に向けて書く。
- Web ページ・アーティファクト・スライド・Office の文書も、ほかの文書と同じく整えてから渡す。
- 規則とスキルを英語で書いた。README と変更履歴には日本語版もある。
- `show-changes` のページは、ほかの言語を指定しなければ英語で表示する。
- `AGENTS.snippet.md` を貼っている人は、新しい全文に入れ替える。

### 修正

- Claude Code で、セッションの始めに読み込む規則が途中で切れていた。全文が届くようになった。

## [0.11.0] - 2026-11-11

### 追加

- エージェントが、文書の目的と読み手から表記を選ぶ。表記は CLAUDE.md で指定できる。

## [0.10.0] - 2026-11-09

### 追加

- Codex・Cursor・GitHub Copilot などのエージェントにも、`npx skills add` と `npx openskills install` でスキルを入れられる（[インストール方法](README.ja.md#インストール方法)）。
- 日付を、文書の言語と読み手の地域の形で書く。
- `show-changes` のページで、ボタンが何をするかを表示し、検索の欄を消せるようにした。

### 変更

- エージェントが書く変更履歴は、何をしたかではなく、使う人にとって何が変わったかを伝える。
- エージェントが書く文書と指示文で、項目の数・繰り返し・要らない補足が減った。
- `summarize-session` は、頼まれなければ作業の記録を文書に入れない。
- `AGENTS.snippet.md` を短くした。貼っている人は、新しい全文に入れ替える。
- `show-changes` のページで、ファイルを閉じても読んでいた位置を保ち、効かない操作は出さない。

## [0.9.0] - 2026-11-06

### 追加

- スキル `summarize-session`。セッションの内容を、居なかった人が使える文書にする。

### 変更

- Claude が動く環境では、`show-changes` のページをアーティファクトで示す。
- 試作や下書きも含め、渡す文書はすべて整えてから渡し、どの手順を行ったかを返答で伝える。
- 文書の中のファイルを、書き手の PC のパスではなく、読み手が見つけられる形で示す。
- ユーザーが指定した書式を残し、`clarify-skill` もそれに従う。

### 修正

- GNU の sed と grep を使う Linux で、`check-terms` が失敗していた。

## [0.8.0] - 2026-11-06

### 追加

- 規則と言い回しの一覧を持つスキル `writing-rules` と `check-terms`。`gh skill install` で入れた人は `--all` を付けて入れ直す。
- スキル `show-changes`。リポジトリやフォルダをまたぐ差分を1つのページにする。
- スキル `clarify-skill`。スキルを、エージェントへの指示文として点検する。

### 変更

- 文書の種類（スキル・README・変更履歴・コミットメッセージ）に合った手順で整える。
- `AGENTS.snippet.md` に貼った範囲の印を付け、アップデートで入れ替えられるようにした。

## [0.7.0] - 2026-11-04

### 変更

- 返答で、同じ対象は同じ語で呼び、結論に掛かる条件を落とさない。
- 推敲で、読み手の助けにならない比喩や飾りを除く。

## [0.6.0] - 2026-11-04

### 追加

- `check-terms` が、文脈によっては別の語のほうが自然な言い回しにも印を付ける。
- `remove-meta-narrative` が、作業の途中の書き残しも見つける。

### 変更

- ユーザーに聞くのは意図と承認だけにし、手段はエージェントが決める。
- 文書で、指示語を使わず、示す対象の名前を書く。
- セッションの始めに読み込む量を減らした。

## [0.5.2] - 2026-10-30

### 変更

- Claude のアプリと Cowork にインストールできるようにした。手順は README にある。

## [0.5.1] - 2026-10-27

### 修正

- 一部の Linux のロケールで、`check-terms` が動かなかった。

## [0.5.0] - 2026-10-27

### 追加

- README の書き方のガイド。
- 使わない言い回しの一覧と、文書からそれを探す `check-terms`。

### 変更

- 判断の問いかけで、作業が目指すことと、何に当たって止まったかを述べる。

## [0.4.0] - 2026-10-25

### 追加

- 判断の問いかけの形（番号付きの見出し・理由・選択肢の表）。`session-status` も同じ形を使う。
- エージェントへの指示文の書き方のガイド。

## [0.3.0] - 2026-10-23

### 変更

- 推敲の確認を、どの言語にも当てるものと、言語ごとに足すものに分けた。
- `session-status` と `explain-clearly` はどの言語でも使え、報告は返答の言語で書く。

## [0.2.3] - 2026-10-22

### 変更

- yomiyasu を wakariyasu のマーケットプレイスから外した。作者のマーケットプレイスから入れる。

## [0.2.2] - 2026-10-22

### 変更

- README の yomiyasu の節を短くした。

## [0.2.1] - 2026-10-22

### 変更

- 整える手順に、yomiyasu を呼ぶ場所を書いた。

## [0.2.0] - 2026-10-22

### 変更

- まず自分で推敲し、人に渡す文書だけ yomiyasu も呼ぶ。

## [0.1.0] - 2026-10-21

### 追加

- 規則 `writing-to-user`・`writing-documents`・`polishing`。
- スキル `session-status`・`explain-clearly`・`remove-meta-narrative`・`review-for-readers`。
- セッションの始めに規則を読み込むフックと、ほかのエージェントに貼る `AGENTS.snippet.md`。

[1.0.1]: https://github.com/kulikala/wakariyasu/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/kulikala/wakariyasu/compare/v0.11.0...v1.0.0
[0.11.0]: https://github.com/kulikala/wakariyasu/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/kulikala/wakariyasu/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/kulikala/wakariyasu/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/kulikala/wakariyasu/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/kulikala/wakariyasu/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/kulikala/wakariyasu/compare/v0.5.2...v0.6.0
[0.5.2]: https://github.com/kulikala/wakariyasu/compare/v0.5.1...v0.5.2
[0.5.1]: https://github.com/kulikala/wakariyasu/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/kulikala/wakariyasu/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/kulikala/wakariyasu/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/kulikala/wakariyasu/compare/v0.2.3...v0.3.0
[0.2.3]: https://github.com/kulikala/wakariyasu/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/kulikala/wakariyasu/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/kulikala/wakariyasu/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/kulikala/wakariyasu/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/kulikala/wakariyasu/releases/tag/v0.1.0
