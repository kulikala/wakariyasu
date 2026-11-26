#!/usr/bin/env python3
"""Build the session-status page from a JSON report. Uses only the Python standard library."""
import argparse
import html
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
import labels as labels_module  # noqa: E402

HERE = Path(__file__).resolve().parent
STATES = ('done', 'in_progress', 'waiting_process', 'waiting_decision', 'not_started', 'problem', 'cancelled')
TEXT_FIELDS = ('goal', 'instruction', 'status')
TOP_KEYS = {'title', 'lang', 'asOf', *TEXT_FIELDS, 'tasks', 'decisions'}
LETTER = re.compile(r'^[A-Za-z0-9]{1,3}$')


class ReportError(ValueError):
    pass


def text(value, where, required=False):
    if value is None and not required:
        return
    if not isinstance(value, str) or (required and not value.strip()):
        raise ReportError(f'{where} must be a non-empty string' if required else f'{where} must be a string')


def validate(report):
    if not isinstance(report, dict):
        raise ReportError('the report must be a JSON object')
    unknown = set(report) - TOP_KEYS
    if unknown:
        raise ReportError(f'unknown keys: {", ".join(sorted(unknown))}')
    text(report.get('title'), 'title', required=True)
    for key in ('lang', 'asOf', *TEXT_FIELDS):
        text(report.get(key), key)

    decisions = report.get('decisions', [])
    if not isinstance(decisions, list):
        raise ReportError('decisions must be a list')
    numbers = set()
    for i, d in enumerate(decisions):
        where = f'decisions[{i}]'
        if not isinstance(d, dict):
            raise ReportError(f'{where} must be an object')
        unknown = set(d) - {'number', 'question', 'context', 'options'}
        if unknown:
            raise ReportError(f'{where}: unknown keys: {", ".join(sorted(unknown))}')
        number = d.get('number')
        if not isinstance(number, int) or isinstance(number, bool) or number < 1:
            raise ReportError(f'{where}.number must be a positive integer')
        if number in numbers:
            raise ReportError(f'decision number {number} is used twice')
        numbers.add(number)
        text(d.get('question'), f'{where}.question', required=True)
        text(d.get('context'), f'{where}.context')
        options = d.get('options', [])
        if not isinstance(options, list):
            raise ReportError(f'{where}.options must be a list')
        letters = set()
        recommended = 0
        for j, o in enumerate(options):
            ow = f'{where}.options[{j}]'
            if not isinstance(o, dict):
                raise ReportError(f'{ow} must be an object')
            unknown = set(o) - {'letter', 'label', 'text', 'recommended'}
            if unknown:
                raise ReportError(f'{ow}: unknown keys: {", ".join(sorted(unknown))}')
            letter = o.get('letter')
            if not isinstance(letter, str) or not LETTER.match(letter):
                raise ReportError(f'{ow}.letter must be 1 to 3 letters or digits, such as "A" or "Y"')
            if letter in letters:
                raise ReportError(f'{where}: option letter {letter} is used twice')
            letters.add(letter)
            text(o.get('label'), f'{ow}.label')
            text(o.get('text'), f'{ow}.text', required=True)
            if not isinstance(o.get('recommended', False), bool):
                raise ReportError(f'{ow}.recommended must be true or false')
            recommended += o.get('recommended', False)
        if recommended > 1:
            raise ReportError(f'{where}: only one option can be recommended')
        if recommended and not options[0].get('recommended'):
            raise ReportError(f'{where}: the recommended option must come first')

    tasks = report.get('tasks', [])
    if not isinstance(tasks, list):
        raise ReportError('tasks must be a list')
    for i, t in enumerate(tasks):
        where = f'tasks[{i}]'
        if not isinstance(t, dict):
            raise ReportError(f'{where} must be an object')
        unknown = set(t) - {'task', 'state', 'notes', 'decision'}
        if unknown:
            raise ReportError(f'{where}: unknown keys: {", ".join(sorted(unknown))}')
        text(t.get('task'), f'{where}.task', required=True)
        text(t.get('notes'), f'{where}.notes')
        state = t.get('state')
        if isinstance(state, dict):
            if set(state) != {'emoji', 'label'}:
                raise ReportError(f'{where}.state must have exactly "emoji" and "label"')
            text(state['emoji'], f'{where}.state.emoji', required=True)
            text(state['label'], f'{where}.state.label', required=True)
        elif state not in STATES:
            raise ReportError(f'{where}.state must be one of {", ".join(STATES)}, or {{"emoji": ..., "label": ...}}')
        decision = t.get('decision')
        if decision is not None:
            if decision not in numbers:
                raise ReportError(f'{where}.decision {decision!r} is not the number of a decision in this report')
            if state != 'waiting_decision':
                raise ReportError(f'{where}.decision is only for the state waiting_decision')
    return report


def make_html(report, template, labels=None, artifact=False):
    """Build the page. labels is the complete set of words for the report's language (default: English)."""
    english = labels_module.english()
    labels = labels or english
    validate(report)
    if labels != english:
        report = {**report, 'labels': labels}
    payload = json.dumps(report, ensure_ascii=False, separators=(',', ':'))
    # Keep the JSON from closing the script element or starting markup inside it.
    payload = payload.replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    if template.count('/*__DATA__*/null') != 1:
        raise ReportError('the template must contain /*__DATA__*/null exactly once')
    before, after = template.split('/*__DATA__*/null')
    after, replaced = re.subn(r'/\*__LABELS__\*/\{\}/\*__LABELS_END__\*/', lambda _: json.dumps(english, ensure_ascii=False).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e'), after, count=1)
    if replaced != 1:
        raise ReportError('the template must contain /*__LABELS__*/{}/*__LABELS_END__*/ once')
    title = html.escape(report['title'])
    page = before.replace('__TITLE__', title, 1) + payload + after
    return artifact_body(page) if artifact else page


def artifact_body(page):
    """Remove the DOCTYPE, html, head and body tags for a host that adds its own document skeleton."""
    page, heads = re.subn(r'\A<!DOCTYPE html>\s*<html[^>]*>\s*<head>\s*', '', page)
    page, middles = re.subn(r'\s*</head>\s*<body[^>]*>\s*', '\n', page, count=1)
    page, tails = re.subn(r'\s*</body>\s*</html>\s*\Z', '\n', page)
    if (heads, middles, tails) != (1, 1, 1):
        raise ReportError('the template does not have the expected document skeleton')
    return page


def main(argv=None):
    parser = argparse.ArgumentParser(description='Build the session-status page from a JSON report.')
    parser.add_argument('report', nargs='?', help='the JSON report; - reads standard input')
    parser.add_argument('-o', '--output', help='the HTML output path; - writes to standard output')
    parser.add_argument('--artifact', action='store_true', help='leave out the DOCTYPE, html, head and body tags (for hosts such as Claude artifacts that add them)')
    parser.add_argument('--labels', metavar='FILE', help='a JSON file of the page words: every word for a language that has no pack in lang/, or single words that replace the pack\'s')
    parser.add_argument('--init', metavar='CODE', help='write the English words to translate for this language (with -o), then stop')
    parser.add_argument('--check', action='store_true', help='only validate the report')
    parser.add_argument('--template', type=Path, default=HERE / 'template.html', help='the page template')
    args = parser.parse_args(argv)
    if args.init:
        if not args.output:
            parser.error('--init needs -o FILE')
        try:
            Path(args.output).expanduser().write_text(labels_module.init_text(), encoding='utf-8')
        except OSError as error:
            print(f'build.py: {error}', file=sys.stderr)
            return 2
        return 0
    if not args.report:
        parser.error('give the report, or --init CODE -o FILE')
    if not args.check and not args.output:
        parser.error('give -o/--output, or --check')
    try:
        raw = sys.stdin.read() if args.report == '-' else Path(args.report).read_text(encoding='utf-8')
        report = json.loads(raw)
        template = args.template.read_text(encoding='utf-8')
        lang = report.get('lang') if isinstance(report, dict) and isinstance(report.get('lang'), str) else None
        labels = labels_module.resolve(lang, labels_module.read(args.labels) if args.labels else None, 'build.py')
        if args.check:
            validate(report)
            print('ok')
            return 0
        page = make_html(report, template, labels, args.artifact)
    except (OSError, json.JSONDecodeError, ReportError, labels_module.LabelsError) as error:
        print(f'build.py: {error}', file=sys.stderr)
        return 2
    if args.output == '-':
        sys.stdout.write(page)
    else:
        Path(args.output).write_text(page, encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
