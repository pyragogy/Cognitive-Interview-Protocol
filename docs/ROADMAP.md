# Roadmap

> This document tracks the research milestones and open questions of the Cognitive Interview Protocol.
>
> A roadmap in a research project is different from a roadmap in a software project.
> It describes what questions we are trying to answer and in what order — not what features we plan to ship.
> Timelines are tentative. They depend on empirical results we do not yet have.

---

## Current Phase: Protocol Design (v0.1)

**Goal.** Establish the basic structure of the protocol — the interview framework, the output format, and the review process — at a level of detail sufficient to conduct the first pilot sessions.

**Status.** In progress.

**Open questions this phase must close:**

- [ ] What is the minimum viable specification of the output format (*knowledge diff*) for a pilot session?
- [ ] What session termination criteria are operationalizable in a first implementation?
- [ ] What review criteria are sufficient for a first reviewer, even if not yet formally specified?

**Deliverables:**
- [ ] `PROTOCOL.md` at a level of detail sufficient for a pilot session (in progress)
- [ ] `GLOSSARY.md` with all terms used in the protocol defined (in progress)
- [ ] At least one annotated example of a *knowledge diff* in `examples/`

---

## Next Phase: Pilot Sessions (v0.2)

**Goal.** Conduct a small number of real interview sessions using the v0.1 protocol and evaluate the results.

**What we are looking for:**

- Does the protocol produce *knowledge diffs* that a reviewer can evaluate independently?
- Do the question types surface tacit knowledge, or do they produce outputs that could have been obtained through simpler methods?
- Where does the protocol break down? What situations does it not handle?

**Open questions this phase will address:**

- What is the actual quality of *knowledge diffs* produced under the protocol?
- What do reviewers need that the format does not provide?
- Which question types produce the most useful evidence?

**Deliverables:**
- [ ] Transcripts of pilot sessions (anonymized where necessary) in `interviews/`
- [ ] Analysis of pilot session outcomes
- [ ] Revised `PROTOCOL.md` incorporating findings

---

## Later Phase: Formalization (v0.3+)

**Goal.** Move from a descriptive protocol to a formal one — with specified review criteria, a formal output schema, and sufficient documentation to allow independent implementation.

**Precondition.** This phase depends on findings from pilot sessions. We do not yet know what a formal specification will look like.

**Open questions for this phase:**

- What are the formal criteria for accepting or rejecting a *knowledge diff*?
- How should disagreement between reviewers be resolved?
- Can the protocol be formally specified in a way that allows automated validation of *knowledge diffs*?
- What does reproducibility mean in this context — and how is it measured? [VERIFY SOURCE: reproducibility criteria in qualitative research; structured elicitation literature]

---

## Standing Open Questions

These questions are not assigned to a specific phase. They are ongoing research questions that may be addressed in parallel with the milestones above, or may be deferred to later work.

- Can AI-assisted interviews surface tacit knowledge that structured questionnaires miss? What evidence would settle this question?
- What is the relationship between interview technique and knowledge diff quality? Is this measurable?
- How does the protocol interact with different knowledge graph formats? Are there formats it cannot handle?
- What is the appropriate scope of a single *knowledge diff*? How do we prevent scope creep (changes that are too broad to be reviewable)?
- Is there a connection between CIP and existing work on knowledge elicitation in expert systems? [VERIFY SOURCE: systematic review of knowledge elicitation methods needed]

---

## What is not on this roadmap

- A production implementation of the protocol in any specific software system.
- Integration with any specific knowledge graph platform.
- Automated review of *knowledge diffs*.

These are not excluded because they are uninteresting. They are excluded because they are downstream of the methodological questions this project is trying to answer. Building a system before the methodology is stable would be premature.
