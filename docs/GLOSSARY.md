# Glossary

> **CIP-KGE v0.2**
>
> Defined terms used in the Cognitive Interview Protocol for Knowledge Graph Evolution.
>
> This glossary distinguishes, for each entry, between:
> - **Project coinage**: terms introduced or defined in a specific sense by this project.
> - **Established field**: terms borrowed from existing literature, with a reference.
>
> Where a term is project coinage, that is stated explicitly.
> Where a term borrows from an established field, the source is cited or marked `[VERIFY SOURCE]`.
> Presenting project coinage as established field is an error this glossary is designed to prevent.

---

## Knowledge Diff

*Project coinage.*

A structured artifact representing a proposed modification to a knowledge graph. A *knowledge diff* is produced as output from a Cognitive Interview Protocol session. It is not the interview itself, and it is not an automatic edit to the knowledge graph. It is a bounded, human-readable proposal for a change, with explicit provenance and review status.

The term borrows the word *diff* from version control practice — where a diff represents a structured, reviewable representation of proposed changes to a document — but applies it to knowledge graph content rather than text files. The extension is project-specific; we do not claim the term is established in knowledge engineering literature.

A *knowledge diff* must include, at minimum:

- A reference to the interview session that generated it.
- A reference to the specific exchange within the session that grounded the proposed change.
- A description of the proposed modification (what would change, what would be added, what would be removed).
- A review status: `proposed`, `under review`, `accepted`, `rejected`, or `deferred`.

---

## Knowledge Graph

*Established field.*

A structured representation of knowledge as a network of entities and relationships. [VERIFY SOURCE: canonical definition in knowledge representation literature — Hogan et al. 2021 "Knowledge Graphs" is a candidate reference]

In the context of this protocol, *knowledge graph* is used broadly to include any formal representation of domain knowledge in which individual statements can be identified, modified, and traced. This includes but is not limited to RDF-based graphs, property graphs, and ontologies.

---

## Cognitive Interview

*Established field, adapted.*

The term *cognitive interview* originates in forensic and investigative psychology, where it refers to a structured technique for eliciting detailed, accurate recall from witnesses. [VERIFY SOURCE: Fisher & Geiselman 1992 "Memory-Enhancing Techniques for Investigative Interviewing" is the canonical reference]

In this project, the term is used in an extended sense: a structured interview designed to surface tacit expert knowledge, conducted with the assistance of an AI system. The AI does not replace the interviewer; it operates according to a defined protocol that shapes the structure, sequence, and style of questions. The adaptation is project-specific; the connection to the forensic original is the emphasis on structured, reliable elicitation rather than free-form conversation.

---

## Knowledge Update Proposal

*Project coinage.*

A synonym for *knowledge diff*, used in contexts where the diff metaphor may not be appropriate (e.g., when the knowledge representation does not have a diff-like structure). The two terms are used interchangeably in this repository; *knowledge diff* is preferred.

---

## Provenance

*Established field.*

Information about the origin of a piece of data or a claim — who produced it, when, under what conditions, and through what process. [VERIFY SOURCE: W3C PROV standard is a candidate reference]

In this protocol, provenance is a required property of every *knowledge diff*. A proposal without provenance cannot be independently reviewed, because the reviewer has no basis for evaluating the conditions under which the evidence was collected.

---

## Review Status

*Project coinage (the specific vocabulary).*

The current state of a *knowledge diff* in the review process. The following states are defined:

- **`proposed`**: The diff has been generated and submitted for review. No evaluation has begun.
- **`under review`**: A reviewer has accepted responsibility for evaluating the diff.
- **`accepted`**: The reviewer has evaluated the diff and judged the proposed change to be well-grounded and appropriate.
- **`rejected`**: The reviewer has evaluated the diff and judged the proposed change to be inadequately grounded, incorrect, or inappropriate.
- **`deferred`**: The reviewer has evaluated the diff and judged that a decision cannot be made without additional evidence or context.

These states are provisional. The review workflow is an open research question.

---

## Tacit Knowledge

*Established field.*

Knowledge that a practitioner possesses but cannot fully articulate — skills, intuitions, and judgments that are acquired through experience and are difficult to transfer through explicit instruction. [VERIFY SOURCE: Polanyi 1966 "The Tacit Dimension" is the canonical reference; Nonaka & Takeuchi 1995 on explicit/tacit knowledge transfer is also relevant]

Surfacing tacit knowledge is one of the primary motivations for using structured interviews rather than direct elicitation methods such as questionnaires or documentation review.

---

## Node

*Project coinage (in this specific sense).*

A node in the Pyragogy Syllabus knowledge graph. Concretely: a single Markdown file in the `content/` directory of [pyragogy/ai-pedagogy](https://github.com/pyragogy/ai-pedagogy), following the seven-section schema defined in [`SYLLABUS_SCHEMA.md`](./SYLLABUS_SCHEMA.md). A node is identified by its path relative to `content/`, without the `.md` extension (e.g., `02_ontogeny/embodied_foundation`).

The term *node* is standard in graph theory and in knowledge graph literature; we use it here in that general sense, with the specific meaning grounded in the Pyragogy Syllabus's Quartz-based structure.

---

## Section

*Project coinage (in this specific sense).*

One of the seven fixed divisions of a syllabus node: `definition`, `use_case`, `human_role`, `ai_role`, `friction`, `risk`, `observable_markers`. A Knowledge Diff operates at the level of a section — not at the level of the node as a whole. A change to a node that does not specify which section it modifies is not a valid Knowledge Diff in CIP-KGE v0.2.

The term *section* is not specific to knowledge graphs; we use it here in the document-structure sense, applied to the node's internal organization.

---

## Backlink

*Established field (in the Quartz/wiki sense).*

A link from a node B to node A that is automatically computed from the presence of a wikilink (`[[A]]`) in node B's content. Quartz computes and displays backlinks automatically. In CIP-KGE, a Knowledge Diff that proposes adding a wikilink to a section must verify that the target node exists — otherwise it creates a dangling reference. A diff that removes a wikilink must consider whether the source node's argument depends on that link.

---

## Merge

*Established field (version control), applied here.*

The act of incorporating an accepted Knowledge Diff into the `pyragogy/ai-pedagogy` repository by merging a pull request into the `main` branch. After merge, Quartz rebuilds the syllabus automatically and the change becomes visible at `syllabus.pyragogy.org`. In CIP-KGE, *merge* is the terminal event of the pipeline — the point at which a Knowledge Diff has produced an observable improvement in the graph.

The term is borrowed from Git and GitHub practice without modification.

---

## Pipeline

*Project coinage.*

The ten-stage process defined in [`PIPELINE.md`](./PIPELINE.md) that transforms an interview session into a syllabus update. The stages are: Session Preparation, Interview Session, Evidence Extraction, Knowledge Diff Generation, Pre-Review Quality Check, Human Review, Markdown Transformation, Pull Request, Syllabus Update, Diff Archival.

The term *pipeline* is common in software engineering and data processing; we use it here in the general sense of a sequential, stage-gated process. The specific ten-stage structure is project coinage.

---

## Evidence Bundle

*Project coinage.*

An intermediate artifact produced in Stage 3 of the pipeline (Evidence Extraction). It maps specific numbered exchanges from a session transcript to specific sections of the target node. The evidence bundle is the input to Knowledge Diff generation; without it, a diff has no traceable connection to the session that produced it.

Stored at `interviews/{session_id}/evidence.md`.
