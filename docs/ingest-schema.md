# Transcript Ingest Schema

## Core Records

### Session

- `schema_version`
- `session_id`
- `provider`
- `repo_path`
- `repo_name`
- `branch`
- `started_at`
- `ended_at`
- `source_path`

### Chunk

- `session_id`
- `chunk_index`
- `role`
- `timestamp`
- `content`
- `content_hash`
- `metadata`

## Provider Requirements

Adapters should preserve:

- raw timestamps where available
- provider-specific ids
- enough source metadata to re-open the original transcript

## Storage Direction

Start with SQLite plus FTS.

Reasons:

- local-first
- simple packaging
- strong enough for exact retrieval and snippets

## Initial Providers

- Codex CLI
- Claude Code
- Gemini CLI
