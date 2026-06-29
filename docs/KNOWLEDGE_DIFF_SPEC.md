# Knowledge Diff Specification

> **CIP-KGE v0.2**
>
> This document defines the operational format of a Knowledge Diff — the primary output artifact
> of a CIP-KGE interview session.
>
> A Knowledge Diff that does not conform to this specification cannot enter the review process.
> A reviewer who receives a non-conformant diff should return it to the session author, not attempt to evaluate it.

---

## What a Knowledge Diff is

A Knowledge Diff (we coin this term in a project-specific sense, as defined in [`GLOSSARY.md`](./GLOSSARY.md)) is a structured, bounded, human-reviewable proposal for a modification to one or more sections of a node in the Pyragogy Syllabus knowledge graph.

It is not a summary of an interview session. It is not a free-form description of what an expert said. It is a machine-readable artifact that maps precisely to the schema defined in [`SYLLABUS_SCHEMA.md`](./SYLLABUS_SCHEMA.md) and that, if accepted, can be transformed into a pull request on [pyragogy/ai-pedagogy](https://github.com/pyragogy/ai-pedagogy).

---

## Specification

### Complete YAML format

```yaml
# ─── Identity ──────────────────────────────────────────────────────────────────
id: "diff-YYYY-MM-DD-NNN"            # e.g. diff-2026-07-15-001
protocol_version: "CIP-KGE-v0.2"
session_id: "session-YYYY-MM-DD-NNN" # reference to the source interview session
generated_at: "2026-07-15T14:30:00Z" # ISO 8601

# ─── Target node ────────────────────────────────────────────────────────────────
target_node:
  path: "02_ontogeny/embodied_foundation"   # relative path in ai-pedagogy/content/
  url: "https://syllabus.pyragogy.org/02_ontogeny/embodied_foundation"
  operation: "modify"
  # operation values:
  #   add      — create a new node (requires full section coverage)
  #   modify   — change one or more sections of an existing node
  #   remove   — mark a node as deprecated (does not delete; adds deprecation notice)
  #   deprecate — flag a node as superseded by another (requires target_successor)

# ─── Section changes ────────────────────────────────────────────────────────────
section_changes:
  - section: "definition"
    # section values: definition | use_case | human_role | ai_role |
    #                 friction | risk | observable_markers
    operation: "modify"
    # operation values: modify | append | remove_sentence
    current_text: |
      The Embodied Foundation is the developmental anchor that grounds early cognition
      in physical, sensory-motor inquiry rather than screen-mediated abstraction.
      It establishes the baseline expectation that learning requires physical manipulation
      and friction.
    proposed_text: |
      The Embodied Foundation is the developmental anchor that grounds early cognition
      in physical, sensory-motor inquiry rather than screen-mediated abstraction.
      It establishes the baseline expectation that learning requires physical manipulation
      and friction. This foundation is not a prerequisite for AI involvement — it is a
      precondition for the learner's capacity to later engage AI-mediated friction productively.
    rationale: |
      The current definition does not state the relationship between the embodied foundation
      and later AI interaction. An expert in early childhood development (session-2026-07-15-001,
      exchange-22) argued that the foundation is meaningful specifically because of what it
      enables downstream: the ability to recognize AI-generated friction as friction, not as
      oracle output. This relationship is currently implicit; making it explicit strengthens
      the node's connection to the rest of the graph.
    proposed_wikilinks: []  # new wikilinks introduced in the proposed_text, if any

# ─── Evidence ────────────────────────────────────────────────────────────────────
evidence:
  session_exchange_ref: "session-2026-07-15-001/exchange-22"
  # Reference to the specific exchange in the session transcript that grounds
  # the proposed change. Format: {session_id}/exchange-{N}
  summary: |
    The expert drew a distinction between "embodied foundation as early childhood milestone"
    (the current framing) and "embodied foundation as prerequisite for productive AI friction"
    (the proposed framing). They described students who had skipped the embodied phase as
    unable to distinguish AI resistance from AI error — they accepted or rejected AI output
    based on surface features, not on argument quality.
  confidence: "medium"
  # confidence values: high | medium | low
  # high   — expert was explicit and consistent; multiple exchanges converge
  # medium — expert was clear but in a single exchange; no corroboration
  # low    — inference from expert's statement; expert did not articulate directly
  confidence_rationale: |
    The expert stated the relationship clearly in exchange-22 and partially in exchange-18,
    but did not explicitly address whether the connection should be in the Definition section
    or in the Risk section. The placement is an editorial judgment.

# ─── Pre-review quality check ────────────────────────────────────────────────────
pre_review_check:
  passes_minimum_quality: true
  # If false, the diff does not enter review. It is returned to the session author
  # with the failure_reason. A new or revised session is required.
  failure_reason: null
  # failure_reason values (when passes_minimum_quality is false):
  #   no_evidence          — no session exchange reference provided
  #   low_confidence_only  — all changes are confidence "low" with no corroboration
  #   target_not_found     — target_node.path does not exist in the graph
  #   wikilink_target_missing — proposed_wikilinks reference non-existent nodes
  #   scope_too_broad      — diff proposes changes to more than 3 sections without
  #                          justification for the interdependency

# ─── Review ──────────────────────────────────────────────────────────────────────
review_status: "proposed"
# review_status values:
#   proposed      — generated and submitted; no evaluation begun
#   under_review  — reviewer has accepted responsibility
#   accepted      — reviewer has approved; diff is merge-ready
#   rejected      — reviewer has rejected; rationale required in review_notes
#   deferred      — reviewer cannot decide without additional evidence
review_notes: []
# Each entry in review_notes:
#   - reviewer: "name or identifier"
#     date: "ISO 8601"
#     status_set: "under_review | accepted | rejected | deferred"
#     note: "free text"

# ─── Merge ───────────────────────────────────────────────────────────────────────
merge_ready: false
pr_url: null
# pr_url is set when a pull request has been opened on pyragogy/ai-pedagogy
# Format: "https://github.com/pyragogy/ai-pedagogy/pull/NNN"
```

---

## Minimum requirements for a valid diff

A diff is valid for review if and only if:

1. `id`, `protocol_version`, `session_id`, `generated_at` are all present.
2. `target_node.path` corresponds to an existing node in the graph, or `operation` is `add`.
3. At least one entry exists in `section_changes`.
4. Every `section_changes` entry has a non-empty `proposed_text` and `rationale`.
5. `evidence.session_exchange_ref` is present and references an identifiable exchange.
6. `evidence.confidence` is not `low` unless `confidence_rationale` explains the corroboration strategy.
7. `pre_review_check.passes_minimum_quality` is `true`.

If any of these conditions is not met, the diff is malformed and must be returned to the session author before entering review.

---

## What a reviewer evaluates

A reviewer evaluating a diff should assess:

1. **Evidence quality** — does the session exchange actually support the proposed change? Read the transcript; don't trust the summary alone.
2. **Section fit** — is the proposed change in the right section of the node? A change to `Definition` that is really a change to `Risk` should be corrected, not accepted.
3. **Graph consistency** — does the proposed change introduce, remove, or alter wikilinks in a way that affects the rest of the graph?
4. **Rationale strength** — is the rationale for the change complete enough that a future reader can understand why it was made?

A reviewer is not a copy editor. Grammar and style are not review criteria. Epistemic grounding is.

---

## One diff, one session

A Knowledge Diff must originate from a single interview session. Diffs that synthesize evidence from multiple sessions are not permitted in v0.2. If multiple sessions produce evidence for the same change, the most recent session's evidence takes precedence, and previous sessions are cited in `review_notes` as supporting context.

This constraint exists to maintain provenance traceability. It may be relaxed in a future version.

---

## Diff naming

Diffs are named with the pattern `diff-YYYY-MM-DD-NNN`, where `NNN` is a zero-padded sequence number for diffs generated on the same date. Diffs are stored in the `diffs/` directory at the root of this repository.

Example: `diffs/diff-2026-07-15-001.yaml`
