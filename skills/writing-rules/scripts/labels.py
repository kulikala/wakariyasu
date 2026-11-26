"""Read, check and start the labels (fixed words) of one skill. Uses only the Python standard library.

Each skill that shows fixed words keeps them in lang/<code>/labels.json of its own folder, with the
English words in lang/en/labels.json. This file is the same in every skill that has it
(dev/test checks that the copies are identical); it reads the folder of the skill it sits in.
"""
import json
from pathlib import Path
import re

LANG_DIR = Path(__file__).resolve().parents[1] / 'lang'
PLACEHOLDER = re.compile(r'\{\w+\}')


class LabelsError(ValueError):
    pass


def read(path):
    """Read a labels file: a JSON object of non-empty strings."""
    try:
        labels = json.loads(Path(path).expanduser().read_text(encoding='utf-8'))
    except OSError as error:
        raise LabelsError(f'cannot read the labels file: {error}')
    except json.JSONDecodeError as error:
        raise LabelsError(f'the labels file is not JSON: {error}')
    if not isinstance(labels, dict) or not all(isinstance(v, str) and v.strip() for v in labels.values()):
        raise LabelsError('the labels must be a JSON object whose values are non-empty strings')
    return labels


def english():
    return read(LANG_DIR / 'en' / 'labels.json')


def init_text():
    """The English labels as a file to translate: one key and value per line."""
    return json.dumps(english(), ensure_ascii=False, indent=2) + '\n'


def check(labels, complete, loose={}):
    """Stop on an unknown key, on a missing key when complete, and on a placeholder that was dropped or added.

    The words in braces are filled in by the tool, so a translation keeps them as they are.
    loose maps a key to the placeholders it may use; such a key may drop placeholders (dates offer more than a language needs).
    """
    reference = english()
    unknown = sorted(set(labels) - set(reference))
    if unknown:
        raise LabelsError(f'unknown label keys: {", ".join(unknown)}')
    missing = sorted(set(reference) - set(labels))
    if complete and missing:
        raise LabelsError(f'missing label keys: {", ".join(missing)}')
    for key, value in labels.items():
        want, got = set(PLACEHOLDER.findall(reference[key])), set(PLACEHOLDER.findall(value))
        if key in loose:
            if got - set(loose[key]):
                raise LabelsError(f'label {key} has a placeholder the tool does not fill in: {", ".join(sorted(got - set(loose[key])))}')
        elif got != want:
            raise LabelsError(f'label {key} must keep the placeholders {" ".join(sorted(want)) or "(none)"}; it has {" ".join(sorted(got)) or "(none)"}')


def resolve(lang, override, command, loose={}):
    """The complete set of labels for the language of the output.

    With the pack of the language (or English), the pack is the base and override changes single words.
    Without a pack, override has to hold every key; with neither, stop with the command that starts the file.
    """
    if lang and not re.fullmatch(r'[a-z]{2,3}(-[A-Za-z0-9]+)*', lang):
        raise LabelsError(f'{lang!r} is not a language code such as ja or pt-BR')
    if not lang or lang == 'en':
        base = english()
    elif (LANG_DIR / lang / 'labels.json').is_file():
        base = read(LANG_DIR / lang / 'labels.json')
    elif override is None:
        raise LabelsError(f'no labels for {lang}; run `{command} --init {lang} -o <file>`, translate the values, and pass the file with --labels')
    else:
        base = {}
    if override is not None:
        check(override, complete=not base, loose=loose)
    labels = {**base, **(override or {})}
    check(labels, complete=True, loose=loose)
    return labels
