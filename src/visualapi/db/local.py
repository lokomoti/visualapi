"""Local SQLite database."""

import os
import sqlite3
import sys
from contextlib import contextmanager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "db.sqlite3")

SQL_BLACKLIST_TABLE = """--sql
    CREATE TABLE IF NOT EXISTS blacklisted_tokens (
        jti TEXT PRIMARY KEY, 
        blacklisted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
"""

INITS = [SQL_BLACKLIST_TABLE]


def init_db():
    """Initialize the SQLite database."""
    with sqlite3.connect(DB_PATH) as conn:
        for i in INITS:
            conn.execute(i)


@contextmanager
def get_db():
    """Context manager to get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()
