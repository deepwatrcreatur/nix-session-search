import json
import sqlite3
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class SessionRecord:
    session_id: str
    provider: str
    repo_path: str
    repo_name: str
    branch: str
    started_at: str
    ended_at: Optional[str] = None
    source_path: Optional[str] = None

@dataclass
class ChunkRecord:
    session_id: str
    chunk_index: int
    role: str
    content: str
    timestamp: str
    content_hash: Optional[str] = None
    metadata: Optional[str] = None

def ingest_session(db_path: Path, session: SessionRecord, chunks: List[ChunkRecord]):
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            INSERT OR REPLACE INTO sessions 
            (session_id, provider, repo_path, repo_name, branch, started_at, ended_at, source_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session.session_id, session.provider, session.repo_path, 
            session.repo_name, session.branch, session.started_at, 
            session.ended_at, session.source_path
        ))

        for chunk in chunks:
            cursor = conn.execute("""
                INSERT INTO chunks 
                (session_id, chunk_index, role, timestamp, content, content_hash, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                chunk.session_id, chunk.chunk_index, chunk.role, 
                chunk.timestamp, chunk.content, chunk.content_hash, chunk.metadata
            ))
            chunk_id = cursor.lastrowid
            conn.execute("INSERT INTO chunks_fts (content, content_id) VALUES (?, ?)", (chunk.content, chunk_id))
