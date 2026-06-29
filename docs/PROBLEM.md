# The Problem

> This document defines the precise problem the Cognitive Interview Protocol addresses.
> It is intentionally narrow. A problem statement that explains everything explains nothing.

---

## What we observe

In most AI-augmented knowledge systems today, there are two dominant patterns for how knowledge gets updated.

**Pattern A — Direct edit.** The AI modifies the knowledge base autonomously, based on context or user interaction. The reasoning behind the edit is either lost or buried in a log that no human review process is structured to examine.

**Pattern B — Free-form output.** The AI produces a response — an answer, a summary, an explanation — and a human decides, informally, whether anything in that response should be incorporated into the knowledge base. There is no structured artifact representing the proposed change. There is no audit trail.

Neither pattern is adequate for environments where the quality of knowledge matters — clinical guidelines, educational curricula, legal interpretation, domain-specific expert systems. In these contexts, the question is not whether the AI can produce useful output. It often can. The question is whether that output can be evaluated, challenged, and integrated in a way that preserves accountability.

---

## The gap we are addressing

The gap is methodological. We do not lack AI systems capable of conducting interviews. We do not lack knowledge graph technologies capable of representing complex domain knowledge. What we lack is a reproducible process that connects the two — that takes a conversation between a human expert and an AI system and produces, as output, a structured artifact that:

- represents a specific, bounded proposed change to a knowledge graph,
- carries explicit provenance (who said what, in what context, under what conditions),
- can be reviewed and challenged by someone who was not present in the original session,
- can be accepted, modified, or rejected through a defined process.

We call this artifact a *knowledge diff* — a term we coin here in a project-specific sense, borrowing from version control the idea of a structured, reviewable representation of a proposed change. Whether this term, or something better, will stabilize is an open question.

---

## What this problem is not

It is not a problem about AI capability. The protocol is designed to be model-agnostic; it does not assume that better models will make the problem disappear.

It is not a problem about knowledge graph completeness. No knowledge graph is complete. The problem is about how changes to a knowledge graph are proposed and evaluated, not about whether the graph is adequate.

It is not primarily a technical problem. The hard part is not building a system that can produce structured outputs. The hard part is defining what *reliable* and *reviewable* mean in this context — and designing a process that makes those properties legible to a human reviewer.

---

## Why this matters

Expert knowledge is tacit. Much of what an experienced practitioner knows is not written anywhere. Interviews — conducted well — can surface it. But "conducted well" is not a stable property of a conversation; it is a property of a methodology. Without a methodology, the quality of what gets surfaced depends on who happens to be asking the questions.

This project is an attempt to make that methodology explicit, reproducible, and improvable.
