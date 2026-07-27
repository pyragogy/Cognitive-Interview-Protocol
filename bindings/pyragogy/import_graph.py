#!/usr/bin/env python3
"""
import_graph.py — Pyragogy binding, Stage 1: Quartz contentIndex.json → CIP-KGE baseline.

Reads the machine-readable graph of https://syllabus.pyragogy.org
(Quartz emitter output: static/contentIndex.json) and produces the
"current state" descriptors the protocol operates against:

  baseline/nodes/<slug>.yaml   one file per node: sections + hashes + relations
  baseline/graph_index.yaml    adjacency index + global baseline hash

Scope note (read before misusing this):
  These files are BASELINE DESCRIPTORS, not Knowledge Diffs — a diff is a
  *proposal* validated against docs/KNOWLEDGE_DIFF_SCHEMA.yaml; a baseline is
  the *state* that a diff's `target.node_id` and `section_changes[].current_text`
  refer to. Conformance to the schema lives in the diff; conformance of the
  baseline to reality lives in the hashes (sha256 of each section's text and
  of the full node content). If the site changes, re-run this script and the
  baseline_hash changes — that is the version tracking.

Usage:
  python bindings/pyragogy/import_graph.py /path/to/contentIndex.json
  python bindings/pyragogy/import_graph.py --url https://syllabus.pyragogy.org/static/contentIndex.json
  python bindings/pyragogy/import_graph.py contentIndex.json -o bindings/pyragogy/baseline
"""

import argparse
import datetime
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

import yaml

# Canonical section order of the Pyragogy binding (docs/SYLLABUS_SCHEMA.md).
# Node content in contentIndex.json is plain text with numbered headers:
# "1. Definition", "2. Use Case", ... — the NUMBER is authoritative.
SECTION_MAP = {
    "1": "definition",
    "2": "use_case",
    "3": "human_role",
    "4": "ai_role",
    "5": "friction",
    "6": "risk",
    "7": "observable_markers",
}
HEADER_RE = re.compile(
    r"^\s*([1-7])\.\s+"
    r"(Definition|Use\s*Case|Human\s*Role|AI\s*Role|Friction|Risk|Observable\s*Markers)"
    r"\s*:?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

IMPORTER_ID = "bindings/pyragogy/import_graph.py"


def sha256_text(s: str) -> str:
    return "sha256:" + hashlib.sha256(s.encode("utf-8")).hexdigest()


def parse_sections(content: str):
    """Split node content into the seven binding sections. Returns None if the
    node does not follow the numbered-section structure (e.g., meta pages)."""
    matches = list(HEADER_RE.finditer(content))
    if not matches:
        return None
    sections = {}
    for i, m in enumerate(matches):
        name = SECTION_MAP[m.group(1)]
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        sections[name] = content[start:end].strip()
    return sections


def load_index(source: str) -> tuple[dict, str]:
    """Load contentIndex.json from a local path or URL. Returns (data, origin)."""
    if source.startswith(("http://", "https://")):
        req = urllib.request.Request(source, headers={"User-Agent": "cip-kge-import/0.1"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8")), source
    p = Path(source)
    return json.loads(p.read_text(encoding="utf-8")), str(p.resolve())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="Path to contentIndex.json, or --url <URL>")
    ap.add_argument("-o", "--out", default="bindings/pyragogy/baseline", help="Output directory")
    args = ap.parse_args()

    index, origin = load_index(args.source)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    out_dir = Path(args.out)
    nodes_dir = out_dir / "nodes"
    nodes_dir.mkdir(parents=True, exist_ok=True)

    # Pass 1: inbound relation map
    inbound = {slug: [] for slug in index}
    for slug, node in index.items():
        for target in node.get("links", []):
            if target in inbound:
                inbound[target].append(slug)

    # Pass 2: per-node descriptors
    index_entries = []
    n_sectioned = 0
    for slug in sorted(index):
        node = index[slug]
        content = node.get("content", "") or ""
        sections = parse_sections(content)
        sectioned = sections is not None
        n_sectioned += sectioned

        descriptor = {
            "node_id": slug,  # opaque id used by diffs: target.node_id
            "title": node.get("title", slug),
            "source": {
                "type": "quartz_content_index",
                "origin": origin,
                "filePath": node.get("filePath"),
                "imported_at": now,
                "importer": IMPORTER_ID,
            },
            "tags": node.get("tags", []),
            "sectioned": sectioned,
            "content_hash": sha256_text(content),
        }
        if sectioned:
            descriptor["sections"] = {
                name: {"text": text, "hash": sha256_text(text)}
                for name, text in sections.items()
            }
        else:
            descriptor["sections"] = {"body": {"text": content, "hash": sha256_text(content)}}
        descriptor["relations"] = {
            "outbound": sorted(node.get("links", [])),
            "inbound": sorted(inbound[slug]),
        }

        (nodes_dir / f"{slug}.yaml").parent.mkdir(parents=True, exist_ok=True)
        with open(nodes_dir / f"{slug}.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(descriptor, f, allow_unicode=True, sort_keys=False, width=100)

        index_entries.append({
            "node_id": slug,
            "title": descriptor["title"],
            "sectioned": sectioned,
            "content_hash": descriptor["content_hash"],
            "outbound": descriptor["relations"]["outbound"],
            "inbound": descriptor["relations"]["inbound"],
        })

    # Global baseline hash: fingerprint of the entire graph state
    fingerprint = "\n".join(f"{e['node_id']}:{e['content_hash']}" for e in index_entries)
    graph_index = {
        "generated_at": now,
        "importer": IMPORTER_ID,
        "source": {"type": "quartz_content_index", "origin": origin},
        "source_hash": sha256_text(json.dumps(index, sort_keys=True)),
        "node_count": len(index_entries),
        "sectioned_nodes": n_sectioned,
        "baseline_hash": sha256_text(fingerprint),
        "nodes": index_entries,
    }
    with open(out_dir / "graph_index.yaml", "w", encoding="utf-8") as f:
        yaml.safe_dump(graph_index, f, allow_unicode=True, sort_keys=False, width=100)

    print(f"imported {len(index_entries)} nodes ({n_sectioned} sectioned, "
          f"{len(index_entries) - n_sectioned} body-only) from {origin}")
    print(f"baseline_hash: {graph_index['baseline_hash']}")
    print(f"output: {out_dir}/ (nodes/ + graph_index.yaml)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
