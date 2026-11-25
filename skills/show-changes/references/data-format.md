# The data format of show-changes diffs

The JSON format that `--json-out` writes and `--data` reads. `--data` checks the format when it reads and stops if it does not match.

```
{
  "schema_version": 1,
  "title": "…", "data_version": "…", "generated_at": "ISO 8601 date and time",
  "group_depth": 2, "full_text": false,
  "lang": "language code of the page (optional; en if absent)", "labels": {"name": "word that replaces an English word of the page (optional)"},
  "sources": [{
    "name": "the target's name (a choice in the filter)",
    "kind": "one of git, plain, patch (git if absent)",
    "base_ref": "the BASE passed (for plain and patch: before)", "target_ref": "the TARGET passed (for plain and patch: after)",
    "base": "the commit of the starting point compared (empty if not git)", "target": "the commit of TARGET (empty if not git)",
    "merge_base": false,
    "commits": [["hash", "author date and time (ISO 8601)", "subject"]],
    "files": [{
      "path": "the path on the after side", "old": "the original path of a move or copy (null if none)",
      "status": "A, M, D, R100, C, T, etc.", "added": 1, "deleted": 0, "binary": false,
      "old_mode": "100644", "new_mode": "100755",
      "body": "the unified diff from the first @@", "notice": "an explanation for the viewer (binary, no content diff, bytes that are not valid UTF-8, etc.; empty if none)",
      "full_body": "the unified diff of the full text (only when full_text is true; null for binary files, submodules and patch targets)"
    }]
  }]
}
```

- Only targets whose `kind` is git have values in `commits`, `base`, `target` and `merge_base`. Targets of other kinds have `commits` as an empty array and have no `merge_base`.
- When `merge_base` is true, `base` is the divergence-point commit.
- `added` and `deleted` are null for binary files.
- `old_mode` and `new_mode` are git modes (regular file 100644, executable file 100755, symbolic link 120000, submodule 160000). They are null, or the key is omitted, on the before side of an addition, on the after side of a deletion, and for diff files that do not give modes. The `body` of a symbolic link is the diff of the link target path.
- `lang` and `labels` are optional. `labels` can only use the names in the `/*__LABELS__*/` block of the template; the page uses the English word for each name that is not given. The notices in `files[].notice` are written in English by `build.py`, and the page replaces the known ones with the labels `noticeBinary`, `noticeNoDiff`, `noticeSubmodule`, `noticeUnreadable` and `noticeNoFull`.
- `generated_at` is renewed each time a page is built (also when it is rebuilt with `--data`).
