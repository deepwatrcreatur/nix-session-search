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

## Example Provider Styles

### Claude Code (`~/.claude/sessions/`)
Claude Code stores sessions in JSON files.
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hello",
      "timestamp": "2026-04-24T10:00:00.000Z"
    },
    {
      "role": "assistant",
      "content": "Hi! How can I help you today?",
      "timestamp": "2026-04-24T10:00:05.000Z"
    }
  ],
  "metadata": {
    "project_name": "nix-session-search",
    "git_branch": "main"
  }
}
```

### Gemini CLI (`~/.gemini/logs/`)
Gemini CLI (standard agent pattern) often logs in append-only JSONL or separate timestamped files.
```json
{
  "timestamp": "2026-04-24T11:00:00Z",
  "event": "request",
  "payload": {
    "prompt": "Explain this code",
    "files": ["src/main.rs"]
  }
}
{
  "timestamp": "2026-04-24T11:00:10Z",
  "event": "response",
  "payload": {
    "text": "This code implements..."
  }
}
```
