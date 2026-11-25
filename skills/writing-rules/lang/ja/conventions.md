# 日本語の読み手が見慣れた名前

日本語で記述する返答と文書では、見出し・列名・状態の語に、この節の名前を使う。読み手は見慣れた名前を手がかりに読む所を探し、エージェントが毎回訳した名前では探せない。

## README

README は、人が手で保守している日本語の README で見慣れた章の名前・組み立て・言葉で記述する。各章の方針に無い章の名前や言い回しは、ファイルやウェブを読めるなら、同じ分野で人が日本語の README を保守しているツールをいくつか開き、ツールの README で使われている形に合わせる。

`readme.md` の各章は、日本語の README では次の名前で記述する。

| `readme.md` の章 | 日本語の章の名前 |
|---|---|
| Opening description | （見出しを立てず、README の冒頭に記述する） |
| Features | 機能 |
| Strengths | 特長 |
| Suitable uses | 向いている用途 |
| Disclaimer | 免責事項 |
| Supported environments | 対応環境 |
| Required disk space and additional software | 必要なディスク容量・別途必要なソフトウェア |
| Installation | インストール方法 |
| Usage | 使い方 |
| Developer guide and license | 開発者ガイド・ライセンス |

`readme.md` の「Wording」の節に加えて、日本語の README では次のようにする。

- 一般の語：日本語では使わない言い回しと、代わりに使う語は、wakariyasu のスキル `check-terms` の一覧（`lang/ja/terms.tsv`）にある。一覧に無い語も同じ考え方で選ぶ。
- 作業の章と節の名前：インストールや設定のように読み手が手を動かす章と節は、「インストール方法」「セットアップ方法」「アップデートの手順」のような、日本語の README で見慣れた名前にする。和語に言い換えた名前では、読み手は探している章だと気付かない。本文の語も見出しと同じ語でそろえる。

## 変更履歴

Keep a Changelog の日本語の版（https://keepachangelog.com/ja/1.1.0/）とセマンティック バージョニングの日本語の版（https://semver.org/lang/ja/）を参照する。変更の種類の小見出しは「追加」「変更」「非推奨」「削除」「修正」「セキュリティ」にする。

## session-status の報告

| 英語の名前 | 日本語で記述するときの名前 |
|---|---|
| Current goal | 現在のゴール |
| Latest instruction | 直近の指示 |
| Tasks | タスク |
| Latest status | 直近のステータス |
| Decisions needed | 判断を求めていること |
| Task（タスクの表の列） | タスク |
| State（タスクの表の列） | 状態 |
| Background and notes（タスクの表の列） | 背景・補足 |

状態欄の語は次のとおり。絵文字は変えない。

| 英語の表記 | 日本語の表記 |
|---|---|
| ✅ Done | ✅ 完了 |
| 🚧 In progress | 🚧 作業中 |
| ⏳ Waiting on a process | ⏳ 処理待ち |
| 🙋 Waiting for your decision | 🙋 判断待ち |
| 📝 Not started | 📝 未着手 |
| ❗ Problem | ❗ 問題あり |
| ⛔ Cancelled | ⛔ 中止 |

## 判断の問いかけ

| 英語の名前 | 日本語で記述するときの名前 |
|---|---|
| Option（表の列） | 案 |
| Background and what happens if chosen（表の列） | 背景・選ぶと起きること |
| (recommended) | （お勧め） |

## session-status のページ

日本語の報告からページを作るときは、`lang` を `ja` にし、`labels` に次の語を渡す。見出し・列名・状態の語は、上の「session-status の報告」と「判断の問いかけ」の節の名前と同じにする。`{asOf}`・`{n}`・`{answered}`・`{total}`・`{title}` は、ページが値を入れる箇所なので、そのまま残す。

```json
{
  "pageKind": "セッションの状況",
  "asOf": "{asOf} 時点",
  "goal": "現在のゴール",
  "instruction": "直近の指示",
  "tasks": "タスク",
  "status": "直近のステータス",
  "decisions": "判断を求めていること",
  "colTask": "タスク",
  "colState": "状態",
  "colNotes": "背景・補足",
  "colOption": "案",
  "colOptionDetail": "背景・選ぶと起きること",
  "recommended": "（お勧め）",
  "decisionRef": "（{n}）",
  "stateDone": "完了",
  "stateInProgress": "作業中",
  "stateWaitingProcess": "処理待ち",
  "stateWaitingDecision": "判断待ち",
  "stateNotStarted": "未着手",
  "stateProblem": "問題あり",
  "stateCancelled": "中止",
  "noteLabel": "添えるメッセージ（任意）",
  "notePlaceholder": "条件や理由など、エージェントに伝えたいこと",
  "freeAnswerLabel": "回答",
  "freeAnswerPlaceholder": "回答を記入してください",
  "clearAnswer": "この回答を消す",
  "overallLabel": "報告全体へのメッセージ（任意）",
  "overallPlaceholder": "ほかにエージェントに伝えたいこと",
  "previewLabel": "セッションに貼り付ける文",
  "progress": "{total} 問中 {answered} 問に回答済み",
  "copy": "回答をコピー",
  "copied": "コピーしました",
  "copyFailed": "ここではコピーできませんでした。上の欄の文を選んでコピーしてください。",
  "copyHeading": "「{title}」の判断を求めていることへの回答",
  "copyAnswer": "回答",
  "copyNoAnswer": "（未回答）",
  "copyNote": "メッセージ",
  "copyOverall": "報告全体へのメッセージ"
}
```

## show-changes のページ

日本語のページを作るときは、次の語を JSON のファイルに書き、`build.py` に `--lang ja --labels <そのファイル>` を渡す。`--title` を渡さないときのページの見出しは、`defaultTitle` の語になる。`{n}`・`{path}`・`{name}`・`{mode}`・`{y}`・`{m}`・`{d}`・`{w}`・`{first}`・`{last}` は、ページが値を入れる箇所なので、そのまま残す。`weekdays` はコンマで区切った日曜から土曜までの 7 語で、`partSep` は文を続けるときの区切りである。

```json
{
  "defaultTitle": "差分レビュー",
  "filesOne": "{n} ファイル",
  "filesMany": "{n} ファイル",
  "sidebar": "変更したファイル",
  "source": "対象",
  "sourceAll": "すべて",
  "sourceTitle": "ファイルの一覧に出す対象を選ぶ",
  "filterPlaceholder": "ファイル名・本文を検索",
  "filterTitle": "ファイル名か本文に、入力した文字列を含むファイルだけを出す",
  "clearFilter": "検索の文字列を消す",
  "clearFilterTitle": "検索の文字列を消して、すべてのファイルを出す",
  "contentOnly": "追加・変更したファイルだけ",
  "contentOnlyOn": "追加・変更したファイルだけを出しています。押すと、すべてのファイルを出す",
  "contentOnlyOff": "押すと、追加・変更したファイルだけを出す（削除・移動・複製・権限だけの変更・シンボリックリンクを出さない）",
  "jumpTo": "{path} の差分へ移動",
  "noFiles": "該当するファイルはありません。",
  "resizer": "ファイル一覧の幅",
  "resizerTitle": "ドラッグで幅を変える（ダブルクリックで元の幅）",
  "toolbar": "差分の表示設定",
  "showList": "ファイル一覧を出す",
  "hideList": "ファイル一覧を隠す",
  "backToList": "ファイル一覧に戻る",
  "copySelection": "選んだ文字列をコピー",
  "copiedSelection": "選んだ文字列をコピーしました",
  "copied": "コピーしました",
  "noNewline": "行末に改行がありません",
  "spaceOnly": "空白の違いだけです。「空白」で「表示」を選ぶと、違いが見えます。",
  "noTextRows": "表示するテキスト行はありません。",
  "modeRegular": "通常のファイル",
  "modeExecutable": "実行できるファイル",
  "modeSymlink": "シンボリックリンク",
  "modeSubmodule": "サブモジュール",
  "modeOther": "モード",
  "modeFormat": "{name}（{mode}）",
  "symlinkNote": "シンボリックリンクの差分は、リンク先のパスです。",
  "partSep": "。",
  "statusA": "追加",
  "statusM": "変更",
  "statusD": "削除",
  "statusR": "移動",
  "statusC": "複製",
  "statusT": "種類変更",
  "statusU": "未解決",
  "statusX": "不明",
  "statusB": "分割",
  "fullMissing": "全文は含まれていません。変更箇所を表示します。",
  "fileClose": "押すと、このファイルの差分を閉じる",
  "fileOpen": "押すと、このファイルの差分を開く",
  "copyPath": "パスをコピー",
  "copiedPath": "パスをコピーしました",
  "root": "ルート",
  "commitsClose": "押すと、コミットの一覧を閉じる",
  "commitsOpen": "押すと、コミットの一覧を開く",
  "mergeBase": "の分岐点",
  "commitsOne": "{n} コミット",
  "commitsMany": "{n} コミット",
  "newestFirst": "新しい順",
  "subjectShrink": "押すと、件名を2行に縮める",
  "subjectExpand": "押すと、コミットメッセージの全文を出す",
  "newestOnlyTitle": "新しい 10 件だけを出す",
  "restTitle": "残りのコミットもすべて出す",
  "newestOnly": "新しい 10 件だけにする",
  "rest": "残り {n} 件を表示",
  "dayFormat": "{y}年{m}月{d}日（{w}）",
  "weekdays": "日,月,火,水,木,金,土",
  "monthDay": "{m}月{d}日",
  "spanRange": "{first}〜{last}",
  "ctlFold": "開閉",
  "openAll": "すべて開く",
  "openAllTitle": "一覧に出ているファイルの差分をすべて開く",
  "closeAll": "すべて閉じる",
  "closeAllTitle": "一覧に出ているファイルの差分をすべて閉じる",
  "ctlLayout": "配置",
  "layoutUnified": "上下",
  "layoutUnifiedTitle": "変更前と変更後の行を上下に並べる",
  "layoutSplit": "左右",
  "layoutSplitTitle": "変更前と変更後を左右に並べる",
  "ctlScope": "範囲",
  "scopeDiff": "差分",
  "scopeDiffTitle": "変わった行と、その前後の数行だけを表示する",
  "scopeFull": "全文",
  "scopeFullTitle": "ファイルの全文を表示し、変わった行に色を付ける",
  "ctlSpace": "空白",
  "spaceShow": "表示",
  "spaceShowTitle": "空白の違いを表示し、変わった空白を記号で示す",
  "spaceIgnore": "無視",
  "spaceIgnoreTitle": "空白（全角スペース・タブ・行末の CR を含む）の違いだけの行を、変わっていない行として表示する。空行の追加と削除は表示する",
  "ctlTheme": "配色",
  "themeLight": "ライト",
  "themeLightTitle": "明るい配色にする",
  "themeDark": "ダーク",
  "themeDarkTitle": "暗い配色にする",
  "themeHybrid": "ミックス",
  "themeHybridTitle": "周りはダーク、差分の部分だけライト",
  "noticeBinary": "バイナリファイルです。",
  "noticeNoDiff": "内容の差分はありません。",
  "noticeSubmodule": "サブモジュールは参照コミットの差分を表示します。",
  "noticeUnreadable": "UTF-8 として読めないバイトは \\xNN の形で表示しています。",
  "noticeNoFull": "全文は差分ファイルから復元できないため含まれません。"
}
```
