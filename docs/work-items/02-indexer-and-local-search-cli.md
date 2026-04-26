# 02 Indexer And Local Search CLI

Status: done

## Goal

Provide useful local search over prior agent sessions.

## Deliverables

- indexing pipeline (implemented in `src/nix_session_search/indexer.py`)
- search CLI with JSON output (implemented in `src/nix_session_search/cli.py`)
- filters for repo, provider, branch, and time range
- snippet extraction with source references

## Notes

- local-first is mandatory
- start with exact/full-text retrieval before semantic retrieval

## Progress

- basic SQLite + FTS schema implemented
- search and index commands functional
- supports multi-adapter ingestion
