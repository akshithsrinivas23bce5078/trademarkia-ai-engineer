# AI Product Designer - Semantic Search & Caching API

This repository contains a FastAPI-based semantic search service with an advanced semantic caching mechanism using **FAISS**, **Sentence Transformers**, and **Fuzzy Clustering (Gaussian Mixture Models)**.

## Overview

The application demonstrates how to build a scalable and efficient semantic search system capable of returning relevant documents instantly by leveraging an intelligent cache. 

Key technologies used:
- **FastAPI**: For high-performance async API endpoints.
- **Sentence Transformers** (`all-MiniLM-L6-v2`): For creating high-quality, dense vector embeddings of text.
- **FAISS**: For fast similarity search across embeddings.
- **Scikit-Learn (PCA & GMM)**: For fuzzy clustering of the semantic space to optimize caching.

## Features

- **Semantic Querying:** Understands the meaning of queries, not just keywords, retrieving documents based on dense vector embeddings.
- **Intelligent Semantic Cache:** Uses fuzzy clustering to organize queries into distinct topic clusters, reducing cache search time.
- **Cache Hit/Miss Analytics:** Provides statistics via API endpoints to monitor cache performance.
- **Built-in Dataset:** Uses the `20newsgroups` dataset out of the box for immediate testing.

## Project Structure

```text
.
├── app
│   ├── main.py          # FastAPI application entry point and endpoints
│   ├── cache.py         # Semantic caching logic
│   ├── clustering.py    # Gaussian Mixture Models & PCA for fuzzy clustering
│   └── embeddings.py    # FAISS Vector Store and dataset ingestion
├── Requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
└── README.md            # Project documentation
```

## Setup & Installation

### Local Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/akshithsrinivas23bce5078/trademarkia-ai-engineer.git
   cd trademarkia-ai-engineer
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r Requirements.txt
   ```

3. **Run the FastAPI Development Server:**
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### Docker Usage

To run the application inside a container:

```bash
docker build -t semantic-search-api .
docker run -p 8000:8000 semantic-search-api
```

## API Endpoints

- `POST /query`: Submits a query to the service. Returns the context document, Cache Hit status, and similarity metrics.
- `GET /cache/stats`: Returns current cache statistics, including total entries, hit/miss count, and hit rate.
- `DELETE /cache`: Clears the semantic cache entirely.

### Example Query

```bash
curl -X 'POST' \
  'http://localhost:8000/query' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "Where can I find some good graphics cards?"
}'
```

## How It Works

1. **Ingestion**: On startup, the `20newsgroups` dataset is loaded and vectorized.
2. **Clustering**: A PCA-reduced Gaussian Mixture Model fits the data into 15 clusters.
3. **Querying**: A user query is vectorized, and its dominant semantic cluster is determined.
4. **Caching**: We look for similar queries within the *same dominant cluster* inside the semantic cache.
    - If similar enough (> 85%), return the cached result.
    - Otherwise, query the FAISS index, find the most relevant document, and store the query-result pair inside the cache for future use.
