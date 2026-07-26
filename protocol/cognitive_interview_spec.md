# Cognitive Interview Protocol for Knowledge Graph Evolution (CIP‑KGE)

## Core concept

Traditional AI tutors act as authoritative sources of knowledge, editing graphs directly (losing reasoning) or producing free‑form output (lacking structure).

**CIP‑KGE flips the paradigm:** AI acts as a **structured interviewer** using cognitive techniques (originally from forensic psychology) to elicit tacit expertise through four evidence‑gathering phases. The output is a **Knowledge Diff** — a bounded, reviewable proposal, not an automatic edit.

**Critical constraint:** The LLM component (if used) is confined to **Stage 3: Evidence Extraction**. All subsequent stages — diff generation, pre‑review checks, human review, markdown transformation — are **human‑executed**. Automation is limited to syntactic validation.

---

## The 4 interview phases

### 1. Context Reinstatement
* **Goal:** Ground the conversation in practical human experience.
* **Agent Strategy:** Ask the user to describe the real‑world environment where they encounter or apply the topic.
* **Transition condition:** Move to Phase 2 when the interviewee has described at least one concrete scenario.

### 2. Free Recall / Structural Elicitation
* **Goal:** Allow unconstrained mental mapping without cognitive bias from the AI.
* **Agent Strategy:** Present the draft graph as flawed/incomplete. Prompt the user to identify missing links, incorrect prerequisites, or outdated concepts without interrupting.
* **Transition condition:** Move to Phase 3 when the interviewee has identified at least one gap or inconsistency.

### 3. Perspective Shift
* **Goal:** Test node resiliency and surface hidden edge cases.
* **Agent Strategy:** Ask "what if" and counterfactual questions:
  * *"If we remove concept X, what happens to concept Y?"*
  * *"How would a beginner vs an expert navigate this transition?"*
* **Transition condition:** Move to Phase 4 when at least one counterfactual reveals a boundary condition.

### 4. Reverse Trace (Dependency Verification)
* **Goal:** Audit prerequisites and graph directionality.
* **Agent Strategy:** Walk backwards from terminal node to root node, asking the user to validate each step in reverse order.
* **Termination condition:** Session ends when the interviewee confirms or corrects the dependency chain.

---

## Validation: automated vs manual (v0.2)

### Automated validation (syntactic)

These checks are performed programmatically by the n8n workflow or YAML validators:

| Check | Implementation | Failure Reason |
|-------|----------------|----------------|
| YAML Schema Compliance | Schema validator (`docs/archive/YAML_SCHEMA.md`) | `yaml_schema_invalid` |
| JSON Parsing | Workflow validation node | `json_parse_error` |
| Required Fields | Workflow validation node | `missing_required_fields` |
| Section Changes Count | Workflow validation (`section_changes.length ≤ 3`) | `scope_too_broad` |
| Status Tags | Workflow validation (`existing`, `added`, `modified`, `removed`) | `invalid_status` |
| Wikilink Format | Workflow validation | `invalid_wikilink_format` |
| Circular References | Graph consistency validator (new) | `circular_dependency_detected` |
| Prerequisite Validity | Graph consistency validator (new) | `prerequisite_invalid` |

### Manual validation (epistemic)

These checks require human judgment during the review stage:

| Check | Reviewer Responsibility |
|-------|-------------------------|
| Evidence Quality | Does the interview exchange support the proposed change? Read the transcript. |
| Section Fit | Is the change in the correct section? (e.g., Definition change shouldn't be in Risk) |
| Graph Consistency | Does the change affect wikilinks in a way that breaks other nodes? |
| Rationale Strength | Can a future reader understand why the change was made? |
| Confidence Level Justification | Is the confidence rating (`high`/`medium`/`low`) appropriately supported? |

### Why this distinction matters

- **Automated checks** prevent malformed diffs from reaching human reviewers.
- **Manual checks** ensure epistemic rigor (evidence quality, rationale strength).
- The protocol requires both — automation alone cannot assess *whether* a change is *good*, only *whether* it is *valid*.

---

## Protocol adherence

**The n8n workflow (`workflows/syllabus_co_creation_agent.json`) implements only Stages 1‑3** (session prep, interview, evidence extraction). Stages 4‑10 remain manual.

**Do not mistake the workflow for a full implementation.** It is a **partial reference** that demonstrates the evidence‑extraction phase, not the end‑to‑end protocol.

---

## Schema versioning policy

Nodes and edges are never hard‑deleted during live sessions. Updates are tracked via audit states:
* `existing`: Unchanged baseline item.
* `added`: New concept introduced by the user.
* `modified`: Label, description, or tag changed.
* `removed`: Marked as deprecated or invalid by the user (retained in historical record).

These states are recorded in the Knowledge Diff's `section_changes` array and must be validated against the epistemic invariants (e.g., Bounded Modification Principle).
