# CIP-KGE Protocol

**Cognitive Interview Protocol for Knowledge Graph Evolution — v0.2**

> Research Draft. This is the current state of thinking, not a stable specification.
> Gaps and open questions are marked explicitly.
> For node structure reference: [`SYLLABUS_SCHEMA.md`](./SYLLABUS_SCHEMA.md).
> For defined terms: [`GLOSSARY.md`](./GLOSSARY.md).

---

## What this protocol does

CIP-KGE is a methodology for conducting structured AI-assisted interviews that produce **Knowledge Diffs** — bounded, human-reviewable proposals for modifying specific nodes in the [Pyragogy Syllabus](https://syllabus.pyragogy.org).

A Knowledge Diff, if accepted, becomes a pull request on [pyragogy/ai-pedagogy](https://github.com/pyragogy/ai-pedagogy). When merged, the syllabus updates automatically.

A Knowledge Diff that cannot be merged into `ai-pedagogy` is outside the scope of this protocol.

---

## The flow

```
1. SESSION PREPARATION     → target node + target section(s) identified
2. INTERVIEW SESSION       → transcript with numbered exchanges
3. EVIDENCE EXTRACTION     → exchanges mapped to node sections
4. KNOWLEDGE DIFF          → YAML file in diffs/ (spec below)
5. PRE-REVIEW CHECK        → passes_minimum_quality: true | false
         ↓ fail → back to step 1 or 4
6. HUMAN REVIEW            → accepted | rejected | deferred
         ↓ accepted
7. MARKDOWN TRANSFORMATION → target node file updated
8. PULL REQUEST            → opened on pyragogy/ai-pedagogy
         ↓ merged
9. SYLLABUS UPDATE         → syllabus.pyragogy.org rebuilt automatically
10. DIFF ARCHIVAL          → diffs/ updated as permanent record
```

**Failure conditions by stage:**

| Stage | Fails if |
|---|---|
| 1 | No target node + at least one target section specified |
| 2 | Transcript lacks exchange numbers |
| 3 | No exchange maps to any section |
| 4 | YAML does not conform to spec below |
| 5 | `passes_minimum_quality: false` |
| 6 | Reviewer receives a diff that failed Stage 5 |

Stages 2, 5, 6, 7, 8 are explicitly manual in v0.2. The AI conducts the interview; a human reviews, transforms, and submits.

---

## How to conduct a session

### Before the session

Read the current published version of the target node at `syllabus.pyragogy.org`. The interview is not about discovering what the node says — it is about finding where it is incomplete, imprecise, or wrong.

Write a session brief:
- Target node path (e.g., `05_systemic_risks/automation_bias`)
- Target section(s) (e.g., `observable_markers`)
- Session ID: `session-YYYY-MM-DD-NNN`

### Five question types

| Type | Purpose | Sections it primarily serves |
|---|---|---|
| **Q1 Elicitation** | Surface knowledge without presupposing structure | `definition`, `use_case`, `observable_markers` |
| **Q2 Clarification** | Make statements precise; operationalize vague terms | `observable_markers`, `use_case`, `friction` |
| **Q3 Socratic** | Test premises; probe limits; act as constructive adversary | `risk`, `friction`, `definition` |
| **Q4 Contrastive** | Compare to related concepts; expose precise boundaries | `definition`, `ai_role`, `human_role` |
| **Q5 Mapping** | Surface relationships to other nodes in the graph | `risk`, `use_case`, wikilink targets |

**Section-to-question-type mapping:**

| Section | Primary types | Notes |
|---|---|---|
| `definition` | Q1, Q4, Q3 | Q1 first; Q4 refines boundaries; Q3 stress-tests |
| `use_case` | Q1, Q2 | Q1 surfaces contexts; Q2 makes them precise |
| `human_role` | Q1, Q2 | Focus on observable behavior, not intentions |
| `ai_role` | Q4, Q3 | What should AI refuse? Contrast with human role |
| `friction` | Q2, Q3 | "Difficulty" is not friction. Q3 finds what bypasses the mechanism |
| `risk` | Q3, Q5 | Q3: what breaks? Q5: what other nodes are affected? |
| `observable_markers` | Q2, Q1 | Must be external and verifiable. Repeat Q2 until the marker is not an internal state |

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

A Knowledge Diff is a YAML file in `diffs/`. It operates at the level of **sections** of a node — not at the level of the node as a whole.

Named: `diffs/diff-YYYY-MM-DD-NNN.yaml`

### Complete format with inline spec

```yaml
# ── Identity ──────────────────────────────────────────────────────────────
id: "diff-YYYY-MM-DD-NNN"
protocol_version: "CIP-KGE-v0.2"
session_id: "session-YYYY-MM-DD-NNN"
generated_at: "2026-07-15T14:30:00Z"          # ISO 8601

# ── Target node ───────────────────────────────────────────────────────────
target_node:
  path: "05_systemic_risks/automation_bias"   # path in ai-pedagogy/content/
  url: "https://syllabus.pyragogy.org/05_systemic_risks/automation_bias"
  operation: "modify"
  # operation: add | modify | remove | deprecate

# ── Section changes ───────────────────────────────────────────────────────
section_changes:
  - section: "observable_markers"
    # section: definition | use_case | human_role | ai_role |
    #          friction | risk | observable_markers
    operation: "modify"
    # operation: modify | append | remove_sentence
    current_text: |
      [exact current text of the section]
    proposed_text: |
      [replacement or addition]
    rationale: |
      [why this change improves the node; citation of session exchange]
    proposed_wikilinks: []   # new [[wikilinks]] introduced, if any

# ── Evidence ──────────────────────────────────────────────────────────────
evidence:
  session_exchange_ref: "session-YYYY-MM-DD-NNN/exchange-NN"
  summary: |
    [what the interviewee said that grounds the change]
  confidence: "medium"
  # confidence: high | medium | low
  # high   — explicit, consistent across multiple exchanges
  # medium — clear in one exchange; no corroboration
  # low    — inference; interviewee did not state directly
  confidence_rationale: |
    [why this confidence level]

# ── Pre-review quality check ──────────────────────────────────────────────
pre_review_check:
  passes_minimum_quality: true
  failure_reason: null
  # failure_reason (when false):
  #   no_evidence | low_confidence_only | target_not_found |
  #   wikilink_target_missing | scope_too_broad

# ── Review ────────────────────────────────────────────────────────────────
review_status: "proposed"
# review_status: proposed | under_review | accepted | rejected | deferred
review_notes: []
# Each entry: { reviewer, date, status_set, note }

# ── Merge ─────────────────────────────────────────────────────────────────
merge_ready: false
pr_url: null
```

### Minimum requirements for a valid diff

A diff enters review if and only if all of these hold:

1. `id`, `protocol_version`, `session_id`, `generated_at` are present.
2. `target_node.path` exists in the graph, or `operation` is `add`.
3. At least one entry in `section_changes`.
4. Every entry has non-empty `proposed_text` and `rationale`.
5. `evidence.session_exchange_ref` references an identifiable exchange.
6. `evidence.confidence` is not `low` unless `confidence_rationale` explains corroboration.
7. `pre_review_check.passes_minimum_quality` is `true`.

A diff that fails any of these is returned to the session author. A reviewer is not expected to fix a malformed diff.

### What a reviewer evaluates

1. **Evidence quality** — does the session exchange support the change? Read the transcript; do not trust the summary alone.
2. **Section fit** — is the change in the correct section? A `Definition` change that is really a `Risk` change should be corrected, not accepted.
3. **Graph consistency** — does the change affect wikilinks in a way that breaks other nodes?
4. **Rationale strength** — can a future reader understand why the change was made?

A reviewer is not a copy editor. Grammar is not a review criterion. Epistemic grounding is.

### One diff, one session

A diff must originate from a single interview session. Diffs synthesizing evidence from multiple sessions are not permitted in v0.2. This constraint exists to maintain provenance traceability.

---

## Known limitations

**L1 — One session, one diff.** Multiple expert perspectives cannot be synthesized in a single diff.

**L2 — No automated quality validation.** The pre-review check is manual. A schema-level YAML validator is a v0.3 candidate.

**L3 — Markdown transformation is manual.** Stage 7 is deterministic but requires a human to execute. Intentional in v0.2 while the format stabilizes.

**L4 — New graph sections not yet defined.** Adding a new top-level section (e.g., `06_institutional_contexts/`) is a structural change above the node level; the protocol does not cover it.

**L5 — Review criteria partially specified.** Calibration requires real review disagreements. `[OPEN: How should two reviewers who disagree on the same diff resolve the conflict?]`

---

## Changelog

| Version | Date | Summary |
|---|---|---|
| v0.1 | 2026-06 | Generic protocol. Three-component structure (interview, diff, pipeline). |
| v0.2 | 2026-06 | Anchored to Pyragogy Syllabus. Section-level diff format. 10-stage pipeline. Interview guide mapped to node sections. |
| v0.2.1 | 2026-06 | Consolidated: PIPELINE, KNOWLEDGE_DIFF_SPEC, INTERVIEW_GUIDE merged into this document. No content removed. |
