# 変更履歴

バージョンの番号は [セマンティック バージョニング](https://semver.org/lang/ja/) に従います。
規則やスキルの書き方が変わり、エージェントの振る舞いが変わる変更は、マイナーバージョンを上げます。

## [0.5.0] - 2026-10-27

### 追加

- リファレンス「README の書き方」（`references/readme.md`）を加えた。リポジトリの最上位に置いて外部に公開する
  日本語の README を、人が保守している日本語の README で見慣れた章の名前・組み立て・言葉で書くための方針で、
  章ごとの目的、1つの章にはその章の目的に当たる中身だけを書くこと、用語の選び方を含む。章の並びは決めない。
- 規則 `writing-documents` から、リポジトリの最上位に置いて外部に公開する README を書く・直すときに、このリファレンスを読むようにした。
- 日本語では使わない言い回しの一覧（`references/terms.tsv`）と、文書からそれを探すスクリプト `scripts/check-terms` を加えた。
  一覧は、使わない言い回し・代わりに使う語・検出と除外の正規表現を持つ。フックが一覧を表にして読み込ませ、
  規則 `polishing` の「日本語では使わない言い回しを探す」で、文書を yomiyasu に通す前に `check-terms` をかける。

### 変更

- リファレンス「判断の問いかけの書き方」で、問いかけの段落に、何を目指す作業の途中か、その作業で何に行き当たって
  判断が必要になったかを書くようにした。表の列には、選ぶと作業の目的に向けて何が起きるかを書く。
- wakariyasu の規則・リファレンス・スキルの本文から、一覧の言い回し（「問い」「要る〜」「版」など）を言い換えた。

## [0.4.0] - 2026-10-25

### 変更

- 規則 `writing-to-user` の判断の問いかけを、リファレンス「判断の問いかけの書き方」（`references/asking.md`）に沿う書き方にした。
  問いごとに、セッションの通し番号の見出し、ユーザーが決める理由、お勧めの度合いの高い順の案の表を書く。
  案の記号には A・B・C… と、二択の Y・N を使える。
- 規則 `writing-to-user` から、問う前に答えの案を出し、調べれば分かることは聞かずに調べる、という項目を外した。
  いつ問うかは決めず、問いの書き方だけを決める。
- スキル `session-status` の「判断を求めていること」を、同じリファレンスの形にした。
- 規則 `writing-documents` から、スキル・規則・プロンプトを書くときに、リファレンス
  「エージェント向けの指示文の書き方」（`references/writing-instructions.md`）を読むようにした。

### 追加

- リファレンス `references/asking.md` と `references/writing-instructions.md`。
  フック・各スキルの写し・`AGENTS.snippet.md` にも入れた。

## [0.3.0] - 2026-10-23

### 変更

- 規則 `polishing` を「書いた文章は、渡す前に整える」とし、どの言語でも確かめる項目と、
  日本語で書いたときに足す項目（表記の選び方・読点・yomiyasu）に分けた。
- 規則 `writing-to-user` の指す先の確かめ方を、指示語一般の書き方にし、英語に直訳して確かめる方法を
  日本語の文のための手順として分けた。
- `session-status` と `explain-clearly` はほかの言語で同じ意味のことを聞かれたときも使う。
  `session-status` の見出しと状態の語は返答と同じ言語で書く。
- 英語の README を外し、日本語の README の冒頭に英語でプラグインの説明を置いた。
- フックと `AGENTS.snippet.md` に、日本語の表記の表（`references/styles.md`）も入れた。

### 追加

- `.editorconfig`・`.gitattributes`・`.gitignore`。
- リポジトリの決まりを確かめる `bin/test` と、それを動かす GitHub Actions。
- スキルが呼ばれるかを測る `claude plugin eval` のケース（`evals/`）。
- 開発の手引き（`docs/development.md`）。

## [0.2.3] - 2026-10-22

### 変更

- wakariyasu の入手先から yomiyasu を外した。yomiyasu は作者の入手先から入れる。

## [0.2.2] - 2026-10-22

### 変更

- README の yomiyasu の節を、入っていれば呼ぶことと、入れ方の案内だけにした。

## [0.2.1] - 2026-10-22

### 変更

- 規則 `writing-documents` の仕上げの手順と、`review-for-readers` の読み直しのあとに、
  yomiyasu を呼ぶ場所を書いた。

## [0.2.0] - 2026-10-22

### 変更

- 整える手順を、まず自分で整え、人に渡す文書だけ yomiyasu にも通す順にした。
  ユーザーへの返答では yomiyasu を呼ばない。
- 自分で整える項目に、前置きの句・間を取るだけの読点・疑問形の見出し・太字とコロンの箇条書き・
  否定してから言い直す文・同じ文末の連続を足した。

## [0.1.0] - 2026-10-21

### 追加

- 規則 `writing-to-user`・`writing-documents`・`polishing` と、日本語の表記の表。
- スキル `session-status`・`explain-clearly`・`remove-meta-narrative`・`review-for-readers`。
- セッションの始めに規則を読み込ませるフック。
- Claude Code 以外のエージェントに貼る `AGENTS.snippet.md`。

[0.5.0]: https://github.com/kulikala/wakariyasu/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/kulikala/wakariyasu/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/kulikala/wakariyasu/compare/v0.2.3...v0.3.0
[0.2.3]: https://github.com/kulikala/wakariyasu/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/kulikala/wakariyasu/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/kulikala/wakariyasu/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/kulikala/wakariyasu/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/kulikala/wakariyasu/releases/tag/v0.1.0
