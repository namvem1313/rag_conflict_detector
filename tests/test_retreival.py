# tests/test_retrieval.py

import unittest
from app.ingestion import ingest_document
from app.retrieval import answer_question

class TestRetrieval(unittest.TestCase):

    def setUp(self):
        # Ingest a known document
        ingest_document("doc_test", "Formula A is calculated as x + y")

    def test_answer_question(self):
        answer = answer_question("How is Formula A calculated?")
        self.assertIsInstance(answer, str)
        self.assertIn("x", answer)
