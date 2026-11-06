#!/usr/bin/env python3
"""名前付きの比較対象から差分を集め、ブラウザで開く 1 つの HTML のページに埋め込みます。"""
import argparse
import ast
import datetime
import difflib
import html
import json
import os
import re
import shutil
from pathlib import Path
import subprocess
import sys

SCHEMA_VERSION = 1
UNREADABLE = 'UTF-8 として読めないバイトは \\xNN の形で表示しています。'

_ARGPARSE_MESSAGES = {
    'usage: ': '使い方: ',
    'options': 'オプション',
    'positional arguments': '位置引数',
    '%(prog)s: error: %(message)s\n': '%(prog)s: エラー: %(message)s\n',
    'unrecognized arguments: %s': '認識できない引数です: %s',
    'argument %s: %s': '引数 %s: %s',
    'argument %(argument_name)s: %(message)s': '引数 %(argument_name)s: %(message)s',
    'expected one argument': '値を 1 つ指定してください',
    'expected %s arguments': '値を %s 個指定してください',
    'invalid %(type)s value: %(value)r': '%(type)s として不正な値です: %(value)r',
    'int': '整数',
    'ignored explicit argument %r': '値 %r は指定できません',
    'the following arguments are required: %s': '必須の引数です: %s',
    'ambiguous option: %(option)s could match %(matches)s': 'オプション %(option)s は複数の候補に一致します: %(matches)s',
}
argparse._ = lambda message: _ARGPARSE_MESSAGES.get(message, message)
argparse.ngettext = lambda singular, plural, count: ('値を %s 個指定してください'
    if singular == 'expected %s argument' else singular if count == 1 else plural)


def git(path, *args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_NO_REPLACE_OBJECTS='1')
    return subprocess.run(
        ['git', '--no-pager', '--literal-pathspecs', '-c', 'core.quotepath=false', '-c',
         'diff.external=', '-c', 'log.showSignature=false', '-c', 'diff.suppressBlankEmpty=false', *args], cwd=path, env=env, check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def decode(value):
    # 読めないバイトを \xNN で残し、違うバイトが同じ字に見えないようにする。
    return value.decode('utf-8', errors='backslashreplace')


def unreadable(*values):
    try:
        for value in values:
            value.decode('utf-8')
    except UnicodeDecodeError:
        return UNREADABLE
    return ''


def notices(*texts):
    return ' '.join(dict.fromkeys(text for text in texts if text))


def revision(path, ref):
    return decode(git(path, 'rev-parse', '--verify', '--end-of-options',
                      ref + '^{commit}')).strip()


def body_of(patch):
    lines = patch.split('\n')
    start = next((i for i, line in enumerate(lines) if line.startswith('@@ ')), len(lines))
    return '\n'.join(lines[start:]).rstrip('\n')


def split_lines(text):
    parts = text.split('\n')
    return [part + '\n' for part in parts[:-1]] + ([parts[-1]] if parts[-1] else [])


def hunk_rows(lines, sign):
    rows = []
    for line in lines:
        rows.append(sign + line.rstrip('\n'))
        if not line.endswith('\n'):
            rows.append('\\ No newline at end of file')
    return rows


def whole_file(before, after):
    """片方が空か両方が同じときの、ファイル全体を 1 つのハンクにした差分。"""
    a, b = split_lines(before), split_lines(after)
    if before == after:
        return '\n'.join([f'@@ -1,{len(a)} +1,{len(a)} @@', *hunk_rows(a, ' ')]) if a else ''
    if not a:
        return '\n'.join([f'@@ -0,0 +1,{len(b)} @@', *hunk_rows(b, '+')])
    return '\n'.join([f'@@ -1,{len(a)} +0,0 @@', *hunk_rows(a, '-')])


def difflib_body(before, after, context):
    a, b = split_lines(before), split_lines(after)
    rows = []
    for line in list(difflib.unified_diff(a, b, n=max(len(a), len(b)) if context is None else context))[2:]:
        rows.append(line.rstrip('\n'))
        if not line.endswith('\n'):
            rows.append('\\ No newline at end of file')
    return '\n'.join(rows)


def text_body(before, after, context, git_diff=None):
    """最初の @@ からの差分。context が None なら全文を入れる。

    git_diff は前後の行数を受けて git の差分を返す関数。無ければ difflib で作る（大きいファイルでは遅い）。
    """
    a, b = decode(before), decode(after)
    if before == after or not before or not after:
        return '' if before == after and context is not None else whole_file(a, b)
    if git_diff:
        return body_of(decode(git_diff(max(a.count('\n'), b.count('\n')) + 1 if context is None else context)))
    return difflib_body(a, b, context)


def no_index_diff(left, right):
    """2 つのファイルを git diff --no-index で比べる関数を返す。git が無ければ None。"""
    if not shutil.which('git'):
        return None
    def run(context):
        result = subprocess.run(
            ['git', '--no-pager', '-c', 'core.quotepath=false', '-c', 'diff.external=', '-c', 'diff.suppressBlankEmpty=false',
             'diff', '--no-index',
             '--no-color', '--no-ext-diff', '--no-textconv', f'-U{context}', '--', str(left), str(right)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode not in (0, 1):
            raise subprocess.CalledProcessError(result.returncode, result.args, result.stdout, result.stderr)
        return result.stdout
    return run


def numstats(raw):
    """Parse NUL-delimited records, including rename paths containing tabs/newlines."""
    tokens = raw.split(b'\0')
    result = {}
    index = 0
    while index < len(tokens) and tokens[index]:
        added, deleted, path = tokens[index].split(b'\t', 2)
        index += 1
        if not path:
            index += 1  # old path
            path = tokens[index]
            index += 1
        key = decode(path)
        previous = result.get(key, (b'0', b'0'))
        result[key] = ((b'-', b'-') if b'-' in (*previous, added, deleted) else
                       tuple(str(int(a) + int(b)).encode('ascii') for a, b in zip(previous, (added, deleted))))
    return result


def patch_body(patches, status):
    """git の差分からファイル 1 つ分の本文と、UTF-8 として読めないバイトがあったときの説明を返す。"""
    first = next(patches, None)
    if first is None:
        raise ValueError('Git の差分数とファイル状態の件数が一致しません')
    raws = [first]
    if status[0] == 'T' and re.search(rb'(?m)^deleted file mode ', first):
        second = next(patches, None)
        if second is None or not re.search(rb'(?m)^new file mode ', second):
            raise ValueError('ファイル種類の変更に対応する追加差分がありません')
        raws.append(second)
    bodies = [body_of(decode(raw)) for raw in raws]
    return '\n'.join(body for body in bodies if body), unreadable(*raws)


def collect(name, location, base_ref, target_ref, merge_base, include_full):
    path = Path(location).expanduser().resolve()
    root = Path(decode(git(path, 'rev-parse', '--show-toplevel')).strip()).resolve()
    base, target = revision(root, base_ref), revision(root, target_ref)
    if merge_base:
        base = decode(git(root, 'merge-base', base, target)).strip()
    common = ['diff', '--no-color', '--no-ext-diff', '--no-textconv', '--submodule=short', '--ignore-submodules=none',
              '--find-renames', base, target]
    # --raw は、名前を git に戻さずに中身を読めるよう、blob の ID とモードを持つ。
    tokens = git(root, *common, '--raw', '--no-abbrev', '-z').split(b'\0')
    stats_by_path = numstats(git(root, *common, '--numstat', '-z'))
    patches = iter(re.split(rb'(?m)^diff --git ', git(root, *common, '--unified=3'))[1:])
    files = []
    index = 0
    while index < len(tokens) and tokens[index]:
        old_mode, new_mode, old_id, new_id, status = decode(tokens[index]).lstrip(':').split(' ')
        index += 1
        old = decode(tokens[index]); index += 1
        filename = old
        if status[0] in 'RC':
            filename = decode(tokens[index]); index += 1
        body, unreadable_notice = patch_body(patches, status)
        stats = stats_by_path.get(filename)
        if stats is None:
            raise ValueError(f'Git の差分に行数がないファイルがあります: {filename}')
        submodule = '160000' in (old_mode, new_mode)
        blobs = lambda: (b'' if status[0] == 'A' else git(root, 'cat-file', 'blob', old_id),
                         b'' if status[0] == 'D' else git(root, 'cat-file', 'blob', new_id))
        # blob どうしの差分には .gitattributes が当たらない。--text は、中身に NUL が無いと確かめてから使う。
        blob_diff = lambda context: git(root, 'diff', '--no-color', '--no-ext-diff', '--no-textconv', '--text',
                                        f'-U{context}', old_id, new_id)
        binary = stats[0] == b'-'
        added, deleted = (None, None) if binary else (int(stats[0]), int(stats[1]))
        if binary and not submodule:
            # .gitattributes で -diff・binary を付けた文字のファイルも、git は行数を - にする。中身で確かめる。
            before, after = blobs()
            if b'\0' not in before and b'\0' not in after:
                binary = False
                body = text_body(before, after, 3, blob_diff)
                rows = body.split('\n')
                added, deleted = sum(row.startswith('+') for row in rows), sum(row.startswith('-') for row in rows)
                unreadable_notice = unreadable(before, after)
        entry = dict(path=filename, old=old if old != filename else None,
                     status=status, added=added, deleted=deleted, binary=binary,
                     body=body, notice=unreadable_notice, **file_modes(old_mode, new_mode))
        if not body:
            entry['notice'] = notices(unreadable_notice, 'バイナリファイルです。' if binary else
                                      '内容の差分はありません。')
        if include_full:
            if binary:
                entry['full_body'] = None
            elif submodule:
                entry['full_body'] = None
                entry['notice'] = notices(unreadable_notice, 'サブモジュールは参照コミットの差分を表示します。')
            else:
                before, after = blobs()
                entry['full_body'] = text_body(before, after, None, blob_diff)
                entry['notice'] = notices(entry['notice'], unreadable(before, after))
        files.append(entry)
    if next(patches, None) is not None:
        raise ValueError('Git の差分数とファイル状態の件数が一致しません')
    commits = []
    log = git(root, 'log', '--reverse', '--format=%H%x00%aI%x00%s%x00', f'{base}..{target}')
    fields = log.split(b'\0')
    for i in range(0, len(fields) - 2, 3):
        commits.append([decode(fields[i]).strip(), decode(fields[i + 1]), decode(fields[i + 2])])
    return dict(name=name, kind='git',
                base_ref=base_ref, target_ref=target_ref, base=base, target=target,
                merge_base=merge_base, commits=commits,
                files=sorted(files, key=lambda f: f['path']))


def file_modes(old_mode, new_mode):
    # git のモード（100644 など）。無い側（追加の前・削除の後）は None。
    absent = lambda mode: None if not mode or set(mode) == {'0'} else mode
    return dict(old_mode=absent(old_mode), new_mode=absent(new_mode))


def text_entry(path, before, after, include_full, old, status, git_diff=None, modes=(None, None)):
    binary = b'\0' in before or b'\0' in after
    entry = dict(path=path, old=old, status=status, binary=binary, added=None, deleted=None, body='',
                 notice='バイナリファイルです。' if binary else unreadable(before, after), **file_modes(*modes))
    if not binary:
        entry['body'] = text_body(before, after, 3, git_diff)
        if not entry['body']:
            entry['notice'] = notices(entry['notice'], '内容の差分はありません。')
        rows = entry['body'].split('\n')
        entry['added'] = sum(row.startswith('+') for row in rows)
        entry['deleted'] = sum(row.startswith('-') for row in rows)
    if include_full:
        entry['full_body'] = None if binary else text_body(before, after, None, git_diff)
    return entry


def plain_paths(location):
    root = Path(location).expanduser().absolute()
    if root.is_symlink():
        raise ValueError('比較元・比較先にシンボリックリンクは指定できません')
    if root.is_file():
        return {'': root}
    if not root.is_dir():
        raise ValueError(f'ファイルまたはディレクトリがありません: {location}')
    paths = {}
    for p in root.rglob('*'):
        if '.git' in p.relative_to(root).parts:
            continue
        # シンボリックリンクは辿らず、git と同じくリンク先のパスを中身として比べる。
        if p.is_symlink() or p.is_file():
            paths[p.relative_to(root).as_posix()] = p
    return paths


def plain_mode(path):
    # git と同じく、リンク・実行できるファイル・通常のファイルの 3 つに分ける。
    if path.is_symlink():
        return '120000'
    return '100755' if path.stat().st_mode & 0o100 else '100644'


def read_plain(path):
    return os.fsencode(os.readlink(path)) if path.is_symlink() else path.read_bytes()


def collect_plain(name, before, after, include_full):
    left, right = plain_paths(before), plain_paths(after)
    if ('' in left) != ('' in right):
        raise ValueError('比較元と比較先は両方ともファイル、または両方ともディレクトリにしてください')
    files = []
    for path in sorted(left.keys() | right.keys()):
        a = read_plain(left[path]) if path in left else b''
        b = read_plain(right[path]) if path in right else b''
        modes = (plain_mode(left[path]) if path in left else None, plain_mode(right[path]) if path in right else None)
        swapped = path in left and path in right and left[path].is_symlink() != right[path].is_symlink()
        if path in left and path in right and a == b and modes[0] == modes[1]:
            continue
        filename = path or Path(after).name
        old = Path(before).name if not path and Path(before).name != filename else None
        status = 'A' if path not in left else 'D' if path not in right else 'T' if swapped else 'M'
        regular = path in left and path in right and not left[path].is_symlink() and not right[path].is_symlink()
        files.append(text_entry(filename, a, b, include_full, old, status,
                                no_index_diff(left[path], right[path]) if regular else None, modes))
    return dict(name=name, kind='plain', base_ref='変更前', target_ref='変更後',
                base='', target='', commits=[], files=files)


def collect_patch(name, location, include_full):
    # Hunk lengths disambiguate --- / +++ content from subsequent file headers.
    raw = Path(location).read_bytes().removeprefix(b'\xef\xbb\xbf')
    if raw.count(b'\n') and raw.count(b'\r\n') == raw.count(b'\n'):
        # 差分ファイル全体が CRLF に変換されているときだけ CR を外す。行の中身の CR は差分の一部なので残す。
        raw = raw.replace(b'\r\n', b'\n')
    raw_lines = raw.split(b'\n')
    lines = [decode(line) for line in raw_lines]
    files = []; i = 0; pending = {}; oldleft = newleft = 0
    # git の差分の a/・b/ のような接頭辞を外すか。None は diff --git の行が無い差分（diff -u など）。
    strip = None
    def unquote(value):
        if value.startswith('"'):
            try:
                return decode(ast.literal_eval('b' + value.encode('utf-8').decode('ascii', errors='backslashreplace')))
            except (ValueError, SyntaxError):
                raise ValueError('差分のパスの引用が不正です')
        return value
    def cut(value):
        return value[2:] if value != '/dev/null' and re.match(r'[a-z]/', value) else value
    def names(old, new):
        old, new = unquote(old.split('\t', 1)[0]), unquote(new.split('\t', 1)[0])
        if strip:
            return cut(old), cut(new)
        if strip is None:
            if old[:2] in ('a/', '/d') and new[:2] in ('b/', '/d'):
                return cut(old), cut(new)
            # diff -ru の差分は、比べた 2 つのフォルダの名前がパスの頭に付く。
            rest = lambda value: value.split('/', 1)[1] if '/' in value else None
            if old == '/dev/null' and rest(new):
                return old, rest(new)
            if new == '/dev/null' and rest(old):
                return rest(old), new
            if rest(old) is not None and rest(old) == rest(new):
                return rest(old), rest(new)
        return old, new
    def flush_pending():
        if not pending.get('path'):
            if pending:
                raise ValueError('Git 差分のファイルヘッダーからパスを読めません')
            return
        binary = pending.get('binary', False)
        old = pending.get('old', pending['path'])
        files.append(dict(path=pending['path'], old=old if old != pending['path'] else None,
            status=pending.get('status', 'M'), binary=binary,
            added=None if binary else 0, deleted=None if binary else 0, body='',
            notice='バイナリファイルです。' if binary else '内容の差分はありません。',
            **file_modes(pending.get('old_mode'), pending.get('new_mode')),
            **({'full_body': None} if include_full else {})))
    while i < len(lines):
        line = lines[i]
        if line.startswith('diff --git '):
            flush_pending()
            header = line[len('diff --git '):]
            half = len(header) // 2
            match = re.match(r'^("(?:\\.|[^"])*"|[a-z]/.*?) ("(?:\\.|[^"])*"|[a-z]/.*)$', header)
            if len(header) % 2 and header[half] == ' ' and header[:half] == header[half + 1:]:
                # --no-prefix の差分。接頭辞のある差分は、2 つのパスの頭の文字が違う。
                strip = False
                pending = dict(old=unquote(header[:half]), path=unquote(header[:half]))
            elif match:
                strip = True
                pending = dict(zip(('old', 'path'), names(match[1], match[2])))
            else:
                # 名前の変更を --no-prefix で書いた差分。パスは rename・---・+++ の行から読む。
                strip = False
                pending = {'header': True}
            i += 1; continue
        if line.startswith('new file mode '): pending['status'] = 'A'; pending['new_mode'] = line.split()[-1]
        if line.startswith('deleted file mode '): pending['status'] = 'D'; pending['old_mode'] = line.split()[-1]
        if line.startswith('old mode '): pending['old_mode'] = line.split()[-1]
        if line.startswith('new mode '):
            pending['new_mode'] = line.split()[-1]
            pending['status'] = 'T' if pending.get('old_mode', '')[:3] != line.split()[-1][:3] else 'M'
        index_mode = re.match(r'^index [0-9a-f]+\.\.[0-9a-f]+ ([0-7]{6})$', line)
        if index_mode and pending.get('header', pending.get('path')):
            pending.setdefault('old_mode', index_mode[1]); pending.setdefault('new_mode', index_mode[1])
        if line.startswith(('Binary files ', 'GIT binary patch')):
            binary_names = re.match(r'^Binary files (.+) and (.+) differ$', line)
            if not pending.get('path') and binary_names:
                # diff -ru の差分は、バイナリのファイルを diff --git の行なしにこの 1 行で書く。
                flush_pending()
                old, new = names(binary_names[1], binary_names[2])
                pending = dict(old=old if old != '/dev/null' else new, path=new if new != '/dev/null' else old,
                               status='A' if old == '/dev/null' else 'D' if new == '/dev/null' else 'M', standalone=True)
            pending['binary'] = True
        for key, prefix in [('old', 'rename from '), ('path', 'rename to '),
                            ('old', 'copy from '), ('path', 'copy to ')]:
            if line.startswith(prefix):
                pending[key] = unquote(line[len(prefix):])
                pending['status'] = 'C' if prefix.startswith('copy') else 'R'
        if line.startswith('--- ') and i + 1 < len(lines) and lines[i+1].startswith('+++ '):
            if pending.get('standalone'):
                flush_pending()
                pending = {}
            # 名前の違いを移動と読むのは git の形の差分だけ。diff -u で名前の違う 2 つのファイルを比べた差分は、--dirs と同じく M にする。
            gitlike = strip or (strip is None and line[4:6] == 'a/' and lines[i+1][4:6] == 'b/')
            old, new = names(line[4:], lines[i+1][4:])
            status = pending.get('status', 'A' if old == '/dev/null' else 'D' if new == '/dev/null' else 'R' if old != new and gitlike else 'M')
            body = []; i += 2; first_row = i
            while i < len(lines):
                row = lines[i]
                hunk = re.match(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', row)
                if hunk:
                    if oldleft or newleft:
                        raise ValueError('差分の行数がハンクの指定と一致しません')
                    oldleft, newleft = int(hunk[2] or 1), int(hunk[4] or 1)
                elif row.startswith('\\'):
                    pass
                elif oldleft or newleft:
                    # 行末の空白を削る編集や道具を通ると、空の文脈の行は先頭の空白を失う。
                    if row == '' and oldleft and newleft: row = ' '
                    if row.startswith(' '): oldleft -= 1; newleft -= 1
                    elif row.startswith('-'): oldleft -= 1
                    elif row.startswith('+'): newleft -= 1
                    else: raise ValueError('差分の行数がハンクの指定と一致しません')
                    if oldleft < 0 or newleft < 0: raise ValueError('差分の行数が不正です')
                else:
                    break
                body.append(row); i += 1
            if oldleft or newleft: raise ValueError('差分のハンクが途中で終わっています')
            files.append(dict(path=old if new == '/dev/null' else new,
                old=old if old != new and old != '/dev/null' else None, status=status,
                binary=False, added=sum(x.startswith('+') for x in body),
                deleted=sum(x.startswith('-') for x in body), body='\n'.join(body),
                notice=notices(unreadable(*raw_lines[first_row - 2:i]),
                               '全文は差分ファイルから復元できないため含まれません。' if include_full else ''),
                **file_modes(pending.get('old_mode'), pending.get('new_mode')),
                **({'full_body': None} if include_full else {})))
            pending = {}
            continue
        i += 1
    flush_pending()
    if not files:
        raise ValueError('unified diff のファイルヘッダーが見つかりません')
    return dict(name=name, kind='patch', base_ref='変更前', target_ref='変更後',
                base='', target='', commits=[], files=files)


def validate(data):
    if not isinstance(data, dict) or data.get('schema_version') != SCHEMA_VERSION:
        raise ValueError(f'JSON の schema_version は {SCHEMA_VERSION} にしてください')
    for key in ('title', 'data_version', 'generated_at'):
        if not isinstance(data.get(key), str):
            raise ValueError(f'{key} は文字列で指定してください')
    if type(data.get('group_depth')) is not int or data['group_depth'] < 0:
        raise ValueError('group_depth は 0 以上の整数で指定してください')
    if type(data.get('full_text')) is not bool or not isinstance(data.get('sources'), list):
        raise ValueError('full_text は真偽値、sources は配列で指定してください')
    names = set()
    for repo in data['sources']:
        if not isinstance(repo, dict):
            raise ValueError('source はオブジェクトで指定してください')
        if repo.get('kind', 'git') not in ('git', 'plain', 'patch'):
            raise ValueError('source.kind は git、plain、patch のいずれかです')
        for key in ('name', 'base_ref', 'target_ref', 'base', 'target'):
            if not isinstance(repo.get(key), str):
                raise ValueError(f'source.{key} は文字列で指定してください')
        if repo['name'] in names:
            raise ValueError('対象名は重複できません')
        names.add(repo['name'])
        if not isinstance(repo.get('commits'), list) or not all(isinstance(c, list) and len(c) == 3 and all(isinstance(s, str) for s in c) for c in repo['commits']):
            raise ValueError('commits は [ハッシュ、ISO 形式の日付、件名] の配列で指定してください')
        if not isinstance(repo.get('files'), list):
            raise ValueError('files は配列で指定してください')
        for file in repo['files']:
            if not isinstance(file, dict):
                raise ValueError('file はオブジェクトで指定してください')
            for key in ('path', 'status', 'body', 'notice'):
                if not isinstance(file.get(key), str):
                    raise ValueError(f'file.{key} は文字列で指定してください')
            if file['status'][:1] not in ('A', 'D', 'M', 'R', 'C', 'T', 'U', 'X', 'B'):
                raise ValueError('ファイル状態の値が不正です')
            if file.get('old') is not None and not isinstance(file['old'], str):
                raise ValueError('file.old は文字列または null で指定してください')
            for key in ('old_mode', 'new_mode'):
                if file.get(key) is not None and not (isinstance(file[key], str) and re.fullmatch(r'[0-7]{6}', file[key])):
                    raise ValueError(f'file.{key} は 6 桁の 8 進数の文字列または null で指定してください')
            if type(file.get('binary')) is not bool:
                raise ValueError('file.binary は真偽値で指定してください')
            for key in ('added', 'deleted'):
                if file.get(key) is not None and (type(file[key]) is not int or file[key] < 0):
                    raise ValueError(f'file.{key} は 0 以上の整数または null で指定してください')
            if data['full_text'] and 'full_body' not in file:
                raise ValueError('full_text が true の場合は full_body が必要です')
            if file.get('full_body') is not None and not isinstance(file['full_body'], str):
                raise ValueError('full_body は文字列または null で指定してください')
    return data


def make_html(data, template, artifact=False):
    data = validate(data)
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    if template.count('/*__DATA__*/null') != 1:
        raise ValueError('テンプレートにはデータの挿入位置を 1 か所指定してください')
    before, after = template.split('/*__DATA__*/null')
    page = (before.replace('__TITLE__', html.escape(data['title'])) + payload
            + after.replace('__TITLE__', html.escape(data['title'])))
    return artifact_body(page) if artifact else page


def artifact_body(page):
    """公開先が文書の骨組みを付けるので、DOCTYPE・html・head・body のタグを外します。"""
    page, heads = re.subn(r'\A<!DOCTYPE html>\s*<html[^>]*>\s*<head>\s*', '', page)
    page, middles = re.subn(r'\s*</head>\s*<body[^>]*>\s*', '\n', page, count=1)
    page, tails = re.subn(r'\s*</body>\s*</html>\s*\Z', '\n', page)
    if (heads, middles, tails) != (1, 1, 1):
        raise ValueError('テンプレートから html・head・body のタグを外せません')
    return page


def repository_paths(location):
    root = Path(decode(git(Path(location).expanduser().resolve(), 'rev-parse', '--show-toplevel')).strip()).resolve()
    # rev-parse は相対パスを返すことがあるので、リポジトリの最上位から解決する。
    return [root, *((root / decode(git(root, 'rev-parse', option)).strip()).resolve()
                    for option in ('--git-dir', '--git-common-dir'))]


def check_output(filename, protected_paths=(), *, data_only=False):
    if filename == '-':
        return
    destination = Path(filename).expanduser().resolve()
    for protected in protected_paths:
        if destination.is_relative_to(Path(protected).expanduser().resolve()):
            raise ValueError(f'比較対象内には出力できません: {filename}')
    if data_only:
        # JSON にリポジトリの場所を保存しないため、再生成時は比べたリポジトリが分からない。
        # Git 管理下でも、無視される場所（作業用のフォルダなど）への出力は許し、管理される場所への出力だけを止める。
        for parent in (destination.parent, *destination.parent.parents):
            if parent.name == '.git' or ((parent / 'HEAD').is_file() and (parent / 'objects').is_dir()
                                         and (parent / 'refs').is_dir()):
                raise ValueError(f'--data の出力先に Git の管理用のフォルダは指定できません: {filename}')
        base = next((d for d in (destination.parent, *destination.parent.parents) if d.is_dir()), None)
        # Git が入っていない環境では、管理される場所かを確かめる手段が無く、コミットもされないので確かめない。
        inside = base is not None and shutil.which('git') is not None and subprocess.run(['git', '-C', str(base), 'rev-parse', '--show-toplevel'],
                                                     capture_output=True).returncode == 0
        if inside and subprocess.run(['git', '-C', str(base), 'check-ignore', '-q', '--no-index', str(destination)],
                                     capture_output=True).returncode != 0:
            raise ValueError(f'--data の出力先は、Git で管理されない場所（リポジトリの外か、無視される場所）にしてください: {filename}')


def write(filename, content):
    if filename == '-':
        sys.stdout.write(content)
    else:
        Path(filename).expanduser().write_text(content, encoding='utf-8')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, add_help=False)
    parser._optionals.title = 'オプション'
    parser.add_argument('-h', '--help', action='help', help='使い方を表示して終了します')
    parser.add_argument('--repo', nargs=4, action='append', default=[], metavar=('名前', 'パス', '比較元', '比較先'), help='名前・パス・比較元・比較先を指定します（複数指定可）')
    parser.add_argument('--dirs', nargs=3, action='append', default=[], metavar=('名前', '変更前', '変更後'), help='通常の2ディレクトリまたは2ファイルを比較します（複数指定可）')
    parser.add_argument('--diff', nargs=2, action='append', default=[], metavar=('名前', '差分ファイル'), help='unified diff を読み込みます（複数指定可）')
    parser.add_argument('--merge-base', action='append', default=[], metavar='名前', help='指定したリポジトリ名の共通祖先から比較します')
    parser.add_argument('--data', metavar='JSON', help='出力済み JSON を再利用します。- は標準入力から読み込みます')
    parser.add_argument('--title', metavar='見出し', help='ページの見出しを指定します')
    parser.add_argument('--data-version', metavar='バージョン', help='データのバージョンを任意の文字列で指定します。新規収集時は必須です。--data では JSON の値を維持します')
    parser.add_argument('--group-depth', type=int, default=None, metavar='階層', help='ディレクトリの分類階層を指定します（既定: 2、0: 分類なし）')
    parser.add_argument('--full-text', action='store_true', help='変更したファイルの変更前と変更後の全文を含めます')
    parser.add_argument('--template', type=Path, default=Path(__file__).with_name('template.html'), metavar='パス', help='HTML テンプレートのパスを指定します')
    parser.add_argument('--json-out', metavar='パス', help='JSON の出力先を指定します。- は標準出力に書き込みます')
    parser.add_argument('--artifact', action='store_true', help='DOCTYPE・html・head・body のタグを付けずに HTML を書き出します（骨組みを付けて表示する公開先向け）')
    parser.add_argument('-o', '--output', metavar='パス', help='HTML の出力先を指定します。- は標準出力に書き込みます')
    args = parser.parse_args(argv)
    try:
        protected_paths = []
        if not args.output and not args.json_out:
            raise ValueError('--output または --json-out を指定してください')
        if args.output == '-' and args.json_out == '-':
            raise ValueError('標準出力を指定できる出力先は 1 つです')
        if args.output and args.json_out and args.output != '-' and args.json_out != '-' and Path(args.output).resolve() == Path(args.json_out).resolve():
            raise ValueError('HTML と JSON の出力先は別々に指定してください')
        if args.data:
            if args.repo or args.dirs or args.diff or args.merge_base or args.full_text:
                raise ValueError('--data と差分の収集オプションは同時に指定できません')
            data = validate(json.loads(sys.stdin.read() if args.data == '-' else Path(args.data).read_text(encoding='utf-8')))
            data['generated_at'] = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
            for key, value in [('title', args.title), ('data_version', args.data_version), ('group_depth', args.group_depth)]:
                if value is not None:
                    data[key] = value
        else:
            names = [r[0] for r in [*args.repo, *args.dirs, *args.diff]]
            if args.data_version is None:
                raise ValueError('--data-version を指定してください')
            if not names or len(set(names)) != len(names):
                raise ValueError('重複しない名前で比較対象を指定してください')
            if set(args.merge_base) - {r[0] for r in args.repo}:
                raise ValueError('--merge-base の名前は --repo の名前と一致させてください')
            protected_paths = [path for _, location, _, _ in args.repo for path in repository_paths(location)]
            protected_paths += [Path(location).expanduser().resolve() for _, a, b in args.dirs for location in (a, b)]
            protected_paths += [Path(location).expanduser().resolve() for _, location in args.diff]
            now = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
            data = dict(schema_version=SCHEMA_VERSION, title=args.title or '差分レビュー',
                        generated_at=now, data_version=args.data_version,
                        group_depth=2 if args.group_depth is None else args.group_depth,
                        full_text=args.full_text, sources=[
                            *[collect(*repo, repo[0] in args.merge_base, args.full_text) for repo in args.repo],
                            *[collect_plain(*item, args.full_text) for item in args.dirs],
                            *[collect_patch(*item, args.full_text) for item in args.diff]])
        validate(data)
        for output in (args.output, args.json_out):
            if output:
                check_output(output, protected_paths, data_only=bool(args.data))
        page = make_html(data, args.template.read_text(encoding='utf-8'), args.artifact) if args.output else None
        if args.json_out:
            write(args.json_out, json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        if args.output:
            write(args.output, page)
        return 0
    except (ValueError, OSError, RecursionError, subprocess.CalledProcessError) as exc:
        message = str(exc)
        if isinstance(exc, subprocess.CalledProcessError):
            message = decode(exc.stderr).strip() or f'{" ".join(map(str, exc.cmd[-3:]))} が終了コード {exc.returncode} で失敗しました'
        parser.exit(2, f'エラー: {message}\n')


if __name__ == '__main__':
    sys.exit(main())
