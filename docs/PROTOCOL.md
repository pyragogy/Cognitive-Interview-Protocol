# CIP-KGE Protocol

**Cognitive Interview Protocol for Knowledge Graph Evolution — v0.3**

> Research Draft. This is the current state of thinking, not a stable specification.
> Gaps and open questions are marked explicitly.
> For the formal diff contract: [`KNOWLEDGE_DIFF_SCHEMA.md`](./KNOWLEDGE_DIFF_SCHEMA.md) (conceptual) and [`KNOWLEDGE_DIFF_SCHEMA.yaml`](./KNOWLEDGE_DIFF_SCHEMA.yaml) (machine-readable).
> For the Pyragogy-specific binding layer: [`SYLLABUS_SCHEMA.md`](./SYLLABUS_SCHEMA.md).
> For defined terms: [`GLOSSARY.md`](./GLOSSARY.md).

---

## What this protocol does

CIP-KGE is a methodology for conducting structured AI-assisted interviews that produce **Knowledge Diffs** — bounded, human-reviewable proposals for modifying specific nodes in a knowledge graph.

The core protocol is **stack-agnostic**: it does not assume Quartz, GitHub, wikilinks, or any specific publishing platform. In the reference implementation, a Knowledge Diff targets the [Pyragogy Syllabus](https://syllabus.pyragogy.org) and, if accepted, becomes a pull request on [pyragogy/ai-pedagogy](https://github.com/pyragogy/ai-pedagogy). That binding is documented separately in [`SYLLABUS_SCHEMA.md`](./SYLLABUS_SCHEMA.md); other stacks implement their own binding against the same core contract.

---

## Epistemic Invariants (Non-Negotiable Constraints)

These constraints define the minimum conditions under which the Cognitive Interview Protocol (CIP-KGE) remains valid. If any of these are violated, the system ceases to produce reliable knowledge evolution.

### 1. Traceability Constraint
Every proposed change to the knowledge graph MUST be traceable to a specific evidence fragment from an interview session. No modification is allowed without explicit linkage to observed or stated data.

### 2. Locality of Change
Knowledge updates MUST operate at the level of individual node sections. Global or cross-node modifications are only allowed as a set of decomposed local patches.

### 3. Separation of Evidence and Interpretation
Evidence collected during interviews MUST remain distinct from interpretative transformations. The system MUST never conflate raw statements with derived conclusions.

### 4. Bounded Modification Principle
Each Knowledge Patch MUST modify only one conceptual dimension at a time. If multiple dimensions are affected, the change MUST be split into separate patches.

### 5. Explicit Uncertainty Requirement
No Knowledge Patch is valid without an explicit confidence level and justification. Uncertainty is a structural component of the system, not optional metadata.

### 6. Failure Visibility Principle
Failures in the protocol (rejected patches, invalid evidence, weak interviews) MUST be preserved and documented. System learning includes both successful and failed transformations.

#### Purpose of these invariants
These constraints ensure that CIP-KGE remains:
- Falsifiable
- Auditable
- Decomposable
- Extensible without loss of rigor

They define the boundary between a structured epistemic system and an unbounded generative process.

---

## The flow

```
1. SESSION PREPARATION     → target node + target section(s) identified
2. INTERVIEW SESSION       → transcript with numbered exchanges
3. EVIDENCE EXTRACTION     → exchanges mapped to node sections
4. KNOWLEDGE DIFF          → YAML file in diffs/ (schema referenced below)
5. PRE-REVIEW CHECK        → passes_minimum_quality: true | false
         ↓ fail → back to step 1 or 4
6. HUMAN REVIEW            → accepted | rejected | deferred | in_arbitration
         ↓ accepted
7. MARKDOWN TRANSFORMATION → target node file updated
8. PULL REQUEST            → opened on the bound repository (e.g., pyragogy/ai-pedagogy)
         ↓ merged
9. SYLLABUS UPDATE         → published graph rebuilt automatically
10. DIFF ARCHIVAL          → diffs/ updated as permanent record
```

**Failure conditions by stage:**

| Stage | Fails if |
|---|---|
| 1 | No target node + at least one target section specified |
| 2 | Transcript lacks exchange numbers |
| 3 | No exchange maps to any section |
| 4 | YAML does not conform to the formal schema |
| 5 | `passes_minimum_quality: false` |
| 6 | Reviewer receives a diff that failed Stage 5 |

Stages 2, 5, 6, 7, 8 are explicitly manual. The AI conducts the interview; a human reviews, transforms, and submits. Stage 3 is the only machine-assisted stage (see the n8n reference workflow in `workflows/`, which produces **draft** diffs only — it has no write access to any graph).

**Reviewer conflict:** if two reviewers disagree on the same diff, the diff enters `in_arbitration` status and follows the formal process in [`ARBITRATION.md`](./ARBITRATION.md).

---

## How to conduct a session

### Before the session

Read the current published version of the target node. The interview is not about discovering what the node says — it is about finding where it is incomplete, imprecise, or wrong.

Write a session brief:
- Target node identifier (e.g., `05_systemic_risks/automation_bias` in the Pyragogy binding)
- Target section(s) (e.g., `observable_markers`)
- Session ID: `session-YYYY-MM-DD-NNN`

### Five question types

| Type | Purpose | Sections it primarily serves |
|---|---|---|
| **Q1 Elicitation** | Surface knowledge without presupposing structure | `definition`, `use_case`, `observable_markers` |
| **Q2 Clarification** | Make statements precise; operationalize vague terms | `observable_markers`, `use_case`, `friction` |
| **Q3 Socratic** | Test premises; probe limits; act as constructive adversary | `risk`, `friction`, `definition` |
| **Q4 Contrastive** | Compare to related concepts; expose precise boundaries | `definition`, `ai_role`, `human_role` |
| **Q5 Mapping** | Surface relationships to other nodes in the graph | `risk`, `use_case`, relation targets |

**Section-to-question-type mapping** (section names shown for the Pyragogy binding; other bindings define their own):

| Section | Primary types | Notes |
|---|---|---|
| `definition` | Q1, Q4, Q3 | Q1 first; Q4 refines boundaries; Q3 stress-tests |
| `use_case` | Q1, Q2 | Q1 surfaces contexts; Q2 makes them precise |
| `human_role` | Q1, Q2 | Focus on observable behavior, not intentions |
| `ai_role` | Q4, Q3 | What should AI refuse? Contrast with human role |
| `friction` | Q2, Q3 | "Difficulty" is not friction. Q3 finds what bypasses the mechanism |
| `risk` | Q3, Q5 | Q3: what breaks? Q5: what other nodes are affected? |
| `observable_markers` | Q2, Q1 | Must be external and verifiable. Repeat Q2 until the marker is not an internal state |

**Formal transition rules** (when to move between question types, termination conditions, and the state machine for Q1–Q5) are specified in [`INTERVIEW_DECISION_TREE.md`](./INTERVIEW_DECISION_TREE.md).

### Session sequence

1. **Context** (5 min): explain the session purpose and that the output is a Knowledge Diff subject to human review.
2. **Elicitation** (Q1): one or two broad questions.
3. **Section focus**: target sections in order. A session focused on one section well outperforms a session that covers all sections superficially.
4. **Mapping** (Q5): near the end, ask about relationships to other nodes.
5. **Closing**: explicit end; ask if anything was missed.

### What the interview must not do

- Do not summarize the interviewee's words back to them during the session. That interpretation belongs in Stage 3, not Stage 2.
- Do not suggest answers. "Would you say the risk here is automation bias?" contaminates the evidence.
- Do not close topics on a thin answer. Return with a different question type.
- Do not ask what the interviewee thinks the node *should* say. Ask what they know about the phenomenon.

### Transcript requirements

Store at `interviews/{session_id}/transcript.md`. Must include:
- Session metadata (date, session ID, target node, protocol version)
- Full verbatim exchange
- Exchange numbers: `[exchange-01]`, `[exchange-02]`, ...

A transcript without exchange numbers cannot be cited in a Knowledge Diff.

---

## The Knowledge Diff format

A Knowledge Diff is a YAML file in `diffs/`, named `diff-YYYY-MM-DD-NNN.yaml`. It operates at the level of **sections** of a node — not at the level of the node as a whole.

The authoritative format specification lives in two places, kept in sync:

- [`KNOWLEDGE_DIFF_SCHEMA.md`](./KNOWLEDGE_DIFF_SCHEMA.md) — conceptual schema, design intent, conditional constraints, confidence vs. corroboration semantics.
- [`KNOWLEDGE_DIFF_SCHEMA.yaml`](./KNOWLEDGE_DIFF_SCHEMA.yaml) — machine-readable JSON Schema (draft-07, expressed in YAML) for automated validation.

Key v0.3 properties of the format:

- **Stack-agnostic addressing** — `target.node_id` is an opaque string; the binding layer maps it to concrete graph locations.
- **Confidence vs. corroboration** — `evidence.confidence` rates clarity *within* the session; `evidence.corroboration_scope` and `evidence.linked_sessions` record support *outside* it. High intra-session confidence is not inter-session corroboration.
- **Bounded modification** — 1 to 3 `section_changes` per diff (Invariant 4).
- **Conditional text requirements** — `current_text` is required for `modify` and `remove_sentence` operations, optional for `append`.

### Minimum requirements for a valid diff

A diff enters review if and only if all of these hold:

1. It validates against `KNOWLEDGE_DIFF_SCHEMA.yaml` (all required fields present, types and patterns correct).
2. `target.node_id` resolves in the binding layer's graph, or `target.operation` is `add`.
3. Every entry in `section_changes` has non-empty `proposed_text` and a `rationale` that cites the session exchange.
4. `evidence.session_exchange_ref` resolves to actual exchanges in the referenced transcript, all belonging to the diff's `session_id`.
5. If `evidence.confidence` is `low`, `confidence_rationale` explicitly states why the diff is submitted despite low confidence.
6. `pre_review_check.passes_minimum_quality` is `true`.

A diff that fails any of these is returned to the session author. A reviewer is not expected to fix a malformed diff.

### What a reviewer evaluates

1. **Evidence quality** — does the session exchange support the change? Read the transcript; do not trust the summary alone.
2. **Section fit** — is the change in the correct section? A `definition` change that is really a `risk` change should be corrected, not accepted.
3. **Graph consistency** — does the change affect cross-references in a way that breaks other nodes?
4. **Corroboration scope** — is the claim supported beyond a single session? A diff with `confidence: high` and `corroboration_scope: none` is valid but weak.
5. **Rationale strength** — can a future reader understand why the change was made?

A reviewer is not a copy editor. Grammar is not a review criterion. Epistemic grounding is.

### One diff, one session (strict)

A diff must originate from a single interview session. If evidence from multiple sessions supports the same change, submit one diff per session and cross-reference them via `evidence.linked_sessions`. The reviewer aggregates; the schema does not. Automatic cross-session synthesis is exactly the kind of interpretive step that Invariant 3 prohibits doing silently.

---

## Known limitations

**L1 — One session, one diff.** Multiple expert perspectives cannot be synthesized in a single diff. *Partially addressed in v0.3: `linked_sessions` allows explicit cross-referencing between per-session diffs, but aggregation remains a manual reviewer task.*

**L2 — Automated quality validation is syntactic only.** *Addressed in v0.3 for the syntactic layer: the formal YAML schema and `scripts/validate_diff.py` enforce structure mechanically. Semantic checks (does the exchange actually support the claim?) remain manual — by design.*

**L3 — Markdown transformation is manual.** Stage 7 is deterministic but requires a human to execute. Intentional while the format stabilizes.

**L4 — New graph sections not yet defined.** Adding a new top-level section is a structural change above the node level; the protocol does not cover it.

**L5 — Reviewer conflict.** *Addressed in v0.3: formal arbitration process in [`ARBITRATION.md`](./ARBITRATION.md), with `in_arbitration` as a first-class review status.*

---

## Changelog

| Version | Date | Summary |
|---|---|---|
| v0.1 | 2026-06 | Generic protocol. Three-component structure (interview, diff, pipeline). |
| v0.2 | 2026-06 | Anchored to Pyragogy Syllabus. Section-level diff format. 10-stage pipeline. Interview guide mapped to node sections. |
| v0.2.1 | 2026-06 | Consolidated: PIPELINE, KNOWLEDGE_DIFF_SPEC, INTERVIEW_GUIDE merged into this document. No content removed. |
| v0.2.2 | 2026-07 | Contract-first diff schema; syntactic validation rules; decision tree for question transitions; explicit confidence perimeter; conflict-resolution roadmap. |
| v0.3 | 2026-07 | Stack-agnostic knowledge diff schema; formal decision tree for Q1–Q5 transitions (`INTERVIEW_DECISION_TREE.md`); conflict-resolution protocol (`ARBITRATION.md`); confidence/corroboration separation; machine-readable YAML schema validator. |
