# Procedural Memory Extraction

This document defines the schema and flow for extracting reusable knowledge from
agent session transcripts.

## Candidate Memory Types

- **Fix:** A technical resolution for a specific error message.
- **Workflow:** A sequence of commands that achieves a high-level goal (e.g., "how to re-encrypt secrets").
- **Identity:** Identifying a machine, user, or service role.
- **Policy:** A rule or constraint (e.g., "always use raw sockets for Kea").

## Record Schema

- `memory_id`: UUID
- `type`: [Fix | Workflow | Identity | Policy]
- `summary`: One-sentence description.
- `content`: The actual procedure or fact.
- `confidence`: [Low | Medium | High]
- `provenance`: `session_id` + `chunk_indices`
- `tags`: List of keywords.
- `created_at`: Timestamp.

## Human-Reviewable Flow

1. **Discovery:** Search `nix-session-search` for a topic.
2. **Extraction:** Use an agent to draft a memory record from relevant chunks.
3. **Review:** A human (or high-confidence agent) verifies the record.
4. **Persistence:** Commit the record to the `docs/memory/` directory in the target repo.

## Rationale

By keeping provenance explicit, we ensure that every piece of "learned" knowledge
can be traced back to the original conversation where it was discovered, avoiding
untraceable "ghost knowledge" in the repo.
