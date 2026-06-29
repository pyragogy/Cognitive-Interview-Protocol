# Protocol Specification — CIP-KGE v0.2

> **Status: Research Draft — v0.2**
>
> CIP-KGE: Cognitive Interview Protocol for Knowledge Graph Evolution.
>
> This version supersedes the generic v0.1 specification. The key difference:
> v0.1 described a generic methodology for producing knowledge diffs against any knowledge graph.
> v0.2 is anchored to the Pyragogy Syllabus — a specific graph with a defined node schema —
> and specifies how diffs produced by this protocol become pull requests on that graph's repository.
>
> Gaps and open questions are marked explicitly. Do not read this as a stable specification;
> read it as the current state of thinking.

---

## System context

CIP-KGE exists to serve one system:

**[Pyragogy Syllabus](https://syllabus.pyragogy.org)** — a living knowledge graph for human-AI learning, cognitive friction, and peer-like co-creation. Source repository: [pyragogy/ai-pedagogy](https://github.com/pyragogy/ai-pedagogy).

The protocol has no purpose outside of producing improvements to that graph. A Knowledge Diff that cannot be merged into `ai-pedagogy` is not within the scope of this protocol.

For the formal structure of a syllabus node, see [`SYLLABUS_SCHEMA.md`](./SYLLABUS_SCHEMA.md).

---

## What the protocol is

CIP-KGE is a structured methodology for conducting AI-assisted interviews that produce *Knowledge Diffs* — structured, reviewable proposals for the evolution of nodes in the Pyragogy Syllabus knowledge graph.

The protocol has three components:

1. **The interview structure** — how a session is organized, which question types are used for which sections, and how evidence is extracted from the transcript.
2. **The Knowledge Diff format** — how the results of a session are represented as a machine-readable, human-reviewable artifact.
3. **The pipeline** — how a Knowledge Diff moves from generation to merge, including review criteria and failure conditions at each stage.

---

## Component 1 — Interview Structure

See [`INTERVIEW_GUIDE.md`](./INTERVIEW_GUIDE.md) for the full specification.

Summary:
- Every session targets a specific node in the Pyragogy Syllabus, identified by its path (e.g., `02_ontogeny/embodied_foundation`).
- Every session targets one or more specific sections of that node (e.g., `definition`, `risk`).
- Five question types are defined (elicitation, clarification, Socratic challenge, contrastive, mapping), each mapped to the sections it primarily serves.
- The session produces a transcript with numbered exchanges, stored in `interviews/{session_id}/`.

---

## Component 2 — Knowledge Diff Format

See [`KNOWLEDGE_DIFF_SPEC.md`](./KNOWLEDGE_DIFF_SPEC.md) for the full specification.

Summary:
- A Knowledge Diff is a YAML file stored in `diffs/`.
- It operates at the level of **sections** of a node — not at the level of the node as a whole.
- It carries provenance (session ID, exchange reference), a proposed change, a rationale, an evidence summary, a confidence level, and a review status.
- It must pass a pre-review quality check before entering human review.

---

## Component 3 — Pipeline

See [`PIPELINE.md`](./PIPELINE.md) for the full specification.

The pipeline has 10 stages:

```
Session Preparation → Interview Session → Evidence Extraction →
Knowledge Diff Generation → Pre-Review Quality Check →
Human Review → Markdown Transformation →
Pull Request (pyragogy/ai-pedagogy) → Syllabus Update → Diff Archival
```

Each stage has defined inputs, outputs, and failure conditions. A stage that does not produce its specified output does not pass to the next stage.

---

## Known limitations of v0.2

### L1 — One session, one diff
A diff must originate from a single interview session. Synthesizing evidence across sessions is not yet defined. This limits the protocol's ability to produce changes that require multiple expert perspectives.

### L2 — No automated quality validation
The pre-review quality check (Stage 5) is performed manually by the session author. There is no automated validator. A schema-level validator for the YAML format is a v0.3 candidate.

### L3 — Markdown transformation is manual
Stage 7 (converting an accepted diff into a Markdown file) is fully manual. The mapping is deterministic but requires a human to execute it. This is intentional in v0.2; it will be a candidate for automation once the format is stable.

### L4 — New section proposal not yet defined
The protocol handles modification of existing nodes and addition of new nodes, but does not yet define the process for proposing a new *section* of the graph (e.g., adding a `06_institutional_contexts/` directory). This is a structural change at a level above the node.

### L5 — Review criteria are partially specified
The criteria by which a reviewer accepts or rejects a diff are defined at a general level in [`KNOWLEDGE_DIFF_SPEC.md`](./KNOWLEDGE_DIFF_SPEC.md) but have not been tested against real review disagreements. Calibration will require pilot sessions.

`[OPEN QUESTION: How should disagreement between two reviewers on the same diff be resolved?]`

---

## Changelog

| Version | Date | Summary |
|---|---|---|
| v0.1 | 2026-06 | Initial draft. Generic protocol for knowledge diff generation. Three-component structure established. |
| v0.2 | 2026-06 | Anchored to Pyragogy Syllabus. Node schema formalized. Knowledge Diff format redesigned to operate at section level. Full pipeline defined in 10 stages. Interview guide linked to node sections. |
