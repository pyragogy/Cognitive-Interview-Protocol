# Related Work — honest positioning

> This document exists because the protocol requires of its users what it must first
> require of itself: explicit provenance. Several CIP-KGE patterns have decades-old
> precedents under other names. Saying so is not a demerit — it is Invariant 1
> (Traceability) applied to the protocol's own intellectual lineage.

---

## Cognitive interviewing (the namesake)

**Origin:** forensic psychology (Fisher & Geiselman, *Cognitive Interview*, 1992) and survey methodology (Willis, *Cognitive Interviewing*, 2005).

CIP-KGE borrows the technique, not the field. The forensic cognitive interview reconstructs episodic memory of an event; the survey variant pre-tests whether respondents understand questions as intended. CIP-KGE uses the elicitation discipline (no leading questions, no premature summarizing, probe until operationalizable) toward a different target: extracting *domain* knowledge an expert holds, not *episodic* memory of an event.

**Verdict:** technique borrowed, name kept, target changed. The name is defensible but should never be cited as if the protocol had inherited the empirical validation of the forensic literature. It has not.

## CommonKADS

**Origin:** Schreiber et al., *Knowledge Engineering and Management: The CommonKADS Methodology* (2000); successor of KADS (1980s).

CommonKADS is the most complete prior art for structured knowledge elicitation: model-driven (task, inference, domain, agent models), explicit interview techniques, iterative refinement of expertise models toward implementation.

| | CommonKADS | CIP-KGE |
|---|---|---|
| Goal | Build a knowledge-based system that *replicates* expertise | Mutate a curated knowledge *graph* with bounded, reviewable patches |
| Output | Expertise models (informal → formal) | Knowledge Diffs validated against a machine-readable contract |
| Audit granularity | Model documentation | Exchange-level transcript references |
| Role of AI | Target of the engineering effort | Generator of *proposals*, structurally denied write access |

**Verdict:** the *elicitation discipline* in CIP-KGE is not new — CommonKADS normalized it twenty-five years ago. What CommonKADS never needed, and CIP-KGE exists to provide, is the gate: a syntactic contract that AI-generated output must satisfy before a human reviews it. That need is a consequence of the generator being an LLM, not a methodological insight.

## Delphi method

**Origin:** Dalkey & Helmer (RAND, 1963); Linstone & Turoff (1975).

Delphi achieves multi-expert convergence through iterated, anonymous rounds with controlled feedback and statistical aggregation of judgments.

CIP-KGE's `linked_sessions` + reviewer aggregation is, honestly, a **single-round Delphi without anonymity and without the feedback loop**. It captures independent statements from multiple experts but provides no mechanism for them to react to each other's positions. `ARBITRATION.md` reintroduces a feedback element at the *reviewer* level, not the *expert* level.

**Verdict:** if inter-expert consensus (not just independent corroboration) becomes a requirement, the correct move is to adopt Delphi's iteration explicitly — experts shown anonymized convergent/divergent positions across `linked_sessions`, then re-interviewed — rather than pretend the current mechanism approximates consensus. It does not.

## Grounded theory & qualitative rigor criteria

**Origin:** Glaser & Strauss (1967); Strauss & Corbin coding paradigm; Lincoln & Guba, *Naturalistic Inquiry* (1985) for trustworthiness criteria.

This is where the mapping is most uncomfortable, because it is closest:

| CIP-KGE pattern | Established precedent | New or renamed? |
|---|---|---|
| Separation of Evidence and Interpretation (Inv. 3) | Distinction between transcript data / in-vivo codes and analytic memos; Lincoln & Guba's *confirmability* | **Renamed** |
| Traceability Constraint (Inv. 1) | Audit trail for *dependability/confirmability* (Lincoln & Guba); cf. also W3C PROV for provenance modeling | **Renamed**; exchange-level granularity is a specificity, not a novelty |
| Failure Visibility Principle (Inv. 6) | Negative case analysis — deviant cases must be sought and reported, not discarded | **Renamed** |
| Bounded Modification (Inv. 4) | Atomic-change discipline from version control; focused coding units | **Renamed**, with one hardening: it is enforced as `maxItems: 3` in the schema, i.e., a norm turned into a syntactic constraint |
| Explicit Uncertainty (Inv. 5) | Confidence elicitation in knowledge engineering (Hoffman et al.) | **Renamed**, hardened into a required field with a conditional constraint |
| One diff, one session + `linked_sessions` | Independence of coders before reconciliation; weak single-round Delphi (above) | **Renamed** |

**Verdict:** five of the six invariants are established qualitative-research rigor criteria translated into a YAML contract. The translation is not trivial — norms that rely on researcher discipline become *machine-checkable preconditions* — but the intellectual content of the norms is inherited, not invented.

---

## What is actually new (the defensible claim)

Not any single pattern. The defensible novelty is the **integration and its direction of enforcement**:

1. Qualitative-rigor norms (evidence/interpretation separation, audit trail, negative-case visibility) expressed as a **JSON Schema contract** that gates *machine-generated* proposals — the validator rejects structurally non-compliant output before any human spends attention on it.
2. The asymmetry Principle 3–4 encode: the LLM is the only participant that is *structurally* constrained (no write access, mandatory uncertainty declaration, bounded scope), while humans retain every decision that requires judgment. Most human-in-the-loop systems constrain the human's interface to the machine's output; CIP-KGE constrains the machine's access to the shared artifact.

Whether this integration is *valuable* is an empirical question, not a design question. It is exactly what Phase 2 of the roadmap (first real external session, blind second review, test-retest) exists to answer. As of v0.3.1, that evidence does not exist yet.

---

## References (pointers, not full citations)

- Fisher, R.P. & Geiselman, R.E. (1992). *Memory-Enhancing Techniques for Investigative Interviewing.*
- Willis, G.B. (2005). *Cognitive Interviewing: A Tool for Improving Questionnaire Design.*
- Schreiber, G. et al. (2000). *Knowledge Engineering and Management: The CommonKADS Methodology.* MIT Press.
- Dalkey, N. & Helmer, O. (1963). *An Experimental Application of the Delphi Method to the Use of Experts.* Management Science.
- Linstone, H. & Turoff, M. (1975). *The Delphi Method: Techniques and Applications.*
- Glaser, B. & Strauss, A. (1967). *The Discovery of Grounded Theory.*
- Lincoln, Y.S. & Guba, E.G. (1985). *Naturalistic Inquiry.*
- W3C PROV-O (2013). *The PROV Ontology* — provenance data model.
