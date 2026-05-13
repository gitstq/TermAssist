#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
History management for TermAssist
历史记录管理
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class HistoryEntry:
    """History entry"""
    id: Optional[int]
    timestamp: str
    input_text: str
    output: str
    mode: str  # 'generate' or 'explain'
    executed: bool
    success: Optional[bool]


class HistoryManager:
    """Manage command history"""
    
    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            config_dir = Path.home() / ".config" / "termassist"
            config_dir.mkdir(parents=True, exist_ok=True)
            db_path = config_dir / "history.db"
        
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    input_text TEXT NOT NULL,
                    output TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    executed INTEGER DEFAULT 0,
                    success INTEGER DEFAULT NULL
                )
            """)
            conn.commit()
    
    def add(self, input_text: str, output: str, mode: str, 
            executed: bool = False, success: Optional[bool] = None) -> int:
        """Add history entry"""
        timestamp = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """INSERT INTO history (timestamp, input_text, output, mode, executed, success)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (timestamp, input_text, output, mode, int(executed), 
                 int(success) if success is not None else None)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_recent(self, limit: int = 20) -> List[HistoryEntry]:
        """Get recent history entries"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """SELECT id, timestamp, input_text, output, mode, executed, success
                   FROM history ORDER BY timestamp DESC LIMIT ?""",
                (limit,)
            )
            rows = cursor.fetchall()
        
        return [
            HistoryEntry(
                id=row[0],
                timestamp=row[1],
                input_text=row[2],
                output=row[3],
                mode=row[4],
                executed=bool(row[5]),
                success=bool(row[6]) if row[6] is not None else None
            )
            for row in rows
        ]
    
    def search(self, query: str, limit: int = 20) -> List[HistoryEntry]:
        """Search history entries"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """SELECT id, timestamp, input_text, output, mode, executed, success
                   FROM history 
                   WHERE input_text LIKE ? OR output LIKE ?
                   ORDER BY timestamp DESC LIMIT ?""",
                (f"%{query}%", f"%{query}%", limit)
            )
            rows = cursor.fetchall()
        
        return [
            HistoryEntry(
                id=row[0],
                timestamp=row[1],
                input_text=row[2],
                output=row[3],
                mode=row[4],
                executed=bool(row[5]),
                success=bool(row[6]) if row[6] is not None else None
            )
            for row in rows
        ]
    
    def update_execution_status(self, entry_id: int, success: bool):
        """Update execution status"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """UPDATE history SET executed = 1, success = ? WHERE id = ?""",
                (int(success), entry_id)
            )
            conn.commit()
    
    def clear(self):
        """Clear all history"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM history")
            conn.commit()
    
    def get_stats(self) -> Dict[str, int]:
        """Get history statistics"""
        with sqlite3.connect(self.db_path) as conn:
            total = conn.execute("SELECT COUNT(*) FROM history").fetchone()[0]
            generate_count = conn.execute(
                "SELECT COUNT(*) FROM history WHERE mode = 'generate'"
            ).fetchone()[0]
            explain_count = conn.execute(
                "SELECT COUNT(*) FROM history WHERE mode = 'explain'"
            ).fetchone()[0]
            executed_count = conn.execute(
                "SELECT COUNT(*) FROM history WHERE executed = 1"
            ).fetchone()[0]
            success_count = conn.execute(
                "SELECT COUNT(*) FROM history WHERE success = 1"
            ).fetchone()[0]
        
        return {
            "total": total,
            "generate": generate_count,
            "explain": explain_count,
            "executed": executed_count,
            "success": success_count,
        }
    
    def export_to_json(self, filepath: Path):
        """Export history to JSON"""
        entries = self.get_recent(limit=10000)
        data = [
            {
                "id": e.id,
                "timestamp": e.timestamp,
                "input": e.input_text,
                "output": e.output,
                "mode": e.mode,
                "executed": e.executed,
                "success": e.success,
            }
            for e in entries
        ]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def import_from_json(self, filepath: Path):
        """Import history from JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for item in data:
            self.add(
                input_text=item["input"],
                output=item["output"],
                mode=item["mode"],
                executed=item.get("executed", False),
                success=item.get("success")
            )
