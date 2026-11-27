#!/usr/bin/env python3
"""Collect the diffs of named comparison targets and embed them in one HTML page that opens in a browser."""
import argparse
import ast
import datetime
import difflib
import html
import importlib.util
import json
import os
import re
import shutil
from pathlib import Path
import subprocess
import sys
import urllib.request

sys.dont_write_bytecode = True
import labels as labels_module  # noqa: E402

SCHEMA_VERSION = 2
INITIAL_SCOPES = ('diff', 'full', 'after')
UTFPACK_PACKER_URL = 'https://cdn.jsdelivr.net/npm/utfpack@0/python/utfpack_pack.py'
# Set by load_packer(): the packer module, its version and the URL of the decoder module that matches it.
utfpack_pack = None
UTFPACK_VERSION = None
UTFPACK_MODULE_URL = None
# The libraries the page imports: module specifier -> URL. A plain HTML file reaches them through an import map,
# and an artifact through the full URL in each import statement, so both forms come from this one table.
CDN = 'https://cdn.jsdelivr.net/npm/'
LIBRARIES = {
    'vue': CDN + 'vue@3/dist/vue.esm-bundler.js/+esm',
    '@lucide/vue': CDN + '@lucide/vue/+esm',
    'highlight.js/core': CDN + 'highlight.js@11/es/core.js/+esm',
    **{f'highlight.js/languages/{name}': CDN + f'highlight.js@11/es/languages/{name}.js/+esm'
       for name in ('javascript', 'typescript', 'python', 'bash', 'yaml', 'xml', 'css', 'json', 'sql')},
}
# Dates offer more words than a language needs, so these labels may leave some out.
LOOSE_LABELS = {'dayFormat': {'{y}', '{m}', '{d}', '{mm}', '{dd}', '{w}'}, 'monthDay': {'{m}', '{d}', '{mm}', '{dd}'}}
UNREADABLE = 'Bytes that are not valid UTF-8 are shown as \\xNN.'
NOTICE_BINARY = 'This is a binary file.'
NOTICE_NO_DIFF = 'There is no difference in content.'
NOTICE_SUBMODULE = 'For a submodule, the diff of the referenced commit is shown.'
NOTICE_NO_FULL = 'The full text cannot be restored from a diff file, so it is not included.'
DEFAULT_TITLE = 'Diff review'


def cache_root():
    if os.name == 'nt':
        base = os.environ.get('LOCALAPPDATA') or str(Path.home() / 'AppData' / 'Local')
    else:
        base = os.environ.get('XDG_CACHE_HOME') or str(Path.home() / '.cache')
    return Path(base) / 'wakariyasu' / 'utfpack'


def version_key(name):
    return tuple(int(part) if part.isdigit() else 0 for part in re.split(r'[.\-]', name))


def import_packer(path):
    spec = importlib.util.spec_from_file_location('utfpack_pack', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_packer():
    """Load utfpack's Python packer: download the newest 0.x from jsDelivr into the user cache, or use the newest cached one."""
    global utfpack_pack, UTFPACK_VERSION, UTFPACK_MODULE_URL
    if utfpack_pack is not None:
        return utfpack_pack
    root = cache_root()
    path = None
    try:
        with urllib.request.urlopen(UTFPACK_PACKER_URL, timeout=20) as response:
            source = response.read()
            version = response.headers.get('x-jsd-version')
        if not version:
            match = re.search(rb'^VERSION = "([^"]+)"', source, re.M)
            version = match.group(1).decode() if match else None
        if version and re.fullmatch(r'[0-9A-Za-z.\-]+', version):
            path = root / version / 'utfpack_pack.py'
            if not path.exists() or path.read_bytes() != source:
                path.parent.mkdir(parents=True, exist_ok=True)
                temporary = path.with_name(f'.{os.getpid()}.tmp')
                temporary.write_bytes(source)
                os.replace(temporary, path)
    except (OSError, ValueError):
        path = None
    if path is None:
        cached = sorted((p for p in root.glob('*/utfpack_pack.py') if p.is_file()), key=lambda p: version_key(p.parent.name), reverse=True) if root.is_dir() else []
        if not cached:
            sys.stderr.write('error: the utfpack packer could not be downloaded from jsDelivr\n')
            sys.exit(2)
        path = cached[0]
    utfpack_pack = import_packer(path)
    UTFPACK_VERSION = utfpack_pack.VERSION
    UTFPACK_MODULE_URL = f'{CDN}utfpack@{UTFPACK_VERSION}/dist/cdn/utfpack.mjs'
    return utfpack_pack


def git(path, *args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_NO_REPLACE_OBJECTS='1')
    return subprocess.run(
        ['git', '--no-pager', '--literal-pathspecs', '-c', 'core.quotepath=false', '-c',
         'diff.external=', '-c', 'log.showSignature=false', '-c', 'diff.suppressBlankEmpty=false', *args], cwd=path, env=env, check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout


def decode(value):
    # Keep unreadable bytes as \xNN so that different bytes never look like the same character.
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
    """The diff that puts the whole file in one hunk, for when one side is empty or both sides are the same."""
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
    """The diff from the first @@. If context is None, include the full text.

    git_diff is a function that takes the number of surrounding lines and returns git's diff. If it is missing, build the diff with difflib (slow for large files).
    """
    a, b = decode(before), decode(after)
    if before == after or not before or not after:
        return '' if before == after and context is not None else whole_file(a, b)
    if git_diff:
        return body_of(decode(git_diff(max(a.count('\n'), b.count('\n')) + 1 if context is None else context)))
    return difflib_body(a, b, context)


def no_index_diff(left, right):
    """Return a function that compares two files with git diff --no-index, or None if git is missing."""
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
    """From git's diff, return the body for one file and, if it has bytes that are not valid UTF-8, a notice."""
    first = next(patches, None)
    if first is None:
        raise ValueError('The number of diffs from git does not match the number of file states')
    raws = [first]
    if status[0] == 'T' and re.search(rb'(?m)^deleted file mode ', first):
        second = next(patches, None)
        if second is None or not re.search(rb'(?m)^new file mode ', second):
            raise ValueError('A file type change has no matching extra diff')
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
    # --raw carries the blob IDs and modes so the content can be read without handing the name back to git.
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
            raise ValueError(f'A file in git\'s diff has no line counts: {filename}')
        submodule = '160000' in (old_mode, new_mode)
        blobs = lambda: (b'' if status[0] == 'A' else git(root, 'cat-file', 'blob', old_id),
                         b'' if status[0] == 'D' else git(root, 'cat-file', 'blob', new_id))
        # .gitattributes does not apply to a diff between blobs. Use --text only after checking that the content has no NUL.
        blob_diff = lambda context: git(root, 'diff', '--no-color', '--no-ext-diff', '--no-textconv', '--text',
                                        f'-U{context}', old_id, new_id)
        binary = stats[0] == b'-'
        added, deleted = (None, None) if binary else (int(stats[0]), int(stats[1]))
        if binary and not submodule:
            # For a text file marked -diff or binary in .gitattributes, git also reports the line counts as -. Check the content.
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
            entry['notice'] = notices(unreadable_notice, NOTICE_BINARY if binary else
                                      NOTICE_NO_DIFF)
        if include_full:
            if binary:
                entry['full_body'] = None
            elif submodule:
                entry['full_body'] = None
                entry['notice'] = notices(unreadable_notice, NOTICE_SUBMODULE)
            else:
                before, after = blobs()
                entry['full_body'] = text_body(before, after, None, blob_diff)
                entry['notice'] = notices(entry['notice'], unreadable(before, after))
        files.append(entry)
    if next(patches, None) is not None:
        raise ValueError('The number of diffs from git does not match the number of file states')
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
    # The git modes (100644 and so on). The side that does not exist (before an addition, after a deletion) is None.
    absent = lambda mode: None if not mode or set(mode) == {'0'} else mode
    return dict(old_mode=absent(old_mode), new_mode=absent(new_mode))


def text_entry(path, before, after, include_full, old, status, git_diff=None, modes=(None, None)):
    binary = b'\0' in before or b'\0' in after
    entry = dict(path=path, old=old, status=status, binary=binary, added=None, deleted=None, body='',
                 notice=NOTICE_BINARY if binary else unreadable(before, after), **file_modes(*modes))
    if not binary:
        entry['body'] = text_body(before, after, 3, git_diff)
        if not entry['body']:
            entry['notice'] = notices(entry['notice'], NOTICE_NO_DIFF)
        rows = entry['body'].split('\n')
        entry['added'] = sum(row.startswith('+') for row in rows)
        entry['deleted'] = sum(row.startswith('-') for row in rows)
    if include_full:
        entry['full_body'] = None if binary else text_body(before, after, None, git_diff)
    return entry


def plain_paths(location):
    root = Path(location).expanduser().absolute()
    if root.is_symlink():
        raise ValueError('A symbolic link cannot be given as a comparison source or destination')
    if root.is_file():
        return {'': root}
    if not root.is_dir():
        raise ValueError(f'No such file or directory: {location}')
    paths = {}
    for p in root.rglob('*'):
        if '.git' in p.relative_to(root).parts:
            continue
        # Do not follow symbolic links; like git, compare the link target path as the content.
        if p.is_symlink() or p.is_file():
            paths[p.relative_to(root).as_posix()] = p
    return paths


def plain_mode(path):
    # Like git, tell apart three kinds: a link, an executable file and a regular file.
    if path.is_symlink():
        return '120000'
    return '100755' if path.stat().st_mode & 0o100 else '100644'


def read_plain(path):
    return os.fsencode(os.readlink(path)) if path.is_symlink() else path.read_bytes()


def collect_plain(name, before, after, include_full):
    left, right = plain_paths(before), plain_paths(after)
    if ('' in left) != ('' in right):
        raise ValueError('Give two files or two directories as the comparison source and destination')
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
    return dict(name=name, kind='plain', base_ref='before', target_ref='after',
                base='', target='', commits=[], files=files)


def collect_files(name, locations):
    """Show whole files or folders without comparing: each file is an addition with its full text."""
    given = [Path(location).expanduser().absolute() for location in locations]
    files = {}
    for root in given:
        # Folders keep their relative paths (prefixed with the folder name when several are given); a file keeps its name.
        for path, source in sorted(plain_paths(root).items()):
            shown = path or root.name
            if path and len(given) > 1:
                shown = f'{root.name}/{path}'
            if shown in files:
                raise ValueError(f'The path appears twice in the files target: {shown}')
            files[shown] = source
    entries = [text_entry(path, b'', read_plain(source), True, None, 'A', None, (None, plain_mode(source)))
               for path, source in files.items()]
    for entry in entries:
        # Nothing is compared, so an empty file has no "no difference" to report.
        entry['notice'] = notices(*(part.strip() for part in entry['notice'].split(NOTICE_NO_DIFF)))
    return dict(name=name, kind='files', base_ref='', target_ref='', base='', target='', commits=[], files=entries)


def collect_patch(name, location, include_full):
    # Hunk lengths disambiguate --- / +++ content from subsequent file headers.
    raw = Path(location).read_bytes().removeprefix(b'\xef\xbb\xbf')
    if raw.count(b'\n') and raw.count(b'\r\n') == raw.count(b'\n'):
        # Strip the CR only when the whole diff file was converted to CRLF. A CR inside a line is part of the diff, so keep it.
        raw = raw.replace(b'\r\n', b'\n')
    raw_lines = raw.split(b'\n')
    lines = [decode(line) for line in raw_lines]
    files = []; i = 0; pending = {}; oldleft = newleft = 0
    # Whether to strip a prefix such as a/ and b/ of a git diff. None is a diff without diff --git lines (diff -u and so on).
    strip = None
    def unquote(value):
        if value.startswith('"'):
            try:
                return decode(ast.literal_eval('b' + value.encode('utf-8').decode('ascii', errors='backslashreplace')))
            except (ValueError, SyntaxError):
                raise ValueError('The quoting of a path in the diff is invalid')
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
            # In a diff -ru diff, the names of the two compared folders come first in each path.
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
                raise ValueError('Cannot read the path from a file header of the git diff')
            return
        binary = pending.get('binary', False)
        old = pending.get('old', pending['path'])
        files.append(dict(path=pending['path'], old=old if old != pending['path'] else None,
            status=pending.get('status', 'M'), binary=binary,
            added=None if binary else 0, deleted=None if binary else 0, body='',
            notice=NOTICE_BINARY if binary else NOTICE_NO_DIFF,
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
                # A --no-prefix diff. In a diff with prefixes, the first characters of the two paths differ.
                strip = False
                pending = dict(old=unquote(header[:half]), path=unquote(header[:half]))
            elif match:
                strip = True
                pending = dict(zip(('old', 'path'), names(match[1], match[2])))
            else:
                # A rename written with --no-prefix. Read the paths from the rename, --- and +++ lines.
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
                # A diff -ru diff writes a binary file as this one line, without a diff --git line.
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
            # Only a git-style diff reads a difference in names as a move. A diff -u diff between two files with different names is M, as with --dirs.
            gitlike = strip or (strip is None and line[4:6] == 'a/' and lines[i+1][4:6] == 'b/')
            old, new = names(line[4:], lines[i+1][4:])
            status = pending.get('status', 'A' if old == '/dev/null' else 'D' if new == '/dev/null' else 'R' if old != new and gitlike else 'M')
            body = []; i += 2; first_row = i
            while i < len(lines):
                row = lines[i]
                hunk = re.match(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', row)
                if hunk:
                    if oldleft or newleft:
                        raise ValueError('The number of diff lines does not match the hunk header')
                    oldleft, newleft = int(hunk[2] or 1), int(hunk[4] or 1)
                elif row.startswith('\\'):
                    pass
                elif oldleft or newleft:
                    # After an editor or tool that trims trailing whitespace, an empty context line loses its leading space.
                    if row == '' and oldleft and newleft: row = ' '
                    if row.startswith(' '): oldleft -= 1; newleft -= 1
                    elif row.startswith('-'): oldleft -= 1
                    elif row.startswith('+'): newleft -= 1
                    else: raise ValueError('The number of diff lines does not match the hunk header')
                    if oldleft < 0 or newleft < 0: raise ValueError('The number of diff lines is invalid')
                else:
                    break
                body.append(row); i += 1
            if oldleft or newleft: raise ValueError('A hunk of the diff ends too early')
            files.append(dict(path=old if new == '/dev/null' else new,
                old=old if old != new and old != '/dev/null' else None, status=status,
                binary=False, added=sum(x.startswith('+') for x in body),
                deleted=sum(x.startswith('-') for x in body), body='\n'.join(body),
                notice=notices(unreadable(*raw_lines[first_row - 2:i]),
                               NOTICE_NO_FULL if include_full else ''),
                **file_modes(pending.get('old_mode'), pending.get('new_mode')),
                **({'full_body': None} if include_full else {})))
            pending = {}
            continue
        i += 1
    flush_pending()
    if not files:
        raise ValueError('No file header of a unified diff was found')
    return dict(name=name, kind='patch', base_ref='before', target_ref='after',
                base='', target='', commits=[], files=files)


def validate(data):
    """Check the data, including the words in data["labels"]."""
    if not isinstance(data, dict) or data.get('schema_version') != SCHEMA_VERSION:
        raise ValueError(f'schema_version of the JSON must be {SCHEMA_VERSION}')
    for key in ('title', 'data_version', 'generated_at'):
        if not isinstance(data.get(key), str):
            raise ValueError(f'{key} must be a string')
    if type(data.get('group_depth')) is not int or data['group_depth'] < 0:
        raise ValueError('group_depth must be an integer of 0 or more')
    if type(data.get('full_text')) is not bool or not isinstance(data.get('sources'), list):
        raise ValueError('full_text must be true or false, and sources must be an array')
    if data.get('initial_scope') not in INITIAL_SCOPES:
        raise ValueError('initial_scope must be diff, full or after')
    if data['initial_scope'] != 'diff' and not data['full_text']:
        raise ValueError('initial_scope full or after needs full_text to be true')
    if data.get('lang') is not None and not isinstance(data['lang'], str):
        raise ValueError('lang must be a string')
    given = data.get('labels', {})
    if not isinstance(given, dict):
        raise ValueError('labels must be an object')
    for key, value in given.items():
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f'labels.{key} must be a non-empty string')
    labels_module.check(given, complete=False, loose=LOOSE_LABELS)
    names = set()
    for repo in data['sources']:
        if not isinstance(repo, dict):
            raise ValueError('source must be an object')
        if repo.get('kind', 'git') not in ('git', 'plain', 'patch', 'files'):
            raise ValueError('source.kind must be git, plain, patch or files')
        for key in ('name', 'base_ref', 'target_ref', 'base', 'target'):
            if not isinstance(repo.get(key), str):
                raise ValueError(f'source.{key} must be a string')
        if repo['name'] in names:
            raise ValueError('Target names must not repeat')
        names.add(repo['name'])
        if not isinstance(repo.get('commits'), list) or not all(isinstance(c, list) and len(c) == 3 and all(isinstance(s, str) for s in c) for c in repo['commits']):
            raise ValueError('commits must be an array of [hash, ISO date, subject]')
        if not isinstance(repo.get('files'), list):
            raise ValueError('files must be an array')
        for file in repo['files']:
            if not isinstance(file, dict):
                raise ValueError('file must be an object')
            for key in ('path', 'status', 'body', 'notice'):
                if not isinstance(file.get(key), str):
                    raise ValueError(f'file.{key} must be a string')
            if file['status'][:1] not in ('A', 'D', 'M', 'R', 'C', 'T', 'U', 'X', 'B'):
                raise ValueError('The file status is invalid')
            if file.get('old') is not None and not isinstance(file['old'], str):
                raise ValueError('file.old must be a string or null')
            for key in ('old_mode', 'new_mode'):
                if file.get(key) is not None and not (isinstance(file[key], str) and re.fullmatch(r'[0-7]{6}', file[key])):
                    raise ValueError(f'file.{key} must be a string of 6 octal digits, or null')
            if type(file.get('binary')) is not bool:
                raise ValueError('file.binary must be true or false')
            for key in ('added', 'deleted'):
                if file.get(key) is not None and (type(file[key]) is not int or file[key] < 0):
                    raise ValueError(f'file.{key} must be an integer of 0 or more, or null')
            if data['full_text'] and 'full_body' not in file:
                raise ValueError('full_body is required when full_text is true')
            if file.get('full_body') is not None and not isinstance(file['full_body'], str):
                raise ValueError('full_body must be a string or null')
    return data


def module_integrity():
    """The integrity value of the decoder module from the same version's sri.json, or None when it cannot be fetched."""
    try:
        with urllib.request.urlopen(f'{CDN}utfpack@{UTFPACK_VERSION}/dist/cdn/sri.json', timeout=10) as response:
            value = json.loads(response.read().decode('utf-8')).get('utfpack.mjs')
        return value if isinstance(value, str) and re.fullmatch(r'sha384-[A-Za-z0-9+/=]+', value) else None
    except (OSError, ValueError):
        return None


def make_html(data, template, artifact=False, embed_decoder=False):
    data = validate(data)
    load_packer()
    payload = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    # The text that closes a script or opens a comment cannot go into the page; pack again in a plainer format.
    for options in ({}, {'ascii': True}, {'format': 'base64'}):
        packed = utfpack_pack.pack({'data.json': payload}, emit='html', embed_decoder=embed_decoder, **options)
        if '</script' not in packed['string'] and '<!--' not in packed['string']:
            break
    else:
        raise ValueError('The packed data contains "</script" or "<!--" in every format, so it cannot be put in an HTML page safely')
    markers = ('<!--__PACKED__-->', '<!--__IMPORTMAP__-->', '<!--__BODY__-->', '__LANG__', '/*__UNPACK__*/', '/*__LABELS__*/{}/*__LABELS_END__*/', '/*__LOAD_WORDS__*/{}/*__LOAD_WORDS_END__*/')
    for marker in markers:
        if template.count(marker) != 1:
            raise ValueError(f'The template must contain {marker} exactly once')
    safe = lambda value: json.dumps(value, ensure_ascii=False).replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    english = labels_module.english()
    # The words for the loading and error messages stay outside the packed data, in the page's language, so they show when the data cannot be opened.
    words = {key: (data.get('labels') or {}).get(key, english[key]) for key in ('loadingData', 'dataLoadError')}
    # The data is a JSON string that the page's module reads and unpacks. With --embed-decoder the decoder is a classic
    # inline script that defines the global `utfpack`; otherwise the module imports the decoder module.
    # The packed string is plain text, not JSON: it goes into a script element that the browser does not run, as is.
    data_script = f'<script type="text/plain" id="packed">{packed["string"]}</script>\n'
    if embed_decoder:
        data_script = f'<script>{utfpack_pack.decoder_script(packed["entry"])}</script>\n' + data_script
    libraries = dict(LIBRARIES)
    if embed_decoder:
        unpack = 'const { unpack } = globalThis.utfpack'
    elif artifact:
        unpack = f"import {{ unpack }} from '{UTFPACK_MODULE_URL}'"
    else:
        libraries['utfpack'] = UTFPACK_MODULE_URL
        unpack = "import { unpack } from 'utfpack'"
    # Replace in the template first and put the data in last, so no replacement can touch the data.
    template = assemble(template, data.get('lang') or 'en', artifact, libraries, module_integrity() if 'utfpack' in libraries else None)
    page = (template.replace('/*__UNPACK__*/', unpack)
                    .replace('/*__LABELS__*/{}/*__LABELS_END__*/', safe(english))
                    .replace('/*__LOAD_WORDS__*/{}/*__LOAD_WORDS_END__*/', safe(words))
                    .replace('__TITLE__', html.escape(data['title'])))
    before, after = page.split('<!--__PACKED__-->')
    return before + data_script + after


def assemble(template, lang, artifact, libraries, integrity=None):
    """Put the template's parts into the shape of the destination.

    The template holds the head parts (title, import map marker, packed data marker, styles), the marker
    <!--__BODY__-->, and the body parts (#app, loading message, module script). A destination that wraps pages in
    its own document skeleton gets the parts alone, starting with the title, and no import map (an import map cannot
    sit in a body), so each import statement of the module names its full URL. A plain HTML file gets a complete
    document whose head carries the import map.
    """
    head, body = template.split('<!--__BODY__-->')
    body = body.replace('__LANG__', html.escape(lang, quote=True)).lstrip('\n')
    if artifact:
        for name, url in libraries.items():
            body = body.replace(f"from '{name}'", f"from '{url}'")
        return head.replace('<!--__IMPORTMAP__-->\n', '') + body
    imports = {'imports': libraries}
    if integrity:
        imports['integrity'] = {libraries['utfpack']: integrity}
    import_map = '<script type="importmap">\n' + json.dumps(imports, indent=2) + '\n</script>\n'
    return ('<!DOCTYPE html>\n' + f'<html lang="{html.escape(lang, quote=True)}">\n<head>\n'
            '<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            + head.replace('<!--__IMPORTMAP__-->\n', import_map) + '</head>\n<body>\n' + body + '</body>\n</html>\n')


def repository_paths(location):
    root = Path(decode(git(Path(location).expanduser().resolve(), 'rev-parse', '--show-toplevel')).strip()).resolve()
    # rev-parse can return a relative path, so resolve it from the top of the repository.
    return [root, *((root / decode(git(root, 'rev-parse', option)).strip()).resolve()
                    for option in ('--git-dir', '--git-common-dir'))]


def check_output(filename, protected_paths=(), *, data_only=False):
    if filename == '-':
        return
    destination = Path(filename).expanduser().resolve()
    for protected in protected_paths:
        if destination.is_relative_to(Path(protected).expanduser().resolve()):
            raise ValueError(f'Cannot write the output inside a compared target: {filename}')
    if data_only:
        # The JSON does not store repository locations, so a rebuild cannot know which repositories were compared.
        # Even under git, allow output to an ignored place (such as a work folder) and stop only output to a managed place.
        for parent in (destination.parent, *destination.parent.parents):
            if parent.name == '.git' or ((parent / 'HEAD').is_file() and (parent / 'objects').is_dir()
                                         and (parent / 'refs').is_dir()):
                raise ValueError(f'The output of --data cannot be inside git\'s own folder: {filename}')
        base = next((d for d in (destination.parent, *destination.parent.parents) if d.is_dir()), None)
        # Where git is not installed there is no way to tell whether a place is managed, and nothing is committed, so do not check.
        inside = base is not None and shutil.which('git') is not None and subprocess.run(['git', '-C', str(base), 'rev-parse', '--show-toplevel'],
                                                     capture_output=True).returncode == 0
        if inside and subprocess.run(['git', '-C', str(base), 'check-ignore', '-q', '--no-index', str(destination)],
                                     capture_output=True).returncode != 0:
            raise ValueError(f'The output of --data must be in a place git does not manage (outside a repository, or an ignored place): {filename}')


def write(filename, content):
    if filename == '-':
        sys.stdout.write(content)
    else:
        Path(filename).expanduser().write_text(content, encoding='utf-8')


def apply_language(data, lang, override):
    """Record the page language and its words (--data keeps the JSON's own when neither is given).

    The words are the pack of the language (or English) with the words of --labels over them; for a
    language without a pack, --labels holds every word. English words are not stored.
    """
    if lang is None and override is None:
        return
    if lang is not None:
        data['lang'] = lang
    labels = labels_module.resolve(lang if lang is not None else data.get('lang'), override, 'build.py', LOOSE_LABELS)
    if labels == labels_module.english():
        data.pop('labels', None)
    else:
        data['labels'] = labels


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, add_help=False)
    parser._optionals.title = 'options'
    parser.add_argument('-h', '--help', action='help', help='show this help and exit')
    parser.add_argument('--repo', nargs=4, action='append', default=[], metavar=('NAME', 'PATH', 'BASE', 'TARGET'), help='a target of two git commits: name, path, base and target (can be repeated)')
    parser.add_argument('--dirs', nargs=3, action='append', default=[], metavar=('NAME', 'BEFORE', 'AFTER'), help='a target of two ordinary folders or two files (can be repeated)')
    parser.add_argument('--diff', nargs=2, action='append', default=[], metavar=('NAME', 'FILE'), help='a target of an existing unified diff (can be repeated)')
    parser.add_argument('--files', nargs='+', action='append', default=[], metavar=('NAME', 'PATH'), help='a target that shows whole files or folders without comparing: a name, then one or more paths (can be repeated); the page opens on the text after the change')
    parser.add_argument('--merge-base', action='append', default=[], metavar='NAME', help='compare the --repo target of this name from the divergence point of BASE and TARGET')
    parser.add_argument('--data', metavar='JSON', help='build from a JSON written earlier; - reads standard input')
    parser.add_argument('--title', metavar='TITLE', help='the page title (default: "Diff review", or the defaultTitle label)')
    parser.add_argument('--data-version', metavar='VERSION', help='the data version, any string; required when collecting new data; --data keeps the JSON\'s value')
    parser.add_argument('--group-depth', type=int, default=None, metavar='N', help='the directory depth for grouping the file list (default 2; 0 means no grouping)')
    parser.add_argument('--full-text', action='store_true', help='also include the full text of changed files')
    parser.add_argument('--lang', metavar='CODE', help='the language of the page being produced, such as ja; the words come from lang/CODE/labels.json of this skill, and --labels changes single words')
    parser.add_argument('--labels', metavar='JSON', help='a JSON file of the page words: every word for a language that has no lang/CODE/labels.json, or single words that replace the pack\'s (start the file with --init CODE -o FILE)')
    parser.add_argument('--init', metavar='CODE', help='write the English words to translate for this language to the -o file, then stop')
    parser.add_argument('--template', type=Path, default=Path(__file__).with_name('template.html'), metavar='PATH', help='the HTML template')
    parser.add_argument('--json-out', metavar='PATH', help='write the diff data as JSON; - writes to standard output')
    parser.add_argument('--artifact', action='store_true', help='write the HTML without the DOCTYPE, html, head and body tags (for destinations that add a document skeleton)')
    parser.add_argument('--embed-decoder', action='store_true', help='put the decoder into the page instead of loading it from the CDN')
    parser.add_argument('-o', '--output', metavar='PATH', help='the HTML output path; - writes to standard output')
    args = parser.parse_args(argv)
    if args.init:
        if not args.output or args.output == '-':
            parser.error('--init needs -o FILE')
        try:
            Path(args.output).expanduser().write_text(labels_module.init_text(), encoding='utf-8')
        except OSError as exc:
            parser.exit(2, f'error: {exc}\n')
        return 0
    try:
        protected_paths = []
        template = args.template.read_text(encoding='utf-8')
        override = labels_module.read(args.labels) if args.labels else None
        words = labels_module.resolve(args.lang, override, 'build.py', LOOSE_LABELS) if args.lang is not None or override is not None else labels_module.english()
        if not args.output and not args.json_out:
            raise ValueError('give --output or --json-out')
        if args.output == '-' and args.json_out == '-':
            raise ValueError('only one output can be standard output')
        if args.output and args.json_out and args.output != '-' and args.json_out != '-' and Path(args.output).resolve() == Path(args.json_out).resolve():
            raise ValueError('give different paths for the HTML and the JSON')
        if args.data:
            if args.repo or args.dirs or args.diff or args.files or args.merge_base or args.full_text:
                raise ValueError('--data cannot be combined with the options that collect diffs')
            data = validate(json.loads(sys.stdin.read() if args.data == '-' else Path(args.data).read_text(encoding='utf-8')))
            data['generated_at'] = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
            apply_language(data, args.lang, override)
            for key, value in [('title', args.title), ('data_version', args.data_version), ('group_depth', args.group_depth)]:
                if value is not None:
                    data[key] = value
        else:
            if any(len(item) < 2 for item in args.files):
                raise ValueError('--files needs a name and at least one path')
            names = [r[0] for r in [*args.repo, *args.dirs, *args.diff, *args.files]]
            if args.data_version is None:
                raise ValueError('give --data-version')
            if not names or len(set(names)) != len(names):
                raise ValueError('give at least one target, each with a different name')
            if set(args.merge_base) - {r[0] for r in args.repo}:
                raise ValueError('the name given to --merge-base must be the name of a --repo target')
            protected_paths = [path for _, location, _, _ in args.repo for path in repository_paths(location)]
            protected_paths += [Path(location).expanduser().resolve() for _, a, b in args.dirs for location in (a, b)]
            protected_paths += [Path(location).expanduser().resolve() for _, location in args.diff]
            protected_paths += [Path(location).expanduser().resolve() for item in args.files for location in item[1:]]
            # A page of whole files has no diff to show, so its text must be in the data and it opens on the text after the change.
            full_text = args.full_text or bool(args.files)
            only_files = bool(args.files) and not (args.repo or args.dirs or args.diff)
            now = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
            data = dict(schema_version=SCHEMA_VERSION, title=args.title or words.get('defaultTitle') or DEFAULT_TITLE,
                        generated_at=now, data_version=args.data_version,
                        group_depth=2 if args.group_depth is None else args.group_depth,
                        full_text=full_text, initial_scope='after' if only_files else 'diff', sources=[
                            *[collect(*repo, repo[0] in args.merge_base, full_text) for repo in args.repo],
                            *[collect_plain(*item, full_text) for item in args.dirs],
                            *[collect_patch(*item, full_text) for item in args.diff],
                            *[collect_files(item[0], item[1:]) for item in args.files]])
            apply_language(data, args.lang, override)
        validate(data)
        for output in (args.output, args.json_out):
            if output:
                check_output(output, protected_paths, data_only=bool(args.data))
        page = make_html(data, template, args.artifact, args.embed_decoder) if args.output else None
        if args.json_out:
            write(args.json_out, json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        if args.output:
            write(args.output, page)
        return 0
    except (ValueError, OSError, RecursionError, subprocess.CalledProcessError) as exc:
        message = str(exc)
        if isinstance(exc, subprocess.CalledProcessError):
            message = decode(exc.stderr).strip() or f'{" ".join(map(str, exc.cmd[-3:]))} failed with exit code {exc.returncode}'
        parser.exit(2, f'error: {message}\n')


if __name__ == '__main__':
    sys.exit(main())
