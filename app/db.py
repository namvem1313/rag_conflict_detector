# app/db.py

import sqlite3
import os
import logging

DB_PATH = "storage/rag_data.db"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id TEXT,
            vector TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            doc_id TEXT PRIMARY KEY,
            content TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS conflicts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_id TEXT,
            previous TEXT,
            current TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            resolution TEXT DEFAULT NULL
        )
    ''')

    conn.commit()
    conn.close()
    logging.info("✅ init_db executed and all tables ensured.")



def insert_embedding(doc_id, vector):
    vector_str = ",".join([str(x) for x in vector.tolist()])
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO embeddings (doc_id, vector) VALUES (?, ?)', (doc_id, vector_str))
    conn.commit()
    conn.close()

def fetch_all_embeddings():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT doc_id, vector FROM embeddings')
    rows = c.fetchall()
    conn.close()
    return rows

def insert_document(doc_id, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('REPLACE INTO documents (doc_id, content) VALUES (?, ?)', (doc_id, content))
    conn.commit()
    conn.close()

def fetch_doc_content(doc_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT content FROM documents WHERE doc_id = ?', (doc_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def log_conflict(doc_id, old_text, new_text):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conflicts (doc_id, previous, current) VALUES (?, ?, ?)",
        (doc_id, old_text, new_text)
    )
    conn.commit()
    conn.close()

def fetch_conflicts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conflicts ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_all_conflicts():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT doc_id, old_text, new_text, resolution FROM conflicts")
    rows = c.fetchall()
    conn.close()
    return rows

def resolve_conflict(doc_id, resolution):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "UPDATE conflicts SET resolution = ? WHERE doc_id = ?",
        (resolution, doc_id)
    )
    conn.commit()
    conn.close()

def ensure_ingest_history_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS ingestion_history (
            doc_id TEXT,
            version TEXT,
            PRIMARY KEY (doc_id, version)
        )
    ''')
    conn.commit()
    conn.close()

def already_ingested(doc_id, version):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT 1 FROM ingestion_history WHERE doc_id = ? AND version = ?', (doc_id, version))
    result = c.fetchone()
    conn.close()
    return result is not None

def mark_as_ingested(doc_id, version):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO ingestion_history (doc_id, version) VALUES (?, ?)', (doc_id, version))
    conn.commit()
    conn.close()
