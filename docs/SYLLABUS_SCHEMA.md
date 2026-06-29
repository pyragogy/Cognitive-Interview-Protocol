# Syllabus Node Schema

> This document describes the formal structure of a node in the Pyragogy Syllabus knowledge graph.
> Every Knowledge Diff produced by CIP-KGE must reference this schema.
> A diff that does not target a specific section of this schema is malformed.

---

## The knowledge graph

The Pyragogy Syllabus ([syllabus.pyragogy.org](https://syllabus.pyragogy.org)) is a public knowledge graph powered by [Quartz v5](https://quartz.jzhao.xyz/). Its source is in the repository [pyragogy/ai-pedagogy](https://github.com/pyragogy/ai-pedagogy). Quartz rebuilds and publishes the graph automatically on every commit to `main`.

Each node is a Markdown file in the `content/` directory of `ai-pedagogy`. Nodes are linked to each other via wikilinks (`[[node_id]]`). Backlinks are computed automatically by Quartz.

A Knowledge Diff that is accepted by the CIP-KGE review process becomes a pull request on `pyragogy/ai-pedagogy`. When merged, the graph updates automatically.

---

## Node file format

Every node in the graph has the following structure:

```markdown
---
title: [Full title of the node]
tags: [pyragogy, pyragogy/practice]
---

## 1. Definition
[text]

## 2. Use Case
[text]

## 3. Human Role
[text]

## 4. AI Role
[text]

## 5. Friction
[text]

## 6. Risk
[text — may contain [[wikilinks]] to risk nodes in 05_systemic_risks/]

## 7. Observable Markers
[text]
```

The file is located at `content/{section_prefix}/{node_id}.md` relative to the `ai-pedagogy` repository root. The published URL is `https://syllabus.pyragogy.org/{section_prefix}/{node_id}`.

---

## The seven sections

Each section has a precise epistemic role. Understanding this role is necessary to conduct an interview that produces useful evidence for that section.

| # | Section | Epistemic role | What CIP interview should extract |
|---|---|---|---|
| 1 | **Definition** | What the concept *is* — boundary-setting | Expert's most concise formulation of the concept and what it excludes |
| 2 | **Use Case** | *When* the concept activates — trigger conditions | Specific situations where the expert has seen the concept apply |
| 3 | **Human Role** | What the *human* does in this node | Observable behaviors, not intentions — what does an evaluator actually see? |
| 4 | **AI Role** | What the *AI system* does — constraints and affordances | What should the system refuse to do? What is its positive contribution? |
| 5 | **Friction** | The *mechanism* of intentional resistance | The specific form of difficulty — not "difficulty" in general |
| 6 | **Risk** | What happens when this node is *absent* or *bypassed* | Documented failure modes, not theoretical risks |
| 7 | **Observable Markers** | How you *know* the concept is working | Concrete, external, verifiable evidence — not internal states |

---

## Graph sections

The graph is currently organized into the following top-level sections:

| Directory | Topic |
|---|---|
| `02_ontogeny/` | Early cognitive development and embodied foundations |
| `03_praxis/` | Active practice, debate, and collaborative learning |
| `04_autonomy/` | Adult reflective practice and professional integration |
| `05_systemic_risks/` | Structural failure modes (e.g., `automation_bias`, `cognitive_debt`) |

New nodes may be added to existing sections or placed in new sections. The addition of a new section is a structural change that requires review at the graph level, not just the node level.

---

## Node identifiers

A node is identified by its path relative to `content/` in `ai-pedagogy`, without the `.md` extension. Examples:

- `02_ontogeny/embodied_foundation`
- `03_praxis/adolescent_sparring_arena`
- `04_autonomy/adult_reflective_practice`
- `05_systemic_risks/automation_bias`

This path is the canonical identifier used in Knowledge Diffs. It is stable as long as the node is not moved or renamed.

---

## Wikilinks and backlinks

Nodes reference each other using the `[[node_id]]` syntax within section text. Quartz resolves these to HTML links and computes backlinks automatically. A Knowledge Diff that proposes adding a wikilink to a section must verify that the target node exists in the graph.

A diff that adds a reference to a non-existent node is a malformed diff.

---

## Known current nodes

As of v0.2 (June 2026), the following nodes have been observed in the published graph:

| Node | Path | Section |
|---|---|---|
| The Embodied Portal | `02_ontogeny/embodied_foundation` | Ontogeny |
| Ontogeny to Praxis Bridge | `02_ontogeny/ontogeny_to_praxis_bridge` | Ontogeny |
| The Dialectic Sparring Arena | `03_praxis/adolescent_sparring_arena` | Praxis |
| Praxis to Autonomy Bridge | `03_praxis/praxis_to_autonomy_bridge` | Praxis |
| Epistemic Integration / Reflective Practice | `04_autonomy/adult_reflective_practice` | Autonomy |
| Automation Bias | `05_systemic_risks/automation_bias` | Systemic Risks |
| Cognitive Debt | `05_systemic_risks/cognitive_debt` | Systemic Risks |

This list is not exhaustive. Check the live graph or the `ai-pedagogy` repository for the current state.
