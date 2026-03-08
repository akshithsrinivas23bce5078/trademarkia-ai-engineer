# app/cache.py
import numpy as np

class SemanticCache:
    def __init__(self, similarity_threshold=0.85):
        self.threshold = similarity_threshold
        self.cache_store = {} # Format: { cluster_id: [ {"query_emb": emb, "text": text, "result": res} ] }
        self.hits = 0
        self.misses = 0

    def check_cache(self, query_emb, dominant_cluster):
        if dominant_cluster not in self.cache_store:
            return None, 0.0

        cluster_cache = self.cache_store[dominant_cluster]
        
        best_score = -1
        best_match = None

        # Compute cosine similarity against items in the dominant cluster ONLY
        for item in cluster_cache:
            score = np.dot(query_emb, item["query_emb"]) # Assuming embeddings are normalized
            if score > best_score:
                best_score = score
                best_match = item

        if best_score >= self.threshold:
            self.hits += 1
            return best_match, best_score
        
        self.misses += 1
        return None, best_score

    def add_to_cache(self, query_emb, text, result, dominant_cluster):
        if dominant_cluster not in self.cache_store:
            self.cache_store[dominant_cluster] = []
        self.cache_store[dominant_cluster].append({
            "query_emb": query_emb,
            "text": text,
            "result": result
        })