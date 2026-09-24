"""SQLite database storage for learner progress and evidence."""
import sqlite3
import json
import os
from typing import Dict, List, Optional, Any

DB_PATH = os.environ.get("PORTAL_DB_PATH", "portal.db")


def get_db_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DB_PATH) -> None:
    conn = get_db_connection(db_path)
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS skill_progress (
                skill_id TEXT PRIMARY KEY,
                state TEXT NOT NULL,
                mastery_score REAL NOT NULL DEFAULT 0.0,
                completed_activities TEXT NOT NULL DEFAULT '[]',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS evidence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill_id TEXT NOT NULL,
                activity_id TEXT NOT NULL,
                is_correct INTEGER NOT NULL,
                given_response TEXT,
                feedback TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.close()


def save_skill_progress(skill_id: str, state: str, mastery_score: float, completed_activities: List[str], db_path: str = DB_PATH) -> None:
    conn = get_db_connection(db_path)
    activities_json = json.dumps(completed_activities)
    with conn:
        conn.execute("""
            INSERT INTO skill_progress (skill_id, state, mastery_score, completed_activities, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(skill_id) DO UPDATE SET
                state = excluded.state,
                mastery_score = excluded.mastery_score,
                completed_activities = excluded.completed_activities,
                updated_at = CURRENT_TIMESTAMP
        """, (skill_id, state, mastery_score, activities_json))
    conn.close()


def get_all_skill_progress(db_path: str = DB_PATH) -> Dict[str, Dict[str, Any]]:
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT skill_id, state, mastery_score, completed_activities FROM skill_progress")
    rows = cursor.fetchall()
    conn.close()

    result = {}
    for row in rows:
        result[row["skill_id"]] = {
            "state": row["state"],
            "mastery_score": row["mastery_score"],
            "completed_activities": json.loads(row["completed_activities"]),
        }
    return result


def record_evidence(skill_id: str, activity_id: str, is_correct: bool, given_response: str, feedback: str, db_path: str = DB_PATH) -> None:
    conn = get_db_connection(db_path)
    with conn:
        conn.execute("""
            INSERT INTO evidence (skill_id, activity_id, is_correct, given_response, feedback)
            VALUES (?, ?, ?, ?, ?)
        """, (skill_id, activity_id, 1 if is_correct else 0, given_response, feedback))
    conn.close()


def reset_learner_db(db_path: str = DB_PATH) -> None:
    conn = get_db_connection(db_path)
    with conn:
        conn.execute("DELETE FROM skill_progress")
        conn.execute("DELETE FROM evidence")
    conn.close()
