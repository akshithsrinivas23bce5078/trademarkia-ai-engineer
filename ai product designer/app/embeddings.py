# app/embeddings.py
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from sklearn.datasets import fetch_20newsgroups

class VectorStore:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatIP(self.dimension) # Inner Product (Cosine Sim if normalized)
        self.documents = []

    def ingest_data(self):
        # Fetching clean data
        dataset = fetch_20newsgroups(subset='all', remove=('headers', 'footers', 'quotes'))
        docs = [doc for doc in dataset.data if len(doc.strip()) > 50] # Discard overly short/noisy docs
        self.documents = docs
        
        # Embed and add to FAISS
        embeddings = self.model.encode(docs, convert_to_numpy=True, normalize_embeddings=True)
        self.index.add(embeddings)
        return embeddings