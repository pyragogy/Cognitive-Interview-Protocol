# Principles

> These are the core commitments of the Cognitive Interview Protocol.
> Each principle is stated with a rationale — not because the principle is obvious,
> but because a principle without rationale cannot be meaningfully challenged or revised.

---

## 1. Knowledge evolves through evidence

**Statement.** A proposed change to a knowledge graph must be grounded in evidence — in something a human expert said, demonstrated, or reasoned through — not in the model's prior confidence or the convenience of automated inference.

**Rationale.** The alternative — allowing knowledge to evolve based on the model's internal state — makes the process opaque in a way that is difficult to recover from. If a change is wrong, and we cannot trace how it was introduced, we cannot systematically prevent similar errors. Evidence is not a guarantee of correctness; it is the minimum condition for reviewability.

**Implication.** Every *knowledge diff* produced by the protocol must carry a reference to the interview session that generated it, and to the specific exchange within that session that grounded the proposed change.

---

## 2. Every proposed modification must be independently reviewable

**Statement.** A person who was not present in the interview session must be able to evaluate a *knowledge diff* — to understand what is being proposed, why, and on what grounds — without asking the original participants for clarification.

**Rationale.** Review that depends on access to the original participants does not scale and is not independent. The value of a review process is precisely that it introduces a perspective that was not present at the moment of production.

**Implication.** The format of a *knowledge diff* must be self-contained. The context needed to evaluate the proposal must be part of the artifact, not assumed to be available elsewhere.

---

## 3. AI proposes; humans validate

**Statement.** No AI-generated proposal may be incorporated into a knowledge graph without explicit human review and acceptance.

**Rationale.** This is not a statement about AI capability. It is a statement about accountability. In any domain where knowledge quality matters, someone must be able to answer the question: "who decided this?" An automated process cannot bear that accountability.

**Implication.** The protocol must define a review step that cannot be bypassed — not even when the proposed change appears unambiguous. The review step is not a filter for bad proposals; it is the mechanism through which human judgment is formally part of the process.

---

## 4. The protocol is model-agnostic

**Statement.** The protocol must be implementable with any AI system capable of conducting a structured conversation. It must not depend on features specific to any one model, platform, or API.

**Rationale.** A protocol tied to a specific technology becomes obsolete when the technology changes. A methodology that does not depend on specific capabilities can survive and adapt.

**Implication.** The protocol is specified in terms of *interview structures*, *output formats*, and *review processes* — not in terms of prompts, system messages, or platform-specific behaviors. Implementations may differ; the methodology must be recognizable across them.

---

## 5. The protocol is itself subject to revision

**Statement.** No version of the protocol is final. Empirical evidence from interview sessions — including evidence that the protocol does not work as intended — is legitimate grounds for revision.

**Rationale.** A methodology that cannot be falsified is not a methodology; it is a doctrine. The protocol is a hypothesis about how AI-assisted interviews can generate reliable knowledge proposals. Like any hypothesis, it should be tested and revised.

**Implication.** This repository documents not only the current version of the protocol but the history of its revisions and the reasoning behind each change. The changelog is part of the research record.
