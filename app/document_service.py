# app/document_service.py

import datetime

class DocumentService:
    def __init__(self):
        self.docs = {}  # format: {doc_id: [ {version, timestamp, text} ]}

    def add_document(self, doc_id, text, version=None):
        timestamp = datetime.datetime.utcnow().isoformat()
        version = version or self._auto_version(doc_id)

        entry = {
            "doc_id": doc_id,
            "version": version,
            "timestamp": timestamp,
            "text": text
        }

        if doc_id not in self.docs:
            self.docs[doc_id] = []

        self.docs[doc_id].append(entry)
        self.docs[doc_id].sort(key=lambda d: d["version"])  # optional sorting

        return entry

    def get_versions(self, doc_id):
        return self.docs.get(doc_id, [])

    def get_latest(self, doc_id):
        return self.get_versions(doc_id)[-1] if doc_id in self.docs else None

    def _auto_version(self, doc_id):
        versions = self.get_versions(doc_id)
        return versions[-1]["version"] + 1 if versions else 1
