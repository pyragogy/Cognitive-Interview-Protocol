# Conflict Resolution Between Concurrent Diffs (CIP‑KGE v0.3)

> This document resolves former **Limitation L5**, which was an open question with no process attached.  
> It defines a formal arbitration procedure that **prioritizes evidence over authority** and prevents silent merges or stalemates.

---

## When arbitration triggers

Two or more diffs are **in conflict** if **both** conditions hold:

1. They target overlapping `(node_id, section)` pairs, **and**
2. Their `proposed_text` values are **not trivially compatible**.

**Trivial compatibility** means one proposal is a strict superset or refinement of the other (e.g., Diff A adds a sentence, Diff B adds the same sentence plus another). That’s a **merge**, not a conflict — the reviewer can accept both.

**Non‑trivial incompatibility** means the proposals contradict, diverge, or propose alternative phrasings that cannot be reconciled without interpretation (e.g., Diff A says “risk is X”, Diff B says “risk is Y, not X”).

Detection is **mechanical** at the `(node_id, section)` level; compatibility judgment is **not** — a human reviewer makes that call. The schema flags candidates, it does not resolve them.

### Schema‑level conflict detection

```yaml
pre_review_check:
  passes_minimum_quality: true
  failure_reason: null
  conflict_check:
    conflicting_diff_ids: ["diff-2026-07-10-004", "diff-2026-07-11-002"]
    overlap:
      - node_id: "automation_bias"
        section: "risk"
      - node_id: "embodied_foundation"
        section: "definition"
```

If `conflicting_diff_ids` is non‑empty, `review_status` is set to **`in_arbitration`** instead of `proposed`, regardless of individual diff quality. The diffs are **frozen** until arbitration concludes.

---

## Arbitration procedure

### 1. Freeze both diffs

Neither diff proceeds to Stage 7 (Markdown transformation) while `review_status: in_arbitration`.

### 2. Assign a second reviewer

The original reviewer(s) of each diff **do not arbitrate their own diff**. A reviewer **not involved in either diff** evaluates both against the same transcript excerpts.

### 3. Compare evidence, not authority

The arbitrating reviewer compares:

- `evidence.confidence` (high/medium/low)
- `evidence.corroboration_scope` (intra_session / inter_session / none)
- `evidence.linked_sessions` (sessions providing independent corroboration)
- The **specificity and operationalizability** of the transcript excerpts cited.

They **do not** consider:
- Seniority of the interviewee
- Recency of the session
- Which diff was submitted first (except as a tie‑breaker when evidence is perfectly balanced)

A diff submitted **later** with `corroboration_scope: inter_session` outranks an earlier diff with `corroboration_scope: intra_session, none`, all else equal.

### 4. Possible outcomes

| Outcome | Description | Logging |
|---------|-------------|---------|
| **One accepted, one rejected** | One diff’s evidence is stronger; the other is rejected. | Rejection reason must cite the **specific evidentiary gap**, logged in `review_notes` of the rejected diff. |
| **Both rejected, new session requested** | The conflict reveals the node’s current framing is **ambiguous enough that neither diff resolves it**. | Log as a `ROADMAP.md` open question; request a **structured debate session** (new interview type) that directly addresses the ambiguity. |
| **Split** | Arbitrator determines the section actually covers **two conceptual dimensions** (violating Invariant 4 in the **original node**, not the diffs). | Escalate above the diff level — request the node be restructured. This is out of CIP‑KGE’s scope per L4. |

### 5. No silent merge

The arbitrator **never** hand‑writes a synthesis of both `proposed_text` values. If a synthesis is warranted, it is submitted as:

- A **new diff** with a new `id`
- From a **new session** (or explicitly marked as `operation: modify` authored by the arbitrating reviewer)
- With `evidence.confidence: n/a — arbitration synthesis`
- Fully attributed as such — **never** presented as if it emerged from the original interview.

This preserves **Invariant 3 (Separation of Evidence and Interpretation)** — the synthesis is an interpretation, not raw evidence, and must be labeled accordingly.

---

## Multi‑party conflicts (more than two diffs)

The procedure above is defined for **two conflicting diffs**. For three or more:

1. Apply the same procedure **pairwise**.
2. If pairwise resolution doesn’t converge after one round, escalate to a **third reviewer** (different from the first two).
3. The third reviewer may:
   - Accept one diff and reject the others **if** one diff’s evidence is decisively stronger.
   - Reject all and request a **structured debate session** with a **panel of experts**.
   - Flag the node as **epistemically unstable** and recommend a **full rewrite** outside CIP‑KGE.

This is a **v0.4 candidate** — we explicitly flag that the two‑diff case does **not** trivially generalize, rather than pretending the problem is solved.

---

## Implementation checklist for workflow builders

If you are integrating CIP‑KGE into an n8n workflow, CI pipeline, or custom tool, implement these steps:

```javascript
// Pseudo‑code for conflict detection
function detectConflicts(diffs) {
  const overlaps = new Map(); // key: `${node_id}/${section}`
  
  for (const diff of diffs) {
    for (const change of diff.section_changes) {
      const key = `${diff.target.node_id}/${change.section}`;
      if (!overlaps.has(key)) overlaps.set(key, []);
      overlaps.get(key).push(diff.id);
    }
  }
  
  const conflicts = [];
  for (const [key, diffIds] of overlaps) {
    if (diffIds.length > 1) {
      conflicts.push({ overlap: key, conflicting_diff_ids: diffIds });
    }
  }
  return conflicts;
}
```

### Required validator additions

1. **Pre‑review conflict check:** Before setting `review_status: proposed`, query the diff store for other diffs targeting the same `(node_id, section)` with `review_status` not in `[rejected, deferred]`. If found, set `review_status: in_arbitration` and populate `pre_review_check.conflict_check`.
2. **Arbitration workflow:** When `review_status: in_arbitration`, route the diff to a dedicated queue/board visible only to reviewers not involved in the conflicting diffs.
3. **Audit trail:** All arbitration decisions must be logged in `review_notes` with `status_set: accepted` or `rejected` plus a `note` explaining the evidentiary rationale.

---

## What this still doesn’t cover

- **Time‑bound arbitration** — no deadline is set for the arbitrator’s decision. In practice, a diff stuck `in_arbitration` for >7 days should trigger an escalation (v0.4).
- **Cross‑node conflicts** — diffs that affect different nodes but have logical interdependencies (e.g., Diff A modifies `definition`, Diff B modifies `risk` of the same node, but they assume incompatible premises). These are **semantic conflicts** not caught by `(node_id, section)` overlap.
- **Arbitrator bias** — the second reviewer may still have unconscious preferences. No blind‑review mechanism is defined (v0.4 candidate).

These gaps are **acknowledged**, not hidden. Each is flagged in `ROADMAP.md` as an open research question.

---

## Versioning

- **v0.3** — initial formalization, covers two‑diff conflicts.
- **v0.4 (planned)** — multi‑party conflicts, time‑bound escalation, cross‑node semantic conflict detection.

---

## Related documents

- [`PROTOCOL.md`](./PROTOCOL.md) — 10‑stage pipeline, epistemic invariants.
- [`INTERVIEW_DECISION_TREE.md`](./INTERVIEW_DECISION_TREE.md) — question‑type transition rules.
- [`KNOWLEDGE_DIFF_SCHEMA.md`](./KNOWLEDGE_DIFF_SCHEMA.md) — formal diff schema with `conflict_check` field.