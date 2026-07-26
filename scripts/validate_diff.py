#!/usr/bin/env python3
"""
validate_diff.py — CIP-KGE Knowledge Diff validator (Stage 5, syntactic layer).

Validates one or more Knowledge Diff YAML files against the formal schema
at docs/KNOWLEDGE_DIFF_SCHEMA.yaml (JSON Schema draft-07 expressed in YAML).

Usage:
    python scripts/validate_diff.py diffs/diff-2026-06-29-001.yaml
    python scripts/validate_diff.py diffs/            # validates every *.yaml in the directory
    python scripts/validate_diff.py diffs/ examples/  # multiple paths allowed

Exit code: 0 if all files valid, 1 otherwise.

Scope note: this is SYNTACTIC validation only. It enforces structure, patterns,
enums, and conditional requirements (e.g., current_text required unless
operation = append). It does NOT resolve session_exchange_ref against real
transcripts, does NOT check that target.node_id exists in a graph, and does
NOT detect boilerplate confidence rationales. Those are semantic checks —
see "Additional constraints" in docs/KNOWLEDGE_DIFF_SCHEMA.yaml.
"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("ERROR: PyYAML not installed. Run: pip install pyyaml")
try:
    import jsonschema
except ImportError:
    sys.exit("ERROR: jsonschema not installed. Run: pip install jsonschema")

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "docs" / "KNOWLEDGE_DIFF_SCHEMA.yaml"


def collect_files(paths):
    files = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            # rglob: recursive — diffs may live one or more levels deep
            # (e.g., examples/diff-001-embodied-foundation/diff.yaml)
            found = sorted(set(p.rglob("*.yaml")) | set(p.rglob("*.yml")))
            if not found:
                print(f"WARNING: directory matched no YAML files: {raw}")
            else:
                print(f"{raw}: {len(found)} file(s) found")
            files.extend(found)
        elif p.is_file():
            files.append(p)
        else:
            print(f"WARNING: path not found, skipped: {raw}")
    return files


def validate_file(path, schema, validator_cls):
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        return [f"YAML parse error: {e}"]
    if not isinstance(doc, dict):
        return ["Document root is not a mapping (legacy 'knowledge_diff:' wrapper? Remove it — v0.3 validates the root object directly)."]
    validator = validator_cls(schema)
    return [
        f"{'/'.join(str(p) for p in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path))
    ]


def main(argv):
    if not SCHEMA_PATH.exists():
        sys.exit(f"ERROR: schema not found at {SCHEMA_PATH}")
    schema = yaml.safe_load(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)

    files = collect_files(argv[1:] or ["diffs/"])
    if not files:
        sys.exit("ERROR: no diff files found.")

    failed = 0
    for f in files:
        errors = validate_file(f, schema, validator_cls)
        if errors:
            failed += 1
            print(f"❌ {f}")
            for e in errors:
                print(f"     {e}")
        else:
            print(f"✅ {f}")

    print(f"\n{len(files) - failed}/{len(files)} diffs valid against {SCHEMA_PATH.relative_to(REPO_ROOT)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
