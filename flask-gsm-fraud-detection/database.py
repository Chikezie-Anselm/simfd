import os
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get('APP_SQLITE_PATH', os.path.join(BASE_DIR, 'app_data.sqlite3'))


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY,
            results_file TEXT UNIQUE,
            save_path TEXT,
            total INTEGER,
            predicted_frauds INTEGER,
            legit_count INTEGER,
            avg_prob REAL,
            note TEXT,
            created_at TEXT
        )
        ''')
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS samples (
            id INTEGER PRIMARY KEY,
            upload_id INTEGER,
            row_index INTEGER,
            row_json TEXT,
            FOREIGN KEY(upload_id) REFERENCES uploads(id) ON DELETE CASCADE
        )
        ''')
    # Users table for authentication
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE,
            password_hash TEXT,
            display_name TEXT,
            created_at TEXT
        )
        ''')
    conn.commit()
    conn.close()


def save_results(results_file: str, save_path: str, df_rows: List[Dict[str, Any]], total: int, predicted_frauds: int, legit_count: int, avg_prob: float, note: str = None):
    """Persist upload metadata and sample rows into the SQLite DB."""
    conn = get_conn()
    cur = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    # Upsert pattern: try insert, on conflict replace
    try:
        cur.execute(
            'INSERT OR REPLACE INTO uploads (results_file, save_path, total, predicted_frauds, legit_count, avg_prob, note, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (results_file, save_path, total, predicted_frauds, legit_count, avg_prob, note, created_at)
        )
        upload_id = cur.lastrowid
        # Delete any existing samples for this upload id (in case of replace)
        cur.execute('DELETE FROM samples WHERE upload_id = ?', (upload_id,))
        # Insert sample rows (store as JSON per row)
        for idx, row in enumerate(df_rows):
            cur.execute('INSERT INTO samples (upload_id, row_index, row_json) VALUES (?, ?, ?)', (upload_id, idx, json.dumps(row)))
        conn.commit()
    finally:
        conn.close()


def list_uploads(limit: int = 100):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, results_file, save_path, total, predicted_frauds, legit_count, avg_prob, note, created_at FROM uploads ORDER BY created_at DESC LIMIT ?', (limit,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def get_upload_by_file(results_file: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, results_file, save_path, total, predicted_frauds, legit_count, avg_prob, note, created_at FROM uploads WHERE results_file = ?', (results_file,))
    r = cur.fetchone()
    if not r:
        conn.close()
        return None
    upload = dict(r)
    cur.execute('SELECT row_index, row_json FROM samples WHERE upload_id = ? ORDER BY row_index', (upload['id'],))
    sample_rows = [json.loads(s['row_json']) for s in cur.fetchall()]
    conn.close()
    upload['sample'] = sample_rows
    return upload


def create_user(email: str, password_hash: str, display_name: str = None):
    conn = get_conn()
    cur = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    try:
        cur.execute('INSERT INTO users (email, password_hash, display_name, created_at) VALUES (?, ?, ?, ?)', (email, password_hash, display_name, created_at))
        conn.commit()
        return cur.lastrowid
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_user_by_email(email: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, email, password_hash, display_name, created_at FROM users WHERE email = ?', (email,))
    r = cur.fetchone()
    conn.close()
    return dict(r) if r else None


def get_user_by_id(user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id, email, password_hash, display_name, created_at FROM users WHERE id = ?', (user_id,))
    r = cur.fetchone()
    conn.close()
    return dict(r) if r else None
