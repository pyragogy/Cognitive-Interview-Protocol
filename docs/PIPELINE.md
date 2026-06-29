# CIP-KGE Pipeline

> **Cognitive Interview Protocol for Knowledge Graph Evolution — v0.2**
>
> This document describes the complete operational pipeline from interview session to syllabus update.
> Every stage has defined inputs, outputs, and failure conditions.
> A stage that does not produce its specified output does not pass to the next stage.

---

## Overview

```
[1. SESSION PREPARATION]
        ↓
[2. INTERVIEW SESSION]
        ↓
[3. EVIDENCE EXTRACTION]
        ↓
[4. KNOWLEDGE DIFF GENERATION]
        ↓
[5. PRE-REVIEW QUALITY CHECK]  ←── fails → back to SESSION PREPARATION
        ↓
[6. HUMAN REVIEW]
        ↓ accepted
[7. MARKDOWN TRANSFORMATION]
        ↓
[8. PULL REQUEST → pyragogy/ai-pedagogy]
        ↓ merged
[9. SYLLABUS UPDATE]
        ↓
[10. DIFF ARCHIVAL]
```

---

## Stage 1 — Session Preparation

**Input:** A research question or a specific node in the Pyragogy Syllabus that is under examination.

**Output:** A session brief containing:
- The target node identifier (e.g., `02_ontogeny/embodied_foundation`)
- The section(s) of the node that the session will focus on
- The interviewee's domain of expertise
- The interview technique to be used (see [`INTERVIEW_GUIDE.md`](./INTERVIEW_GUIDE.md))
- The session ID (`session-YYYY-MM-DD-NNN`)

**Failure condition:** The session brief does not specify a target node and at least one target section. A session without a target is not a CIP-KGE session — it is an exploratory conversation. Exploratory conversations have value, but they do not produce Knowledge Diffs in this version of the protocol.

**Note on new nodes:** If the session's purpose is to propose an entirely new node (rather than modify an existing one), the session brief must specify the proposed node path and the section of the graph it would belong to.

---

## Stage 2 — Interview Session

**Input:** Session brief from Stage 1.

**Output:** A session transcript stored at `interviews/{session_id}/transcript.md`.

The transcript must include:
- Session metadata (date, session ID, target node, AI system used, protocol version)
- Full verbatim exchange between the AI system and the interviewee
- Exchange numbers (e.g., `[exchange-01]`, `[exchange-02]`) for later reference
- Anonymization notes, if any content has been modified

The AI system conducts the interview using the question types defined in [`INTERVIEW_GUIDE.md`](./INTERVIEW_GUIDE.md). The guide specifies which question types are appropriate for which section of the node.

**Failure condition:** The transcript does not include exchange numbers. A transcript without exchange numbers cannot be cited in a Knowledge Diff.

---

## Stage 3 — Evidence Extraction

**Input:** Session transcript from Stage 2.

**Output:** An evidence bundle stored at `interviews/{session_id}/evidence.md`.

The evidence bundle maps specific exchanges to specific sections of the target node:

```markdown
# Evidence Bundle — {session_id}

## Target node: {node_path}

### Section: definition
- Exchange: [exchange-22]
- Type: direct statement
- Summary: [what the expert said that is relevant to the Definition section]

### Section: risk
- Exchange: [exchange-18], [exchange-24]
- Type: inference from contrast
- Summary: [what the expert said]
```

**Failure condition:** No exchange can be mapped to any section. If this happens, the session did not produce actionable evidence. The session is archived but does not proceed to Stage 4.

---

## Stage 4 — Knowledge Diff Generation

**Input:** Evidence bundle from Stage 3.

**Output:** One or more Knowledge Diff files stored at `diffs/diff-YYYY-MM-DD-NNN.yaml`, conforming to the specification in [`KNOWLEDGE_DIFF_SPEC.md`](./KNOWLEDGE_DIFF_SPEC.md).

**One diff per proposed change.** If the evidence bundle contains evidence for changes to three sections of one node, three separate diffs may be generated — or one diff with three `section_changes` entries if the changes are strongly interdependent. Changes to different nodes always produce separate diffs.

**Who generates the diff?** In the current version of the protocol, diff generation is performed by the AI system that conducted the interview, under human supervision. The human must review the generated diff before it enters Stage 5. The diff is not AI output that bypasses human judgment; it is a structured representation of the interview's content, subject to human correction before review.

---

## Stage 5 — Pre-Review Quality Check

**Input:** Knowledge Diff from Stage 4.

**Output:** `pre_review_check.passes_minimum_quality: true` or `false`.

The check verifies the minimum requirements defined in [`KNOWLEDGE_DIFF_SPEC.md`](./KNOWLEDGE_DIFF_SPEC.md). It is performed by the session author (not the reviewer) before submitting the diff for review.

**Failure condition:** `passes_minimum_quality: false`. The diff is returned to Stage 4 (if the issue is formatting) or to Stage 1 (if the issue is missing evidence). The `failure_reason` field must be populated.

This stage exists to protect the reviewer's time. A reviewer who receives a malformed diff is not expected to fix it — they should return it immediately.

---

## Stage 6 — Human Review

**Input:** Knowledge Diff with `pre_review_check.passes_minimum_quality: true`.

**Output:** `review_status: accepted | rejected | deferred`.

The reviewer is a human who was not present in the interview session. They have access to:
- The Knowledge Diff
- The full session transcript
- The evidence bundle
- The current published state of the target node at `syllabus.pyragogy.org`

**Review criteria** (see [`KNOWLEDGE_DIFF_SPEC.md`](./KNOWLEDGE_DIFF_SPEC.md) for full list):
1. Does the session exchange support the proposed change?
2. Is the change in the correct section?
3. Is the proposed text consistent with the rest of the node?
4. Does the change introduce or require wikilinks to non-existent nodes?

**Deferred diffs** may be assigned a follow-up session in Stage 1 to collect additional evidence.

**Rejected diffs** are archived with a rationale. They are not deleted. A rejection is evidence about the protocol's limitations.

---

## Stage 7 — Markdown Transformation

**Input:** Knowledge Diff with `review_status: accepted`.

**Output:** A modified Markdown file corresponding to the target node, ready for a pull request.

The transformation is deterministic: each `section_changes` entry replaces or appends to the corresponding section in the node's Markdown file. The transformation must be performed and verified by a human — not applied automatically — in this version of the protocol.

If the diff proposes a **new node** (`operation: add`), the Markdown file is created from scratch following the schema in [`SYLLABUS_SCHEMA.md`](./SYLLABUS_SCHEMA.md).

---

## Stage 8 — Pull Request

**Input:** Modified or new Markdown file from Stage 7.

**Output:** A pull request on [pyragogy/ai-pedagogy](https://github.com/pyragogy/ai-pedagogy), with the `pr_url` field of the diff updated.

The pull request description must include:
- Reference to the Knowledge Diff ID (e.g., `diff-2026-07-15-001`)
- A human-readable summary of the proposed change
- The review status and reviewer (from the diff's `review_notes`)

The PR is subject to the standard review process of the `ai-pedagogy` repository. CIP-KGE review and GitHub repository review are separate steps.

---

## Stage 9 — Syllabus Update

**Input:** Merged pull request.

**Output:** Updated node at `syllabus.pyragogy.org`.

Quartz rebuilds and publishes automatically on merge to `main`. No manual deployment step is required.

The diff's `merge_ready` field is set to `true` and `pr_url` is populated when the PR is opened (Stage 8). After merge, the diff is considered closed.

---

## Stage 10 — Diff Archival

**Input:** Merged diff.

**Output:** The diff file in `diffs/` is updated with the final `review_status: accepted`, `merge_ready: true`, and `pr_url`, and committed to this repository as a permanent record.

The archive in `diffs/` is the audit trail of the protocol. It is not a queue — it is a log.

---

## What the pipeline does not automate

In CIP-KGE v0.2, the following steps are **explicitly manual** and are not candidates for automation:

- Stage 2: The interview itself (the AI conducts it, but under human direction)
- Stage 5: The pre-review check (performed by the session author)
- Stage 6: Human review (by definition human)
- Stage 7: Markdown transformation (human-verified)
- Stage 8: Pull request creation (human action)

Automation of these steps is a research question for later versions. In v0.2, the priority is establishing that the methodology produces reliable results — not that it produces them quickly.
