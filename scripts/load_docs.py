# scripts/load_docs.py

import json
from app.ingestion import ingest_document

with open("scripts/example_docs.json", "r") as f:
    data = json.load(f)

for doc in data["documents"]:
    print(f"Ingesting: {doc['doc_id']}")
    ingest_document(doc["doc_id"], doc["text"])
