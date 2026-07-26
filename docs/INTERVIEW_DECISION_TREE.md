# Interview Decision Tree — Question‑Type Transition Rules (CIP‑KGE v0.3)

> This document replaces the qualitative heuristic from v0.2.1 (“repeat Q2 until the marker is not an internal state”).  
> That instruction told the interviewer **what a good answer looks like** but not **when to stop trying** or **what to do next**.  
> Below is the formal decision procedure that eliminates interviewer‑driven variance while preserving epistemic rigor.

---

## The problem this fixes

v0.2.1’s mapping table linked question types to node sections. It did **not** define:

- When a Q1 answer is “thin enough” to warrant staying on Q1 vs moving to Q2.
- How many failed Q2 attempts justify escalating to Q3.
- When to abandon a section entirely for this session versus push further.

Without these rules, two interviewers running the same protocol on the same expert produce different‑depth evidence for no principled reason. That’s a **reliability problem**, not a style difference. This document fixes it.

---

## Per‑section state machine

For each target section, the interview is in one of four states:

```
OPEN → PROBING → SATURATED → CLOSED
                    ↑
               CLOSED-THIN (alternate terminal state)
```

### OPEN (initial state)

**Action:** Ask Q1 (elicitation) for the section.

**Response scoring — two criteria:**

| Criterion | Meaning | Example passes |
|-----------|---------|----------------|
| **Specific** | Names a concrete instance, not a category | “Last week I saw a team skip unit tests because they trusted the AI’s generated code” |
| **Non‑circular** | Does not merely restate the section’s current text back to you | Current text: “Risk arises when…” / Answer: “The risk is that teams over‑rely…” (circular) vs. “I’ve seen three projects hit integration dead‑ends because…” (non‑circular) |

**Transition rules:**

- **BOTH criteria met** → go to **SATURATED** (Q1 answer stands; move to Q5/mapping or next section).
- **NEITHER criterion met** → go to **PROBING** (Q2, up to 2 attempts).
- **ONE criterion met** → go to **PROBING** (Q2, 1 attempt) then re‑score.

### PROBING (Q2 — clarification)

**Action:** Ask Q2, maximum **2 attempts per section**.

**Response scoring:** Is the term/claim now **operationalized**?  
*Operationalized* = a third party could verify the claim without asking the expert again (i.e., it points to an observable behavior, a measurable outcome, a repeatable test).

**Transition rules:**

- **YES** → **SATURATED**.
- **NO after 2 attempts** → escalate to **Q3 (Socratic)** — **1 attempt only**.
  - Q3 response scored: did a contradiction or edge case surface?
    - **YES** → **SATURATED** (the edge case **is** the evidence — capture it).
    - **NO** → **CLOSED‑THIN**.

### SATURATED (terminal, successful)

The section has enough evidence to draft a `section_change` entry.

**Optional follow‑ups:**

- Run **Q4 (contrastive)** if the section is `definition` or `ai_role` — sharpens boundaries.
- Run **Q5 (mapping)** if the session is near closing — surfaces graph relationships.

**Then:** Move to **CLOSED**. Do **not** reopen with a different question type “just to check” — that violates the interview’s non‑leading posture and risks contaminating evidence collected while the section was OPEN.

### CLOSED‑THIN (terminal, unsuccessful)

Reached when **Q1 → Q2 (×2) → Q3 (×1)** still fails to operationalize the section.

**What to do:**

1. **Do not fabricate resolution.** Do not ask “would you say X?” to force closure — this is explicitly prohibited (contamination).
2. **Record the section as `CLOSED-THIN` in the session brief**, not as a silent gap. This is a first‑class outcome, not a failure to hide.
3. **No diff is drafted for this section from this session.** A `CLOSED-THIN` section produces **zero** `section_changes` entries — it is **not** submitted with `confidence: low` as a placeholder. Low confidence is for weak‑but‑present evidence, not absent evidence.
4. This connects directly to **Invariant 6 (Failure Visibility)**: a CLOSED‑THIN outcome is preserved in the session record precisely because “this expert did not have operationalizable knowledge here” is itself useful information for whoever runs the next session on this node.

---

## Explicit stopping rule for the whole session (not just per‑section)

Stop the session when **any** of these conditions is met:

1. All target sections reach **SATURATED** or **CLOSED‑THIN**.
2. **45 minutes elapse** (soft budget — state this to the interviewee at minute 40).
3. **Three consecutive sections in a row hit CLOSED‑THIN** — a signal that either:
   - The expert isn’t the right source for this node, or
   - The node’s current framing doesn’t match how practitioners think about it.

Both are **findings worth recording**, not reasons to push harder.

---

## What this does **not** solve

This state machine assumes a **single‑topic, single‑expert session**. It does **not** define behavior for:

- Group interviews (multiple experts simultaneously).
- An interviewee who actively resists the Q1→Q2→Q3 escalation (e.g., repeatedly deflecting, answering every question with “it depends”).
- Sessions where the expert introduces a **completely new concept** that isn’t yet a node in the graph (handled by the `add` operation, but the decision tree doesn’t prescribe when to switch from modifying an existing node to proposing a new one).

These remain **open research questions** — flagged in `docs/ROADMAP.md`, not papered over here.

---

## Quick reference table

| State | Question type | Max attempts | Next state(s) |
|-------|---------------|--------------|---------------|
| OPEN | Q1 (elicitation) | 1 | SATURATED (both criteria met)<br>PROBING (otherwise) |
| PROBING | Q2 (clarification) | 2 | SATURATED (operationalized)<br>Q3 escalation (not operationalized after 2) |
| PROBING → escalation | Q3 (Socratic) | 1 | SATURATED (edge case surfaced)<br>CLOSED-THIN (no edge case) |
| SATURATED | Optional Q4/Q5 | — | CLOSED |
| CLOSED‑THIN | (none) | — | (terminal) |

---

## Versioning

- **v0.3** — initial formalization, replaces v0.2.1’s qualitative heuristic.
- **Future work** — extend to multi‑expert sessions, handle deflection patterns, integrate with automated confidence scoring.

---

## Related documents

- [`PROTOCOL.md`](./PROTOCOL.md) — 10‑stage pipeline, epistemic invariants.
- [`ARBITRATION.md`](./ARBITRATION.md) — conflict resolution between concurrent diffs.
- [`KNOWLEDGE_DIFF_SCHEMA.md`](./KNOWLEDGE_DIFF_SCHEMA.md) — formal diff schema.