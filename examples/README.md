# examples/

This directory contains annotated worked examples of *knowledge diffs* — structured proposals for knowledge graph modifications generated through Cognitive Interview Protocol sessions.

Examples serve two purposes:

1. **Protocol validation.** They demonstrate what a well-formed *knowledge diff* looks like in practice, and surface edge cases the protocol specification does not yet handle.
2. **Onboarding.** They allow a new contributor to understand the expected output format without reading the full protocol specification.

## Structure of an example

Each example is a subdirectory containing:

```
examples/
└── example-001-[short-description]/
    ├── README.md           ← what this example demonstrates
    ├── diff.yaml           ← the knowledge diff itself
    ├── context.md          ← the interview exchange that generated the diff
    └── review-notes.md     ← simulated or real reviewer response
```

## Status

No examples exist yet. The first examples will be produced from pilot interview sessions, planned for the v0.2 phase. See `docs/ROADMAP.md`.
