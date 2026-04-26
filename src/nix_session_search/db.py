import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    provider TEXT,
    repo_path TEXT,
    repo_name TEXT,
    branch TEXT,
    started_at TEXT,
    ended_at TEXT,
    source_path TEXT
);

CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    chunk_index INTEGER,
    role TEXT,
    timestamp TEXT,
    content TEXT,
    content_hash TEXT,
    metadata TEXT,
    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
);

CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
    content,
    content_id UNINDEXED
);
"""

def init_db(db_path: Path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.executescript(SCHEMA)
