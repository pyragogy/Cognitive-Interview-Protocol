# Knowledge Diff — Formal Schema (CIP‑KGE v0.3)

> This schema is **stack‑agnostic**. It does not assume Quartz, GitHub, wikilinks, or any specific publishing platform.  
> Bindings to concrete graph implementations live in separate binding documents (e.g., `SYLLABUS_SCHEMA.md` for the Pyragogy Syllabus).  
> If you implement CIP‑KGE against a different knowledge graph, write your own binding — **do not modify this schema**.

---

## Design intent

Each field in the schema exists to enforce **one of the six Epistemic Invariants**. If you consider removing a required field, name which invariant you are breaking. There is no decorative field here.

| Invariant | Schema enforcement |
|-----------|-------------------|
| **Traceability** | `id`, `session_id`, `evidence.session_exchange_ref` patterns, mandatory transcript reference |
| **Locality of Change** | `section_changes` array, each entry scoped to a single section |
| **Separation of Evidence and Interpretation** | Distinct `evidence.summary` (raw) vs `rationale` (interpretation) fields |
| **Bounded Modification Principle** | `section_changes` array length ≤ 3 |
| **Explicit Uncertainty Requirement** | `evidence.confidence` enum + required `confidence_rationale` |
| **Failure Visibility Principle** | `pre_review_check.failure_reason` logged, `review_status` preserved |

The schema is **contract‑first**: it defines the shape of a Knowledge Diff independent of how diffs are stored, transmitted, or rendered. A valid diff is **portable** across implementations.

---

## Core concepts

### Stack‑agnostic addressing

The `target.node_id` field is an **opaque string**. It carries no assumption about file paths, URL structures, or database keys. The binding layer maps this identifier to concrete graph locations.

Example bindings:

| Graph platform | `node_id` format | Binding |
|----------------|------------------|---------|
| Pyragogy Syllabus (Quartz) | `section_prefix/node_name` | `SYLLABUS_SCHEMA.md` |
| Notion database | UUID of page | Custom binding |
| Neo4j property graph | Integer node ID | Custom binding |

### One diff, one session (strict)

A diff’s `evidence.session_exchange_ref` values **must** all belong to the diff’s `session_id`. The `evidence.linked_sessions` field may reference **other sessions** that corroborate the same claim, but those sessions do **not** contribute `section_changes` to this diff.

If evidence from three sessions supports the same change, submit **three diffs** with populated `linked_sessions` pointing at each other. The reviewer aggregates; the schema does not.

**Why?** Automatic cross‑session synthesis is exactly the kind of **interpretive step** that Invariant 3 prohibits doing silently.

### Confidence vs. corroboration scope

v0.2.1 conflated two epistemically different things under `confidence: high`:

1. **Intra‑session coherence** — the expert made a clear, consistent statement within this session.
2. **Inter‑session corroboration** — multiple independent experts made convergent statements across sessions.

v0.3 separates them:

| Field | Purpose | Values |
|-------|---------|--------|
| `evidence.confidence` | How clear/explicit the evidence is **within this session** | `high`, `medium`, `low` |
| `evidence.corroboration_scope` | Whether the claim is supported **outside this session** | `intra_session`, `inter_session`, `none` |
| `evidence.linked_sessions` | Which other sessions provide independent support | Array of `session-id`s |

A diff with `confidence: high` and `corroboration_scope: none` is **valid but weak** — high confidence in what one person said, no independent support. Reviewers must **not** treat this as equivalent to `inter_session` corroboration.

### Conditional constraints

The schema includes **conditional validation rules** that cannot be expressed in pure YAML Schema:

1. **If `confidence == "low"`**, `confidence_rationale` must be non‑empty and **explicitly state why the diff is being submitted despite low confidence** (e.g., “no other node covers this failure mode; documenting the gap outweighs the uncertainty”). Machine-enforced in the YAML schema: `confidence_rationale` has `minLength: 1` always, raised to `minLength: 20` when `confidence == "low"` (via `if/then`), to reject empty strings and alibi rationales like "ok". Genuinely boilerplate-but-long rationales still require human Stage 5 judgment (`failure_reason: low_confidence_only`) — no regex replaces that.
2. **If `target.operation != "add"`**, `target.node_id` must resolve in the binding layer’s graph (semantic check, not syntactic).
3. **Every `section_changes` entry** must have a non‑empty `rationale` that **cites the session exchange** (not just “makes it clearer”).

---

## Full schema reference

A machine‑readable YAML Schema is available at [`KNOWLEDGE_DIFF_SCHEMA.yaml`](./KNOWLEDGE_DIFF_SCHEMA.yaml). Below is a human‑oriented summary.

### Root object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Pattern: `^diff-\d{4}-\d{2}-\d{2}-\d{3}$` |
| `protocol_version` | string | yes | Const: `"CIP-KGE-v0.3"` |
| `session_id` | string | yes | Pattern: `^session-\d{4}-\d{2}-\d{2}-\d{3}$` |
| `generated_at` | string (ISO 8601) | yes | Timestamp of diff generation |
| `target` | object | yes | Stack‑agnostic pointer to the node |
| `section_changes` | array[1..3] | yes | Bounded modifications |
| `evidence` | object | yes | Grounding evidence |
| `pre_review_check` | object | yes | Result of automated validation |
| `review_status` | string | yes | Enum: `proposed`, `under_review`, `accepted`, `rejected`, `deferred`, `in_arbitration` |
| `review_notes` | array | no | Log of review activity |
| `merge_ready` | boolean | no | Implementation‑specific flag |
| `pr_url` | string (URI) | no | Pull‑request URL (if any) |

### `target` object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `node_id` | string | yes | Opaque identifier for the target node |
| `operation` | string | yes | Enum: `add`, `modify`, `remove`, `deprecate`, `retract` |

**On `retract`:** withdraws a previously accepted change that later evidence contradicts. The retraction diff must cite the superseding session, and the retracted content stays in the graph's history — a retraction is a new event, not a deletion (Invariant 6). Use `deprecate` for planned obsolescence, `retract` for epistemic error. Specified *before* the first real case requires it: a governance protocol that lacks a retraction path forces reviewers to choose between silent edits and leaving known-wrong content published.

### `section_changes` array items

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `section` | string | yes | Binding‑defined enum (e.g., `definition`, `use_case`, …) |
| `operation` | string | yes | Enum: `modify`, `append`, `remove_sentence` |
| `current_text` | string | conditional | Required if `operation` is `modify` or `remove_sentence` |
| `proposed_text` | string | yes | Non‑empty replacement or addition |
| `rationale` | string | yes | Non‑empty explanation, citing session exchange |
| `proposed_relations` | array[string] | no | New cross‑references introduced (binding‑agnostic) |

### `evidence` object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `session_exchange_ref` | string | yes | Pattern: `^session-\d{4}-\d{2}-\d{2}-\d{3}/exchange-\d{2}(,exchange-\d{2})*$` (comma-separated lists allowed for multi-exchange corroboration within the same session) |
| `summary` | string | yes | Verbatim‑adjacent restatement of what the interviewee said |
| `confidence` | string | yes | Enum: `high`, `medium`, `low` |
| `confidence_rationale` | string | yes | Justification for the confidence level |
| `corroboration_scope` | string | no | Enum: `intra_session`, `inter_session`, `none` (default) |
| `linked_sessions` | array[string] | no | Sessions independently supporting this same claim |

### `pre_review_check` object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `passes_minimum_quality` | boolean | yes | Result of automated syntactic validation |
| `failure_reason` | string or `null` | yes | Enum: `null`, `no_evidence`, `low_confidence_only`, `target_not_found`, `relation_target_missing`, `scope_too_broad`, `exchange_ref_unresolved`, `conflicting_diff_pending` |

---

## Minimum requirements for a valid diff (machine‑checkable, v0.3)

A diff is **syntactically valid** if and only if:

1. All required fields per the schema are present and type‑correct.
2. `section_changes` length is between 1 and 3 inclusive.
3. `evidence.session_exchange_ref` matches the pattern **and** resolves to an actual exchange in the referenced transcript (semantic check, requires transcript lookup).
4. If `evidence.confidence == "low"`, `evidence.confidence_rationale` is non‑empty and passes a boilerplate‑detection blocklist (implementation detail left to validator).
5. `target.operation == "add"` **or** `target.node_id` resolves in the binding layer’s graph.
6. No entry in `section_changes` has empty `proposed_text` or empty `rationale`.

A diff can be **syntactically valid** and still be **semantically weak** (e.g., `confidence: low`, `corroboration_scope: none`). Syntactic validity gates entry into human review. It does not gate acceptance.

---

## Automated validation

### Using the YAML Schema directly

The file `KNOWLEDGE_DIFF_SCHEMA.yaml` is a valid [JSON Schema](https://json-schema.org/) draft‑07 schema expressed in YAML. You can validate a Knowledge Diff with any JSON‑Schema validator:

```bash
# Example using Python (pip install jsonschema)
python -c "
import yaml, jsonschema, sys
schema = yaml.safe_load(open('docs/KNOWLEDGE_DIFF_SCHEMA.yaml'))
diff = yaml.safe_load(open('diffs/diff-2026-06-29-001.yaml'))
jsonschema.validate(diff, schema)
print('✓ Schema valid')
"
```

### Integration with n8n

Add a **“Validate YAML Schema”** node to your n8n workflow after the LLM generates a draft diff. Use a library like `ajv` (Node.js) or a subprocess call to a validator script.

### CI/CD pipeline

Add a validation step to your CI pipeline that runs on every PR containing a `.yaml` file in `diffs/`:

```yaml
# GitHub Actions example
name: Validate Knowledge Diffs
on:
  pull_request:
    paths:
      - 'diffs/*.yaml'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Python dependencies
        run: pip install jsonschema pyyaml
      - name: Validate diffs
        run: python scripts/validate_diff.py diffs/
```

A reference validator script is provided at [`scripts/validate_diff.py`](../scripts/validate_diff.py).

---

## Versioning

- **v0.3** — stack‑agnostic core, formal YAML Schema, confidence/corroboration split, conditional constraints.
- **Future** — additional validation rules (e.g., circular‑reference detection), richer relation types.

---

## Related documents

- [`PROTOCOL.md`](./PROTOCOL.md) — 10‑stage pipeline, epistemic invariants.
- [`INTERVIEW_DECISION_TREE.md`](./INTERVIEW_DECISION_TREE.md) — question‑type transition rules.
- [`ARBITRATION.md`](./ARBITRATION.md) — conflict resolution between concurrent diffs.
- [`SYLLABUS_SCHEMA.md`](./SYLLABUS_SCHEMA.md) — Pyragogy‑specific binding layer (example).