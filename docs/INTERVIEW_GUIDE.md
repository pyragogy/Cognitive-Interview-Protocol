# Interview Guide

> **CIP-KGE v0.2**
>
> This guide defines the question types used in CIP-KGE interview sessions and maps each type
> to the sections of the Pyragogy Syllabus node schema.
>
> An interviewer (or an AI system conducting an interview) that uses this guide produces evidence
> that can be mapped to specific sections of a node. An interviewer that does not use this guide
> produces a conversation — useful, but not directly transformable into a Knowledge Diff.

---

## Prerequisite: read the target node

Before beginning a session, read the current published version of the target node at `syllabus.pyragogy.org`. Know what is already there. The interview is not about discovering what the node says — it is about finding where it is incomplete, imprecise, or wrong.

---

## The five question types

### Q1 — Elicitation

**Purpose:** Surface what the interviewee knows about the concept, without presupposing the structure of the answer.

**When to use:** At the start of the session, before more targeted questions. Also useful when the interviewee goes silent — a broad elicitation question restarts the flow.

**Example forms:**
- *"Can you describe how [concept X] manifests in your experience?"*
- *"When you encounter [situation Y], what typically happens?"*
- *"What would a student look like who has developed [concept X] well?"*

**Sections it primarily serves:** `definition`, `use_case`, `observable_markers`

---

### Q2 — Clarification

**Purpose:** Make a statement the interviewee has made more precise — operationalize vague terms, specify scope, pin down generalities.

**When to use:** Immediately after any statement that contains undefined scope ("usually", "sometimes", "in most cases", "this can lead to").

**Example forms:**
- *"When you say 'usually' — what conditions determine the exception?"*
- *"You said 'the learner struggles'. What does that struggling look like, concretely?"*
- *"What would have to be different for [X] not to apply?"*

**Sections it primarily serves:** `observable_markers`, `use_case`, `friction`

---

### Q3 — Socratic challenge

**Purpose:** Test the reasoning behind a claim by probing its premises and its limits. The AI acts as a constructive adversary, not a validator.

**When to use:** When the interviewee has stated something with confidence. When a claim seems to rest on an assumption the interviewee has not articulated.

**Example forms:**
- *"What would have to be true for that not to hold?"*
- *"You said [X]. A critic might say [Y]. How would you respond?"*
- *"Is there a case where [the recommended approach] makes things worse?"*

**Sections it primarily serves:** `risk`, `friction`, `definition` (boundary refinement)

**Note:** This question type is the hardest to conduct well. The challenge must be substantive — based on the actual content of the interviewee's statements — not a generic Devil's Advocate. A Socratic challenge that the interviewee cannot engage with means the question was poorly formed, not that the interviewee is wrong.

---

### Q4 — Contrastive

**Purpose:** Ask the interviewee to compare the concept under discussion to an alternative or a closely related concept. Contrasts often reveal the precise boundary of a concept better than direct definitions.

**When to use:** When the definition feels underspecified. When two concepts in the graph seem to overlap. When the interviewee has not drawn a distinction that the graph requires.

**Example forms:**
- *"How does [concept X] differ from [concept Y]?"*
- *"If someone said [concept X] and [concept Z] are the same thing, what would you correct?"*
- *"In what way is [the proposed approach] different from simply doing [the standard approach]?"*

**Sections it primarily serves:** `definition`, `ai_role`, `human_role`

---

### Q5 — Mapping

**Purpose:** Ask the interviewee to describe the relationships between this concept and other concepts — upstream prerequisites, downstream consequences, related failure modes.

**When to use:** When the interview has produced strong evidence for isolated sections but the node's connections to the rest of the graph are unclear. Also useful near the end of the session.

**Example forms:**
- *"What needs to be in place before [concept X] can work?"*
- *"What typically breaks if [concept X] is skipped?"*
- *"Is there a node in the graph that [concept X] depends on, or that depends on it?"*

**Sections it primarily serves:** `risk`, `use_case`, wikilink targets

---

## Section-to-question-type mapping

| Section | Primary question types | Notes |
|---|---|---|
| **definition** | Q1, Q4, Q3 | Start with Q1; use Q4 to refine boundaries; use Q3 to stress-test |
| **use_case** | Q1, Q2 | Q1 to surface contexts; Q2 to make them precise |
| **human_role** | Q1, Q2 | Focus on *observable behavior*, not intentions |
| **ai_role** | Q4, Q3 | What should AI refuse? What does it contribute? Use contrast with human role |
| **friction** | Q2, Q3 | The mechanism must be specific. "Difficulty" is not friction. Q3 surfaces what would bypass it |
| **risk** | Q3, Q5 | Q3: what breaks? Q5: what other nodes are affected? |
| **observable_markers** | Q2, Q1 | Must be *external* and *verifiable*. Q2 repeatedly until the marker is observable, not internal |

---

## Conducting a session: sequence

A session that follows this sequence produces evidence that is easier to map to sections:

1. **Context** (5 min): explain the session purpose, the target node, and that the output is a Knowledge Diff subject to human review.

2. **Elicitation** (Q1): one or two broad questions to let the interviewee orient.

3. **Section focus**: move through the node's sections in order, using the primary question types for each. You do not need to cover all sections in one session — a session focused on `risk` and `observable_markers` is more valuable than a session that covers everything superficially.

4. **Mapping** (Q5): near the end, ask about relationships to other nodes. This often surfaces evidence for new wikilinks or reveals gaps in the graph's structure.

5. **Closing**: ask the interviewee if there is something the questions did not reach. End the session explicitly.

---

## What the interview should not do

- **Do not summarize or paraphrase** the interviewee's words back to them as confirmation. Summarizing introduces the interviewer's interpretation before it belongs in the process — that happens in Stage 3 (Evidence Extraction), not during the session.

- **Do not suggest answers.** A question like "Would you say the risk here is automation bias?" has contaminated the evidence before it is collected.

- **Do not close topics prematurely.** If an interviewee gives a thin answer to a section question, do not move on. Return to it with a different question type.

- **Do not conduct an opinion poll.** The interview is not asking "what do you think the node should say?" It is asking "what do you know about this phenomenon?" The Knowledge Diff is where the session's evidence is translated into a proposal — that translation happens after the session, not during it.
