#!/usr/bin/env python3
"""show-changes の差分ページを作って検証し、必要に応じて比較対象の外にサンプルを保存します。"""
import argparse
import copy
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
DEV = Path(__file__).resolve().parent
SCRIPTS = DEV.parent / 'skills' / 'show-changes' / 'scripts'
sys.path.insert(0, str(SCRIPTS))
# build.py のキャッシュ（__pycache__）をリポジトリに残さない。
sys.dont_write_bytecode = True
import build  # noqa: E402


def snapshot(path):
    root = Path(build.decode(build.git(path, 'rev-parse', '--show-toplevel')).strip())
    directory = Path(build.decode(build.git(path, 'rev-parse', '--absolute-git-dir')).strip())
    digest = hashlib.sha256()
    digest.update(build.git(root, 'status', '--porcelain=v1', '-z', '--untracked-files=all'))
    for raw in build.git(root, 'ls-files', '-z', '--cached', '--others', '--exclude-standard').split(b'\0'):
        if not raw:
            continue
        file = root / os.fsdecode(raw)
        digest.update(raw + b'\0')
        if file.is_symlink():
            digest.update(os.fsencode(os.readlink(file)))
        elif file.is_file():
            digest.update(file.read_bytes())
        else:
            digest.update(b'<absent-or-directory>')
    for name in ('HEAD', 'index', 'MERGE_HEAD', 'MERGE_MSG', 'MERGE_MODE'):
        file = directory / name
        digest.update(file.read_bytes() if file.exists() else b'<absent>')
    return digest.hexdigest()


def command(args, stdin=None):
    result = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'build.py'), *args],
                            input=stdin, text=True, capture_output=True)
    if result.returncode:
        raise AssertionError(result.stderr)
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__, add_help=False)
    parser._optionals.title = 'オプション'
    parser.add_argument('-h', '--help', action='help', help='使い方を表示して終了します')
    parser.add_argument('--repo', nargs=4, action='append', required=True,
                        metavar=('名前', 'パス', '比較元', '比較先'), help='検証するリポジトリと比較コミットを指定します（複数指定可）')
    parser.add_argument('--merge-base', action='append', default=[], metavar='名前', help='指定したリポジトリの共通祖先から比較します')
    parser.add_argument('--sample-dir', type=Path, metavar='保存先', help='書き込み可能な既存の保存先を指定します。省略時はメモリ上だけで検証します')
    parser.add_argument('--skip-browser', action='store_true', help='ブラウザー操作を実行せず、HTML の静的検査と Python の回帰検証を行います')
    args = parser.parse_args()
    before = {path: snapshot(path) for _, path, _, _ in args.repo}
    protected_paths = [root for _, path, _, _ in args.repo for root in build.repository_paths(path)]
    cli = []
    for repo in args.repo:
        cli += ['--repo', *repo]
    for name in args.merge_base:
        cli += ['--merge-base', name]
    pages = {}
    report = {}
    for full in (False, True):
        kind = 'full' if full else 'diff'
        flags = cli + ['--title', '差分検証 <offline>', '--data-version', '検証用', '--output', '-']
        if full:
            flags += ['--full-text']
        page = command(flags)
        data = json.loads(re.search(r'const DATA = (.*?);?\n', page).group(1))
        build.validate(data)
        assert data['data_version'] == '検証用'
        assert 'id="generated"' not in page
        assert all('source' not in repo and 'protected_paths' not in repo for repo in data['sources'])
        assert all(str(root) not in page for root in protected_paths)
        browser_flags = ['--static-only'] if args.skip_browser else []
        result = subprocess.run(['node', str(DEV / 'test-show-changes-page.mjs'), *browser_flags], input=page,
                                capture_output=True, text=True, timeout=600)
        if result.returncode:
            raise AssertionError(result.stderr)
        report[kind] = json.loads(result.stdout)
        report[kind]['repositories'] = [dict(name=r['name'], files=len(r['files']), base=r['base'], target=r['target']) for r in data['sources']]
        # Test the actual JSON-only CLI and re-embedding through stdin.
        exported = command([*cli, '--data-version', '任意の値', '--json-out', '-'] + (['--full-text'] if full else []))
        exported_data = json.loads(exported)
        assert all(str(root) not in exported for root in protected_paths)
        assert exported_data['data_version'] == '任意の値'
        roundtrip = command(['--data', '-', '--output', '-'], exported)
        restored = json.loads(re.search(r'const DATA = (.*?);?\n', roundtrip).group(1))
        assert restored['sources'] == data['sources']
        assert restored['full_text'] == full
        assert restored['data_version'] == exported_data['data_version']
        for version in ('任意のバージョン <第2回> & "確認"', ''):
            customized = command(['--data', '-', '--data-version', version, '--output', '-'], exported)
            custom_data = json.loads(re.search(r'const DATA = (.*?);?\n', customized).group(1))
            assert custom_data['data_version'] == version
        report[kind]['jsonRoundtrip'] = True
        pages[kind] = (page, data)
    missing = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'build.py'), *cli, '--json-out', '-'], capture_output=True, text=True)
    assert missing.returncode == 2 and '--data-version' in missing.stderr
    assert build.numstats(b'2\t1\t\0old\tname\0new\nname\0' + b'1\t0\told\tname\0') == {'new\nname': (b'2', b'1'), 'old\tname': (b'1', b'0')}
    assert build.numstats(b'0\t1\tpath\0' + b'2\t0\tpath\0')['path'] == (b'2', b'1')
    assert build.patch_body(iter([b'a/x b/x\ndeleted file mode 100644\n@@ -1 +0,0 @@\n-old\n', b'a/x b/x\nnew file mode 120000\n@@ -0,0 +1 @@\n+target\n']), 'T') == ('@@ -1 +0,0 @@\n-old\n@@ -0,0 +1 @@\n+target', '')
    assert build.patch_body(iter([b'a/x b/x\n@@ -1 +1 @@\n-\x82\xa0\n+\x82\xa1\n']), 'M') == ('@@ -1 +1 @@\n-\\x82\\xa0\n+\\x82\\xa1', build.UNREADABLE)
    full = build.text_body('a\u2028b\n'.encode(), 'a\u2028c\n'.encode(), None)
    assert full.startswith('@@ -1 +1 @@\n') and '\\ No newline at end of file' not in full
    assert '\\ No newline at end of file' in build.text_body(b'old', b'new', None)
    assert build.text_body(b'same\n', b'same\n', 3) == '' and build.text_body(b'same\n', b'same\n', None) == '@@ -1,1 +1,1 @@\n same'
    # All output guards are checked without opening a destination.
    data = pages['full'][1]
    for root in protected_paths:
        for data_only in (False, True):
            try:
                build.check_output(str(root / 'forbidden.html'), () if data_only else protected_paths, data_only=data_only)
            except ValueError:
                pass
            else:
                raise AssertionError('Repository output was not rejected')
    # The JSON-only CLI must reject destinations before opening any repository file.
    for option in ('--output', '--json-out'):
        rejected = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'build.py'),
                                   '--data', '-', option, str(protected_paths[0] / 'forbidden.html')],
                                  input=json.dumps(data), text=True, capture_output=True)
        assert rejected.returncode == 2 and 'Git で管理されない場所' in rejected.stderr
    malformed = copy.deepcopy(data)
    malformed['sources'][0]['files'] = ['x']
    rejected = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'build.py'), '--data', '-', '--json-out', '-'],
                              input=json.dumps(malformed), text=True, capture_output=True)
    assert rejected.returncode == 2 and 'Traceback' not in rejected.stderr
    hostile = copy.deepcopy(data)
    hostile['title'] = '/*__DATA__*/null __TITLE__ </title><script>throw Error("unsafe")</script>'
    first_file = next((f for r in hostile['sources'] for f in r['files']), None)
    if first_file:
        first_file['body'] += '\n+</script><script>throw Error("unsafe")</script>'
    escaped = build.make_html(hostile, (SCRIPTS / 'template.html').read_text())
    template = (SCRIPTS / 'template.html').read_text()
    assert len(re.findall(r'<script\b', escaped)) == len(re.findall(r'<script\b', template))
    assert escaped.count('</script>') == template.count('</script>')
    assert '<title>' + html.escape(hostile['title']) + '</title>' in escaped
    assert json.loads(re.search(r'const DATA = (.*?);?\n', escaped).group(1)) == hostile
    artifact = command([*cli, '--data-version', '検証用', '--artifact', '-o', '-'])
    assert not re.search(r'(?i)<!doctype|<html[\s>]|<head>|</head>|<body[\s>]|</body>|</html>', artifact)
    result = subprocess.run(['node', str(DEV / 'test-show-changes-page.mjs'), *browser_flags], input=artifact,
                            capture_output=True, text=True, timeout=600)
    if result.returncode:
        raise AssertionError(result.stderr)
    report['artifact'] = json.loads(result.stdout)
    report['regressions'] = ['file type change patches and stats', 'NUL-delimited rename stats', 'LF-only full-text lines', 'missing final newline', 'protected output paths', 'HTML/script escaping', 'required data version', 'arbitrary and empty versions', 'JSON version preservation', 'title data-marker separation', 'no repository path metadata', 'JSON-only output guards', 'malformed JSON files', 'non-UTF-8 bytes', 'artifact page', 'diff -ru binary lines', 'suppressed blank context', '-diff attribute text', 'symlink type change', 'renamed plain diff', 'CRLF diff file', 'file modes']
    with tempfile.TemporaryDirectory(prefix='plain-', dir=args.sample_dir or None) as folder:
        folder = Path(folder); left = folder / 'before'; right = folder / 'after'
        left.mkdir(); right.mkdir()
        (left / '変更.py').write_text('def old():\n    return 1\n', encoding='utf-8')
        (right / '変更.py').write_text('def new():\n    return 2\n', encoding='utf-8')
        (left / '削除.txt').write_text('削除\n', encoding='utf-8')
        (right / '追加.md').write_text('# 見出し\n**太字** と `code`\n- 項目\n[リンク](https://example.com)\n', encoding='utf-8')
        (right / '空ファイル').touch()
        (left / 'binary').write_bytes(b'old\0'); (right / 'binary').write_bytes(b'new\0')
        (left / '改行なし').write_bytes(b'old'); (right / '改行なし').write_bytes(b'new')
        (left / 'sjis.txt').write_bytes(b'\x82\xa0\n'); (right / 'sjis.txt').write_bytes(b'\x82\xa1\n')
        (left / 'link').symlink_to('変更.py'); (right / 'link').symlink_to('追加.md')
        originals = {str(p): p.read_bytes() for root in (left,right) for p in root.iterdir()}
        plain_cli = ['--dirs', '通常のフォルダ', str(left), str(right), '--data-version', 'フォルダ検証']
        for full in (False,True):
            page = command([*plain_cli, *(['--full-text'] if full else []), '-o', '-'])
            result = subprocess.run(['node', str(DEV / 'test-show-changes-page.mjs'), *browser_flags], input=page, text=True, capture_output=True, timeout=600)
            assert result.returncode == 0, result.stderr
            plain_data = json.loads(re.search(r'const DATA = (.*?);?\n', page).group(1))
            by_path = {f['path']: f for f in plain_data['sources'][0]['files']}
            assert len(by_path) == 8
            assert '-\\x82\\xa0' in by_path['sjis.txt']['body'] and by_path['sjis.txt']['notice'] == build.UNREADABLE
            assert '-変更.py' in by_path['link']['body'] and '+追加.md' in by_path['link']['body']
            assert by_path['空ファイル']['status'] == 'A'
            assert by_path['binary']['binary']
            assert 'No newline' in by_path['改行なし']['body']
            assert by_path['変更.py']['added'] == 2 and by_path['変更.py']['deleted'] == 2
            if args.sample_dir:
                (args.sample_dir / ('plain-full.html' if full else 'plain-diff.html')).write_text(page, encoding='utf-8')
        patch = folder / 'input.diff'
        patch.write_text('--- a/old name.txt\n+++ b/new name.txt\n@@ -1,2 +1,2 @@\n---- 本文\n++++ 本文\n 文脈\n--- /dev/null\n+++ b/追加.md\n@@ -0,0 +1 @@\n+# 見出し\n', encoding='utf-8')
        patch_cli = ['--diff','差分ファイル',str(patch),'--data-version','差分検証','--full-text']
        patch_data = json.loads(command([*patch_cli,'--json-out','-']))
        assert len(patch_data['sources'][0]['files']) == 2
        assert patch_data['sources'][0]['files'][0]['old'] == 'old name.txt'
        assert patch_data['sources'][0]['files'][0]['status'] == 'R'
        assert patch_data['sources'][0]['files'][0]['full_body'] is None
        metadata_patch = folder / 'metadata.diff'
        metadata_patch.write_text('diff --git a/old.md b/new.md\nsimilarity index 100%\nrename from old.md\nrename to new.md\ndiff --git a/data.bin b/data.bin\nBinary files a/data.bin and b/data.bin differ\ndiff --git a/run.sh b/run.sh\nold mode 100644\nnew mode 100755\n', encoding='utf-8')
        metadata_data = json.loads(command(['--diff','メタデータ',str(metadata_patch),'--data-version','検証','--json-out','-']))
        metadata_files = metadata_data['sources'][0]['files']
        assert [f['status'] for f in metadata_files] == ['R','M','M']
        assert metadata_files[1]['binary'] and metadata_files[0]['old'] == 'old.md'
        assert (metadata_files[2]['old_mode'], metadata_files[2]['new_mode']) == ('100644', '100755')
        variants = folder / 'variants.diff'
        variants.write_bytes(b'diff --git x.txt x.txt\n--- x.txt\n+++ x.txt\n@@ -1,3 +1,3 @@\n a\n\n-b\n+c\n'
                             b'diff --git i/y.txt w/y.txt\n--- i/y.txt\n+++ w/y.txt\n@@ -1 +1 @@\n-\x82\n+z\n')
        variant_files = json.loads(command(['--diff', '形の違う差分', str(variants), '--data-version', '検証', '--json-out', '-']))['sources'][0]['files']
        assert [(f['path'], f['status']) for f in variant_files] == [('x.txt', 'M'), ('y.txt', 'M')]
        assert variant_files[0]['notice'] == '' and build.UNREADABLE in variant_files[1]['notice']
        recursive = folder / 'recursive.diff'
        recursive.write_text('--- before/z.txt\t2026-01-01\n+++ after/z.txt\t2026-01-02\n@@ -1 +1 @@\n-1\n+2\n', encoding='utf-8')
        recursive_file = json.loads(command(['--diff', 'diff -ru', str(recursive), '--data-version', '検証', '--json-out', '-']))['sources'][0]['files'][0]
        assert (recursive_file['path'], recursive_file['old'], recursive_file['status']) == ('z.txt', None, 'M')
        recursive.write_text('Binary files before/b.bin and after/b.bin differ\n--- before/z.txt\n+++ after/z.txt\n@@ -1 +1 @@\n-1\n+2\n', encoding='utf-8')
        recursive_files = json.loads(command(['--diff', 'diff -ru', str(recursive), '--data-version', '検証', '--json-out', '-']))['sources'][0]['files']
        assert [(f['path'], f['binary']) for f in recursive_files] == [('b.bin', True), ('z.txt', False)]
        # A user setting that drops the space of empty context lines must not cut hunks short.
        blank = folder / 'blank'; (blank / 'a').mkdir(parents=True); (blank / 'b').mkdir()
        (blank / 'a' / 'x.txt').write_text('a\nb\n\nc\n', encoding='utf-8'); (blank / 'b' / 'x.txt').write_text('a\nB\n\nc\n', encoding='utf-8')
        suppressed = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'build.py'), '--dirs', '空行', str(blank / 'a'), str(blank / 'b'), '--data-version', '検証', '--json-out', '-'],
                                    capture_output=True, text=True, env={**os.environ, 'GIT_CONFIG_COUNT': '1', 'GIT_CONFIG_KEY_0': 'diff.suppressBlankEmpty', 'GIT_CONFIG_VALUE_0': 'true'})
        assert '\n \n c' in json.loads(suppressed.stdout)['sources'][0]['files'][0]['body']
        # Text files marked -diff in .gitattributes are shown as text, not as binary.
        marked = folder / 'marked'; marked.mkdir()
        git_env = {**os.environ, 'GIT_AUTHOR_NAME': 't', 'GIT_AUTHOR_EMAIL': 't@example.com', 'GIT_COMMITTER_NAME': 't', 'GIT_COMMITTER_EMAIL': 't@example.com'}
        subprocess.run(['git', 'init', '-q', str(marked)], check=True)
        (marked / '.gitattributes').write_text('*.lock -diff\n'); (marked / 'x.lock').write_text('v1\n')
        subprocess.run(['git', '-C', str(marked), 'add', '-A'], check=True); subprocess.run(['git', '-C', str(marked), 'commit', '-qm', '1'], check=True, env=git_env)
        (marked / 'x.lock').write_text('v2\n')
        subprocess.run(['git', '-C', str(marked), 'commit', '-qam', '2'], check=True, env=git_env)
        lock = json.loads(command(['--repo', 'ロック', str(marked), 'HEAD~1', 'HEAD', '--full-text', '--data-version', '検証', '--json-out', '-']))['sources'][0]['files'][0]
        assert not lock['binary'] and lock['added'] == 1 and '+v2' in lock['full_body']
        # A regular file replaced by a symlink with the same bytes is a type change.
        swap = folder / 'swap'; (swap / 'a').mkdir(parents=True); (swap / 'b').mkdir()
        (swap / 'a' / 'x').write_text('target'); (swap / 'b' / 'x').symlink_to('target')
        swapped = json.loads(command(['--dirs', '種類', str(swap / 'a'), str(swap / 'b'), '--data-version', '検証', '--json-out', '-']))['sources'][0]['files']
        assert [(f['path'], f['status']) for f in swapped] == [('x', 'T')] and swapped[0]['notice']
        assert (swapped[0]['old_mode'], swapped[0]['new_mode']) == ('100644', '120000')
        # A permission-only change in two folders is listed with both modes.
        chmod = folder / 'chmod'; (chmod / 'a').mkdir(parents=True); (chmod / 'b').mkdir()
        (chmod / 'a' / 'run.sh').write_text('echo\n'); (chmod / 'b' / 'run.sh').write_text('echo\n'); (chmod / 'b' / 'run.sh').chmod(0o755)
        changed = json.loads(command(['--dirs', '権限', str(chmod / 'a'), str(chmod / 'b'), '--data-version', '検証', '--json-out', '-']))['sources'][0]['files']
        assert [(f['path'], f['status'], f['old_mode'], f['new_mode']) for f in changed] == [('run.sh', 'M', '100644', '100755')]
        # diff -u of two differently named files reads as a change, as --dirs does; a CRLF diff file reads like LF.
        named = folder / 'named.diff'
        named.write_bytes(b'--- old.txt\r\n+++ new.txt\r\n@@ -1 +1 @@\r\n-1\r\n+2\r\n')
        named_file = json.loads(command(['--diff', '名前', str(named), '--data-version', '検証', '--json-out', '-']))['sources'][0]['files'][0]
        assert (named_file['path'], named_file['old'], named_file['status'], named_file['body']) == ('new.txt', 'old.txt', 'M', '@@ -1 +1 @@\n-1\n+2')
        mixed = command([*cli, *plain_cli, '--diff','差分ファイル',str(patch),'--json-out','-'])
        assert len(json.loads(mixed)['sources']) == len(args.repo)+2
        single = json.loads(command(['--dirs','ファイル',str(left/'変更.py'),str(right/'追加.md'),'--data-version','単体','--json-out','-']))
        assert single['sources'][0]['files'][0]['old'] == '変更.py'
        for source in (left,right,patch):
            output = source / 'forbidden.html' if source.is_dir() else source
            protected = subprocess.run([sys.executable,'-B',str(SCRIPTS / 'build.py'), *plain_cli,'--diff','差分ファイル',str(patch),'-o',str(output)], text=True,capture_output=True)
            assert protected.returncode == 2 and '比較対象内' in protected.stderr
        assert originals == {str(p): p.read_bytes() for root in (left,right) for p in root.iterdir()}
        report['plainAndPatch'] = dict(files=8, modes=2, singleFiles=True, unifiedDiff=True, mixedSources=True, inputsUnchanged=True)
    after = {path: snapshot(path) for _, path, _, _ in args.repo}
    assert before == after, 'Compared repositories changed during verification'
    report['repositoriesUnchanged'] = True
    report['savedPages'] = []
    if args.sample_dir:
        for kind, (page, data) in pages.items():
            output = args.sample_dir / f'sample-{kind}.html'
            build.check_output(str(output), protected_paths)
            output.write_text(page, encoding='utf-8')
            report['savedPages'].append(str(output.resolve()))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
