# app/__init__.py

from .vector_store import VectorStore
from .models import load_models

# Global store and models (shared across routes/modules)
embedder, nli_model, qa_model = load_models()
store = VectorStore(embedder)

