# interviews/

This directory contains transcripts from Cognitive Interview Protocol sessions.

Each session is stored in its own subdirectory, named by date and a short identifier:

```
interviews/
└── 2026-07-XXXXXXX/
    ├── transcript.md       ← full session transcript
    ├── knowledge_diffs/    ← structured diffs produced from this session
    │   └── diff-001.yaml
    └── notes.md            ← reviewer or analyst notes (optional)
```

## What to include in a transcript

- The full exchange between the AI system and the interviewee.
- Metadata: date, session ID, knowledge graph domain, AI system used, protocol version.
- Anonymization notes, if any content has been modified to protect the interviewee's identity.

## What not to include

- Automatically processed or summarized versions of the transcript. The raw transcript is the record.
- Edits to the interviewee's words that are not marked as such.

No sessions have been conducted yet. This directory documents the intended structure.
