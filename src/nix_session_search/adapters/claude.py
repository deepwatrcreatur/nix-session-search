import json
from pathlib import Path
from ..indexer import SessionRecord, ChunkRecord

def parse_claude_session(file_path: Path):
    with open(file_path, "r") as f:
        data = json.load(f)
    
    session_id = file_path.stem
    metadata = data.get("metadata", {})
    repo_name = metadata.get("project_name", "unknown")
    branch = metadata.get("git_branch", "unknown")
    
    messages = data.get("messages", [])
    if not messages:
        return None, []
        
    started_at = messages[0].get("timestamp", "unknown")
    ended_at = messages[-1].get("timestamp", "unknown")
    
    session = SessionRecord(
        session_id=session_id,
        provider="claude",
        repo_path=str(file_path.parent),
        repo_name=repo_name,
        branch=branch,
        started_at=started_at,
        ended_at=ended_at,
        source_path=str(file_path)
    )
    
    chunks = []
    for i, msg in enumerate(messages):
        chunks.append(ChunkRecord(
            session_id=session_id,
            chunk_index=i,
            role=msg.get("role", "unknown"),
            content=msg.get("content", ""),
            timestamp=msg.get("timestamp", "unknown")
        ))
        
    return session, chunks
