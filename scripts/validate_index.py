"""Offline metadata validation. Error messages never echo untrusted field values."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / 'schemas/question-index.schema.json'

def validate_document(document, sources=None, allow_empty=False):
    schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
    errors = ['schema violation' for _ in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(document)]
    if not isinstance(document, dict) or not isinstance(document.get('questions'), list):
        return errors
    questions = document['questions']
    if not questions and not allow_empty:
        errors.append('empty dataset: pilot incomplete')
    ids, positions = set(), set()
    for q in questions:
        if not isinstance(q, dict):
            continue
        # Schema rejects extra properties at every structured level, including bodies.
        identifier = q.get('id')
        if isinstance(identifier, str):
            if identifier in ids: errors.append('duplicate id')
            ids.add(identifier)
        position = tuple(q.get(k) for k in ('exam_system', 'year', 'paper', 'question_number'))
        if all(isinstance(v, (str, int)) for v in position):
            if position in positions: errors.append('duplicate original exam position')
            positions.add(position)
        year, exam = q.get('year'), q.get('exam_system')
        if type(year) is int and ((exam == 'national-judicial-exam' and year >= 2018) or (exam == 'national-legal-qualification-exam' and year < 2018)):
            errors.append('exam system/year mismatch')
        grade = q.get('provenance_grade')
        try:
            host = urlparse(q.get('source_url') if isinstance(q.get('source_url'), str) else '').hostname
        except ValueError:
            host = None
            errors.append('invalid source URL')
        if sources is not None and grade == 'synthetic':
            errors.append('synthetic fixture cannot populate production pilot')
        if grade == 'official' and host != 'www.moj.gov.cn':
            errors.append('official provenance requires audited official source')
        if host == 'www.moj.gov.cn' and grade in ('recalled', 'third-party'):
            errors.append('official source mislabeled')
        if grade == 'official' and type(year) is int and year >= 2018:
            errors.append('post-reform official question requires separate review')
        rights = q.get('rights')
        if isinstance(rights, dict):
            for claim in rights.values():
                if isinstance(claim, dict) and claim.get('status') in ('verified', 'not-applicable'):
                    # Gate 1 has no reviewed grant ledger. A URL alone cannot authorize use.
                    errors.append('unsupported rights grant: independent review required')
        if sources is not None and grade != 'synthetic':
            source = next((s for s in sources if isinstance(s, dict) and s.get('id') == q.get('source_id')), None)
            if source is None:
                errors.append('missing source registry entry')
            elif source.get('verification') != 'verified-locator' or q.get('source_url') != source.get('url'):
                errors.append('source locator not verified')
    return errors

def validate_sources(registry):
    schema = json.loads((ROOT / 'schemas/source-index.schema.json').read_text(encoding='utf-8'))
    errors = ['source schema violation' for _ in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(registry)]
    if not isinstance(registry, dict) or not isinstance(registry.get('sources'), list): return errors
    seen = set()
    for source in registry['sources']:
        if not isinstance(source, dict): continue
        ident = source.get('id')
        if isinstance(ident, str):
            if ident in seen: errors.append('duplicate source id')
            seen.add(ident)
        claims = source.get('rights', {})
        if isinstance(claims, dict):
            for claim in claims.values():
                if isinstance(claim, dict) and claim.get('status') in ('verified', 'not-applicable'):
                    errors.append('source grant requires independent review')
        claim = source.get('indexing')
        if isinstance(claim, dict) and claim.get('status') == 'verified' and source.get('verification') != 'verified-locator':
            errors.append('indexing permission does not establish verified locator')
    return errors

def validate_public_tree(root):
    """Check disk and Git index paths; never read potentially restricted bodies."""
    root = Path(root)
    errors = []
    paths = {}
    for p in root.rglob('*'):
        relative = p.relative_to(root)
        # Only repository metadata is exempt, never checkout ancestors or work/.
        if relative.parts[0] == '.git':
            continue
        paths[relative] = p.is_file() or p.is_symlink()

    if (root / '.git').exists():
        try:
            result = subprocess.run(
                ['git', '-C', str(root), 'ls-files', '--cached', '-z'],
                check=True, capture_output=True,
            )
        except (OSError, subprocess.CalledProcessError):
            errors.append('cannot inspect Git index paths')
        else:
            # Include staged/tracked paths even if absent from the working tree.
            # NUL separation preserves filenames containing whitespace/newlines.
            for name in result.stdout.split(b'\0'):
                if name:
                    paths[Path(name.decode('utf-8', errors='surrogateescape'))] = True

    for relative, is_file in paths.items():
        parts = relative.parts
        if any(part.lower() in ('holdout', 'private', 'secrets') for part in parts):
            errors.append('forbidden private/holdout path')
        if is_file and relative.suffix.lower() in ('.pdf', '.zip', '.jsonl', '.csv', '.parquet'):
            errors.append('unapproved content file')
        if is_file and relative.suffix == '.json' and 'data' in parts and relative.as_posix() not in ('data/questions/index.json', 'data/sources/index.json'):
            errors.append('unregistered public data file')
    return errors

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', type=Path, default=ROOT / 'data/questions/index.json')
    parser.add_argument('--allow-empty', action='store_true', help='Structure-only diagnostic; never satisfies pilot')
    args = parser.parse_args(argv)
    try:
        document = json.loads(args.path.read_text(encoding='utf-8'))
        registry = json.loads((ROOT / 'data/sources/index.json').read_text(encoding='utf-8'))
        sources = registry['sources']
        if not isinstance(sources, list) or not sources: raise ValueError()
    except (OSError, UnicodeError, ValueError, KeyError, TypeError):
        print('INDEX_ERROR: unreadable or invalid JSON/registry', file=sys.stderr)
        return 1
    errors = validate_sources(registry) + validate_document(document, sources, args.allow_empty) + validate_public_tree(ROOT)
    for e in errors: print('INDEX_INVALID: ' + e, file=sys.stderr)
    if errors: return 1
    print(f"INDEX_VALID: {len(document['questions'])} metadata records; rights/legal review not established")
    if not document['questions']: print('PILOT_INCOMPLETE: 0/30; structure-only validation')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
