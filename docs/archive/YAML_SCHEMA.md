# YAML Schema for Knowledge Diff (CIP-KGE v0.2)

> **Authoritative Reference:** `docs/archive/YAML_SCHEMA.md`
> 
> This schema defines the structure of Knowledge Diffs produced by the Cognitive Interview Protocol for Knowledge Graph Evolution (CIP-KGE).
> 
> **Validation Status:** Automated validation is performed at v0.2; manual validation remains required per protocol.

---

## Schema Version

```yaml
$schema: "https://pyragogy.org/schemas/knowledge-diff-v0.2.json"
$id: "https://pyragogy.org/schemas/knowledge-diff-v0.2.json"
title: "Knowledge Diff"
description: "A structured proposal for modifying a knowledge graph node section"
version: "CIP-KGE-v0.2"
```

---

## Top-Level Structure

```yaml
id:
  type: string
  pattern: "^diff-\\d{4}-\\d{2}-\\d{2}-\\d{3}$"
  description: "Unique identifier for the diff (e.g., diff-2026-06-29-001)"

protocol_version:
  type: string
  enum: ["CIP-KGE-v0.1", "CIP-KGE-v0.2"]
  description: "Protocol version that governs this diff"

session_id:
  type: string
  pattern: "^session-\\d{4}-\\d{2}-\\d{2}-\\d{3}$"
  description: "Reference to the interview session (e.g., session-2026-06-29-001)"

generated_at:
  type: string
  format: date-time
  description: "ISO 8601 timestamp when the diff was generated"
```

---

## Target Node

```yaml
target_node:
  type: object
  required: [path, operation]
  properties:
    path:
      type: string
      pattern: "^[0-9]{2}_\\w+/\\w+$"
      description: "Node path relative to content/ (e.g., 05_systemic_risks/automation_bias)"
    url:
      type: string
      format: uri
      description: "Published URL of the node"
    operation:
      type: string
      enum: ["add", "modify", "remove", "deprecate"]
      description: "Type of operation on the node"
```

---

## Section Changes

```yaml
section_changes:
  type: array
  minItems: 1
  maxItems: 3  # Bounded Modification Principle
  items:
    type: object
    required: [section, operation, proposed_text, rationale]
    properties:
      section:
        type: string
        enum: ["definition", "use_case", "human_role", "ai_role", "friction", "risk", "observable_markers"]
        description: "Target section of the node"
      operation:
        type: string
        enum: ["modify", "append", "remove_sentence"]
        description: "Type of change to apply"
      current_text:
        type: string
        description: "Exact current text of the section (required for modify/remove)"
      proposed_text:
        type: string
        description: "Replacement or addition text"
      rationale:
        type: string
        description: "Why this change improves the node; citation of session exchange"
      proposed_wikilinks:
        type: array
        items:
          type: string
          pattern: "^\\[\\[.*?\\]\\]$"
        description: "New wikilinks introduced, if any"
      confidence:
        type: string
        enum: ["high", "medium", "low"]
        description: "Confidence level for the proposed change"
      confidence_rationale:
        type: string
        description: "Justification for confidence level (required for 'low')"
```

---

## Evidence

```yaml
evidence:
  type: object
  required: [session_exchange_ref, summary, confidence, confidence_rationale]
  properties:
    session_exchange_ref:
      type: string
      pattern: "^session-\\d{4}-\\d{2}-\\d{2}-\\d{3}/exchange-\\d+(,\\s*exchange-\\d+)*$"
      description: "Reference to exchange(s) that ground this change"
    summary:
      type: string
      description: "What the interviewee said that grounds the change"
    confidence:
      type: string
      enum: ["high", "medium", "low"]
      description: "Confidence level for the evidence"
    confidence_rationale:
      type: string
      description: "Why this confidence level"
```

---

## Pre-Review Check

```yaml
pre_review_check:
  type: object
  required: [passes_minimum_quality]
  properties:
    passes_minimum_quality:
      type: boolean
      description: "Does the diff meet minimum quality thresholds?"
    failure_reason:
      type: string
      enum: [null, "no_evidence", "low_confidence_only", "target_not_found", "wikilink_target_missing", "scope_too_broad"]
      description: "Reason for failure (null if passes)"
    automated_checks:
      type: object
      properties:
        yaml_schema_valid:
          type: boolean
        required_fields_present:
          type: boolean
        section_changes_count_valid:
          type: boolean
        confidence_rationale_present:
          type: boolean
        target_node_format_valid:
          type: boolean
```

---

## Review

```yaml
review_status:
  type: string
  enum: ["proposed", "under_review", "accepted", "rejected", "deferred"]

review_notes:
  type: array
  items:
    type: object
    required: [reviewer, date, status_set, note]
    properties:
      reviewer:
        type: string
      date:
        type: string
        format: date
      status_set:
        type: string
        enum: ["proposed", "under_review", "accepted", "rejected", "deferred"]
      note:
        type: string
```

---

## Merge

```yaml
merge_ready:
  type: boolean

pr_url:
  type: string
  format: uri
  nullable: true
```

---

## Valid Examples

### Minimal Valid Diff (passes v0.2 automated validation)

```yaml
id: "diff-2026-06-29-001"
protocol_version: "CIP-KGE-v0.2"
session_id: "session-2026-06-29-001"
generated_at: "2026-06-29T10:45:00Z"

target_node:
  path: "05_systemic_risks/automation_bias"
  url: "https://syllabus.pyragogy.org/05_systemic_risks/automation_bias"
  operation: "modify"

section_changes:
  - section: "observable_markers"
    operation: "modify"
    current_text: "Current text here"
    proposed_text: "New text here"
    rationale: "Rationale for change"

evidence:
  session_exchange_ref: "session-2026-06-29-001/exchange-01"
  summary: "Summary of interview evidence"
  confidence: "medium"
  confidence_rationale: "Rationale for confidence"

pre_review_check:
  passes_minimum_quality: true
```

### Invalid Diff (fails automated validation)

```yaml
# ❌ FAILS: More than 3 section changes
section_changes:
  - section: "definition"
    operation: "modify"
    proposed_text: "..."
  - section: "use_case"
    operation: "modify"
    proposed_text: "..."
  - section: "human_role"
    operation: "modify"
    proposed_text: "..."
  - section: "ai_role"    # ❌ maxItems: 3 violated

# ❌ FAILS: confidence "low" without confidence_rationale
evidence:
  confidence: "low"  # ❌ requires confidence_rationale
```

---

## Automated Validation Rules (v0.2)

These checks are performed automatically by the n8n workflow:

| Check | Rule | Failure Reason |
|-------|------|----------------|
| **YAML Schema Valid** | Document parses as valid YAML and matches this schema | `yaml_schema_invalid` |
| **Required Fields Present** | All required fields at every level are present | `missing_required_fields` |
| **Section Changes Count** | `section_changes.length ≤ 3` | `scope_too_broad` |
| **Confidence Rationale** | If `evidence.confidence === "low"`, then `evidence.confidence_rationale` must exist | `low_confidence_without_rationale` |
| **Target Node Format** | `target_node.path` matches pattern `^[0-9]{2}_\w+/\w+$` | `target_node_path_invalid_format` |
| **Wikilink Targets** | All `[[node_id]]` in `proposed_text` target existing nodes | `wikilink_target_missing` |
| **Circular References** | No circular dependency in `connections` array | `circular_dependency_detected` |
| **Prerequisite Valid** | All `from` and `to` in `connections` reference existing nodes | `prerequisite_invalid` |

---

## Manual Validation Requirements (v0.2)

These checks require human judgment:

| Check | Reviewer Responsibility |
|-------|-------------------------|
| **Evidence Quality** | Does the interview exchange support the proposed change? Read the transcript. |
| **Section Fit** | Is the change in the correct section? (e.g., a Definition change shouldn't be in Risk) |
| **Graph Consistency** | Does the change affect wikilinks in a way that breaks other nodes? |
| **Rationale Strength** | Can a future reader understand why the change was made? |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v0.2 | 2026-06-29 | Initial published schema for CIP-KGE |
| v0.1 | 2026-06 | Draft schema (not published) |

---

**Note:** This schema is authoritative. Any Knowledge Diff that does not conform to this schema is considered malformed and should be returned to the author for revision.
