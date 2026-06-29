# Roadmap

> This document tracks the research milestones and open questions of CIP-KGE.
>
> A roadmap in a research project is different from a roadmap in a software project.
> It describes what questions we are trying to answer and in what order — not what features we plan to ship.
> Timelines are tentative. They depend on empirical results we do not yet have.

---

## Phase 1 — Protocol Design (v0.2) ✓ COMPLETE

**Goal.** Establish the basic structure of the protocol — the interview framework, the output format, and the review process — at a level of detail sufficient to conduct the first pilot sessions.

**What was built:**
- [x] Syllabus node schema formalized ([`SYLLABUS_SCHEMA.md`](./SYLLABUS_SCHEMA.md))
- [x] Knowledge Diff specification, anchored to node sections ([`KNOWLEDGE_DIFF_SPEC.md`](./KNOWLEDGE_DIFF_SPEC.md))
- [x] Complete 10-stage pipeline with failure conditions ([`PIPELINE.md`](./PIPELINE.md))
- [x] Interview guide mapping question types to node sections ([`INTERVIEW_GUIDE.md`](./INTERVIEW_GUIDE.md))
- [x] Annotated synthetic example: `diff-001-embodied-foundation/`

**Known limitations carried into Phase 2:**
- Review criteria are partially specified; calibration requires real review disagreements
- Markdown transformation (Stage 7) is fully manual; no tooling yet
- The process for proposing new *graph sections* is not yet defined

---

## Phase 2 — Pilot Sessions (v0.2 validation)

**Goal.** Conduct a small number of real interview sessions using the v0.2 protocol and evaluate whether the pipeline produces Knowledge Diffs that are:
1. Independently reviewable by someone who was not in the session
2. Mergeable into `pyragogy/ai-pedagogy` without requiring the reviewer to rewrite the proposal
3. Descriptive of actual knowledge that improves the node's precision or coverage

**What we are looking for:**

- Do the question types in the Interview Guide surface evidence that maps to specific sections?
- Where does the pre-review quality check fail most often, and why?
- Do reviewers disagree? If so, on what grounds?
- What does the first real PR on `pyragogy/ai-pedagogy` look like?

**Milestone targets:**

- [ ] First real interview session (with transcript and evidence bundle)
- [ ] First real Knowledge Diff (passes pre-review quality check)
- [ ] First real review decision (accepted or rejected, with rationale)
- [ ] First real PR on `pyragogy/ai-pedagogy` (or first rejection at this stage, with reason)
- [ ] Post-session analysis: what did the protocol fail to capture?

---

## Phase 3 — Formalization (v0.3)

**Goal.** Move from a descriptive protocol to a formal one — with calibrated review criteria, a validated output schema, and sufficient documentation to allow independent implementation.

**Precondition.** This phase depends on findings from Phase 2. We do not yet know what a formal specification will look like.

**Candidate work items (not yet committed):**

- YAML schema validator for Knowledge Diffs
- Formal review criteria derived from real review disagreements
- Protocol for proposing new graph sections (not just new nodes)
- Assessment of whether the Interview Guide question types need revision
- First working paper: protocol design rationale and Phase 2 findings

---

## Standing open questions

These are not assigned to a specific phase. They are ongoing research questions.

- Can AI-assisted interviews surface tacit knowledge that structured questionnaires miss? What evidence would settle this question?
- What is the appropriate scope of a single Knowledge Diff? The current `scope_too_broad` pre-review check (>3 section changes) is arbitrary — what should it actually be?
- Is the mechanism distinction between automation_bias and the embodied foundation risk (as described in `diff-001-embodied-foundation`) empirically supportable? [VERIFY SOURCE: automation bias literature; embodied cognition literature]
- Can the pipeline be partially automated without sacrificing the accountability properties that make the review meaningful?
- What does it mean for a Knowledge Diff to fail the review — and how do rejected diffs improve the protocol?

---

## What is not on this roadmap

- A production implementation of the pipeline in any specific software system
- Integration with any specific AI platform
- Automated review of Knowledge Diffs

These are downstream of the methodological questions this project is trying to answer. Building systems before the methodology is stable would be premature.
