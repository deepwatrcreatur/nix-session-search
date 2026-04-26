import argparse
import json
import sqlite3
import sys
from pathlib import Path
from .db import init_db
from .indexer import ingest_session
from .adapters.claude import parse_claude_session
from .adapters.gemini import parse_gemini_log

DEFAULT_DB_PATH = Path("~/.cache/nix-session-search/sessions.db").expanduser()

def search_command(args):
    if not args.db.exists():
        print(f"Error: Database not found at {args.db}", file=sys.stderr)
        return 1

    with sqlite3.connect(args.db) as conn:
        conn.row_factory = sqlite3.Row
        # Simple FTS search query
        query = """
            SELECT chunks.content, chunks.role, chunks.timestamp, sessions.repo_name, sessions.session_id 
            FROM chunks 
            JOIN sessions ON chunks.session_id = sessions.session_id 
            JOIN chunks_fts ON chunks.id = chunks_fts.content_id 
            WHERE chunks_fts MATCH ?
        """
        
        params = [args.query]
        
        results = []
        for row in conn.execute(query, params):
            results.append(dict(row))

    print(json.dumps({
        "status": "ok",
        "query": args.query,
        "result_count": len(results),
        "results": results
    }, indent=2))
    return 0

def index_command(args):
    init_db(args.db)
    print(f"Initialized database at {args.db}")
    
    # Simple indexing of provided paths
    for path_str in args.paths:
        path = Path(path_str).expanduser().resolve()
        if not path.exists():
            print(f"Warning: path {path} does not exist, skipping", file=sys.stderr)
            continue
            
        if path.is_dir():
            files = list(path.glob("*.json")) + list(path.glob("*.jsonl"))
        else:
            files = [path]
            
        for f in files:
            session, chunks = None, []
            if f.suffix == ".json":
                # Try Claude adapter
                try:
                    session, chunks = parse_claude_session(f)
                except Exception:
                    pass
            elif f.suffix == ".jsonl":
                # Try Gemini adapter
                try:
                    session, chunks = parse_gemini_log(f)
                except Exception:
                    pass
                    
            if session and chunks:
                print(f"Indexing session {session.session_id} from {f.name}")
                ingest_session(args.db, session, chunks)
                
    return 0

def main():
    parser = argparse.ArgumentParser(prog="nix-session-search")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH)
    subparsers = parser.add_subparsers(dest="subcommand")

    index_parser = subparsers.add_parser("index")
    index_parser.add_argument("paths", nargs="+", help="Files or directories to index")
    
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("query")
    search_parser.add_argument("--repo")
    search_parser.add_argument("--provider")

    args = parser.parse_args()
    
    if args.subcommand == "index":
        return index_command(args)
    elif args.subcommand == "search":
        return search_command(args)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
