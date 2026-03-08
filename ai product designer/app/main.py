# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

# Import your classes here
from .embeddings import VectorStore
from .clustering import FuzzyClusterer
from .cache import SemanticCache

app = FastAPI()

# Global state (Initialize these on startup in a real app)
vector_store = VectorStore()
clusterer = FuzzyClusterer()
semantic_cache = SemanticCache(similarity_threshold=0.82)


@app.on_event("startup")
def startup_event():
    # Ingest documents into the vector store and fit the clustering model
    embeddings = vector_store.ingest_data()
    try:
        clusterer.fit(embeddings)
    except Exception:
        # If clustering fails (e.g., too few samples), continue without crashing
        pass

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def process_query(req: QueryRequest):
    # 1. Embed Query
    query_emb = vector_store.model.encode([req.query], normalize_embeddings=True)[0]
    
    # 2. Find Dominant Cluster (Fuzzy Distribution)
    dist = clusterer.get_cluster_distribution(query_emb)
    dominant_cluster = int(np.argmax(dist))
    
    # 3. Check Cache
    match, score = semantic_cache.check_cache(query_emb, dominant_cluster)
    
    if match:
        return {
            "query": req.query,
            "cache_hit": True,
            "matched_query": match["text"],
            "similarity_score": float(score),
            "result": match["result"],
            "dominant_cluster": dominant_cluster
        }
    
    # 4. Cache Miss - Compute Result (Fetch from FAISS)
    D, I = vector_store.index.search(np.array([query_emb]), k=1)
    result_text = vector_store.documents[I[0][0]]
    
    # 5. Store in Cache
    semantic_cache.add_to_cache(query_emb, req.query, result_text, dominant_cluster)
    
    return {
        "query": req.query,
        "cache_hit": False,
        "matched_query": None,
        "similarity_score": None,
        "result": result_text,
        "dominant_cluster": dominant_cluster
    }

@app.get("/cache/stats")
async def get_stats():
    total_entries = sum(len(items) for items in semantic_cache.cache_store.values())
    total_requests = semantic_cache.hits + semantic_cache.misses
    hit_rate = semantic_cache.hits / total_requests if total_requests > 0 else 0.0
    
    return {
        "total_entries": total_entries,
        "hit_count": semantic_cache.hits,
        "miss_count": semantic_cache.misses,
        "hit_rate": hit_rate
    }

@app.delete("/cache")
async def clear_cache():
    semantic_cache.cache_store.clear()
    semantic_cache.hits = 0
    semantic_cache.misses = 0
    return {"status": "Cache cleared"}