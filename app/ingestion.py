# app/ingestion.py

from app.vector_store import VectorStore
from app.db import already_ingested, mark_as_ingested
from app import store,nli_model
from app.db import log_conflict
import logging
from app.document_service import DocumentService


# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
doc_service = DocumentService()


def ingest_document(doc_id: str, text: str, version: int = None):

    if already_ingested(doc_id, version):
        print(f"Document {doc_id} v{version} already ingested. Skipping.")
        return
    
    logger.info(f"Ingesting document: {doc_id} (version {version})")

    # Add to versioned document store
    entry = doc_service.add_document(doc_id, text, version)

    # Check conflict with latest version before this
    previous_versions = doc_service.get_versions(doc_id)
    if len(previous_versions) > 1:
        latest_prior = previous_versions[-2]["text"]
        conflicts = detect_conflict_pair(text, latest_prior)
        if conflicts:
            logger.warning(f"Conflict with previous version of {doc_id}")
            logger.warning(f"→ Previous: {latest_prior}")
            logger.warning(f"→ New: {text}")
            log_conflict(doc_id, latest_prior, text)
    else:
        logger.info("No previous version to compare.")

    # Add to vector store
    store.add([text], [f"{doc_id}_v{entry['version']}"])
    mark_as_ingested(doc_id, version)


def detect_conflict_pair(new_text, old_text, threshold: float = 0.7):
    combined = new_text + " </s> " + old_text
    result = nli_model(combined)[0]
    if result["label"] == "CONTRADICTION" and result["score"] > threshold:
        return [result]
    return []
