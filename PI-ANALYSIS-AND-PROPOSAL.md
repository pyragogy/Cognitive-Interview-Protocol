# PI-ANALYSIS-AND-PROPOSAL: Cognitive Interview Protocol Repository

**Generated:** 2025-07-21  
**Analyst:** PI Coding Agent  
**Repository:** `Cognitive-Interview-Protocol`  

---

## Executive Summary

This repository houses the **Cognitive Interview Protocol for Knowledge Graph Evolution (CIP-KGE)**, an open research initiative by Pyragogy aiming to establish a rigorous, traceable methodology for AI-assisted knowledge evolution.

The protocol is at **v0.2 (Phase 2: Pilot Sessions)** — the design phase is complete, and real-world validation is the next milestone. The repository is remarkably well-structured, but several high-impact improvements can be implemented *now* to solidify it as the definitive artifact for Pyragogy's future.

---

## 1. ANALYSIS OF INTENT AND STRUCTURE

### 1.1 Vision and Core Intent

The project addresses a fundamental tension in AI-augmented knowledge systems:

| **Dominant Pattern** | **Problem** | **CIP-KGE's Third Path** |
|----------------------|-------------|--------------------------|
| Model edits directly | Reasoning buried in logs | Every modification is independently reviewable |
| Model produces free-form output | No structured artifact, no audit trail | Output is a *Knowledge Diff* — a bounded, traceable proposal |

**The Core Question:** *How can AI-assisted interviews produce reliable, reviewable proposals for the evolution of a knowledge graph?*

### 1.2 The Pyragogical Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Pyragogy Syllabus (knowledge graph)                  │
│                     https://syllabus.pyragogy.org                            │
│  Source: https://github.com/pyragogy/ai-pedagogy                           │
│  Format: Quartz v5 (Markdown + Frontmatter)                                 │
└────────────────────┬────────────────────────────────────────────────────────┘
                     │
                     │ Update Trigger
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CIP-KGE Pipeline (10 stages)                             │
│  1. Session Preparation  →  2. Interview Session  →  3. Evidence Extraction │
│  4. Knowledge Diff → 5. Pre-Review Check → 6. Human Review                 │
│  7. Markdown Transform → 8. Pull Request → 9. Syllabus Update → 10. Archival│
└────────────────────┬────────────────────────────────────────────────────────┘
                     │
                     │ User Input
                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│              Cognitive Interview Protocol (4 Phases)                        │
│  1. Context Reinstatement  →  2. Free Recall / Mapping                     │
│  3. Perspective Shift      →  4. Reverse Trace (Dependency Verification)   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.3 Integration Points

**n8n Workflow (`workflows/syllabus_co_creation_agent.json`)** implements a *partial pipeline automation*:
- Handles interview session orchestration (webhook → wait → resume)
- Integrates with GPT-4o-mini for transcript analysis
- Validates output JSON schema
- Routes success/failure paths

**Documented Protocol (`docs/PROTOCOL.md`)** provides the *human-executable methodology*:
- 10-stage pipeline with failure conditions
- 5 question types mapped to 7 node sections
- Knowledge Diff YAML specification
- Pre-review quality check criteria

**The Gap:** The n8n workflow is *not* fully aligned with the documented protocol. It automates only the interview and analysis phases, leaving human review and transformation manual — which is intentional per the spec (v0.2), but creates confusion.

---

## 2. TECHNICAL AND DOCUMENTARY AUDIT

### 2.1 Code Quality Assessment

| **Component** | **Status** | **Notes** |
|---------------|------------|-----------|
| `workflows/syllabus_co_creation_agent.json` | ✅ Well-structured | Clean node separation, good error handling |
| Validation code (Node "Validate Syllabus JSON") | ✅ Comprehensive | Checks JSON parsing, required keys, status tags |
| Prompt engineering (Agent "Prepare Syllabus Agent") | ✅ Strong | 4-phase interview framework embedded in system prompt |
| YAML diff files (`diffs/diff-2026-06-29-001.yaml`) | ✅ Spec-compliant | FollowsKnowledge Diff format exactly |
| Example artifacts (`examples/diff-001-embodied-foundation/`) | ⚠️ Incomplete | Missing `context.md`, `review-notes.md` per spec |

### 2.2 Schema and Data Integrity

**Syllabus Node Schema (7 sections):**
1. Definition (boundary-setting)
2. Use Case (trigger conditions)
3. Human Role (observable behaviors)
4. AI Role (constraints/affordances)
5. Friction (mechanism of resistance)
6. Risk (failure modes)
7. Observable Markers (verification evidence)

**ValidationGaps Identified:**

| **Issue** | **Location** | **Impact** | **Urgency** |
|-----------|--------------|------------|-------------|
| No YAML schema validator | Protocol spec | Manual validation required | Medium |
| No automated pre-review check | Workflow node missing | Reviewer burden increased | High |
| Missing `context.md` in example | `examples/diff-001-embodied-foundation/` | Onboarding confusion | Low |
| Status tags not enforced in n8n JSON | Validation code | Could allow invalid states | Medium |

### 2.3 Documentative Consistency

**Strengths:**
- Clear separation between protocol design (`docs/`) and implementation (workflows/)
- Glossary explicitly marks project coinage vs. established field terms
- Roadmap transparently distinguishes design phase from pilot phase
- Contributing guide correctly sets expectations (analytical > implementational)

**Inconsistencies:**

1. **README.md vs. Protocol:**
   - README states "v0.2. Research Draft" 
   - Protocol references "CIP-KGE v0.2" 
   - Roadmap shows "Phase 1 (complete)" but no v0.1 artifacts exist
   - **Recommendation:** Add `docs/V0.1-ARCHIVE.md` preserving v0.1 seed document if it exists elsewhere

2. **Protocol spec L1-L4 limitations:**
   - "One session, one diff" constraint is reasonable for v0.2
   - "No automated quality validation" is explicitly flagged as v0.3 candidate
   - **However:** The n8n workflow *does* include validation code — this creates confusion about what "automated" means

3. **Interview Guide terminology:**
   - Five question types (Q1-Q5) defined in protocol
   - n8n workflow system prompt references "4 phases" but not question types
   - **Recommendation:** Align workflow prompts with documented question types

---

## 3. EDGE CASES AND VULNERABILITIES

### 3.1 Critical Edge Cases

| **Edge Case** | **Current Handling** | **Risk** |
|---------------|----------------------|----------|
| Interviewee introduces new node (not in graph) | Not covered in spec | Diff rejected as invalid target |
| Interviewee requests new graph section (e.g., `06_institutional_contexts/`) | Protocol states "structural change above node level" | Requires manual intervention |
| Confidence rating is "low" without corroboration | `confidence_rationale` required but not validated | Reviewer must catch this |
| Multiple reviewers disagree on diff acceptance | Protocol has no conflict resolution process | Stalls pipeline |

### 3.2 Technical Edge Cases (n8n Workflow)

| **Scenario** | **Workflow Behavior** | **Issue** |
|--------------|----------------------|-----------|
| Transcript missing exchange numbers | Workflow proceeds (no validation) | Downstream diff generation fails |
| GPT-4o-mini returns malformed JSON | Validation node catches error → goes to "Validation Failed Log" | Correct, but error message could be more helpful |
| User session_id conflicts with existing session | No duplicate check in workflow | Could overwrite evidence bundle |
| Baseline syllabus has circular references | No validation for graph consistency | Could produce invalid diff |

---

## 4. PROPOSAL OF VALUE: "THE LAST BEAT" IMPROVEMENTS

### 4.1 Priority 1: Fix Protocol Specification Gaps (High Impact, Low Effort)

#### 4.1.1 Add v0.1 Archive

**Problem:** Protocol references v0.1 but only `CIP_v0.1.md` (seed document) exists in root. No actual v0.1 documentation exists.

**Action:**
```bash
# Create archive directory for early design docs
mkdir -p docs/archive/V0.1

# Move and rename existing seed document
mv CIP_v0.1.md docs/archive/V0.1/SEED.md
```

**Update `README.md`:**
```markdown
> **v0.1 (2026-06)** Generic protocol. Three-component structure (interview, diff, pipeline).
```

**Impact:** Historical continuity for researchers tracing protocol evolution.

---

#### 4.1.2 Add YAML Schema Validator

**Problem:** Protocol states "No automated quality validation" as a v0.3 limitation, but the n8n workflow *does* validate JSON. This creates confusion about what "automated" means.

**Action:** Create a YAML schema validator for Knowledge Diffs.

**File:** `docs/archive/YAML_SCHEMA.md`

```yaml
# YAML Schema for Knowledge Diff (CIP-KGE v0.2)

id:
  type: string
  pattern: "^diff-\\d{4}-\\d{2}-\\d{2}-\\d{3}$"

protocol_version:
  type: string
  enum: ["CIP-KGE-v0.1", "CIP-KGE-v0.2"]

session_id:
  type: string
  pattern: "^session-\\d{4}-\\d{2}-\\d{2}-\\d{3}$"

target_node:
  type: object
  required: [path, operation]
  properties:
    path:
      type: string
      pattern: "^[0-9]{2}_\\w+/\\w+$"  # section_prefix/node_id
    operation:
      type: string
      enum: ["add", "modify", "remove", "deprecate"]

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
      operation:
        type: string
        enum: ["modify", "append", "remove_sentence"]
      confidence:
        type: string
        enum: ["high", "medium", "low"]
        required: [confidence, confidence_rationale]

# ... (full schema in YAML)
```

**Impact:** Enables automated pre-review checks, reduces human reviewer burden.

---

#### 4.1.3 Clarify "Automated Validation" Definition

**Action:** Add a section to `docs/PROTOCOL.md`:

```markdown
## Automated vs. Manual Validation

**Automated validation** (v0.2 capability):
- YAML schema compliance checking (file format, required fields)
- JSON parsing validation (n8n workflow)
- Structural checks (e.g., exchange references exist in transcript)

**Manual validation** (v0.2 requirement):
- Evidence quality assessment (does the interview exchange support the change?)
- Section fit evaluation (is the change in the correct section?)
- Graph consistency judgment (does the change affect wikilinks correctly?)
- Rationale strength assessment (can a future reader understand why?)

The n8n workflow performs automated validation; manual validation remains human-executed per v0.2 spec.
```

**Impact:** Eliminates confusion about what automation is possible at v0.2.

---

### 4.2 Priority 2: Implement Missing Example Artifacts (Medium Impact, Low Effort)

**Problem:** Example `diff-001-embodied-foundation` is incomplete per its own README:

```
examples/
└── example-001-[short-description]/
    ├── README.md           ← what this example demonstrates
    ├── diff.yaml           ← the knowledge diff itself
    ├── context.md          ← the interview exchange that generated the diff  ← MISSING
    └── review-notes.md     ← simulated or real reviewer response            ← MISSING
```

**Action:** Create missing files:

**File:** `examples/diff-001-embodied-foundation/context.md`
```markdown
# Interview Context — Example 001

**Node:** `02_ontogeny/embodied_foundation`
**Target section:** `definition`
**Interview type:** Solo-agent validation (no external interviewee)
**Epistemic constraint:** Every claim must be traceable to either (a) current node text, (b) published literature, or (c) logical derivation

** Interview flow:**
1. Elicitation (Q1): Broad question about what "embodied" means in this context
2. Clarification (Q2): Probe "sensory-motor inquiry" vs. "screen-mediated abstraction"
3. Socratic (Q3): What if the concept was removed? What breaks?
4. Mapping (Q5): How does this connect to `adolescent_sparring_arena`?

**Evidence extraction:**
- exchange-01: Q1 elicitation → definition boundary
- exchange-02: Q2 clarification → operationalization
- exchange-03: Q3 Socratic → failure modes
- exchange-04: Q5 mapping → graph relationships
```

**File:** `examples/diff-001-embodied-foundation/review-notes.md`
```markdown
# Review Notes — Example 001

**Reviewer:** CIP-KGE validation run 001  
**Date:** 2026-06-29  
**Status:** Accepted (illustrative only — not a real session)

**Review criteria:**

1. **Evidence quality** — The synthetic interview contains coherent reasoning, but since there is no external interviewee, this is a demonstration, not empirical evidence.

2. **Section fit** — The proposed change targets `definition` section correctly. The current text describes the node's *what*, and the proposed text refines the boundary.

3. **Graph consistency** — No new wikilinks introduced. No other nodes affected.

4. **Rationale strength** — The rationale explains why the change improves precision. The derivation from "sensory-motor inquiry" to "physical manipulation and friction" is clear.

**Recommendation:** Accept for illustrative purposes only. Do not merge into `ai-pedagogy` without a real interview session.

**Open questions:**
- Is "physical manipulation and friction" too vague? Should it be operationalized further?
- Does the proposed definition capture what makes `embodied_foundation` distinct from `adolescent_sparring_arena`?
```

**Impact:** Completes the example per protocol spec, aids onboarding.

---

### 4.3 Priority 3: Add Pre-Review Check Node to n8n Workflow (High Impact, Medium Effort)

**Problem:** The protocol specifies pre-review quality checks (Stage 5), but the n8n workflow does not implement this. Reviewers must manually check the diff YAML.

**Action:** Add a new workflow node before "Syllabus Valid?":

**Node:** "Pre-Review Quality Check"

**Parameters:**
```javascript
// Pre-Review Quality Check
// Implements CIP-KGE v0.2 Stage 5: Pre-Review Quality Check

const diff = $json.updated_syllabus || $json;

// 1. Required fields check
const REQUIRED_FIELDS = ['id', 'protocol_version', 'session_id', 'target_node', 'section_changes', 'evidence', 'pre_review_check'];
const missingFields = REQUIRED_FIELDS.filter(f => !(f in diff));
if (missingFields.length > 0) {
  return {
    json: {
      ...$json,
      pre_review_result: {
        passes_minimum_quality: false,
        failure_reason: `missing_required_fields: ${missingFields.join(', ')}`
      }
    }
  };
}

// 2. Section changes count check (Bounded Modification Principle)
if (Array.isArray(diff.section_changes) && diff.section_changes.length > 3) {
  return {
    json: {
      ...$json,
      pre_review_result: {
        passes_minimum_quality: false,
        failure_reason: 'scope_too_broad'
      }
    }
  };
}

// 3. Confidence level check
if (diff.evidence.confidence === 'low' && !diff.evidence.confidence_rationale) {
  return {
    json: {
      ...$json,
      pre_review_result: {
        passes_minimum_quality: false,
        failure_reason: 'low_confidence_without_rationale'
      }
    }
  };
}

// 4. Target node existence check (if not 'add' operation)
// Note: This requires API call to syllabus.pyragogy.org or local node index
// For v0.2, we can only check format compliance
if (diff.target_node.operation !== 'add') {
  const pathPattern = /^[0-9]{2}_\w+\/\w+$/;
  if (!pathPattern.test(diff.target_node.path)) {
    return {
      json: {
        ...$json,
        pre_review_result: {
          passes_minimum_quality: false,
          failure_reason: 'target_node_path_invalid_format'
        }
      }
    };
  }
}

// All checks passed
return {
  json: {
    ...$json,
    pre_review_result: {
      passes_minimum_quality: true,
      failure_reason: null
    }
  }
};
```

**Impact:** Reduces reviewer burden, catches errors before human review.

---

### 4.4 Priority 4: Add Node Version Validation (High Impact, Medium Effort)

**Problem:** Workflow validates JSON schema but does not check if baseline syllabus node version matches current published version.

**Action:** Add a new node "Fetch Current Syllabus Node" before "Load Draft Syllabus":

**Node:** "Fetch Current Syllabus Node"

**Parameters:**
```javascript
// Fetch Current Syllabus Node
// Get the current version of the target node from syllabus.pyragogy.org
// This ensures the baseline is current before interview begins

const targetPath = $json.baseline_syllabus?.target_node?.path || '05_systemic_risks/automation_bias';

try {
  // Fetch from published syllabus (this would be replaced with actual API call)
  const response = await fetch(`https://syllabus.pyragogy.org/${targetPath}.json`);
  const currentNode = await response.json();
  
  return {
    json: {
      ...$json,
      current_node_version: currentNode.version,
      current_node_text: currentNode.content,  // Full markdown content
      baseline_version_match: $json.baseline_syllabus.version === currentNode.version
    }
  };
} catch (error) {
  return {
    json: {
      ...$json,
      fetch_error: error.message,
      baseline_version_match: null  // Could not verify
    }
  };
}
```

**Then add validation:**
```javascript
// Baseline Version Check
if (!$json.baseline_version_match) {
  return {
    json: {
      ...$json,
      version_mismatch_warning: true,
      suggestion: 'Proceed with caution — baseline syllabus version does not match current published version'
    }
  };
}
```

**Impact:** Prevents working with stale baseline, ensures diffs are targeted at correct version.

---

### 4.5 Priority 5: Add Graph Consistency Validator (High Impact, High Effort)

**Problem:** No automated check for wikilink target existence or graph-level consistency.

**Action:** Create a "Graph Consistency Validator" node:

**Node:** "Graph Consistency Validator"

**Parameters:**
```javascript
// Graph Consistency Validator
// Check for:
// 1. Wikilink targets exist in graph
// 2. No circular references in proposed connections
// 3. Prerequisites are consistent (no node depends on non-existent node)

const diff = $json.updated_syllabus || $json;
const errors = [];

// 1. Check wikilinks in proposed_text
const wikilinkRegex = /\[\[(.*?)\]\]/g;
let match;
while ((match = wikilinkRegex.exec(diff.proposed_text || '')) !== null) {
  const targetNode = match[1];
  // In production, this would check against node index or API
  // For now, we just flag that verification is needed
  if (!targetNode.match(/^[0-9]{2}_\w+\/\w+$/)) {
    errors.push(`Invalid wikilink target format: [[${targetNode}]]`);
  }
}

// 2. Check connections for circular references
if (Array.isArray(diff.nodes)) {
  const nodeIds = new Set(diff.nodes.map(n => n.id));
  
  // Build dependency graph
  const dependencies = new Map();
  diff.connections?.forEach(conn => {
    if (!dependencies.has(conn.to)) {
      dependencies.set(conn.to, new Set());
    }
    dependencies.get(conn.to).add(conn.from);
  });
  
  // Detect cycles
  const visited = new Set();
  const recursionStack = new Set();
  
  function hasCycle(nodeId) {
    if (recursionStack.has(nodeId)) return true;
    if (visited.has(nodeId)) return false;
    
    visited.add(nodeId);
    recursionStack.add(nodeId);
    
    const deps = dependencies.get(nodeId) || new Set();
    for (const dep of deps) {
      if (hasCycle(dep)) return true;
    }
    
    recursionStack.delete(nodeId);
    return false;
  }
  
  for (const nodeId of nodeIds) {
    if (hasCycle(nodeId)) {
      errors.push(`Circular dependency detected involving node: ${nodeId}`);
      break;
    }
  }
}

// 3. Check prerequisite consistency
if (Array.isArray(diff.nodes) && Array.isArray(diff.connections)) {
  const nodeMap = new Map(diff.nodes.map(n => [n.id, n]));
  
  diff.connections?.forEach(conn => {
    if (!nodeMap.has(conn.from)) {
      errors.push(`Connection references non-existent node: ${conn.from}`);
    }
    if (!nodeMap.has(conn.to)) {
      errors.push(`Connection references non-existent node: ${conn.to}`);
    }
  });
}

return {
  json: {
    ...$json,
    graph_consistency: {
      isValid: errors.length === 0,
      errors: errors
    }
  }
};
```

**Impact:** Prevents malformed diffs from being submitted, improves graph integrity.

---

## 5. IMPLEMENTATION ROADMAP

### Phase A: Protocol Clarification (Week 1)
1. ✅ Add v0.1 archive
2. ✅ Create YAML schema validator spec
3. ✅ Clarify automated vs. manual validation

### Phase B: Example Completion (Week 1-2)
4. ✅ Create missing example files (`context.md`, `review-notes.md`)

### Phase C: Workflow Enhancement (Week 2-3)
5. ✅ Implement Pre-Review Quality Check node
6. ✅ Add Baseline Version Check node
7. ✅ Add Graph Consistency Validator node

### Phase D: Testing & Documentation (Week 3-4)
8. ✅ Test enhanced workflow with real interview data
9. ✅ Update protocol documentation
10. ✅ Create "CIP-KGE v0.2.1" release notes

---

## 6. CONCLUSION

The Cognitive Interview Protocol repository is **exceptionally well-structured** for a research draft. The distinction between protocol design and implementation is clear, the documentation is thorough, and the example artifacts demonstrate deep understanding of the methodology.

The proposed improvements focus on **closing the gap** between the protocol's aspirations (traceability, reviewability) and its current implementation (manual validation, incomplete examples). These changes do not alter the methodology — they strengthen its execution.

**Ultimate Goal:** Transform this repository into the **definitive artifact** for Pyragogy's future — a clean, self-documenting, rigorously validated foundation for knowledge evolution.

The last beat is not about perfection — it's about **rigor**.

---

*Generated by PI Coding Agent on 2025-07-21*  
*Repository: `Cognitive-Interview-Protocol`*  
*Protocol Version: CIP-KGE v0.2 (Phase 2: Pilot Sessions)*
