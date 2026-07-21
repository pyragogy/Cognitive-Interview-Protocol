# Cognitive Interview Protocol for Dynamic Knowledge Mapping

## Core Concept
Traditional AI tutors act as authoritative sources of knowledge. The **Pyragogical Cognitive Interviewer** flips this dynamic by using cognitive interviewing techniques (originally developed for memory retrieval in investigative settings) to elicit, extract, and structure tacit human knowledge.

## The 4 Interview Phases

### 1. Context Reinstatement
* **Goal:** Ground the conversation in practical human experience.
* **Agent Strategy:** Ask the user to describe the real-world environment where they encounter or apply the topic.

### 2. Free Recall / Structural Elicitation
* **Goal:** Allow unconstrained mental mapping without cognitive bias from the AI.
* **Agent Strategy:** Present the draft graph as flawed/incomplete. Prompt the user to identify missing links, incorrect prerequisites, or outdated concepts without interrupting.

### 3. Perspective Shift
* **Goal:** Test node resiliency and surface hidden edge cases.
* **Agent Strategy:** Ask "what if" and counterfactual questions:
  * *"If we remove concept X, what happens to concept Y?"*
  * *"How would a beginner vs an expert navigate this transition?"*

### 4. Reverse Trace (Dependency Verification)
* **Goal:** Audit prerequisites and graph directionality.
* **Agent Strategy:** Walk backwards from terminal node to root node, asking the user to validate each step in reverse order.

## Schema Versioning Policy
Nodes and edges are never hard-deleted during live sessions. Updates are tracked via audit states:
* `existing`: Unchanged baseline item.
* `added`: New concept introduced by the user.
* `modified`: Label, description, or tag changed.
* `removed`: Marked as deprecated or invalid by the user (retained in historical record).

## Validation: Automatic vs. Manual

### Automated Validation (v0.2 Capability)

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

### Manual Validation (v0.2 Requirement)

These checks require human judgment during the review stage:

| Check | Reviewer Responsibility |
|-------|-------------------------|
| Evidence Quality | Does the interview exchange support the proposed change? Read the transcript. |
| Section Fit | Is the change in the correct section? (e.g., Definition change shouldn't be in Risk) |
| Graph Consistency | Does the change affect wikilinks in a way that breaks other nodes? |
| Rationale Strength | Can a future reader understand why the change was made? |
| Confidence Level Justification | Is the confidence rating (`high`/`medium`/`low`) appropriately supported? |

### Why This Distinction Matters

- **Automated checks** prevent malformed diffs from reaching human reviewers
- **Manual checks** ensure epistemic rigor (evidence quality, rationale strength)
- The protocol requires both — automation alone cannot assess *whether* a change is *good*, only *whether* it is *valid*
