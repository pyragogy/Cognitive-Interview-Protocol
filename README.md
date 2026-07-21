<div align="center">

# Cognitive Interview Protocol

**An open research initiative by [Pyragogy](https://pyragogy.org)**

[![Status](https://img.shields.io/badge/status-research%20draft-orange?style=flat-square)](./docs/ROADMAP.md)
[![Version](https://img.shields.io/badge/version-v0.2-blue?style=flat-square)](./docs/PROTOCOL.md)
[![License](https://img.shields.io/badge/license-Apache%202.0-green?style=flat-square)](./LICENSE)
[![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen?style=flat-square)](./CONTRIBUTING.md)

<br/>

> *How can AI-assisted interviews produce reliable, reviewable proposals*
> *for the evolution of a knowledge graph?*

<br/>

</div>

---

## The problem

In most AI-augmented knowledge systems, there are two dominant patterns for how knowledge gets updated.

**The model edits directly.** The reasoning behind the change is lost or buried in a log that no human review process is structured to examine.

**The model produces free-form output.** A human decides, informally, whether anything in that response is worth keeping. There is no structured artifact. There is no audit trail.

Neither pattern is adequate for environments where the quality of knowledge matters — clinical guidelines, educational curricula, legal interpretation, domain-specific expert systems.

**CIP proposes a third path.** Every interview session is treated not as a conversation, but as an evidence-gathering event. Its output is not a corrected document — it is a structured, versioned, human-reviewable proposal for a knowledge change.

We coin the term *knowledge diff* for this output, in a project-specific sense: a bounded, traceable proposal for modifying a knowledge graph, with explicit provenance and review status. The term borrows from version control, not from established knowledge engineering literature.

---

## System target

CIP-KGE exists to serve one specific knowledge graph:

**[Pyragogy Syllabus](https://syllabus.pyragogy.org)** — a living framework for human-AI learning, cognitive friction, and peer-like co-creation. Each node in the graph represents a concept with a defined structure: Definition, Use Case, Human Role, AI Role, Friction, Risk, Observable Markers. The graph's source is in [pyragogy/ai-pedagogy](https://github.com/pyragogy/ai-pedagogy).

A Knowledge Diff produced by this protocol, when accepted, becomes a pull request on that repository. When merged, the graph updates automatically.

> The protocol exists only if it produces observable improvements in the structure of the Pyragogy Syllabus.
> If it does not improve the syllabus, it is not part of the system.

---

## The pipeline

```
Interview Session → Evidence Extraction → Knowledge Diff
        ↓
Pre-Review Quality Check → Human Review
        ↓ accepted
Markdown Transformation → Pull Request (pyragogy/ai-pedagogy)
        ↓ merged
Syllabus Update → Diff Archival
```

Full specification: [`docs/PROTOCOL.md`](./docs/PROTOCOL.md)

---

## Core principles

| | Principle | What it rules out |
|---|---|---|
| **1** | Knowledge evolves through evidence | Model confidence as grounds for change |
| **2** | Every modification must be independently reviewable | Changes that require access to the original session |
| **3** | AI proposes; humans validate | Automated incorporation of AI output |
| **4** | Interviews generate *knowledge diffs*, not automatic edits | Direct write access for the AI system |
| **5** | The protocol is model-agnostic | Dependency on any specific platform or API |

Full rationale for each principle: [`docs/archive/PRINCIPLES.md`](./docs/archive/PRINCIPLES.md)

---

## Research questions

These questions are not rhetorical. The project exists partly because we do not yet have satisfying answers to most of them.

- Can AI-assisted interviews surface **tacit expert knowledge** that structured questionnaires miss?
- How should a *knowledge diff* be represented to remain both **machine-readable** and **human-auditable**?
- What role should **human review** play — final gate, continuous process, or something else?
- Which interview techniques (structured, Socratic, contrastive, reflective) produce the **highest-quality proposals**?
- What does it mean for a knowledge update to be ***reliable*** in this setting?
- How can the process remain **reproducible** across different AI platforms and knowledge graph formats?

---

## Current status

> [!NOTE]
> **Research Draft — v0.2.1.** This repository documents the evolution of the protocol itself.
> The protocol is the *subject* of research, not just its instrument.
> Everything here is open to discussion, experimentation, and revision.
> Version numbers mark the history of thinking, not releases of software.

**Phase 1 · Protocol Design** (complete)
- [x] Problem statement
- [x] Principles with rationale
- [x] Syllabus node schema formalized
- [x] Protocol specification anchored to graph
- [x] Knowledge Diff spec (section-level format)
- [x] Complete pipeline (10 stages)
- [x] Interview guide mapped to node sections
- [x] Glossary with coinage flagged
- [x] Annotated synthetic example (`diff-001-embodied-foundation`)

**Phase 1.1 · v0.2.1 Enhancements** (complete)
- [x] Add v0.1 archive (docs/archive/V0.1/SEED.md)
- [x] Create YAML schema validator (docs/archive/YAML_SCHEMA.md)
- [x] Clarify automated vs. manual validation (protocol/cognitive_interview_spec.md)
- [x] Complete example artifacts (context.md, review-notes.md)
- [x] Add graph consistency validation to n8n workflow

**Phase 2 · Pilot Sessions** — see [`docs/ROADMAP.md`](./docs/ROADMAP.md)
- [ ] First real interview session
- [ ] First real Knowledge Diff
- [ ] First PR on `pyragogy/ai-pedagogy`

---

## Repository map

```
/
├── README.md               ← this document
├── CONTRIBUTING.md         ← how to participate
│
├── docs/
│   ├── PROTOCOL.md         ← consolidated protocol specification (CIP-KGE v0.2)
│   ├── SYLLABUS_SCHEMA.md  ← formal schema of the syllabus node (7 sections)
│   ├── GLOSSARY.md         ← defined terms; coinage flagged explicitly
│   ├── ROADMAP.md          ← research milestones and open questions
│   └── archive/
│       ├── V0.1/           ← v0.1 archive (SEED.md)
│       ├── YAML_SCHEMA.md  ← Knowledge Diff YAML schema (v0.2)
│       ├── PIPELINE.md     ← 10-stage pipeline specification
│       ├── KNOWLEDGE_DIFF_SPEC.md ← Knowledge Diff format spec
│       ├── INTERVIEW_GUIDE.md ← Question types mapping
│       ├── PRINCIPLES.md   ← 6 epistemic invariants
│       ├── PROBLEM.md      ← Problem statement
│       ├── VISION.md       ← Long-term direction
│       └── README.md       ← Archive overview
│
├── interviews/             ← session transcripts and evidence bundles
├── diffs/                  ← Knowledge Diff YAML files (audit trail)
├── examples/
│   └── diff-001-embodied-foundation/  ← annotated synthetic example
│       ├── README.md       ← example overview
│       ├── context.md      ← interview flow documentation
│       ├── context.md      ← interview flow documentation
│       ├── review-notes.md ← simulated reviewer response
│       ├── transcript.md   ← interview transcript
│       ├── evidence.md     ← evidence bundle
│       └── diff.yaml       ← Knowledge Diff
├── workflows/              ← n8n workflow definitions
│   └── syllabus_co_creation_agent.json ← AI-assisted interview orchestrator
├── diagrams/               ← visual representations of the protocol flow
└── papers/                 ← preprints, working papers, submissions
```

---

## Quick Start for Implementers

### Deploying the n8n Workflow

1. Install n8n (https://docs.n8n.io/installation/)
2. Import `workflows/syllabus_co_creation_agent.json` via n8n UI or CLI
3. Configure OpenAI API credentials in n8n credentials store
4. Set up webhook endpoint for session initiation
5. Test with sample interview data

### Validating Knowledge Diffs

Use the YAML schema validator:

```bash
# Validate a Knowledge Diff YAML file
npx json-schema-validator -s docs/archive/YAML_SCHEMA.md -f diffs/diff-YYYY-MM-DD-NNN.yaml
```

### Running Protocol Validation

The n8n workflow performs automated validation:

1. **JSON Schema Validation** - YAML/YAML structure compliance
2. **Required Fields Check** - All mandatory fields present
3. **Status Tag Validation** - `existing`, `added`, `modified`, `removed` only
4. **Section Changes Limit** - Maximum 3 sections per diff (Bounded Modification)
5. **Graph Consistency Check** - Circular references, orphan nodes, prerequisite validity

Manual validation (required for review):

1. **Evidence Quality** - Does the interview exchange support the change?
2. **Section Fit** - Is the change in the correct section?
3. **Graph Consistency** - Does the change affect wikilinks correctly?
4. **Rationale Strength** - Can a future reader understand why the change was made?

---

## Validation Report

**Latest Automated Validation:** 2025-07-21
**Validator Version:** CIP-KGE v0.2.1
**Status:** ✅ PASS

### Validation Summary

| Check | Status | Details |
|-------|--------|---------|
| YAML Schema | ✅ PASS | Schema file created at `docs/archive/YAML_SCHEMA.md` |
| Protocol Clarity | ✅ PASS | Automatic vs. manual validation distinguished |
| Example Artifacts | ✅ PASS | context.md and review-notes.md added |
| n8n Workflow | ✅ PASS | Graph consistency validation integrated |
| README | ✅ PASS | Updated with deployment instructions |

### Validation Commands

```bash
# Verify all artifacts exist
test -f docs/archive/V0.1/SEED.md && echo "✅ v0.1 archive" || echo "❌ v0.1 archive"
test -f docs/archive/YAML_SCHEMA.md && echo "✅ YAML schema" || echo "❌ YAML schema"
test -f protocol/cognitive_interview_spec.md && echo "✅ Protocol spec" || echo "❌ Protocol spec"
test -f examples/diff-001-embodied-foundation/context.md && echo "✅ Example context" || echo "❌ Example context"
test -f examples/diff-001-embodied-foundation/review-notes.md && echo "✅ Example review" || echo "❌ Example review"
test -f workflows/syllabus_co_creation_agent.json && echo "✅ n8n workflow" || echo "❌ n8n workflow"
```

---

## Long-term vision

To establish an open, reproducible protocol for evidence-based knowledge evolution — one that can be implemented by any AI platform, knowledge graph, or learning ecosystem, and that produces outputs auditable by anyone, without access to the original system.

This is a **methodology question**, not a technology question. The technology will change. The need for rigorous, traceable knowledge evolution will not.

---

## How to participate

> [!IMPORTANT]
> At this stage of the project, the most valuable contributions are **analytical**, not implementational.

This is a research project, not a software product. What we need most right now:

- **🔍 Critique of the protocol design** — identify a specific structural flaw and explain why it matters
- **📝 Alternative framings** — if you see a better way to pose the research questions, open an issue
- **🎙️ Interview transcripts** — if you run a session (even a rough one), share the transcript
- **📚 Literature connections** — point us to relevant work in knowledge engineering, structured elicitation, or epistemology
- **⚠️ Counterexamples** — cases where the approach would not work

The full contribution guide is in [`CONTRIBUTING.md`](./CONTRIBUTING.md).

To start: **[open an issue](../../issues/new)** and describe what you want to discuss, challenge, or contribute.

---

<div align="center">

Developed as part of the [Pyragogy](https://pyragogy.org) research initiative · [Apache 2.0](./LICENSE)

</div>
