# Agent Prompts

## Prompt 1

Define the ingest schema.

Requirements:
- normalize session id, provider, repo, branch, timestamps, and transcript chunks
- support incremental ingestion
- keep raw text retrievable

## Prompt 2

Build the indexer and search CLI.

Requirements:
- support local full-text search
- add filters for repo, provider, date range, and branch
- return snippets with stable references

## Prompt 3

Add provider adapters.

Requirements:
- support Codex, Claude Code, and Gemini CLI transcript layouts
- isolate provider-specific parsing from the core schema
- fail safely on partial or malformed logs
