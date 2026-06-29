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

Full specification: [`docs/PIPELINE.md`](./docs/PIPELINE.md)

---

## Core principles

| | Principle | What it rules out |
|---|---|---|
| **1** | Knowledge evolves through evidence | Model confidence as grounds for change |
| **2** | Every modification must be independently reviewable | Changes that require access to the original session |
| **3** | AI proposes; humans validate | Automated incorporation of AI output |
| **4** | Interviews generate *knowledge diffs*, not automatic edits | Direct write access for the AI system |
| **5** | The protocol is model-agnostic | Dependency on any specific platform or API |

Full rationale for each principle: [`docs/PRINCIPLES.md`](./docs/PRINCIPLES.md)

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
> **Research Draft — v0.2.** This repository documents the evolution of the protocol itself.
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
│   ├── PROBLEM.md          ← the precise problem this protocol addresses
│   ├── VISION.md           ← long-term direction and scope
│   ├── PRINCIPLES.md       ← core commitments, with rationale
│   ├── SYLLABUS_SCHEMA.md  ← formal schema of the syllabus node (7 sections)
│   ├── PROTOCOL.md         ← protocol specification CIP-KGE v0.2
│   ├── PIPELINE.md         ← complete 10-stage pipeline
│   ├── KNOWLEDGE_DIFF_SPEC.md ← Knowledge Diff format (section-level)
│   ├── INTERVIEW_GUIDE.md  ← question types mapped to node sections
│   ├── GLOSSARY.md         ← defined terms; coinage flagged explicitly
│   └── ROADMAP.md          ← research milestones and open questions
│
├── interviews/             ← session transcripts and evidence bundles
├── diffs/                  ← Knowledge Diff YAML files (audit trail)
├── examples/
│   └── diff-001-embodied-foundation/  ← annotated synthetic example
│       ├── README.md
│       ├── transcript.md
│       ├── evidence.md
│       └── diff.yaml
├── diagrams/               ← visual representations of the protocol flow
└── papers/                 ← preprints, working papers, submissions
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
