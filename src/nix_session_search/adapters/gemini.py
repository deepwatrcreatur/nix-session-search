import json
from pathlib import Path
from ..indexer import SessionRecord, ChunkRecord

def parse_gemini_log(file_path: Path):
    session_id = file_path.stem
    chunks = []
    
    # Assume JSONL for Gemini CLI logs as per ingest-schema.md example
    with open(file_path, "r") as f:
        for i, line in enumerate(f):
            try:
                data = json.loads(line)
                chunks.append(ChunkRecord(
                    session_id=session_id,
                    chunk_index=i,
                    role=data.get("event", "unknown"),
                    content=json.dumps(data.get("payload", {})),
                    timestamp=data.get("timestamp", "unknown")
                ))
            except json.JSONDecodeError:
                continue
                
    if not chunks:
        return None, []
        
    session = SessionRecord(
        session_id=session_id,
        provider="gemini",
        repo_path=str(file_path.parent),
        repo_name="unknown", # Gemini logs might need better repo detection
        branch="unknown",
        started_at=chunks[0].timestamp,
        ended_at=chunks[-1].timestamp,
        source_path=str(file_path)
    )
    
    return session, chunks
