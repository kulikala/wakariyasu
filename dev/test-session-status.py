#!/usr/bin/env python3
"""Test the session-status page builder: building, validation, and the Japanese labels."""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'skills' / 'session-status' / 'scripts'))
sys.dont_write_bytecode = True
import build  # noqa: E402

template = (ROOT / 'skills' / 'session-status' / 'scripts' / 'template.html').read_text(encoding='utf-8')
report = json.loads((ROOT / 'tests' / 'session-status-report.json').read_text(encoding='utf-8'))
labels = build.default_labels(template)
failures = []


def check(name, condition):
    print(('ok   ' if condition else 'FAIL ') + name)
    if not condition:
        failures.append(name)


def rejects(name, change):
    broken = json.loads(json.dumps(report))
    change(broken)
    try:
        build.validate(broken, labels)
    except build.ReportError:
        check('rejects ' + name, True)
    else:
        check('rejects ' + name, False)


page = build.make_html(report, template)
check('full page keeps the document skeleton', page.startswith('<!DOCTYPE html>') and page.rstrip().endswith('</html>'))
check('title is filled in', '<title>Docs site migration</title>' in page)
check('data is filled in once', '/*__DATA__*/' not in page and page.count('"Docs site migration"') == 1)

artifact = build.make_html(report, template, artifact=True)
check('artifact page has no skeleton', not re.search(r'<!DOCTYPE|<html|<head>|</head>|<body|</body>|</html>', artifact))

tricky = json.loads(json.dumps(report))
tricky['title'] = 'A & B <c>'
tricky['goal'] = '</script><script>alert(1)</script>'
page = build.make_html(tricky, template)
check('title is escaped', '<title>A &amp; B &lt;c&gt;</title>' in page)
check('data cannot close the script element', '</script><script>alert' not in page and page.count('</script>') == template.count('</script>'))

rejects('an unknown state', lambda r: r['tasks'][0].update(state='doing'))
rejects('an unknown key', lambda r: r.update(summary='x'))
rejects('an unknown label', lambda r: r.update(labels={'copyButton': 'x'}))
rejects('a duplicate decision number', lambda r: r['decisions'][1].update(number=1))
rejects('a duplicate option letter', lambda r: r['decisions'][0]['options'][1].update(letter='A'))
rejects('two recommended options', lambda r: r['decisions'][0]['options'][1].update(recommended=True))
rejects('a recommended option that is not first', lambda r: (r['decisions'][0]['options'][0].pop('recommended'), r['decisions'][0]['options'][1].update(recommended=True)))
rejects('a task that points to a missing decision', lambda r: r['tasks'][3].update(decision=9))
rejects('a decision on a task in another state', lambda r: r['tasks'][0].update(decision=1))
rejects('a missing title', lambda r: r.pop('title'))

conventions = (ROOT / 'skills' / 'writing-rules' / 'lang' / 'ja' / 'conventions.md').read_text(encoding='utf-8')
block = re.search(r'## session-status のページ.*?```json\n(.*?)```', conventions, re.S)
check('the ja pack has page labels', bool(block))
if block:
    ja = json.loads(block.group(1))
    check('the ja page labels are all known', set(ja) <= set(labels))
    missing = set(labels) - set(ja) - {'colNumber'}
    check('the ja page labels cover every word' + (f' (missing: {", ".join(sorted(missing))})' if missing else ''), not missing)
    for key in labels:
        if key in ja:
            want = set(re.findall(r'\{\w+\}', labels[key]))
            check(f'ja label {key} keeps its placeholders', set(re.findall(r'\{\w+\}', ja[key])) == want)
    japanese = json.loads(json.dumps(report))
    japanese.update(lang='ja', labels=ja)
    build.validate(japanese, labels)

sys.exit(1 if failures else 0)
