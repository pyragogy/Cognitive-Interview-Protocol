# diffs/

This directory is the audit trail of the CIP-KGE pipeline.

Every Knowledge Diff produced from an interview session is stored here as a YAML file, following the specification in [`docs/KNOWLEDGE_DIFF_SPEC.md`](../docs/KNOWLEDGE_DIFF_SPEC.md).

## File naming

```
diff-YYYY-MM-DD-NNN.yaml
```

Where `NNN` is a zero-padded sequence number for diffs generated on the same date.

## Lifecycle

A diff file in this directory is **never deleted**. Its `review_status` and `merge_ready` fields are updated in place as the diff moves through the pipeline. The git history of the file is the record of its review process.

## Current contents

No diffs have been generated yet. The first diffs will be produced from pilot interview sessions (Phase 2 — see [`docs/ROADMAP.md`](../docs/ROADMAP.md)).

The annotated example in [`examples/diff-001-embodied-foundation/`](../examples/diff-001-embodied-foundation/) shows what a completed diff looks like.
