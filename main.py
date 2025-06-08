import logging
from flask import Flask
from api.routes import app
from app.db import init_db
import sqlite3

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s:%(lineno)d - %(message)s"
)

# Initialize persistent storage
init_db()

conn = sqlite3.connect("./storage/rag_data.db")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
conn.close()

# Run Flask server
if __name__ == "__main__":
    logging.info("Starting RAG Conflict Detection System with persistent storage...")
    app.run(host="0.0.0.0", port=5055, debug=True)