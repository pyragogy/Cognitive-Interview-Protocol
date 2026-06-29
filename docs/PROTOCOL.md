# Protocol Specification

> **Status: Research Draft — v0.1**
>
> This document describes the Cognitive Interview Protocol as currently understood.
> It is a living document. Gaps, open questions, and known limitations are marked explicitly.
> Do not read this as a stable specification; read it as a record of the current state of thinking.

---

## What the protocol is

The Cognitive Interview Protocol (CIP) is a structured methodology for conducting AI-assisted interviews that produce *knowledge diffs* — structured, reviewable proposals for the evolution of a knowledge graph.

The protocol has three components:

1. **The interview structure** — how the interview is organized, how questions are sequenced, and what techniques are used to elicit tacit knowledge.
2. **The output format** — how the results of an interview session are represented as a *knowledge diff*.
3. **The review process** — how a *knowledge diff* is evaluated, challenged, and either accepted or rejected.

These three components are described below in their current, incomplete form.

---

## Component 1: The Interview Structure

### Session framing

A CIP session begins with an explicit framing. The interviewee is told:

- The purpose of the session is to produce a *knowledge diff* — a proposal for a change to a specific knowledge graph.
- The AI system is conducting the interview according to a defined protocol; it is not a free-form conversation.
- The interviewee may challenge, correct, or refuse any question.
- Nothing said in the session is automatically incorporated into the knowledge graph; all output is subject to human review.

This framing is not merely procedural. It establishes the epistemic status of the session: the interviewee is a source of evidence, not a passive subject.

### Question types

The following question types are currently under investigation. Their relative effectiveness is an open research question.

**Elicitation questions.** Open questions designed to surface what the interviewee knows, without presupposing the structure of the answer. Example: *"Can you describe how you approach this decision?"*

**Clarification questions.** Questions that ask the interviewee to make a statement more precise. Example: *"When you say 'usually,' what conditions determine the exception?"*

**Socratic questions.** Questions that probe the reasoning behind a claim. Example: *"What would have to be true for that not to hold?"*

**Contrastive questions.** Questions that ask the interviewee to compare the stated claim to an alternative. Example: *"How does this differ from [X]?"*

**Boundary questions.** Questions that ask the interviewee to identify the limits of a claim. Example: *"In what contexts would this not apply?"*

The sequence and balance of question types within a session is not yet specified. This is one of the central open questions of the project.

### Session termination

A session ends when one of the following conditions is met:

- The interviewee indicates that they have nothing more to add.
- The AI system determines (according to criteria not yet fully defined) that the exchange has produced sufficient evidence for a well-grounded *knowledge diff*.
- A predefined time or exchange limit is reached.

`[OPEN QUESTION: How should the AI system determine that sufficient evidence has been collected? What criteria apply?]`

---

## Component 2: The Output Format

A *knowledge diff* produced by a CIP session must be a structured document. The following fields are required in v0.1. The format is provisional.

```
knowledge_diff:
  id: [unique identifier]
  session_id: [reference to the source interview session]
  generated_at: [ISO 8601 timestamp]
  
  proposed_change:
    type: [add | modify | remove | deprecate]
    target: [identifier of the node or edge in the knowledge graph]
    description: [human-readable description of the proposed change]
    
  evidence:
    source_exchange: [reference to the specific exchange in the session transcript]
    summary: [brief description of the evidence for the proposed change]
    
  review_status: proposed
  review_notes: []
```

This format is a starting point. Known limitations:

- It does not represent changes that span multiple nodes or edges.
- It does not represent conditional changes (changes that depend on other changes being accepted).
- It does not represent uncertainty gradients — situations where the evidence supports the change but with varying degrees of confidence.

`[OPEN QUESTION: How should the format represent compound changes? How should it represent uncertainty?]`

---

## Component 3: The Review Process

A *knowledge diff* in `proposed` status must be assigned to a reviewer — a human who was not present in the interview session that generated it. The reviewer has access to:

- The *knowledge diff* itself.
- The full transcript of the source interview session.
- The current state of the knowledge graph.

The reviewer may:

- **Accept** the proposed change, with or without modification.
- **Reject** the proposed change, with a recorded rationale.
- **Defer** the proposed change, requesting additional evidence or a follow-up interview session.
- **Escalate** the proposed change for review by a second reviewer.

The criteria by which a reviewer evaluates a *knowledge diff* are not yet formally specified. This is a significant gap.

`[OPEN QUESTION: What are the formal criteria for accepting or rejecting a knowledge diff? How should disagreement between reviewers be resolved?]`

---

## Known Limitations of v0.1

This version of the protocol has the following known limitations, which are research priorities for v0.2:

1. The review criteria are unspecified.
2. The session termination criteria are unspecified.
3. The output format does not handle compound or conditional changes.
4. The protocol has not been tested with real interview sessions.
5. The connection to existing literature on structured knowledge elicitation is incomplete. [VERIFY SOURCE: knowledge elicitation methods in knowledge engineering; expert systems literature]

---

## Changelog

| Version | Date | Summary |
|---|---|---|
| v0.1 | 2026-06 | Initial draft. Three-component structure established. Format and review process identified as primary open questions. |
