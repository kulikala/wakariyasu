#!/usr/bin/env python3
"""Build and check show-changes diff pages, and save samples outside the compared targets if asked."""
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
# Do not leave build.py's cache (__pycache__) in the repository.
sys.dont_write_bytecode = True
import build  # noqa: E402
import labels as labels_module  # noqa: E402


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


def check_page_structure(page, artifact=False):
    """Read the HTML text of a built page: the decoder tag, the data script, and a packed string that cannot break out of its script."""
    decoder = f'<script src="{build.UTFPACK_DECODER_URL}" integrity="{build.utfpack_pack.decoder_sri("utfpack")}" crossorigin="anonymous"></script>'
    assert page.count(decoder) == 1
    start = page.index('globalThis.utfpackData=')
    assert page.index(decoder) < start, 'the decoder must come before the data script'
    end = page.index('</script>', start)
    packed = page[start:end]
    assert '</script' not in packed and '<!--' not in packed
    assert page.count('<!--__PACKED__-->') == 0 and '/*__LABELS__*/' not in page
    assert '"layoutInline"' in page and "id: 'inline'" in page and 'data-old' in page, 'the inline layout is in the page'
    parts = ['<title>', 'type="importmap"', decoder, 'globalThis.utfpackData=', '@tailwindcss/browser', 'type="text/tailwindcss"', 'prefers-color-scheme', '<div id="app" lang="', '<script type="module">']
    positions = [page.find(part) for part in parts]
    assert -1 not in positions and positions == sorted(positions), 'the page parts are out of order'
    skeleton = re.compile(r'(?i)<!doctype|<html[\s>]|<head>|</head>|<body[\s>]|</body>|</html>|charset|name="viewport"')
    if artifact:
        assert page.startswith('<title>') and not skeleton.search(page), 'an artifact page is a part of a document'
    else:
        assert page.startswith('<!DOCTYPE html>\n<html lang="') and '<meta charset="UTF-8">' in page and 'name="viewport"' in page
        assert page.index('<head>') < page.index('<title>') < page.index('</head>') < page.index('<body>') < page.index('<div id="app"') < page.index('</body>') < page.index('</html>')


def main():
    parser = argparse.ArgumentParser(description=__doc__, add_help=False)
    parser._optionals.title = 'options'
    parser.add_argument('-h', '--help', action='help', help='show this help and exit')
    parser.add_argument('--repo', nargs=4, action='append', required=True,
                        metavar=('NAME', 'PATH', 'BASE', 'TARGET'), help='a repository to check and the commits to compare (can be repeated)')
    parser.add_argument('--merge-base', action='append', default=[], metavar='NAME', help='compare the repository of this name from the divergence point')
    parser.add_argument('--sample-dir', type=Path, metavar='DIR', help='an existing writable folder to save samples in; without it, check in memory only')
    args = parser.parse_args()
    build.load_packer()
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
        flags = cli + ['--title', 'Diff check <offline>', '--data-version', 'for-check', '--output', '-']
        if full:
            flags += ['--full-text']
        with tempfile.TemporaryDirectory(prefix='page-') as folder:
            data_path = Path(folder) / 'data.json'
            page = command(flags + ['--json-out', str(data_path)])
            data = json.loads(data_path.read_text(encoding='utf-8'))
        build.validate(data)
        assert data['data_version'] == 'for-check'
        assert 'id="generated"' not in page
        assert all('source' not in repo and 'protected_paths' not in repo for repo in data['sources'])
        assert all(str(root) not in page for root in protected_paths)
        assert build.UTFPACK_DECODER_URL in page
        assert f'integrity="{build.utfpack_pack.decoder_sri("utfpack")}"' in page
        assert 'globalThis.utfpackData=' in page
        check_page_structure(page)
        report[kind] = {}
        report[kind]['repositories'] = [dict(name=r['name'], files=len(r['files']), base=r['base'], target=r['target']) for r in data['sources']]
        # Test the actual JSON-only CLI and re-embedding through stdin.
        exported = command([*cli, '--data-version', 'any value', '--json-out', '-'] + (['--full-text'] if full else []))
        exported_data = json.loads(exported)
        assert all(str(root) not in exported for root in protected_paths)
        assert exported_data['data_version'] == 'any value'
        roundtrip = command(['--data', '-', '--json-out', '-'], exported)
        restored = json.loads(roundtrip)
        assert restored['sources'] == data['sources']
        assert restored['full_text'] == full
        assert restored['data_version'] == exported_data['data_version']
        for version in ('custom version <2nd> & "check"', ''):
            customized = command(['--data', '-', '--data-version', version, '--json-out', '-'], exported)
            custom_data = json.loads(customized)
            assert custom_data['data_version'] == version
        report[kind]['jsonRoundtrip'] = True
        pages[kind] = (page, data)
    # English is the default: the page says "Diff review" and carries no labels.
    english = command([*cli, '--data-version', 'for-check', '--json-out', '-'])
    assert json.loads(english)['title'] == 'Diff review' and 'labels' not in json.loads(english) and 'lang' not in json.loads(english)
    # Japanese comes from the pack lang/ja/labels.json of the skill: --lang ja alone takes its words.
    ja_labels = labels_module.read(SCRIPTS.parent / 'lang' / 'ja' / 'labels.json')
    template_labels = labels_module.english()
    assert set(ja_labels) == set(template_labels), sorted(set(ja_labels) ^ set(template_labels))
    for key, english_word in template_labels.items():
        placeholders = set(re.findall(r'\{\w+\}', ja_labels[key]))
        if key in ('dayFormat', 'monthDay'):  # the page offers y, m, d, mm, dd and w for dates
            assert placeholders <= {'{y}', '{m}', '{d}', '{mm}', '{dd}', '{w}'}, key
        else:
            assert placeholders == set(re.findall(r'\{\w+\}', english_word)), key
    assert json.loads(command([*cli, '--data-version', 'for-check', '--lang', 'ja', '--json-out', '-']))['labels'] == ja_labels
    assert json.loads(command([*cli, '--data-version', 'for-check', '--lang', 'en', '--json-out', '-'])).get('labels') is None
    with tempfile.TemporaryDirectory(prefix='labels-') as label_folder:
        label_file = Path(label_folder) / 'ja.json'
        label_file.write_text(json.dumps(ja_labels, ensure_ascii=False), encoding='utf-8')
        japanese = command([*cli, '--data-version', 'for-check', '--lang', 'ja', '--labels', str(label_file), '--json-out', '-'])
        ja_data = json.loads(japanese)
        assert ja_data['lang'] == 'ja' and ja_data['labels'] == ja_labels and ja_data['title'] == '差分レビュー'
        kept = json.loads(command(['--data', '-', '--json-out', '-'], japanese))
        assert kept['lang'] == 'ja' and kept['labels'] == ja_labels
        page_ja = command(['--data', '-', '--json-out', '-'], japanese)
        assert json.loads(page_ja)['labels'] == ja_labels
        override = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'build.py'), '--data', '-', '--json-out', '-', '--lang', 'ja', '--labels', str(label_file)], input=english, text=True, capture_output=True)
        assert override.returncode == 0 and json.loads(override.stdout)['lang'] == 'ja'
        bad_file = Path(label_folder) / 'bad.json'
        build_py = [sys.executable, '-B', str(SCRIPTS / 'build.py')]
        for name, content, message in (('an unknown key', '{"copyButton": "x"}', 'unknown label keys'),
                                       ('a dropped placeholder', json.dumps({'filesMany': 'files'}), 'must keep the placeholders')):
            bad_file.write_text(content, encoding='utf-8')
            bad = subprocess.run([*build_py, '--data', '-', '-o', '-', '--labels', str(bad_file)], input=english, text=True, capture_output=True)
            assert bad.returncode == 2 and message in bad.stderr and 'Traceback' not in bad.stderr, name
        # A language without a pack: --init writes the English words, and --labels with every word builds the page.
        refused = subprocess.run([*build_py, '--data', '-', '-o', '-', '--lang', 'fr'], input=english, text=True, capture_output=True)
        assert refused.returncode == 2 and 'no labels for fr; run `build.py --init fr -o <file>`' in refused.stderr and 'Traceback' not in refused.stderr
        started = Path(label_folder) / 'fr.json'
        init = subprocess.run([*build_py, '--init', 'fr', '-o', str(started)])
        assert init.returncode == 0 and json.loads(started.read_text(encoding='utf-8')) == template_labels
        started.write_text(json.dumps({**template_labels, 'sidebar': 'Fichiers modifiés'}, ensure_ascii=False), encoding='utf-8')
        french = subprocess.run([*build_py, '--data', '-', '--json-out', '-', '--lang', 'fr', '--labels', str(started)], input=english, text=True, capture_output=True)
        fr_data = json.loads(french.stdout)
        assert french.returncode == 0 and fr_data['lang'] == 'fr' and fr_data['labels']['sidebar'] == 'Fichiers modifiés'
        started.write_text(json.dumps({k: v for k, v in template_labels.items() if k != 'sidebar'}), encoding='utf-8')
        partial = subprocess.run([*build_py, '--data', '-', '-o', '-', '--lang', 'fr', '--labels', str(started)], input=english, text=True, capture_output=True)
        assert partial.returncode == 2 and 'missing label keys: sidebar' in partial.stderr
        page_en = command(['--data', '-', '-o', '-'], english)
        assert page_en.count('"sidebar": "Changed files"') + page_en.count('"sidebar":"Changed files"') == 1
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
        assert rejected.returncode == 2 and 'a place git does not manage' in rejected.stderr
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
    template = (SCRIPTS / 'template.html').read_text()
    escaped = build.make_html(hostile, template)
    assert escaped.count('</script>') == template.count('</script>') + 2
    assert '</script><script>throw Error("unsafe")</script>' not in escaped
    assert '<title>' + html.escape(hostile['title']) + '</title>' in escaped
    assert 'globalThis.utfpackData=' in escaped
    # A packed string that could close the script or open an HTML comment is refused.
    real_pack = build.utfpack_pack.pack
    for bad in ('</script', '<!--'):
        build.utfpack_pack.pack = lambda files, emit='html', embed_decoder=False, bad=bad, **options: {
            'string': 'x' + bad, 'codec': 'deflate', 'format': 'base91', 'entry': 'utfpack/base91', 'module': ''}
        try:
            build.make_html(data, template)
        except ValueError as error:
            assert 'packed data' in str(error)
        else:
            raise AssertionError(f'The packed data check did not stop {bad}')
    # A first pack that would close the script is packed again in another format.
    calls = []
    def flaky(files, emit='html', embed_decoder=False, **options):
        calls.append(options)
        return real_pack(files, emit=emit, embed_decoder=embed_decoder, **options) if len(calls) > 1 else {
            'string': 'x</script', 'codec': 'deflate', 'format': 'base91', 'entry': 'utfpack/base91', 'module': ''}
    build.utfpack_pack.pack = flaky
    retried = build.make_html(data, template)
    assert len(calls) == 2 and calls[1] == {'ascii': True} and 'x</script' not in retried
    build.utfpack_pack.pack = real_pack
    # The words for a failed load come in the page's language, outside the packed data.
    ja_words = json.loads((SCRIPTS.parent / 'lang' / 'ja' / 'labels.json').read_text(encoding='utf-8'))
    ja_page = command([*cli, '--data-version', 'for-check', '--lang', 'ja', '-o', '-'])
    assert json.dumps(ja_words['dataLoadError'], ensure_ascii=False)[1:-1] in ja_page and ja_words['dataLoadError'] not in escaped
    artifact = command([*cli, '--data-version', 'for-check', '--artifact', '-o', '-'])
    check_page_structure(artifact, artifact=True)
    report['artifact'] = {}
    embedded = command([*cli, '--data-version', 'for-check', '--embed-decoder', '-o', '-'])
    assert build.UTFPACK_DECODER_URL not in embedded
    assert 'globalThis.utfpackData=' in embedded and 'var utfpack=' in embedded
    report['embeddedDecoder'] = True
    # A page of whole files: no comparison, every file an addition with its text, opening on the text after the change.
    with tempfile.TemporaryDirectory(prefix='files-') as folder:
        folder = Path(folder)
        (folder / 'docs' / 'sub').mkdir(parents=True)
        (folder / 'docs' / 'a.md').write_text('# Title\nsecond line\n', encoding='utf-8')
        (folder / 'docs' / 'sub' / 'b.py').write_text('print(1)\n', encoding='utf-8')
        (folder / 'empty.txt').write_text('', encoding='utf-8')
        files_cli = ['--files', 'whole', str(folder / 'docs'), str(folder / 'empty.txt'), '--data-version', 'files check']
        json_path = folder / 'files.json'
        files_page = command([*files_cli, '-o', '-', '--json-out', str(json_path)])
        files_data = json.loads(json_path.read_text(encoding='utf-8'))
        build.validate(files_data)
        assert files_data['schema_version'] == 2 and files_data['initial_scope'] == 'after' and files_data['full_text'] is True
        source = files_data['sources'][0]
        assert source['kind'] == 'files' and source['base_ref'] == '' and source['base'] == '' and source['commits'] == []
        by_path = {f['path']: f for f in source['files']}
        assert sorted(by_path) == ['docs/a.md', 'docs/sub/b.py', 'empty.txt'], sorted(by_path)
        assert all(f['status'] == 'A' and f['deleted'] == 0 for f in source['files'])
        assert by_path['empty.txt']['notice'] == ''
        assert by_path['docs/a.md']['full_body'] == '@@ -0,0 +1,2 @@\n+# Title\n+second line' and by_path['docs/a.md']['added'] == 2
        mixed = json.loads(command([*files_cli, '--dirs', 'plain', str(folder / 'docs'), str(folder / 'docs'), '--json-out', '-']))
        assert mixed['initial_scope'] == 'diff' and mixed['full_text'] is True
        for bad in ({**files_data, 'initial_scope': 'sideways'}, {**files_data, 'initial_scope': 'after', 'full_text': False}, {**files_data, 'schema_version': 1}):
            try:
                build.validate(bad)
            except ValueError:
                pass
            else:
                raise AssertionError('validate accepted data that does not fit schema version 2')
        again = json.loads(command(['--data', '-', '--json-out', '-'], json_path.read_text(encoding='utf-8')))
        assert again['sources'] == files_data['sources'] and again['initial_scope'] == 'after'
        check_page_structure(files_page)
        report['filesPage'] = {}
    report['regressions'] = ['file type change patches and stats', 'NUL-delimited rename stats', 'LF-only full-text lines', 'missing final newline', 'protected output paths', 'HTML/script escaping', 'packed data script safety', 'required data version', 'arbitrary and empty versions', 'JSON version preservation', 'title data-marker separation', 'no repository path metadata', 'JSON-only output guards', 'malformed JSON files', 'non-UTF-8 bytes', 'artifact page', 'diff -ru binary lines', 'suppressed blank context', '-diff attribute text', 'symlink type change', 'renamed plain diff', 'CRLF diff file', 'file modes', 'embedded decoder', 'files page']
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
        plain_cli = ['--dirs', 'plain folder', str(left), str(right), '--data-version', 'folder check']
        for full in (False,True):
            data_path = folder / 'page-data.json'
            page = command([*plain_cli, *(['--full-text'] if full else []), '-o', '-', '--json-out', str(data_path)])
            check_page_structure(page)
            plain_data = json.loads(data_path.read_text(encoding='utf-8'))
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
        patch_cli = ['--diff','diff file',str(patch),'--data-version','diff check','--full-text']
        patch_data = json.loads(command([*patch_cli,'--json-out','-']))
        assert len(patch_data['sources'][0]['files']) == 2
        assert patch_data['sources'][0]['files'][0]['old'] == 'old name.txt'
        assert patch_data['sources'][0]['files'][0]['status'] == 'R'
        assert patch_data['sources'][0]['files'][0]['full_body'] is None
        metadata_patch = folder / 'metadata.diff'
        metadata_patch.write_text('diff --git a/old.md b/new.md\nsimilarity index 100%\nrename from old.md\nrename to new.md\ndiff --git a/data.bin b/data.bin\nBinary files a/data.bin and b/data.bin differ\ndiff --git a/run.sh b/run.sh\nold mode 100644\nnew mode 100755\n', encoding='utf-8')
        metadata_data = json.loads(command(['--diff','metadata',str(metadata_patch),'--data-version','check','--json-out','-']))
        metadata_files = metadata_data['sources'][0]['files']
        assert [f['status'] for f in metadata_files] == ['R','M','M']
        assert metadata_files[1]['binary'] and metadata_files[0]['old'] == 'old.md'
        assert (metadata_files[2]['old_mode'], metadata_files[2]['new_mode']) == ('100644', '100755')
        variants = folder / 'variants.diff'
        variants.write_bytes(b'diff --git x.txt x.txt\n--- x.txt\n+++ x.txt\n@@ -1,3 +1,3 @@\n a\n\n-b\n+c\n'
                             b'diff --git i/y.txt w/y.txt\n--- i/y.txt\n+++ w/y.txt\n@@ -1 +1 @@\n-\x82\n+z\n')
        variant_files = json.loads(command(['--diff', 'diffs in other forms', str(variants), '--data-version', 'check', '--json-out', '-']))['sources'][0]['files']
        assert [(f['path'], f['status']) for f in variant_files] == [('x.txt', 'M'), ('y.txt', 'M')]
        assert variant_files[0]['notice'] == '' and build.UNREADABLE in variant_files[1]['notice']
        recursive = folder / 'recursive.diff'
        recursive.write_text('--- before/z.txt\t2026-01-01\n+++ after/z.txt\t2026-01-02\n@@ -1 +1 @@\n-1\n+2\n', encoding='utf-8')
        recursive_file = json.loads(command(['--diff', 'diff -ru', str(recursive), '--data-version', 'check', '--json-out', '-']))['sources'][0]['files'][0]
        assert (recursive_file['path'], recursive_file['old'], recursive_file['status']) == ('z.txt', None, 'M')
        recursive.write_text('Binary files before/b.bin and after/b.bin differ\n--- before/z.txt\n+++ after/z.txt\n@@ -1 +1 @@\n-1\n+2\n', encoding='utf-8')
        recursive_files = json.loads(command(['--diff', 'diff -ru', str(recursive), '--data-version', 'check', '--json-out', '-']))['sources'][0]['files']
        assert [(f['path'], f['binary']) for f in recursive_files] == [('b.bin', True), ('z.txt', False)]
        # A user setting that drops the space of empty context lines must not cut hunks short.
        blank = folder / 'blank'; (blank / 'a').mkdir(parents=True); (blank / 'b').mkdir()
        (blank / 'a' / 'x.txt').write_text('a\nb\n\nc\n', encoding='utf-8'); (blank / 'b' / 'x.txt').write_text('a\nB\n\nc\n', encoding='utf-8')
        suppressed = subprocess.run([sys.executable, '-B', str(SCRIPTS / 'build.py'), '--dirs', 'blank lines', str(blank / 'a'), str(blank / 'b'), '--data-version', 'check', '--json-out', '-'],
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
        lock = json.loads(command(['--repo', 'lock', str(marked), 'HEAD~1', 'HEAD', '--full-text', '--data-version', 'check', '--json-out', '-']))['sources'][0]['files'][0]
        assert not lock['binary'] and lock['added'] == 1 and '+v2' in lock['full_body']
        # A regular file replaced by a symlink with the same bytes is a type change.
        swap = folder / 'swap'; (swap / 'a').mkdir(parents=True); (swap / 'b').mkdir()
        (swap / 'a' / 'x').write_text('target'); (swap / 'b' / 'x').symlink_to('target')
        swapped = json.loads(command(['--dirs', 'type', str(swap / 'a'), str(swap / 'b'), '--data-version', 'check', '--json-out', '-']))['sources'][0]['files']
        assert [(f['path'], f['status']) for f in swapped] == [('x', 'T')] and swapped[0]['notice']
        assert (swapped[0]['old_mode'], swapped[0]['new_mode']) == ('100644', '120000')
        # A permission-only change in two folders is listed with both modes.
        chmod = folder / 'chmod'; (chmod / 'a').mkdir(parents=True); (chmod / 'b').mkdir()
        (chmod / 'a' / 'run.sh').write_text('echo\n'); (chmod / 'b' / 'run.sh').write_text('echo\n'); (chmod / 'b' / 'run.sh').chmod(0o755)
        changed = json.loads(command(['--dirs', 'permissions', str(chmod / 'a'), str(chmod / 'b'), '--data-version', 'check', '--json-out', '-']))['sources'][0]['files']
        assert [(f['path'], f['status'], f['old_mode'], f['new_mode']) for f in changed] == [('run.sh', 'M', '100644', '100755')]
        # diff -u of two differently named files reads as a change, as --dirs does; a CRLF diff file reads like LF.
        named = folder / 'named.diff'
        named.write_bytes(b'--- old.txt\r\n+++ new.txt\r\n@@ -1 +1 @@\r\n-1\r\n+2\r\n')
        named_file = json.loads(command(['--diff', 'names', str(named), '--data-version', 'check', '--json-out', '-']))['sources'][0]['files'][0]
        assert (named_file['path'], named_file['old'], named_file['status'], named_file['body']) == ('new.txt', 'old.txt', 'M', '@@ -1 +1 @@\n-1\n+2')
        mixed = command([*cli, *plain_cli, '--diff','diff file',str(patch),'--json-out','-'])
        assert len(json.loads(mixed)['sources']) == len(args.repo)+2
        single = json.loads(command(['--dirs','file',str(left/'変更.py'),str(right/'追加.md'),'--data-version','single','--json-out','-']))
        assert single['sources'][0]['files'][0]['old'] == '変更.py'
        for source in (left,right,patch):
            output = source / 'forbidden.html' if source.is_dir() else source
            protected = subprocess.run([sys.executable,'-B',str(SCRIPTS / 'build.py'), *plain_cli,'--diff','diff file',str(patch),'-o',str(output)], text=True,capture_output=True)
            assert protected.returncode == 2 and 'inside a compared target' in protected.stderr
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
