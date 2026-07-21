# <img src="https://pyragogy.org/images/logo.svg" alt="Pyragogy" width="32"/> Cognitive Interview Protocol v0.2.1

<div align="center">

[![Status](https://img.shields.io/badge/status-Standby%20%2F%20Open%20Reference%20Architecture-purple?style=flat-square)](docs/ROADMAP.md)
[![Version](https://img.shields.io/badge/version-v0.2.1-blue?style=flat-square)](docs/PROTOCOL.md)
[![License](https://img.shields.io/badge/license-MIT-007bff?style=flat-square)](LICENSE)
[![Contributions](https://img.shields.io/badge/contributions-welcome-28a745?style=flat-square)](CONTRIBUTING.md)

</div>

---

## 🎯 Elevator Pitch

The **Cognitive Interview Protocol (CIP)** is a methodology for conducting structured AI-assisted interviews that produce *knowledge diffs* — bounded, human-reviewable proposals for modifying knowledge graphs.

**Traditional AI tutoring** treats the AI as an authoritative source of knowledge, either editing the graph directly (losing reasoning) or producing free-form output (lacking structure).

**CIP flips the paradigm**: The AI acts as a *co-learner facilitator*, using cognitive interview techniques (originally from forensic psychology) to elicit tacit expertise through 4 evidence-gathering phases. Every interview produces a traceable, reviewable knowledge change proposal.

The result isn't an automatic edit — it's a **reviewable proposal** that can be validated, accepted, or rejected by human reviewers. Knowledge evolves through evidence, not authority.

---

## 📋 Repository Structure

```
Cognitive-Interview-Protocol/
├── README.md                          ← This file — quick start guide
├── CONTRIBUTING.md                    ← How to contribute (analytical > implementational)
├── LICENSE                            ← MIT License
│
├── 🌐 DOCS (Protocol & Specifications)
│   ├── PROTOCOL.md                    ← Main protocol spec (10-stage pipeline)
│   ├── SYLLABUS_SCHEMA.md             ← 7-section node structure
│   ├── GLOSSARY.md                    ← Terminology with coinage flags
│   ├── ROADMAP.md                     ← Research milestones & open questions
│   └── archive/
│       ├── V0.1/                      ← Early design documents
│       ├── YAML_SCHEMA.md             ← Knowledge Diff YAML schema (v0.2)
│       ├── PIPELINE.md                ← 10-stage pipeline details
│       ├── KNOWLEDGE_DIFF_SPEC.md     ← Diff format specification
│       ├── INTERVIEW_GUIDE.md         ← 5 question types mapping
│       ├── PRINCIPLES.md              ← 6 epistemic invariants
│       ├── PROBLEM.md                 ← Problem statement
│       └── VISION.md                  ← Long-term direction
│
├── 🧪 EXAMPLES (Worked Demonstrations)
│   └── diff-001-embodied-foundation/  ← Complete annotated example
│       ├── README.md                  ← Example overview
│       ├── context.md                 ← Interview flow documentation
│       ├── review-notes.md            ← Simulated reviewer response
│       ├── transcript.md              ← Synthetic interview transcript
│       ├── evidence.md                ← Evidence bundle (exchanges → sections)
│       └── diff.yaml                  ← Knowledge Diff in spec format
│
├── 🔧 WORKFLOWS (n8n Automation)
│   └── syllabus_co_creation_agent.json
│       └── AI-assisted interview orchestrator with graph validation
│
├── 📝 PROTOCOL (Quick Reference)
│   └── cognitive_interview_spec.md    ← 4-phase protocol + validation
│
├── 📊 ARCHIVES (Audit Trail)
│   ├── interviews/                    ← Session transcripts & evidence bundles
│   └── diffs/                         ← Knowledge Diff YAML files (audit trail)
│
├── 📈 DIAGRAMS (Visual representations)
└── 📚 PAPERS (Preprints & working papers)
```

---

## ⚡ Quick Start for Implementers

### 1️⃣ Import the n8n Workflow

```bash
# Install n8n (if not already)
npm install --global n8n

# Start n8n server
n8n start
```

Then in the n8n UI:
- Go to **Settings** → **Import**
- Upload `workflows/syllabus_co_creation_agent.json`
- Or use CLI: `n8n import:workflow --input=workflows/syllabus_co_creation_agent.json`

### 2️⃣ Configure Credentials

In n8n credentials store:
- **Add OpenAI API key** (required for GPT-4o-mini interview analysis)
- **Update credentials reference** in workflow node "Analyze Co-creation & Update Syllabus"

### 3️⃣ Test the Workflow

```bash
# Send a test session to the webhook
curl -X POST http://localhost:5678/webhook/test-session \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-001",
    "topic": "networking_fundamentals",
    "transcript": "[exchange-01] User explains their experience with networking..."
  }'
```

---

## 🔍 Technical Highlights

### 4-Phase Cognitive Interview Protocol

| Phase | Goal | Agent Strategy |
|-------|------|----------------|
| **1. Context Reinstatement** | Ground in real-world experience | Ask user to describe practical contexts |
| **2. Free Recall / Mapping** | Unconstrained mental mapping | Present graph as incomplete; prompt identification of gaps |
| **3. Perspective Shift** | Test resiliency & edge cases | Ask "what if" and counterfactual questions |
| **4. Reverse Trace** | Audit prerequisites & directionality | Walk backwards from terminal to root node |

### Graph Consistency Validation (n8n Workflow)

The workflow performs **automated validation** before human review:

| Check | Description | Failure Reason |
|-------|-------------|----------------|
| **JSON Schema Compliance** | YAML structure matches schema | `yaml_schema_invalid` |
| **Required Fields** | All mandatory fields present | `missing_required_fields` |
| **Status Tags** | Only `existing`, `added`, `modified`, `removed` allowed | `invalid_status` |
| **Section Changes ≤ 3** | Bounded Modification Principle | `scope_too_broad` |
| **Circular References** | No dependency cycles in connections | `circular_dependency_detected` |
| **Orphan Nodes** | All nodes must have connections | `orphan_nodes_detected` |
| **Prerequisite Validity** | Connection references must exist | `prerequisite_invalid` |

### Knowledge Diff Format

A `Knowledge Diff` is a structured proposal for modifying a knowledge graph node section:

```yaml
id: "diff-2026-06-29-001"
protocol_version: "CIP-KGE-v0.2"
session_id: "session-2026-06-29-001"

target_node:
  path: "05_systemic_risks/automation_bias"
  operation: "modify"

section_changes:
  - section: "observable_markers"
    operation: "modify"
    current_text: "Current text..."
    proposed_text: "New text..."
    rationale: "Why this change..."

evidence:
  session_exchange_ref: "session-2026-06-29-001/exchange-01"
  summary: "What user said..."
  confidence: "medium"
  confidence_rationale: "Justification..."

pre_review_check:
  passes_minimum_quality: true
```

---

## 📚 Core Principles

| # | Principle | What it rules out |
|---|-----------|-------------------|
| **1** | Knowledge evolves through evidence | Model confidence as grounds for change |
| **2** | Every modification must be independently reviewable | Changes requiring original session access |
| **3** | AI proposes; humans validate | Automated incorporation of AI output |
| **4** | Interviews generate *knowledge diffs*, not automatic edits | Direct write access for AI system |
| **5** | Protocol is model-agnostic | Dependency on any specific platform/API |

Full rationale: [`docs/archive/PRINCIPLES.md`](docs/archive/PRINCIPLES.md)

---

## 🎓 Research Questions

CIP is an **open research initiative** — these questions drive ongoing development:

- Can AI-assisted interviews surface **tacit expert knowledge** that structured questionnaires miss?
- How should a *knowledge diff* be represented to remain both **machine-readable** and **human-auditable**?
- What role should **human review** play — final gate, continuous process, or something else?
- Which interview techniques produce the **highest-quality proposals**?
- What does it mean for a knowledge update to be ***reliable*** in this setting?
- How can the process remain **reproducible** across different AI platforms?

Full discussion: [`docs/ROADMAP.md`](docs/ROADMAP.md)

---

## 📖 Protocol Specification

**Current Version:** v0.2.1  
**Status:** Standby / Open Reference Architecture  
**Next Phase:** Pilot Sessions (v0.2 validation)

The protocol is implemented in two complementary artifacts:

1. **[docs/PROTOCOL.md](docs/PROTOCOL.md)** — The 10-stage pipeline specification
2. **[protocol/cognitive_interview_spec.md](protocol/cognitive_interview_spec.md)** — Quick reference for 4-phase protocol

See also:
- [docs/SYLLABUS_SCHEMA.md](docs/SYLLABUS_SCHEMA.md) — Node structure (7 sections)
- [docs/GLOSSARY.md](docs/GLOSSARY.md) — Terminology & definitions

---

## 🤝 How to Participate

> [!IMPORTANT]  
> At this stage, the most valuable contributions are **analytical**, not implementational.

This is a research project, not a software product. We need:

- **🔍 Critique of the protocol design** — identify structural flaws and explain why they matter
- **📝 Alternative framings** — better ways to pose the research questions
- **🎙️ Interview transcripts** — share real or simulated sessions (even if they didn't go well)
- **📚 Literature connections** — point to relevant work in knowledge engineering or epistemology
- **⚠️ Counterexamples** — cases where the approach would not work

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for full guidelines.

**→ [Open an issue](../../issues/new) to start a discussion**

---

## 🏛️ Credits

**Author:** Fabrizio Terzi  
**Affiliation:** Pyragogy ([https://pyragogy.org](https://pyragogy.org))  
**License:** [MIT](LICENSE)

---

<div align="center" style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #e1e4e8;">

**Cognitive Interview Protocol** — Evidence-based knowledge evolution for AI-augmented learning  
© 2026 Pyragogy · [Apache 2.0](LICENSE)

</div>
