# api/routes.py

from flask import Flask, request, jsonify
from app import store
from app.ingestion import ingest_document
from app.retrieval import answer_question
from app.db import fetch_conflicts

app = Flask(__name__)

@app.route("/")
def health_check():
    return "RAG Conflict System is running."

@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.json
    doc_id = data.get("doc_id")
    text = data.get("text")
    version = data.get("version")

    if not doc_id or not text:
        return jsonify({"error": "Missing 'doc_id' or 'text'"}), 400

    ingest_document(doc_id, text, version)
    return jsonify({"status": f"Document {doc_id} ingested"}), 200


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    result = answer_question(question)
    return jsonify(result), 200

@app.route("/doc/<doc_id>", methods=["DELETE"])
def delete_doc(doc_id):
    store.delete(doc_id)
    return jsonify({"status": f"document {doc_id} deleted"}), 200

@app.route("/docs", methods=["GET"])
def list_docs():
    return jsonify({"documents": [doc["doc_id"] for doc in store.metadata]}), 200

@app.route("/conflicts", methods=["GET"])
def list_conflicts():
    rows = fetch_conflicts()
    return jsonify([
        {"id": row[0], "doc_id": row[1], "old": row[2], "new": row[3], "timestamp": row[4]}
        for row in rows
    ])

@app.route("/delta-ingest", methods=["POST"])
def delta_ingest():
    data = request.json
    doc_id = data["doc_id"]
    text = data["text"]
    version = data.get("version", "1")

    try:
        ingest_document(doc_id, text, version)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

