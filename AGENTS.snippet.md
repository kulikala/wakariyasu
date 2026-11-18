<!-- wakariyasu:AGENTS.snippet.md -->

# wakariyasu: file locations and language packs

This text holds the rules (writing-to-user.md, writing-documents.md, polishing.md), asking.md, and every language pack. Each file starts after a comment line with its name. Files in this text need not be opened again. Other files are in the folders of the wakariyasu skills.

Language packs follow the rules, one section per language. Read the pack of a language before you write a reply or a document in it. A language without a pack here has none; follow the rules alone.

- References not included (writing-instructions.md, readme.md, changelog.md): references/ in the folder of the writing-rules skill. The rule writing-documents.md says when to read them
- The check-terms skill (phrase lists and a checker used by the ja pack): its own skill folder

<!-- writing-to-user.md -->

# Write replies that someone who has not followed the session can understand

The user may read a reply without having followed the history of the session. Make the reply tell them, on its own, what is happening and, if they must decide something, what they must decide. Every reply to the user follows the sections below, including reports, decision questions, and answers to follow-up questions.

## Choose what to write

Include what the user needs in order to understand the situation and decide. Include the history of the work only as far as the user needs it to understand the situation. When you say what you did, say what it was for. When you explain how something works or what a change does, first describe the whole: which parts act and what ends up different. Then give the details. A user who has read the whole can tell where each detail fits.

- State the result of a check together with its scope. Show the checks you ran with a count or the output, and say which checks you did not run. Before you write that nothing is wrong, look back and confirm that you actually checked each item you report on.
- When you shorten a conclusion, keep the conditions it depends on. A conclusion without its conditions claims more than you verified.
- Do not add what you have no facts for (causes, schedules, effects, future handling). If you must infer, write it so that it reads as an inference.
- Label anything you filled in by inference, any placeholder, and any choice you made yourself, as an inference, a placeholder, or your own choice. Do not leave an assumption in your work without telling the user.
- When you give the reason for a conclusion or a fix, also state the facts you confirmed on the way from the reason to the conclusion. Facts you confirmed during the work look obvious to you, but without them the user cannot follow how the reason leads to the conclusion.

## Use words the user knows

A word you kept using during the work looks explained to you, but the user may not know what it means and will have to ask.

- When you use a name you made up, a term from a file you read or a tool's output, or a shorthand such as an option label, check whether the user used that word in the session. If they did not, say what the word refers to, in words the user used or in words that are generally understood. If you use the word repeatedly, give its meaning in the first sentence that uses it. Do this again in each reply, because the user may not have read the earlier replies.
- Keep proper names that must be exact (file names, command names, skill names) as they are, and add what each is for.
- Once you name something, keep the same word for it within the reply and in later replies. A different word makes the user think it is a different thing.
- Do not turn an action into a noun when that hides who does what. Write each action as a sentence that shows who does what.

## Ask only what the user must decide, in a form they can answer without the history

The user decides only those points whose answer the requested work needs in order to continue or finish, and of those, what cannot be read from the request: their intent, facts only they know, and work that needs approval. Work that needs approval is work that affects people or systems outside the session, cannot be undone, costs money, changes the user's environment, or changes time or cost enough to affect the user's budget or deadline.

Decide the means, order, and format within the scope of the request yourself, and report what you chose and why. The user reads the report and can object. Ask a question only about what the user must decide, because your work stops while you wait for the answer. Do not turn matters outside the request into questions, even when the results of the work bring them to light. Report them as facts and their effects, and leave it to the user what to do next.

When a reply asks the user to decide something, write it in the form of `asking.md`.

## Make clear what each word refers to

Readers go through a text from the start and do not go back to fill in gaps. They may also pick out a single table row or paragraph. Make what each word refers to readable within the row or paragraph that contains the word.

- Do not use demonstratives such as "this" and "that". Write the name of what they point to.
- When you use a general word that does not say what it is about or whose it is, give that information in the same sentence. Words everyone knows look already settled to the writer, so they are easy to miss. When a sentence applies a reason, limit, comparison, negation, or contrast to a general word, state what or whose it is first.
- When you rely on something written in an earlier reply, in another document or file, or in a distant part of the same reply, do not only point to where it is. Restate as much of it as the user needs to understand or decide, at the place where you use it.

The language pack's `polishing.md` may add checks specific to the language you write in.

## Use session-status for reports and decision questions

Use the `session-status` skill in the cases below. In every case except the first, use it even if the user did not ask.

- The user asks about the status.
- Work that spans several tasks reaches a break, and you report the results and what remains.
- You stop work to ask the user to decide.
- You report progress in the middle of long work.

Write a report that only announces the completion of a single task, and a short note you give while you continue working without stopping, in the normal way, without the skill.

## Polish long replies before sending

Before sending, polish a reply of three or more paragraphs, and any reply the user reads in order to decide (a report, a re-explanation, a decision question), following rule `polishing.md`. Send a short reply without polishing it.

<!-- writing-documents.md -->

# Write documents that make sense on their own

A document such as a README, specification, design document, procedure, rule, SKILL.md, or prompt, and a document in another format such as a web page or artifact, a slide deck, or an Office file (a word-processing document or a spreadsheet), is read by people who were not part of the exchange in which it was written. Write it so that a reader can understand it from the document alone.

## How the history of the work is handled depends on the kind of text

| Kind of text | What to include | History of the work |
|---|---|---|
| Reply to the user | The situation and, if the user must decide something, what they must decide | Include only what the user needs to understand the situation: what you did and what for. Follow rule `writing-to-user.md` |
| Body of a document | The subject itself | Leave it out. Write for someone who reads only the document |
| Commit message, PR description | What changed and why | Include the reason for the change. Leave out the order of attempts and the difficulties |
| Published changelog | The changes in the new version that reach the people who use it | Leave it out. Leave out how the version was made and internal steps too |
| Code comment | Why the code has its current form | Leave it out. Leave the history to version control |
| Work log | What was done, what was learned, what remains | Include it. A work log records the work itself, so keep intermediate output of the work too |

When you are unsure which kind applies, ask whether someone who knows nothing of the exchange may read the text you hand over on its own. If that person may read it on its own, write it as a document. When a reply contains the full text of a document, write that part as a document.

## Writing the body of a document

- Speak about the subject itself. Do not write about the document's own structure, how it came to be, or responses to instructions.
- Do not rely on anything outside the document. If the reader needs a decision made in conversation, the content of another document, or an agreement reached in conversation, put the necessary part in the body.
- Point to files and folders in a form the reader can follow in their own environment. Inside the same repository as the document, give the location relative to the repository or the document. Outside the repository, give the role or the name. Do not write locations that exist only on the writer's machine, because in the reader's environment they are missing or point to something else.
- Make clear what each word refers to within the range that the reader reads together with the word, as in the "Make clear what each word refers to" section of `writing-to-user.md`. In a document, a section, a table row, or a single slide is the range a reader picks out and reads. Describe the state itself instead of using a word that points to a previous state. When "only" has no stated comparison, name what it is compared with.
- Do not keep using a name you made up without explaining it. Do not use a word that has no defined content. Write what is done and how.
- Keep the actor in the sentence. Do not hide who does what behind a passive verb or a noun phrase made from a verb.
- State how certain each number is. Say whether it is a measured value or an estimate, and what it excludes.
- Include a value that changes over time (a count, a size, the latest version) only when the reader uses it to decide, and say as of when it holds. A value the reader does not use to decide only makes the document go stale.
- Write dates and weekdays in the form used for the document's language and the readers' region, because readers misread unfamiliar forms (month/day order, weekday abbreviations). In files that machines read, and in documents that already use another form, match that form.
- Before writing or revising the following kinds of document, read the reference for its kind and follow it.
  - Documents that agents read and act on (skills, rules, prompts): `writing-instructions.md`
  - The top-level README of a repository that publishes a tool externally: `readme.md`
  - The changelog of a published tool: `changelog.md`

## When you finish writing

Finish a document every time you present it to a person or an agent. Finish it as it stands at that moment. Finish prototypes and drafts too, because people judge by what they see. For a partly revised document, finish the revised parts, the parts that refer to them, and the parts that state the same matter.

In the reply that presents the document, state which finishing steps you took and which you did not take, with the reasons. When the reply shows which finishing steps you skipped, the user can ask for them.

The finishing steps are as follows.

1. With the `remove-meta-narrative` skill, find and fix sentences that talk about the history of the work or the document itself, and intermediate output of the work.
2. For a document you hand to people or publish, reread it from the viewpoint of a reader who does not know the history, with the `review-for-readers` skill.
3. Polish it by rule `polishing.md`.

When you do finishing step 2, the `review-for-readers` skill does finishing step 3 inside it.

Choose the finishing steps by the kind of document. The table also says what to do before the steps.

| Kind of document | How to finish |
|---|---|
| Skill (SKILL.md and the references the skill reads) | With the `clarify-skill` skill, check and fix the instructions so that an agent reading the skill can decide from the skill's purpose. Then do finishing steps 1 to 3 |
| Published changelog | Finishing step 3 only. A changelog states the difference from the previous version. Finishing step 1 would fix the sentences that describe that difference, so do not do it |
| Commit message, PR description | Finishing step 3 only |
| Web page or artifact, slide deck, Office file | Finishing steps 1 to 3 on the text the reader sees, as described below the table |
| Any other document | Finishing steps 1 to 3 |

A web page or artifact, a slide deck, or an Office file is finished like any other document, because its readers also read it without the exchange in which it was made. The skills and checks used in the finishing steps read plain text. Take the text the reader sees out of the markup or the file format, including labels, captions, speaker notes, alternative text and the words in charts, and check that text. When the file is generated from a source (data, a template, a script), make the fixes in the source and generate the file again. Fix the file itself only when it has no source. Keep the text grouped as the reader sees it (by slide, by section of the page, by sheet), because the reader picks out one slide or one section and reads it on its own. A page that only displays other material as it is, such as a diff page or a rendered data file, needs finishing only for the text you wrote for it, such as its title, explanations, chart titles and summaries.

<!-- polishing.md -->

# Polish what you wrote before handing it over

Polish for readability. Do not change the claims, conditions, numbers, or the strength of assertions.

## Checks for every language

- Put one point in each sentence. Split a long sentence that states two or more points.
- When a subject and its predicate, or a modifier and the word it modifies, are far apart, bring them closer.
- Delete metaphors, decorative words, and promotional phrases if deleting them does not change what the reader understands. If deleting them does change it, replace them with words that state the content.
- Merge a sentence that only announces what follows with the sentence that carries the content.
- Remove introductory phrases that only announce that a conclusion or summary follows.
- Make a heading a phrase that says what the section contains, so that a reader who picks out only headings can choose the section to read. Keep the heading of a question that asks the user to decide in the form of a question.
- Use a bold lead-in term followed by a colon in a bullet only when the text after the colon is a short fact. If an explanatory sentence follows the term, write plain prose.
- When a sentence denies something and then restates it, write only the side you mean if that side stands on its own.
- When consecutive sentences repeat the same pattern (the same opening, the same ending, or the same structure) and read monotonously, change how the sentences connect.
- Do not state the number of listed items or steps. Every time you add or remove an item, you would have to update the number, and a forgotten update makes the text contradict itself. State a number only when the number itself is the rule, such as a limit or a count of times.
- Check each parenthetical remark and each quoted example, one at a time. Ask whether its content is essential to the reader. If it is not essential, remove it.
  - If it is essential, work it into the main text.
  - Keep parentheses only when working the content into the sentence would make the sentence hard to follow.
  - Keep quotation marks when they mark text whose exact characters matter, such as headings, screen labels, and command output that readers or tools search for.
  - When you show a bracket or symbol itself in the text, show it in inline code format so that it is distinct from brackets in the prose.

## Checks for the language you wrote in

Apply the `polishing.md` in the language pack for the language of the text. If the pack has a `styles.md`, choose notation by it. The language packs are in `lang/<code>/` of the `writing-rules` skill's folder. A language with no pack gets only the checks for every language.

## Read it through at the end

Read the text through yourself from the start. If you went back to an earlier place while reading, fix the sentence that made you go back.

<!-- asking.md -->

# How to write a decision question

Write each point the user must decide in a reply as a decision question, one question per answer the user returns, in the form below.
Number the heading even when there is only one question, so that the user can answer with only the question number and the option letter.
Number questions continuously across what you know of the session, and do not reuse the number of a question that has been answered.

Before writing a question, check that you can name the requested work that the answer lets you move forward. If you cannot, do not ask; report the matter as facts and their effects.

```markdown
### 1. <Question sentence stating what the user must decide>

<Paragraph stating what the work is aiming at, what the work ran into that requires a decision, and why the user and not the agent decides>

| Option | Background and what happens if chosen |
|---|---|
| A | … |
| B | … |
```

- Make the question a sentence that shows what is being decided without the rest of the reply. Include the proper name of the subject if there is one.
- State the purpose of the work, as far as it can be read from the user's request. Stating the purpose lets the writer and the user keep the same purpose in mind while the decision is pending. It also lets the writer check that the question is a step toward the purpose and that the options line up against the purpose.
- State why the user decides. Say, in words the user understands, which of the situations in rule `writing-to-user.md` where the user must decide applies.
- Give each option one row, and order the rows from most to least recommended. The number of options depends on the question.
- Put the letter used to answer in the option column. For a list of options, use A, B, C… from the top. For a yes-or-no choice, use the pair Y and N. If letters alone make the options hard to tell apart, add a short word to the letter.
- In the "Background and what happens if chosen" column, state the content of the option instead of only its label. Then state what happens toward the purpose of the work if the option is chosen. When the content of the option alone does not show why it is a choice at all, state the background that led to the option too.
- If one option is especially recommended, write "(recommended)" after the letter of the top option. End the "Background and what happens if chosen" column of that row with the reason for recommending it.
- For a question that cannot list options, omit the table and state in the question what you want answered.
- The column names in the template and "(recommended)" are the English labels. Use them as written in an English reply. In a reply in another language, use the names that the language pack's `conventions.md` defines for that language. If the pack has no `conventions.md`, write the labels in the reply's language. Language packs are in `skills/writing-rules/lang/<code>/` (the `lang/` folder of the `writing-rules` skill).
- When there are several questions, put first the question whose answer changes the later work the most.
- Even for a question with a recommendation, the user decides which option to choose. You list what happens for each option.

<!-- lang/en: read only when writing in this language -->

<!-- lang/en/polishing.md -->

# Checks to add when writing in English

Apply these checks in addition to the "Checks for every language" section of `polishing.md`.

## Prefer plain words

Use the common word when it carries the same meaning as the formal one. Readers who use English as a second language, and readers outside the field, misread rare words and idioms. Keep a technical term when it is the name readers will search for, and give its meaning the first time it appears.

## Pass documents for people through a reviewer skill, if one is available

Documents written in English that people will read or that will be published (READMEs, manuals, specifications, proposals) can be passed through an English reviewer skill after you polish them yourself. If the skill avoid-ai-writing is among the available skills, use it. Check that the reviewed text keeps every claim, condition, number, and level of certainty of your text. Where the reviewer changed the meaning, restore your original wording.

Do not pass replies to the user, work reports, commit messages, pull request descriptions, or code comments through a reviewer skill.

<!-- lang/ja: read only when writing in this language -->

<!-- lang/ja/conventions.md -->

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

- 一般の語：日本語では使わない言い回しと、代わりに使う語は、wakariyasu のスキル `check-terms` の一覧（`references/terms.tsv`）にある。一覧に無い語も同じ考え方で選ぶ。
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

日本語の報告からページを作るときは、`lang` を `ja` にし、`labels` に次の語を渡す。見出し・列名・状態の語は、上の「session-status の報告」と「判断の問いかけ」の節の名前と同じにする。`{answered}`・`{total}`・`{title}` は、ページが値を入れる箇所なので、そのまま残す。

```json
{
  "pageKind": "セッションの状況",
  "asOf": "時点",
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

<!-- lang/ja/polishing.md -->

# 日本語で記述したときに足す確認

日本語で記述した返答と文書は、規則 `polishing.md` の「Checks for every language」の節の確認に加えて、次の節の確認をしてから渡す。

## 表記を文章ごとに選ぶ

表記は、この言語パックの `styles.md` の順番で選び、選んだ書き方にそろえる。語の選び方も、和語と漢語のどちらにも寄せない標準表記と、漢語を中心に記述する漢語表記のどちらかを、`styles.md` に沿って選ぶ。

## 示す対象と動く人の欠落を確認する

日本語の文は主語や目的語を省いても文になるので、示す対象（目的語が表すもの）や動く人（主語）が欠けていても、書き手は気付きにくい。
主語や目的語を省いた文のうち、前後の文から補えるか迷う文は、主語と目的語を省けない英語に一語ずつ訳すつもりで読み、訳すのに補う語が要るかを確認する。
補う語が要るなら、補った語が示す対象を、日本語の文として自然な言い方で記述する。
英語に訳すのは欠落を見つけるための手段で、訳した英文の語の選び方や語順を日本語の文に写すと、翻訳調の言い方になる。

## 読点を確かめる

間を取るだけの読点は外す。条件や場面の区切り、並べた語の区切り、
外すと掛かり先が変わる所の読点は残す。

## 日本語では使わない言い回しを探す

翻訳調の語や作業の中で生まれた造語が混ざると、読み手は意味を取り違え、文書を信頼しにくくなる。
英語の語句や名前を日本語にするときは、語ごとに置き換えず、文脈に合わせて日本語の書き手が使う言い方を選ぶ。

言い回しの一覧は、wakariyasu のスキル `check-terms` のフォルダの `references/` にある。使わない言い回しの一覧（`terms.tsv`）の語は作成する時点から避け、文脈で確かめる言い回しの一覧（`terms-caution.tsv`）の語は作成する時点から候補の語と比べる。
2つの一覧の本文が会話に無ければ、セッションで初めて日本語を記述する前に読む。

一覧に無い語も、同じ観点で確認する。和語は意味の幅が広く、作業の中で使い続けると、書き手にだけ通じる意味を帯びる。
文書の中で、和語の動詞や名詞を日常の具体的な意味から離れて使っているときは、示す対象を正確に表す漢語に言い換えられないかを確認する。
標準表記の文書では、日常の具体的な意味で使う和語と、漢語にすると硬くなって読み手に通じにくくなる語は残す。漢語表記の文書では、それらの語も、意味と読みやすさを失わずに漢語にできるかを確認する。

ファイルに保存した文書は、スキル `check-terms` に沿って、言い回しの一覧の語を探して替える。

## 人に渡す文書は、yomiyasu があれば yomiyasu に通す

README・手順書・仕様書・提案書のように、人が読むために渡す・公開する日本語の文書は、自分で整え、`check-terms` で確かめたあとで、使えるスキルの中に yomiyasu があれば yomiyasu スキルに通す。
yomiyasu には文書と、`styles.md` の表の「種類」の列にある文章の種類の名前を渡す。読み手の詳しさが分かっていれば、expert（同じ分野の人）・informed（分野は違うが、技術や業務に詳しい人）・general（専門の知識が無い人）のどれかも渡す。
漢語表記の文書は、yomiyasu を通したあとで、選んだ漢語が和語に言い換えられていないかを確かめ、言い換えられていれば漢語に戻す。
ユーザーへの返答・作業の報告・コミットメッセージ・PR・コードのコメントには通さない。返答に文書の全文を載せるときは、全文の部分だけを文書として扱う。

<!-- lang/ja/skills.md -->

# 日本語で記述したときに、スキルごとに足すこと

wakariyasu のスキルを日本語の文書や返答に使うときは、スキルの本文に加えて、そのスキルの名前の節に従う。

## review-for-readers

日本語の文書なら、読み手に、迷った文を英語に直訳させる。主語・目的語・冠詞を補わないと英文にならないなら、元の日本語の文は示す対象が足りない。

日本語の文書で、読み手が理解を妨げる箇所を挙げなくなったら、使えるスキルの中に yomiyasu があれば yomiyasu スキルを呼び出し、文書と文章の種類を渡して整える。種類の名前は、この言語パックの `styles.md` の表の「種類」の列にある。

## clarify-skill

観点 16「Wording」では、日本語では使わない言い回しを避ける。wakariyasu のスキル `check-terms` に沿って確かめる。環境の文書で定義された語の扱いは、clarify-skill の SKILL.md の「Handling terms」の節のとおりにする。

## extract-insights

- 日本語の発言は主語と目的語を省くので、知見の1文では、誰が何を何に対してするかを補う。補えないときは推定として扱うか、知見から落とす。
- 日本語の文字起こしには同じ読みの別の語への誤変換が混ざる。固有名詞・数・専門の語は元の文章のほかの箇所や、呼び出し元が渡した資料と照らして戻す。

<!-- lang/ja/styles.md -->

# 日本語の表記の選び方

日本語の表記は、文章の種類と読み手で選ぶ。選ぶ順番は次のとおり。

1. ユーザーの指示（CLAUDE.md や AGENTS.md に記載された指示を含む）。
2. 同じ文書や同じリポジトリで、すでに使われている書き方。
3. 「種類ごとの既定」の節の表にある、文章の種類ごとの既定。

## 種類ごとの既定

| 記述するもの | 種類 | 文末 | 体言止め | 箇条書き |
|---|---|---|---|---|
| ユーザーへの返答・チャット | mail | 敬体 | 使わない | 並んだ項目だけに使う |
| コミットメッセージ・PR の本文 | pr | 常体 | 変更点の行で使ってよい | 変更点と確かめたことに使う |
| README・技術記事 | article | 文書に合わせる | 見出し以外では使わない | 並んだ項目だけに使う |
| 手順書・使い方の説明 | manual | 文書に合わせる | 見出し以外では使わない | 番号つきの手順に使う |
| 規則・仕様書・SKILL.md | formal | 常体 | 見出し以外では使わない | 並んだ条件に使う |
| 提案書 | proposal | 敬体 | 見出し以外では使わない | 並んだ項目だけに使う |
| 議事録 | minutes | 常体 | 項目で使ってよい | 項目の並びに使う |
| 障害報告 | incident | 常体 | 時系列の行で使ってよい | 時系列に使う |
| スライド | slides | 句で止めてよい | 使ってよい | 使ってよい |

当てはまる種類が無ければ、種類は定めず、上の 1 と 2 だけで選ぶ。

## 標準表記と漢語表記

語の選び方は、標準表記と漢語表記のどちらかを文書ごとに選ぶ。

- 標準表記：和語と漢語のどちらかに寄せず、文脈と読み手に合う語を選ぶ。
- 漢語表記：意味と読みやすさを失わない範囲で、漢語を中心に表記する。概念・プロセス・解析結果を説明したり可視化したりするビジネス文書では、和語で書き下すより、漢語で記述したほうが、読み手は意味を明確に捉えられる。漢語を中心にしても、語どうしの関係は助詞と動詞で示し、漢語の名詞だけを詰めて並べない。

ユーザーの指示と、すでに使われている書き方で決まらなければ、文書の目的と読み手から、どちらの表記で記述すれば読み手に意味が伝わるかで選ぶ。

## 読み手

読み手の詳しさが分かっていれば、用語の扱いを次のように選ぶ。

- 同じ分野の人には、用語を言い換えずに使う。
- 分野の違う人や、専門の知識が無い人には、用語を言い換えるか、初めて出すところで意味を添える。
- 読み手の分野が分からなければ、読み手に合わせた言い換えはしない。用語は言い換えずに使い、意味の要りそうな語に説明を添える。

## 種類で変えないもの

数字・英字の全角と半角、外来語の長音（サーバとサーバー）、送り仮名は、種類では定めない。
同じ文書の中でそろえ、そろえ方は、冒頭に挙げた選ぶ順番の 1（ユーザーの指示）と 2（すでに使われている書き方）で選ぶ。

# 日本語では使わない言い回し

日本語の文章では、次の言い回しを使わずに、代わりの語で書く。翻訳調の語や作業の中で生まれた造語が混ざると、
読み手は意味を取り違え、文書を信頼しにくくなる。括弧の中は、使わない意味を示す。

| 言い回し | 代わりに使う語 |
|---|---|
| 束（まとめて渡すデータやファイル） | 中身を表す語（JSON ファイル、修正の一式など） |
| 打つ（コマンドを実行する、文字を入力する） | 実行する、入力する |
| 旗（コマンドのオプション） | オプション、フラグ |
| 問い（問いかけ・質問の意味の名詞） | 問いかけ、質問 |
| 勧め（お勧めの意味の名詞。「お」を付けない形） | お勧め、推奨 |
| 導入（ソフトウェアをインストールする） | インストール、セットアップ |
| 要る〜（必要な〜の意味で、名詞に続く形） | 必要な〜 |
| 端末（コマンドを実行するターミナル、TTY） | ターミナル |
| 版（ソフトウェアのバージョン） | バージョン |
| 枝（git のブランチ） | ブランチ |
| 窓（画面のウィンドウ） | ウィンドウ |
| 見張る（処理やファイルを監視する） | 監視する |
| 写し（ファイルのコピー） | コピー |
| 落とす（ダウンロードする） | ダウンロードする |
| 走らせる（実行する） | 実行する |
| 生きている（プロセスや接続が動いている） | 動いている、有効な |
| 殺す（プロセスを終了させる） | 終了する、強制終了する |
| 投げる（依頼や要求を送る） | 送る |
| 箱（図や画面の枠） | 枠、ボックス |
| 段（作業や処理のステップ） | ステップ |
| 台（検査や計測をする環境・仕組み。「計る台」など） | 検査の環境、計測の仕組み、ベンチマーク |
| 直し（改修・修正・更新の意味の名詞） | 改修、修正、更新 |
| 確かめ（検証・確認の意味の名詞） | 検証、検証の手順、テスト、確認 |
| 出す（ソフトウェアやバージョンを公開する） | 公開する、リリースする |
| 限り（できないこと・限界の意味の名詞。「検査の限り」など） | 限界、できないこと、検査が見つけられる範囲 |
| 回す（検査やテストを実行する） | 実施する、適用する、実行する |
| 調べ（調査・探索・集計の意味の名詞） | 調査、探索、集計 |
| 入れ方（ソフトウェアのインストール方法） | インストール方法 |
| 入るもの（インストールされるもの） | インストールされるもの |
| 使うエージェント（利用者が使っているエージェント） | お使いのエージェント、インストール先のエージェント |
| 包み（ほかのコマンドや関数を呼び出すだけの薄い層。wrapper の訳語） | ラッパー、〜を呼び出すスクリプト |
| 札（見出しや項目に添える短い語の表示） | タグ、ラベル |

# 文脈によっては別の語のほうが自然な言い回し

次の言い回しは誤りではないが、技術文書では日本語の書き手が別の語を選ぶ場面がある。文脈を見て、候補の語のほうが
自然なら替える。括弧の中は、候補の語に替える意味を示す。

| 言い回し | 候補の語 |
|---|---|
| 当てる（規則や検査を文書に適用する、相手に問い合わせる、照らし合わせる） | 適用する、問い合わせる、突き合わせる、実施する |
| 決まり（規則・約束事、決めた事柄） | ルール、決定事項 |
| 落ちる（情報や設定が失われる） | 失われる、抜ける |
| 引く（文や文書を引用する） | 引用する |
| 順（並べる順番） | 順番、順序 |
| 指す（「語の指す先」のように、語や記述が別のものを参照する） | 参照する、示す |
| 置き場所（ファイルやデータを置く所） | 配置する場所、保存する場所、保存先 |
| 一般の文（「一般の文に直す」のように、特定の事例を離れて言う文） | 汎化した表現の文、一般化した文 |
| 目（「読み手の目で読む」のように、見る立場を表す語） | 視点、観点 |
| 次の表（「次の表に示す」のように、位置で表を示す書き方） | 表の中身を名指す（「料金の表」など） |
| 拾う（「夜間の処理がログを拾う」のように、機械の処理を人の動作で言う） | 読み込む、集める、検出する |
| 通る（「リクエストが通る」「検査が通る」のように、処理が受け付けられたり成功したりする） | 受け付けられる、成功する、合格する |
| 効く（「設定が効く」のように、仕組みが働く） | 有効になる、反映される、働く |
| 響く（「性能に響く」のように、影響する） | 影響する |
| 入口（「サーバーの入口」のように、処理を受け付ける所を場所にたとえる） | エンドポイント、最初に呼ばれる処理 |
| 受け口（「通知の受け口」のように、処理を受け付ける所を場所にたとえる） | 受け付ける処理、エンドポイント |
| 渡し先（「渡し先」「投げ先」のように、処理を渡す相手を場所にたとえる） | 渡す相手の処理やサービスの名前 |
| 流す（「検査を流す」のように、手順やスクリプトを実行する） | 実行する、適用する、実施する |
| 道具（「ページを作る道具」のように、スクリプト・ツール・スキルをまとめて言う） | 対象の名前（スクリプト、ツール、コマンド、スキルなど） |
| 決めたこと（決定した事柄） | 決定事項、確定事項、判断した項目 |
| 例外は〜です（何の、どの決まりの例外かを書かずに「例外は」で文を始める） | どの決まりに何が当たらないかを書く |
| 直す（文書・コード・設定の誤りや足りない所を改める） | 修正する、訂正する、改修する |
| 書く（文書やファイルに内容を記す） | 記述する、表記する、記載する |
| 決める（方針・値・扱いを定める） | 判断する、決定する、定める |
| 選ぶ（候補の中から取る。多くの場面では選ぶのままが自然なので、参考にとどめる） | 選択する |
| 切る（「データを切る」「作業を切る」のように、名詞を目的語にして、分けることや区切ることを言う） | 分割する、切り分ける、区切る |
| 渡すとき（文書や結果を相手に出す場面を、渡すと言う） | 提出するとき、提示するとき、共有するとき、引き渡すとき |
| 節（文書の区切りを指す語。日常の意味で使うときは除く） | 章、項、段落、見出しの名前で示す |
| 材料（文書や判断のもとになる情報を指す語。日常の意味で使うときは除く） | 資料、根拠、情報源、データ |
| 届く（情報・規則・成果物が相手に伝わる、使われることを言う。日常の意味で使うときは除く） | 伝わる、反映される、配布される、利用者が使える |
| 広がり（範囲や対象が増えることを指す語。日常の意味で使うときは除く） | 拡大、対象の範囲、適用範囲 |
| 抜け（「主語の抜け」「確認の抜け」のように、あるべきものが欠けていることを言う名詞） | 欠落、漏れ、不足 |
| 確かめる（「動作を確かめる」のように、検証・確認する動作を言う動詞） | 確認する、検証する、点検する |
| 当たる（「条件に当たる」「どの節に当たるか」のように、該当することを言う） | 該当する、相当する、対応する |

<!-- /wakariyasu:AGENTS.snippet.md -->
