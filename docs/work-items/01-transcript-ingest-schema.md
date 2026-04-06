# 01 Transcript Ingest Schema

Status: in-progress

## Goal

Define a stable schema for transcript ingestion.

## Deliverables

- canonical record format
- session-level and chunk-level fields
- storage choice recommendation
- examples from at least two provider transcript styles

## Notes

- optimize for later retrieval and indexing
- do not depend on one vendor format

## Progress

- session and chunk record shapes defined
- SQLite plus FTS chosen as the initial storage direction
- provider targets narrowed to Codex CLI, Claude Code, and Gemini CLI
