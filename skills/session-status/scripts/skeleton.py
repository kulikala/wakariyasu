#!/usr/bin/env python3
"""Print the session-status reply with its headings, column names and state words filled in for one language.

The words come from lang/<code>/labels.json of this skill. A language without a pack gets a labels file
from --init, translated, and passed with --labels. Uses only the Python standard library.
"""
import argparse
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import labels as labels_module  # noqa: E402

STATES = (('✅', 'stateDone'), ('🚧', 'stateInProgress'), ('⏳', 'stateWaitingProcess'),
          ('🙋', 'stateWaitingDecision'), ('📝', 'stateNotStarted'), ('❗', 'stateProblem'), ('⛔', 'stateCancelled'))


def mark(word):
    """The mark after the letter of the recommended option; a space separates it from the letter unless the word starts with a non-ASCII character."""
    return word if ord(word[0]) > 127 else ' ' + word


def render(labels):
    L = labels
    rows = []
    for number, (emoji, key) in enumerate(STATES, 1):
        word = f'{emoji} {L[key]}'
        if key == 'stateWaitingDecision':
            word += L['decisionRef'].replace('{n}', '1')
        rows.append(f'| {number} | … | {word} | … |')
    lines = [f'## {L["goal"]}', '', '…', '',
             f'## {L["instruction"]}', '', '…', '',
             f'## {L["tasks"]}', '',
             f'| {L["colNumber"]} | {L["colTask"]} | {L["colState"]} | {L["colNotes"]} |', '|---|---|---|---|', *rows, '',
             f'## {L["status"]}', '', '…', '',
             f'## {L["decisions"]}', '',
             '### 1. …', '', '…', '',
             f'| {L["colOption"]} | {L["colOptionDetail"]} |', '|---|---|',
             f'| A{mark(L["recommended"])} | … |', '| B | … |']
    return '\n'.join(lines) + '\n'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lang', metavar='CODE', help='the language of the reply (default: English)')
    parser.add_argument('--labels', metavar='FILE', help='a labels file: every word for a language without a pack, or single words that replace the pack\'s')
    parser.add_argument('--init', metavar='CODE', help='write the English labels to translate for this language (with -o)')
    parser.add_argument('-o', '--output', metavar='FILE', help='where --init writes the file')
    args = parser.parse_args(argv)
    try:
        if args.init:
            if not args.output:
                parser.error('--init needs -o FILE')
            Path(args.output).expanduser().write_text(labels_module.init_text(), encoding='utf-8')
            return 0
        override = labels_module.read(args.labels) if args.labels else None
        sys.stdout.write(render(labels_module.resolve(args.lang, override, 'skeleton.py')))
    except labels_module.LabelsError as error:
        print(f'skeleton.py: {error}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
