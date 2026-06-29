# Vision

> This document describes the long-term direction of the Cognitive Interview Protocol.
> It is a direction, not a plan. Plans change when contact with reality changes them.
> This document changes when our understanding of the problem changes.

---

## The question this project is organized around

Knowledge evolves. The question is whether it can evolve *well* — with traceability, with accountability, with a process that preserves the reasoning behind each change and makes that reasoning available for critique.

In the short term, this is a question about methodology. In the longer term, it becomes a question about what kind of epistemic infrastructure AI-assisted knowledge systems need in order to remain trustworthy over time.

The Cognitive Interview Protocol is an attempt to build part of that infrastructure.

---

## What we are trying to make possible

Five years from now, we would like it to be possible for a researcher, a knowledge engineer, or a domain expert to do the following:

1. Conduct a structured interview with an AI system — using the protocol defined in this repository — and obtain, as output, a *knowledge diff*: a structured, bounded, human-readable proposal for a change to a knowledge graph.

2. Submit that knowledge diff to a review process in which another human — who was not present in the interview — can evaluate it, challenge it, request clarification, and accept or reject it with a recorded rationale.

3. Accumulate a corpus of such diffs, their review outcomes, and the reasoning behind those outcomes — and use that corpus to improve the protocol itself.

None of these steps requires new AI capability. All of them require methodological work that, to our knowledge, has not been done in a systematic and open way. [VERIFY SOURCE: literature on human-in-the-loop knowledge graph curation; structured elicitation methods in knowledge engineering]

---

## The scope we are holding to

The protocol is concerned with *the interview as an evidence-gathering event*. It is not a knowledge graph technology project. It does not propose a new representation language, a new query system, or a new AI architecture.

This boundary is deliberate. The methodology must be portable — applicable across different AI systems, different knowledge graph formats, different domain contexts. If the protocol can only work with one technology stack, it has failed its own design criteria.

---

## What "open" means here

The protocol is open in three senses.

**Openly documented.** Every version of the protocol, every decision made in its design, and every revision to its rationale is recorded in this repository. A researcher who wants to implement or critique the protocol should be able to do so without asking for permission or access.

**Openly improvable.** The protocol is a living document. Empirical evidence from interview sessions, counterexamples, and theoretical challenges are all legitimate grounds for revision. The process for proposing revisions is documented in [CONTRIBUTING.md](../CONTRIBUTING.md).

**Open to failure.** It is possible that the approach does not work — that AI-assisted interviews, structured in this way, do not produce knowledge diffs of sufficient quality to be useful. If that is what the evidence shows, the project will say so. Documenting a negative result rigorously is within scope.

---

## The long horizon

We are not trying to automate knowledge creation. We are trying to make knowledge evolution *legible* — to create conditions under which the question "why does this knowledge graph say what it says?" has a traceable, auditable answer.

That is a narrower ambition than it might appear. And it is, we think, more durable.
