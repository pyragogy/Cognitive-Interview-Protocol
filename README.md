# Pyragogy Cognitive Interview Protocol (CIP‑KGE) v0.3‑draft

<div align="center">

[![Status](https://img.shields.io/badge/status-Open%20Reference%20Architecture-purple?style=flat-square)](docs/ROADMAP.md)
[![Version](https://img.shields.io/badge/version-v0.3--draft-blue?style=flat-square)](docs/PROTOCOL.md)
[![License](https://img.shields.io/badge/license-MIT-007bff?style=flat-square)](LICENSE)
[![Contributions](https://img.shields.io/badge/contributions-welcome-28a745?style=flat-square)](CONTRIBUTING.md)

</div>

---

## What this is

**CIP‑KGE is an Epistemic Governance Protocol for Knowledge Graph Evolution.**

It is **not** an “AI interview orchestrator.” Calling it that overstates what the system automates and understates what it actually is: a **human‑gated review process** with one automated sub‑stage.

Read this before anything else:

> **This is a human‑in‑the‑loop system.** Of the 10 pipeline stages, only Stage 3 (Evidence Extraction / classification) is machine‑assisted. Stages 2, 5, 6, 7, 8 are manual **by design**, not by current limitation. The LLM does **not** write to the knowledge graph. It never has write access. A human reads the transcript, a human validates the diff, a human opens the pull request.

If you came here expecting an autonomous agent that ingests interviews and updates a graph — this is the wrong tool. If you need a **traceable, falsifiable process for turning tacit expert knowledge into reviewable, bounded proposals**, keep reading.

---

## The trade‑off, stated up front

Cognitive interviewing (the technique, borrowed from forensic psychology) produces higher‑fidelity, more falsifiable evidence than a questionnaire or a free‑form chat. It also costs more human time per unit of knowledge captured:

| | Cognitive Interview (CIP‑KGE) | Free‑form AI Q&A | Structured questionnaire |
|---|--------------------------------|-------------------|---------------------------|
| **Evidence traceability** | High — exchange‑level | None | Medium — field‑level |
| **Tacit knowledge surfaced** | High | Variable | Low |
| **Human review cost per update** | High (full transcript read) | Low/none | Low |
| **Throughput (updates/hour)** | Low | High | Medium |
| **Risk of unreviewed error entering the graph** | Near‑zero (gated) | High | Low‑medium |

**This protocol is not a scaling solution.** It is a correctness solution. Do not deploy it where you need volume; deploy it where a single wrong node is more costly than a slow one. This is the honest trade‑off — the earlier README did not state it, and that was a gap.

---

## Repository structure

```
Cognitive-Interview-Protocol/
├── README.md                          ← This file
├── CONTRIBUTING.md
├── LICENSE
│
├── docs/                             ← Protocol specifications
│   ├── PROTOCOL.md                   ← 10‑stage pipeline + Epistemic Invariants
│   ├── KNOWLEDGE_DIFF_SCHEMA.md       ← Formal, stack‑agnostic diff schema (conceptual)
│   ├── KNOWLEDGE_DIFF_SCHEMA.yaml     ← Machine‑readable YAML schema for validation
│   ├── ARBITRATION.md                 ← Conflict resolution between concurrent diffs (ex‑L5)
│   ├── INTERVIEW_DECISION_TREE.md     ← Q1–Q5 termination rules (state machine)
│   ├── SYLLABUS_SCHEMA.md             ← Pyragogy‑specific binding (optional layer)
│   ├── GLOSSARY.md
│   ├── ROADMAP.md
│   └── archive/
│
├── examples/                         ← Worked demonstrations
│   └── diff‑001‑embodied‑foundation/
│
├── workflows/                        ← Reference implementation (n8n)
│   └── syllabus_co_creation_agent.json  ← Stage 3 automation only. Not an “agent” in the autonomous sense.
│
├── protocol/                         ← Quick reference
│   └── cognitive_interview_spec.md   ← 4‑phase protocol + validation breakdown
│
├── interviews/   ← audit trail
├── diffs/        ← Knowledge Diff YAML files
├── diagrams/     ← visual representations
└── papers/       ← preprints & working papers
```

---

## What is model‑agnostic and stack‑agnostic (and what wasn’t, until now)

The previous version of this protocol coupled the Knowledge Diff format directly to:
- Quartz‑generated wikilinks (`[[node_id]]`)
- GitHub PR mechanics on a specific repository (`pyragogy/ai‑pedagogy`)
- File paths in a specific content‑directory structure

This violated the protocol’s own **Principle 5 — “Protocol is model‑agnostic.”** A contract that hardcodes a publishing stack is not agnostic to anything except which LLM API you call. That was a real inconsistency between the stated principle and the shipped artifact.

**Fixed in v0.3:** the Knowledge Diff core schema (`docs/KNOWLEDGE_DIFF_SCHEMA.md`) no longer references Quartz, wikilinks, or GitHub paths. Those become an **optional binding layer** — `SYLLABUS_SCHEMA.md` documents how to project the generic diff onto the Pyragogy Syllabus specifically. Anyone using CIP‑KGE against a different knowledge graph (Notion, a plain JSON store, a different wiki engine) implements their own binding layer against the same core contract.

---

## Core principles (unchanged, still non‑negotiable)

| # | Principle | What it rules out |
|---|-----------|-------------------|
| 1 | Knowledge evolves through evidence | Model confidence as grounds for change |
| 2 | Every modification is independently reviewable | Changes requiring original session access |
| 3 | AI proposes; humans validate | Automated incorporation of AI output |
| 4 | Interviews generate diffs, not edits | Direct write access for AI system |
| 5 | Protocol is model‑ and stack‑agnostic | Dependency on any specific platform, publishing engine, or repo layout |

Full rationale: `docs/archive/PRINCIPLES.md`

---

## Automated verification (CI / n8n / script)

Before a Knowledge Diff reaches human review, it **must** pass **syntactic validation** against the formal YAML schema (`docs/KNOWLEDGE_DIFF_SCHEMA.yaml`). This ensures the diff is at least well‑formed and respects the epistemic invariants (e.g., ≤ 3 section changes).

### Validating a single diff with Python

```bash
# Install jsonschema and PyYAML
pip install jsonschema pyyaml

# Validate against the schema
python -c "
import yaml, jsonschema, sys
schema = yaml.safe_load(open('docs/KNOWLEDGE_DIFF_SCHEMA.yaml'))
diff = yaml.safe_load(open('diffs/diff‑2026‑07‑15‑001.yaml'))
try:
    jsonschema.validate(diff, schema)
    print('✅ Schema valid')
except jsonschema.ValidationError as e:
    print('❌ Validation failed:', e.message)
    sys.exit(1)
"
```

### Integration with n8n workflows

Add a **“Validate YAML Schema”** node after the LLM generates a draft diff. Use the `ajv` library (Node.js) or call a Python subprocess as above.

### CI/CD pipeline (GitHub Actions example)

```yaml
name: Validate Knowledge Diffs
on:
  pull_request:
    paths:
      - 'diffs/*.yaml'

jobs:
  validate:
    runs‑on: ubuntu‑latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Python dependencies
        run: pip install jsonschema pyyaml
      - name: Validate all diffs
        run: |
          for f in diffs/*.yaml; do
            python scripts/validate_diff.py "$f" || exit 1
          done
```

A reference validator script (`scripts/validate_diff.py`) is a **v0.3‑candidate contribution** — not yet provided, but trivial to write once the schema exists.

**Why this matters:** Automated syntactic validation catches malformed diffs **before** they reach a human reviewer, reducing review burden and preventing epistemic errors (e.g., missing exchange references) from slipping through.

---

## Quick start for implementers

### 1. Understand what gets automated

Only this:

```
[Transcript] → [Stage 3: LLM classifies exchanges → candidate section_changes] → [Draft Diff]
```

Everything before and after is manual. The n8n workflow in `workflows/` implements Stage 3 only — evidence extraction and preliminary schema‑shape checking. It is **not** a substitute for human review at Stage 6.

### 2. Import the workflow (Stage 3 automation)

```bash
npm install --global n8n
n8n start
```

In the n8n UI: **Settings → Import → `workflows/syllabus_co_creation_agent.json`**

### 3. Run a test extraction

```bash
curl -X POST http://localhost:5678/webhook/test‑session \
  -H "Content‑Type: application/json" \
  -d '{
    "session_id": "test‑001",
    "topic": "networking_fundamentals",
    "transcript": "[exchange‑01] User explains their experience with networking..."
  }'
```

This produces a **draft** Knowledge Diff. It does **not** touch any graph. A human still has to validate it against `docs/KNOWLEDGE_DIFF_SCHEMA.yaml` and run Stage 5–8 manually.

---

## What changed from v0.2.1 → v0.3‑draft

| Area | v0.2.1 | v0.3‑draft |
|------|--------|-------------|
| **Positioning** | “AI‑assisted interview orchestrator” | “Epistemic Governance Protocol” — human‑gated, LLM handles Stage 3 only |
| **Diff schema** | Coupled to Quartz/GitHub/wikilinks | Stack‑agnostic core + optional binding layer |
| **Multi‑expert corroboration** | Undefined — “high confidence” meant intra‑session only | Explicit distinction: intra‑session coherence ≠ inter‑session corroboration |
| **Reviewer conflict** | Open question (L5) | Formal arbitration process (`ARBITRATION.md`) |
| **Question‑type transitions (Q1–Q5)** | Qualitative heuristic | Formal decision tree with termination rules (`INTERVIEW_DECISION_TREE.md`) |
| **Schema validation** | Manual, described in prose | Formal YAML Schema, machine‑checkable (`KNOWLEDGE_DIFF_SCHEMA.yaml`) |

---

## Contributing

This is a research project, not a software product. Valuable contributions are **analytical**: critique of protocol design, alternative framings, interview transcripts (real or simulated), literature connections, counterexamples.

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

<div align="center" style="margin‑top: 2rem; padding‑top: 2rem; border‑top: 1px solid #e1e4e8;">

**CIP‑KGE v0.3‑draft** — Epistemic governance protocol for evidence‑based knowledge‑graph evolution<br>
© 2026 Pyragogy · [MIT License](LICENSE)

</div>
