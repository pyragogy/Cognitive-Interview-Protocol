# Pyragogy binding

Binding layer between the stack-agnostic CIP-KGE core and the Pyragogy Syllabus
(Quartz site, https://syllabus.pyragogy.org). Everything Quartz/JSON-specific
lives here; the core protocol never imports from this directory.

## Contents

- `import_graph.py` — **Input binding (Stage 1)**. Reads `static/contentIndex.json`
  (local path or `--url`) and generates per-node baseline descriptors under
  `baseline/nodes/<slug>.yaml` plus `baseline/graph_index.yaml`
  (adjacency + global `baseline_hash`).
- `baseline/` — generated snapshot of the live graph (60 nodes at last import).
  **Derived artifact**: re-run the importer to refresh; `baseline_hash` changes
  when the site changes. These files are *state*, not Knowledge Diffs — a diff
  proposes a change against this state (`target.node_id` = node slug;
  `section_changes[].current_text` must match the section text hashed here).

## Section convention

Pyragogy nodes follow seven numbered sections (`1. Definition` … `7. Observable
Markers`), mapped to the binding section names used by the diff schema:
`definition`, `use_case`, `human_role`, `ai_role`, `friction`, `risk`,
`observable_markers`. Nodes without that structure are imported as
`sectioned: false` with a single `body` section — section-level diffs do not
apply to them.

## Output binding (Stage 7, not yet automated)

An accepted diff is applied by a human to the corresponding `content/<slug>.md`
file in the `pyragogy/ai-pedagogy` repository and submitted as a pull request.
Automation of this step (PR generation + CI validation + rebuild) is planned;
see `docs/ROADMAP.md`. Until then: **no automated writes to the syllabus, ever.**

## Workflow

`workflows/syllabus_co_creation_agent.json` fetches the live graph, extracts the
local sub-graph for a target node, runs Stage 3 extraction, and emits a **draft**
diff. It has no write access by design (Principles 3–4).
