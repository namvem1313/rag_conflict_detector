# tests/test_ingestion.py

import unittest
from app.ingestion import ingest_document, detect_conflict
from app.vector_store import VectorStore

class TestIngestion(unittest.TestCase):

    def setUp(self):
        # Set up a new vector store for each test
        self.store = VectorStore()

    def test_no_conflict(self):
        ingest_document("doc1", "Formula A = x + y")
        conflicts = detect_conflict("Formula B = x - y")
        self.assertEqual(len(conflicts), 0)

    def test_detect_conflict(self):
        ingest_document("doc2", "Formula A = x + y")
        conflicts = detect_conflict("Formula A = x - y")
        self.assertGreaterEqual(len(conflicts), 1)
