from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path("data/experiments.db")


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                topic TEXT NOT NULL,
                hook TEXT,
                category TEXT,
                script TEXT,
                keywords_json TEXT,
                strategist_score REAL,
                commercial_relevance REAL,
                status TEXT NOT NULL DEFAULT 'planned',
                video_path TEXT,
                metadata_json TEXT
            )
            """
        )


def save_experiment(item: dict[str, Any]) -> int:
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            """
            INSERT INTO experiments (
                topic, hook, category, script, keywords_json,
                strategist_score, commercial_relevance, status, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item.get("topic"),
                item.get("hook"),
                item.get("category"),
                item.get("script"),
                json.dumps(item.get("keywords", []), ensure_ascii=False),
                item.get("viral_score"),
                item.get("commercial_relevance"),
                item.get("status", "planned"),
                json.dumps(item.get("metadata", {}), ensure_ascii=False),
            ),
        )
        return int(cur.lastrowid)


def mark_rendered(experiment_id: int, video_path: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE experiments SET status='rendered', video_path=? WHERE id=?",
            (video_path, experiment_id),
        )
