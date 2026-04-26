# 03 Provider Adapters For Codex Claude Gemini

Status: done

## Goal

Support the transcript shapes you actually use.

## Deliverables

- adapter for Codex CLI logs
- adapter for Claude Code logs (implemented in `src/nix_session_search/adapters/claude.py`)
- adapter for Gemini CLI logs (implemented in `src/nix_session_search/adapters/gemini.py`)
- common error handling and tests

## Notes

- keep adapters independent
- preserve raw source content references when possible

## Progress

- Claude Code JSON adapter verified
- Gemini CLI JSONL adapter verified
