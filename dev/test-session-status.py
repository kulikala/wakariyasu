#!/usr/bin/env python3
"""Test the session-status page builder and skeleton: building, validation, the labels of each language, and the labels of a language without a pack."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'skills' / 'session-status' / 'scripts'))
sys.dont_write_bytecode = True
import build  # noqa: E402
import labels as labels_module  # noqa: E402
import skeleton  # noqa: E402

template = (ROOT / 'skills' / 'session-status' / 'scripts' / 'template.html').read_text(encoding='utf-8')
report = json.loads((ROOT / 'tests' / 'session-status-report.json').read_text(encoding='utf-8'))
labels = labels_module.english()
SCRIPTS = ROOT / 'skills' / 'session-status' / 'scripts'
failures = []


def check(name, condition):
    print(('ok   ' if condition else 'FAIL ') + name)
    if not condition:
        failures.append(name)


def rejects(name, change):
    broken = json.loads(json.dumps(report))
    change(broken)
    try:
        build.validate(broken)
    except build.ReportError:
        check('rejects ' + name, True)
    else:
        check('rejects ' + name, False)


page = build.make_html(report, template)
check('full page keeps the document skeleton', page.startswith('<!DOCTYPE html>') and page.rstrip().endswith('</html>'))
check('title is filled in', '<title>Docs site migration</title>' in page)
check('data is filled in once', '/*__DATA__*/' not in page and page.count('"Docs site migration"') == 1)

artifact = build.make_html(report, template, artifact=True)
check('artifact starts with the title', artifact.startswith('<title>Docs site migration</title>'))
check('artifact has no skeleton, charset or viewport', not re.search(r'(?i)<!doctype|<html[\s>]|<head[\s>]|</head>|<body[\s>]|</body>|</html>|charset|name="viewport"', artifact))
check('artifact keeps the viewport-fit meta right after the title', artifact.startswith('<title>Docs site migration</title>\n  <meta name="claude:viewport-fit-sides" content="cover">'))
check('plain page has charset, viewport, html lang and body', all(t in page for t in ('<html lang="en">', '<meta charset="UTF-8">', 'name="viewport"', '<head>', '<body>')) and 'claude:viewport-fit-sides' not in page)
def in_order(text, tokens):
    positions = [text.find(t) for t in tokens]
    return -1 not in positions and positions == sorted(positions)
parts = ['<title>', 'type="importmap"', '@tailwindcss/browser', 'type="text/tailwindcss"', 'prefers-color-scheme', '<div id="app"', '<script type="module">']
check('artifact parts are in order', in_order(artifact, parts))
check('plain page parts are in order', in_order(page, ['<!DOCTYPE html>', '<head>', *parts, '</body>', '</html>']))
check('the app element carries lang', '<div id="app" v-cloak lang="en">' in artifact)

tricky = json.loads(json.dumps(report))
tricky['title'] = 'A & B <c>'
tricky['goal'] = '</script><script>alert(1)</script>'
page = build.make_html(tricky, template)
check('title is escaped', '<title>A &amp; B &lt;c&gt;</title>' in page)
check('data cannot close the script element', '</script><script>alert' not in page and page.count('</script>') == template.count('</script>'))

rejects('an unknown state', lambda r: r['tasks'][0].update(state='doing'))
rejects('an unknown key', lambda r: r.update(summary='x'))
rejects('a labels key in the report', lambda r: r.update(labels={'copy': 'x'}))
rejects('a duplicate decision number', lambda r: r['decisions'][1].update(number=1))
rejects('a duplicate option letter', lambda r: r['decisions'][0]['options'][1].update(letter='A'))
rejects('two recommended options', lambda r: r['decisions'][0]['options'][1].update(recommended=True))
rejects('a recommended option that is not first', lambda r: (r['decisions'][0]['options'][0].pop('recommended'), r['decisions'][0]['options'][1].update(recommended=True)))
rejects('a task that points to a missing decision', lambda r: r['tasks'][3].update(decision=9))
rejects('a decision on a task in another state', lambda r: r['tasks'][0].update(decision=1))
rejects('a missing title', lambda r: r.pop('title'))

ja = labels_module.read(ROOT / 'skills' / 'session-status' / 'lang' / 'ja' / 'labels.json')
check('the ja labels cover every word', set(ja) == set(labels))
for key in labels:
    if key not in ('dayFormat', 'monthDay'):
        check(f'ja label {key} keeps its placeholders', set(re.findall(r'\{\w+\}', ja[key])) == set(re.findall(r'\{\w+\}', labels[key])))
labels_module.check(ja, complete=True)
japanese = {**json.loads(json.dumps(report)), 'lang': 'ja'}
page_ja = build.make_html(japanese, template, labels_module.resolve('ja', None, 'build.py'))
check('the ja page carries the ja words', json.dumps(ja['decisions'], ensure_ascii=False)[1:-1] in page_ja)
check('the English words are put into the template once', page_ja.count('"stateWaitingProcess":"Waiting on a process"') + page_ja.count('"stateWaitingProcess": "Waiting on a process"') == 1)
check('the English page carries no extra labels', '"labels":{' not in page)


def stops(name, call, message):
    try:
        call()
    except labels_module.LabelsError as error:
        check(name, message in str(error))
    else:
        check(name, False)


stops('no pack and no file stops with the command that starts the file', lambda: labels_module.resolve('fr', None, 'build.py'), 'no labels for fr; run `build.py --init fr -o <file>`')
stops('a path is not a language code', lambda: labels_module.resolve('../x', None, 'build.py'), 'not a language code')
stops('an unknown key', lambda: labels_module.resolve('ja', {'nope': 'x'}, 'build.py'), 'unknown label keys: nope')
stops('a dropped placeholder', lambda: labels_module.resolve('ja', {'progress': '回答済み'}, 'build.py'), 'must keep the placeholders')
stops('a missing key for a language without a pack', lambda: labels_module.resolve('fr', {'goal': 'But'}, 'build.py'), 'missing label keys')
check('a word over the ja pack changes one word', labels_module.resolve('ja', {'copy': 'X'}, 'build.py')['copy'] == 'X' and labels_module.resolve('ja', {'copy': 'X'}, 'build.py')['goal'] == ja['goal'])

with tempfile.TemporaryDirectory(prefix='status-labels-') as folder:
    file = Path(folder) / 'fr.json'
    run = lambda *args, **kw: subprocess.run([sys.executable, '-B', *map(str, args)], capture_output=True, text=True, **kw)
    started = run(SCRIPTS / 'build.py', '--init', 'fr', '-o', file)
    check('--init writes the English words', started.returncode == 0 and json.loads(file.read_text(encoding='utf-8')) == labels)
    translated = {key: value.replace('Current goal', 'Objectif actuel') for key, value in labels.items()}
    file.write_text(json.dumps(translated, ensure_ascii=False), encoding='utf-8')
    report_file = Path(folder) / 'report.json'
    report_file.write_text(json.dumps({**report, 'lang': 'fr'}), encoding='utf-8')
    built = run(SCRIPTS / 'build.py', report_file, '-o', '-', '--labels', file)
    check('build.py takes the words of a language without a pack from --labels', built.returncode == 0 and 'Objectif actuel' in built.stdout)
    refused = run(SCRIPTS / 'build.py', report_file, '-o', '-')
    check('build.py stops for a language without a pack and names the command', refused.returncode == 2 and '--init fr' in refused.stderr and 'Traceback' not in refused.stderr)
    shown = run(SCRIPTS / 'skeleton.py', '--lang', 'fr', '--labels', file)
    check('skeleton.py prints the words of --labels', shown.returncode == 0 and '## Objectif actuel' in shown.stdout)
    refused = run(SCRIPTS / 'skeleton.py', '--lang', 'fr')
    check('skeleton.py stops for a language without a pack', refused.returncode == 2 and 'skeleton.py --init fr' in refused.stderr)
    file.write_text(json.dumps({**translated, 'progress': 'x'}), encoding='utf-8')
    check('build.py rejects a dropped placeholder', run(SCRIPTS / 'build.py', report_file, '-o', '-', '--labels', file).returncode == 2)

for code in ('en', 'ja'):
    shipped = (ROOT / 'skills' / 'session-status' / 'lang' / code / 'reply-template.md').read_text(encoding='utf-8')
    check(f'reply-template.md of {code} is what skeleton.py prints', shipped == skeleton.render(labels_module.resolve(code, None, 'skeleton.py')))
check('the ja skeleton has the ja state words', '🙋 判断待ち（1）' in skeleton.render(ja) and '## 現在のゴール' in skeleton.render(ja))
check('the skeleton prints the state words once each', all(skeleton.render(labels).count(f'{e} {labels[k]}') == 1 for e, k in skeleton.STATES))

sys.exit(1 if failures else 0)
