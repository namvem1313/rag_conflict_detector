# app/models.py

from transformers import pipeline
from sentence_transformers import SentenceTransformer

def load_models():
    """
    Loads all necessary models:
    - Embedding model for vector DB
    - NLI model for conflict detection
    - QA model for RAG answer generation
    """
    # Sentence embedding model for vector store
    embedder = SentenceTransformer('all-MiniLM-L6-v2')

    # Natural Language Inference model for conflict detection
    nli_model = pipeline("text-classification", model="roberta-large-mnli")

    # QA model for retrieval-augmented generation
    qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

    return embedder, nli_model, qa_model
