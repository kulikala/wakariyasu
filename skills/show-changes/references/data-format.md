# show-changes の差分のデータの形

`--json-out` が書き出し、`--data` が読む JSON の形。`--data` は読み込むときに形を確かめ、合わなければ止まる。

```
{
  "schema_version": 1,
  "title": "…", "data_version": "…", "generated_at": "ISO 8601 の日時",
  "group_depth": 2, "full_text": false,
  "sources": [{
    "name": "対象の名前（絞り込みの選択肢）",
    "kind": "git・plain・patch のどれか（無ければ git）",
    "base_ref": "渡した BASE（plain・patch は「変更前」）", "target_ref": "渡した TARGET（plain・patch は「変更後」）",
    "base": "比べた起点のコミット（git 以外は空）", "target": "TARGET のコミット（git 以外は空）",
    "merge_base": false,
    "commits": [["ハッシュ", "作者の日時（ISO 8601）", "件名"]],
    "files": [{
      "path": "変更後の側のパス", "old": "移動・複製の元のパス（無ければ null）",
      "status": "A・M・D・R100・C・T など", "added": 1, "deleted": 0, "binary": false,
      "old_mode": "100644", "new_mode": "100755",
      "body": "最初の @@ からの unified diff", "notice": "見る人への説明（バイナリ、内容の差分が無い、UTF-8 として読めないバイトがある、など。無ければ空）",
      "full_body": "全文の unified diff（full_text のときだけ。バイナリ・サブモジュール・patch の対象は null）"
    }]
  }]
}
```

- `kind` が git の対象だけが、`commits`・`base`・`target`・`merge_base` に値を持つ。git 以外の対象は `commits` が空の配列で、`merge_base` を持たない
- `merge_base` が true のとき、`base` は分岐点のコミット
- `added`・`deleted` は、バイナリのとき null
- `old_mode`・`new_mode` は git のモード（通常のファイル 100644・実行できるファイル 100755・シンボリックリンク 120000・サブモジュール 160000）。追加の前と削除の後の側、モードの分からない差分ファイルでは null か、キーを省く。シンボリックリンクの `body` は、リンク先のパスの差分
- `generated_at` は、ページを作るたびに新しくなる（`--data` で作り直したときも）
