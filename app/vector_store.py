# app/vector_store.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from app.db import init_db,insert_embedding, fetch_all_embeddings,fetch_doc_content,insert_document

import logging

class VectorStore:
    def __init__(self, embedder):
        init_db()
        self.model = embedder
        self.index = faiss.IndexFlatL2(384)
        self.metadata = []
        self.embed_dim = 384
        self.embeddings = []  
        self._load_from_db()

    def _load_from_db(self):
        rows = fetch_all_embeddings()
        for doc_id, vec_str in rows:
            vec = np.array([float(x) for x in vec_str.split(",")], dtype='float32')
            text = fetch_doc_content(doc_id) or "[N/A]"
            self.embeddings.append(vec)
            self.metadata.append({"doc_id": doc_id, "text": text})
        if self.embeddings:
            self.index.add(np.vstack(self.embeddings))

    def add(self, texts, doc_ids):
        embeddings = self.model.encode(texts)
        for i, text in enumerate(texts):
            vec = embeddings[i].astype('float32')
            self.index.add(np.array([vec]))
            insert_embedding(doc_ids[i], vec)
            insert_document(doc_ids[i],text)
            self.metadata.append({
                "doc_id": doc_ids[i],
                "text": text
            })

    def search(self, query, k=3):
        if self.index.ntotal == 0:
            return []
        query_vec = self.model.encode([query]).astype('float32')
        D, I = self.index.search(np.array(query_vec), k)
        return [self.metadata[i] for i in I[0] if i < len(self.metadata)]
