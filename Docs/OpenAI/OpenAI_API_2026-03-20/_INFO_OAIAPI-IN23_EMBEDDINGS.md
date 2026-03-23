# Embeddings

**Doc ID**: OAIAPI-IN23
**Goal**: Document embeddings API with models, dimensions, use cases, and similarity search
**Version scope**: API v1, Documentation date 2026-03-20

**Depends on:**
- `__OAIAPI_TOC.md [OAIAPI-TOC]` for topic index
- `__OAIAPI_SOURCES.md [OAIAPI-SOURCES]` for source references

## Summary

OpenAI Embeddings API (POST /v1/embeddings) converts text into numerical vector representations for semantic similarity, search, clustering, and recommendations. Models: text-embedding-3-large (3072 dimensions, highest quality), text-embedding-3-small (1536 dimensions, cost-effective), text-embedding-ada-002 (legacy, 1536 dimensions). Embeddings encode semantic meaning - similar texts have similar vectors measured by cosine similarity. Supports dimension reduction for smaller vectors without retraining. Input max 8191 tokens per text. Batch processing supported for multiple texts in single request. Use cases: semantic search, RAG, clustering, classification, anomaly detection. Embeddings are deterministic - same input produces same output. Normalized to unit length for cosine similarity. [VERIFIED] (OAIAPI-SC-OAI-EMBCRT, OAIAPI-SC-OAI-GEMBED)

## Key Facts

- **Endpoint**: POST /v1/embeddings [VERIFIED] (OAIAPI-SC-OAI-EMBCRT)
- **Models**: text-embedding-3-large, text-embedding-3-small, text-embedding-ada-002 [VERIFIED] (OAIAPI-SC-OAI-GEMBED)
- **Dimensions**: Up to 3072 (configurable) [VERIFIED] (OAIAPI-SC-OAI-EMBCRT)
- **Max input**: 8191 tokens per text [VERIFIED] (OAIAPI-SC-OAI-EMBCRT)
- **Batch**: Multiple texts per request [VERIFIED] (OAIAPI-SC-OAI-EMBCRT)

## Use Cases

- **Semantic search**: Find relevant documents by meaning
- **RAG**: Retrieve context for language models
- **Clustering**: Group similar texts
- **Classification**: Categorize text by semantic similarity
- **Recommendations**: Suggest similar items
- **Anomaly detection**: Identify outliers

## Quick Reference

```python
POST /v1/embeddings
{
  "model": "text-embedding-3-large",
  "input": "The quick brown fox",
  "dimensions": 1024
}
```

## Models

### text-embedding-3-large
- **Dimensions**: 3072 (default), configurable down
- **Quality**: Highest
- **Cost**: Premium
- **Use case**: Best quality search, RAG

### text-embedding-3-small
- **Dimensions**: 1536 (default), configurable down
- **Quality**: Good
- **Cost**: Lower
- **Use case**: Cost-effective applications

### text-embedding-ada-002 (Legacy)
- **Dimensions**: 1536 (fixed)
- **Quality**: Good
- **Cost**: Lower
- **Use case**: Legacy applications

## Request Parameters

### Required

- **model**: Model ID
- **input**: Text string or array of strings

### Optional

- **dimensions**: Output vector size (only for v3 models)
- **encoding_format**: "float" or "base64" (default: "float")
- **user**: End-user identifier

## Dimension Reduction

Reduce vector size without retraining:

```python
{
  "model": "text-embedding-3-large",
  "input": "Sample text",
  "dimensions": 1024  # Reduce from 3072 to 1024
}
```

**Benefits:**
- Smaller storage requirements
- Faster similarity computation
- Lower memory usage

**Trade-off:** Slightly reduced accuracy

## Response Format

```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "index": 0,
      "embedding": [0.123, -0.456, 0.789, ...]
    }
  ],
  "model": "text-embedding-3-large",
  "usage": {
    "prompt_tokens": 10,
    "total_tokens": 10
  }
}
```

## Similarity Calculation

### Cosine Similarity

```python
import numpy as np

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
```

OpenAI embeddings are normalized, so dot product = cosine similarity:

```python
similarity = np.dot(embedding1, embedding2)
```

### Distance Metrics

- **Cosine similarity**: -1 to 1 (1 = identical)
- **Euclidean distance**: 0 to ∞ (0 = identical)
- **Dot product**: -∞ to ∞ (higher = more similar)

## SDK Examples (Python)

### Basic Embedding

```python
from openai import OpenAI

client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-large",
    input="The quick brown fox jumps over the lazy dog"
)

embedding = response.data[0].embedding
print(f"Embedding dimensions: {len(embedding)}")
```

### Batch Embeddings

```python
from openai import OpenAI

client = OpenAI()

texts = [
    "Machine learning is a subset of AI",
    "Neural networks are inspired by the brain",
    "Deep learning uses multiple layers"
]

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts
)

for i, data in enumerate(response.data):
    print(f"Text {i}: {len(data.embedding)} dimensions")
```

### Dimension Reduction

```python
from openai import OpenAI

client = OpenAI()

# Full dimensions
response_full = client.embeddings.create(
    model="text-embedding-3-large",
    input="Sample text"
)
print(f"Full: {len(response_full.data[0].embedding)} dimensions")

# Reduced dimensions
response_reduced = client.embeddings.create(
    model="text-embedding-3-large",
    input="Sample text",
    dimensions=1024
)
print(f"Reduced: {len(response_reduced.data[0].embedding)} dimensions")
```

### Semantic Search

```python
from openai import OpenAI
import numpy as np

client = OpenAI()

# Documents
documents = [
    "The cat sat on the mat",
    "The dog played in the park",
    "Machine learning is fascinating",
    "Deep learning uses neural networks"
]

# Get embeddings for all documents
doc_embeddings = []
for doc in documents:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=doc
    )
    doc_embeddings.append(response.data[0].embedding)

# Query
query = "Tell me about artificial intelligence"
query_response = client.embeddings.create(
    model="text-embedding-3-small",
    input=query
)
query_embedding = query_response.data[0].embedding

# Calculate similarities
similarities = []
for i, doc_emb in enumerate(doc_embeddings):
    similarity = np.dot(query_embedding, doc_emb)
    similarities.append((i, similarity))

# Sort by similarity
similarities.sort(key=lambda x: x[1], reverse=True)

print("Most relevant documents:")
for i, sim in similarities[:2]:
    print(f"{documents[i]} (similarity: {sim:.4f})")
```

### Clustering

```python
from openai import OpenAI
from sklearn.cluster import KMeans
import numpy as np

client = OpenAI()

texts = [
    "Python programming",
    "Java development",
    "Cooking recipes",
    "Baking bread",
    "Machine learning",
    "Deep learning"
]

# Get embeddings
embeddings = []
for text in texts:
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    embeddings.append(response.data[0].embedding)

# Cluster
X = np.array(embeddings)
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

# Print clusters
for i, label in enumerate(kmeans.labels_):
    print(f"Cluster {label}: {texts[i]}")
```

### Recommendation System

```python
from openai import OpenAI
import numpy as np

class RecommendationEngine:
    def __init__(self):
        self.client = OpenAI()
        self.model = "text-embedding-3-small"
        self.items = []
        self.embeddings = []
    
    def add_items(self, items: list[str]):
        """Add items to recommendation engine"""
        for item in items:
            response = self.client.embeddings.create(
                model=self.model,
                input=item
            )
            self.items.append(item)
            self.embeddings.append(response.data[0].embedding)
    
    def recommend(self, query: str, top_k: int = 3):
        """Get top-k recommendations"""
        response = self.client.embeddings.create(
            model=self.model,
            input=query
        )
        query_embedding = response.data[0].embedding
        
        # Calculate similarities
        similarities = []
        for i, emb in enumerate(self.embeddings):
            sim = np.dot(query_embedding, emb)
            similarities.append((i, sim))
        
        # Sort and return top-k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [(self.items[i], sim) for i, sim in similarities[:top_k]]

# Usage
engine = RecommendationEngine()
engine.add_items([
    "Action movie with explosions",
    "Romantic comedy",
    "Sci-fi thriller",
    "Documentary about nature",
    "Animated family film"
])

recommendations = engine.recommend("I want something exciting with technology")
for item, score in recommendations:
    print(f"{item} (score: {score:.4f})")
```

### Production Embedding Service

```python
from openai import OpenAI
from typing import List, Union
import numpy as np

class EmbeddingService:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.client = OpenAI()
        self.model = model
    
    def embed(
        self,
        texts: Union[str, List[str]],
        dimensions: int = None
    ) -> np.ndarray:
        """Get embeddings for text(s)"""
        if isinstance(texts, str):
            texts = [texts]
        
        params = {"model": self.model, "input": texts}
        if dimensions:
            params["dimensions"] = dimensions
        
        response = self.client.embeddings.create(**params)
        
        embeddings = [data.embedding for data in response.data]
        return np.array(embeddings)
    
    def similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        embeddings = self.embed([text1, text2])
        return float(np.dot(embeddings[0], embeddings[1]))
    
    def find_most_similar(
        self,
        query: str,
        candidates: List[str],
        top_k: int = 5
    ) -> List[tuple]:
        """Find most similar candidates to query"""
        all_texts = [query] + candidates
        embeddings = self.embed(all_texts)
        
        query_emb = embeddings[0]
        candidate_embs = embeddings[1:]
        
        similarities = []
        for i, emb in enumerate(candidate_embs):
            sim = np.dot(query_emb, emb)
            similarities.append((candidates[i], float(sim)))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

# Usage
service = EmbeddingService(model="text-embedding-3-large")

query = "AI and machine learning"
candidates = [
    "Neural networks and deep learning",
    "Cooking pasta recipes",
    "Artificial intelligence applications",
    "Gardening tips"
]

results = service.find_most_similar(query, candidates, top_k=2)
for text, similarity in results:
    print(f"{text}: {similarity:.4f}")
```

## Error Responses

- **400 Bad Request** - Invalid input or parameters
- **413 Payload Too Large** - Input exceeds token limit
- **429 Too Many Requests** - Rate limit exceeded

## Rate Limiting / Throttling

- **Token-based pricing**: Charged per input token
- **Batch limits**: Max texts per request varies by tier
- **RPM limits**: Standard rate limits apply

## Differences from Other APIs

- **vs Cohere**: Similar capabilities, different models
- **vs Sentence Transformers**: OpenAI hosted service, ST self-hosted
- **vs Google Vertex AI**: Similar quality, different pricing

## Limitations and Known Issues

- **8191 token limit**: Longer texts must be chunked [VERIFIED] (OAIAPI-SC-OAI-EMBCRT)
- **English-optimized**: Best performance on English text [COMMUNITY] (OAIAPI-SC-SO-EMBLANG)
- **Static**: Embeddings don't change with context [COMMUNITY] (OAIAPI-SC-SO-EMBSTAT)

## Gotchas and Quirks

- **Normalized vectors**: All embeddings normalized to unit length [VERIFIED] (OAIAPI-SC-OAI-GEMBED)
- **Dimension reduction**: Can only reduce, not increase dimensions [VERIFIED] (OAIAPI-SC-OAI-EMBCRT)
- **Deterministic**: Same input always produces same embedding [VERIFIED] (OAIAPI-SC-OAI-GEMBED)

## Sources

- OAIAPI-SC-OAI-EMBCRT - POST Create embeddings
- OAIAPI-SC-OAI-GEMBED - Embeddings guide

## Document History

**[2026-03-20 15:52]**
- Initial documentation created
