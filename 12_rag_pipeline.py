"""
Demo 22: Complete RAG Pipeline
Goal: Production-ready Retrieval-Augmented Generation implementation

Key Teaching Points:
- Document chunking strategies
- Embedding generation
- Vector storage and retrieval
- RAG orchestration
- Production patterns
"""

import os
from pathlib import Path
from typing import List, Dict, Tuple
from strands import Agent, tool
from dotenv import load_dotenv
import json
import hashlib
from datetime import datetime

# Load environment variables
load_dotenv()


class DocumentChunker:
    """Handle document chunking with overlap."""

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size

            # Find the last sentence boundary within chunk
            if end < len(text):
                # Look for sentence endings
                last_period = text[start:end].rfind('.')
                last_newline = text[start:end].rfind('\n')
                boundary = max(last_period, last_newline)

                if boundary > 0:
                    end = start + boundary + 1

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunk_id = hashlib.md5(chunk_text.encode()).hexdigest()[:8]
                chunks.append({
                    "id": chunk_id,
                    "text": chunk_text,
                    "start": start,
                    "end": end,
                    "length": len(chunk_text)
                })

            # Move to next chunk with overlap
            start = end - overlap if end < len(text) else end

        return chunks


class SimpleVectorStore:
    """Simple in-memory vector store with keyword-based retrieval."""

    def __init__(self):
        self.documents = []
        self.index = {}

    def add_document(self, doc_id: str, text: str, metadata: Dict = None):
        """Add a document to the store."""
        doc = {
            "id": doc_id,
            "text": text,
            "metadata": metadata or {},
            "added_at": datetime.now().isoformat()
        }
        self.documents.append(doc)

        # Build keyword index
        words = text.lower().split()
        for word in set(words):
            if word not in self.index:
                self.index[word] = []
            self.index[word].append(doc_id)

    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for relevant documents."""
        query_words = query.lower().split()

        # Score documents by keyword overlap
        scores = {}
        for word in query_words:
            if word in self.index:
                for doc_id in self.index[word]:
                    scores[doc_id] = scores.get(doc_id, 0) + 1

        # Get top-k documents
        sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        results = []
        for doc_id, score in sorted_docs:
            doc = next((d for d in self.documents if d["id"] == doc_id), None)
            if doc:
                results.append({
                    **doc,
                    "relevance_score": score
                })

        return results


# Global vector store
vector_store = SimpleVectorStore()


class RAGPipeline:
    """Complete RAG pipeline implementation."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunker = DocumentChunker()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def ingest_document(self, doc_id: str, text: str, metadata: Dict = None):
        """Ingest a document into the RAG pipeline."""
        # Step 1: Chunk the document
        chunks = self.chunker.chunk_text(text, self.chunk_size, self.chunk_overlap)

        # Step 2: Store chunks in vector store
        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc_id}_chunk_{i}"
            chunk_metadata = {
                **(metadata or {}),
                "doc_id": doc_id,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            vector_store.add_document(chunk_id, chunk["text"], chunk_metadata)

        return len(chunks)

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """Retrieve relevant chunks for a query."""
        return vector_store.search(query, top_k)


# Initialize RAG pipeline
rag_pipeline = RAGPipeline(chunk_size=400, chunk_overlap=50)


@tool
def ingest_document(doc_id: str, content: str, doc_type: str = "text") -> str:
    """Ingest a document into the RAG system."""
    metadata = {"type": doc_type, "ingested_at": datetime.now().isoformat()}
    num_chunks = rag_pipeline.ingest_document(doc_id, content, metadata)
    return f"✅ Document '{doc_id}' ingested successfully! Created {num_chunks} chunks."


@tool
def search_knowledge_base(query: str, top_k: int = 3) -> str:
    """Search the knowledge base for relevant information."""
    results = rag_pipeline.retrieve(query, top_k)

    if not results:
        return "No relevant information found in the knowledge base."

    response = f"Found {len(results)} relevant chunks:\n\n"

    for i, result in enumerate(results, 1):
        response += f"[Result {i}] (Relevance: {result['relevance_score']})\n"
        response += f"Source: {result['metadata'].get('doc_id', 'unknown')}\n"
        response += f"Text: {result['text'][:200]}...\n\n"

    return response


@tool
def get_rag_stats() -> str:
    """Get statistics about the RAG system."""
    total_docs = len(vector_store.documents)
    index_size = len(vector_store.index)

    stats = f"""RAG Pipeline Statistics:

📊 Total chunks stored: {total_docs}
🔍 Indexed terms: {index_size}
💾 Storage: In-memory vector store

Configuration:
- Chunk size: {rag_pipeline.chunk_size} characters
- Chunk overlap: {rag_pipeline.chunk_overlap} characters
- Retrieval top-k: 3 by default
"""
    return stats


# RAG-powered agent
rag_agent = Agent(
    tools=[ingest_document, search_knowledge_base, get_rag_stats],
    system_prompt="""You are a RAG-powered assistant with access to a knowledge base.

When answering questions:
1. Use search_knowledge_base to find relevant information
2. Synthesize information from multiple chunks if needed
3. Cite sources by mentioning document IDs
4. If information isn't in the knowledge base, say so clearly
5. Provide accurate, well-grounded responses

When users want to add information:
1. Use ingest_document to add new content
2. Confirm successful ingestion

Be helpful, accurate, and transparent about your knowledge sources.
"""
)


def main():
    """Run the RAG pipeline demo."""
    print("=" * 70)
    print("🔍 Complete RAG Pipeline Demo")
    print("=" * 70)
    print()

    # Sample documents to ingest
    documents = [
        {
            "id": "company_policy",
            "content": """
Employee Handbook - Remote Work Policy

All employees are eligible for remote work up to 3 days per week.
Core hours are 10 AM to 3 PM EST for all team members.
Employees must maintain a dedicated workspace with reliable internet.
Monthly stipend of $100 provided for home office expenses.
Video must be enabled for all team meetings.

Performance reviews are conducted quarterly.
Annual bonus potential is 15-20% of base salary.
Health insurance covers employee and dependents at 100%.
"""
        },
        {
            "id": "product_features",
            "content": """
Product Documentation - AI Assistant Platform

Key Features:
1. Multi-model support (Claude, Llama, Mistral)
2. Custom tool integration via API
3. Knowledge base RAG system
4. Real-time streaming responses
5. Enterprise SSO authentication

API Rate Limits:
- Free tier: 100 requests/day
- Pro tier: 10,000 requests/day
- Enterprise: Unlimited

Supported integrations:
- Slack, Discord, Microsoft Teams
- Salesforce, HubSpot
- GitHub, GitLab
- AWS, Azure, GCP
"""
        },
        {
            "id": "technical_specs",
            "content": """
Technical Specifications

Architecture: Microservices on Kubernetes
Database: PostgreSQL 14 with TimescaleDB
Cache: Redis Cluster
Message Queue: Apache Kafka
Monitoring: Prometheus + Grafana

Security:
- SOC 2 Type II certified
- GDPR compliant
- End-to-end encryption
- Regular penetration testing

SLA: 99.9% uptime guarantee
Response time: < 200ms p95
Data retention: 90 days default
Backup frequency: Every 6 hours
"""
        }
    ]

    # Ingest documents
    print("📥 Ingesting documents into RAG system...\n")
    for doc in documents:
        result = ingest_document(doc["id"], doc["content"], "documentation")
        print(f"  {result}")

    print("\n" + "=" * 70)
    print("📊 RAG System Status")
    print("=" * 70)
    stats = get_rag_stats()
    print(stats)

    # Query the RAG system
    print("\n" + "=" * 70)
    print("💬 Querying RAG-Powered Agent")
    print("=" * 70)

    queries = [
        "What is the remote work policy?",
        "What are the API rate limits?",
        "Tell me about the security features",
        "What database do we use?",
        "What's the bonus structure?"
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n❓ Question {i}: {query}")
        print("-" * 70)
        response = rag_agent(query)
        print(f"💡 Answer: {response}\n")

    print("=" * 70)
    print("✨ Demo complete!")
    print("\n📚 Production RAG Enhancements:")
    print("\n1. Vector Embeddings:")
    print("   - Use AWS Bedrock Titan embeddings")
    print("   - Use sentence-transformers (open source)")
    print("   - Use Cohere embeddings")
    print("\n2. Vector Databases:")
    print("   - Pinecone (managed)")
    print("   - Weaviate (open source)")
    print("   - Qdrant (open source)")
    print("   - ChromaDB (embedded)")
    print("   - pgvector (PostgreSQL extension)")
    print("\n3. Advanced Features:")
    print("   - Hybrid search (dense + sparse)")
    print("   - Query rewriting")
    print("   - Re-ranking")
    print("   - Multi-hop reasoning")
    print("   - Citation tracking")
    print("=" * 70)


if __name__ == "__main__":
    main()


"""
Setup Instructions:

1. Install required packages:
   uv add python-dotenv

2. For production RAG, add:
   uv add boto3 sentence-transformers chromadb pinecone-client

3. Run the demo:
   python 20_rag_pipeline.py

Features Demonstrated:
- Document chunking with overlap
- Simple vector storage
- Keyword-based retrieval
- RAG orchestration
- Source attribution
- Knowledge base management

Production RAG with AWS Bedrock Embeddings:

```python
import boto3
import json
import numpy as np
from typing import List

bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

class EmbeddingVectorStore:
    def __init__(self):
        self.documents = []
        self.embeddings = []

    def add_document(self, text: str, metadata: dict = None):
        # Generate embedding with Bedrock Titan
        body = json.dumps({"inputText": text})
        response = bedrock_runtime.invoke_model(
            modelId="amazon.titan-embed-text-v1",
            body=body
        )
        response_body = json.loads(response['body'].read())
        embedding = response_body['embedding']

        self.documents.append({
            'text': text,
            'metadata': metadata or {},
            'embedding': embedding
        })

    def cosine_similarity(self, a: List[float], b: List[float]) -> float:
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def search(self, query: str, top_k: int = 3):
        # Get query embedding with Bedrock Titan
        body = json.dumps({"inputText": query})
        response = bedrock_runtime.invoke_model(
            modelId="amazon.titan-embed-text-v1",
            body=body
        )
        response_body = json.loads(response['body'].read())
        query_embedding = response_body['embedding']

        # Calculate similarities
        similarities = []
        for doc in self.documents:
            similarity = self.cosine_similarity(
                query_embedding,
                doc['embedding']
            )
            similarities.append((doc, similarity))

        # Sort by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)

        return [doc for doc, _ in similarities[:top_k]]
```

Using ChromaDB:

```python
import chromadb
from chromadb.config import Settings

# Initialize ChromaDB
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db"
))

collection = client.create_collection("documents")

# Add documents
collection.add(
    documents=["This is document 1", "This is document 2"],
    metadatas=[{"source": "doc1"}, {"source": "doc2"}],
    ids=["id1", "id2"]
)

# Query
results = collection.query(
    query_texts=["search query"],
    n_results=3
)
```

Using Pinecone:

```python
import pinecone
import boto3
import json

# Initialize Bedrock client
bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')

# Initialize Pinecone
pinecone.init(
    api_key="your-api-key",
    environment="us-west1-gcp"
)

index = pinecone.Index("documents")

# Generate and upsert embeddings
def upsert_document(doc_id: str, text: str, metadata: dict):
    body = json.dumps({"inputText": text})
    response = bedrock_runtime.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=body
    )
    response_body = json.loads(response['body'].read())
    embedding = response_body['embedding']

    index.upsert([(doc_id, embedding, metadata)])

# Search
def search_similar(query: str, top_k: int = 3):
    body = json.dumps({"inputText": query})
    response = bedrock_runtime.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=body
    )
    response_body = json.loads(response['body'].read())
    query_embedding = response_body['embedding']

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    return results
```

Advanced RAG Patterns:

1. **Hybrid Search**:
```python
def hybrid_search(query: str):
    # Dense retrieval (semantic)
    dense_results = vector_db.search(query)

    # Sparse retrieval (keyword)
    sparse_results = keyword_search(query)

    # Combine and re-rank
    combined = merge_and_rerank(dense_results, sparse_results)
    return combined
```

2. **Query Rewriting**:
```python
def rewrite_query(original_query: str) -> List[str]:
    # Generate alternative phrasings
    prompt = f"Generate 3 alternative ways to ask: {original_query}"
    alternatives = llm.generate(prompt)
    return alternatives
```

3. **Re-ranking**:
```python
def rerank_results(query: str, results: List[dict]) -> List[dict]:
    # Use cross-encoder for re-ranking
    from sentence_transformers import CrossEncoder

    model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')

    pairs = [[query, doc['text']] for doc in results]
    scores = model.predict(pairs)

    # Sort by score
    reranked = sorted(
        zip(results, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [doc for doc, _ in reranked]
```

Use Cases:
- Enterprise knowledge bases
- Customer support systems
- Research and documentation tools
- Legal document analysis
- Medical information retrieval
- E-commerce product search
- Code search and documentation

Production Best Practices:
1. Implement proper chunking strategies
2. Use semantic embeddings over keyword search
3. Implement hybrid search for better recall
4. Add re-ranking for precision
5. Track and cite sources
6. Implement caching for common queries
7. Monitor retrieval quality metrics
8. Version your embeddings and indices
9. Implement incremental updates
10. Add feedback loops for improvement
"""


"""Sample output

emil@Franklins-MacBook-Pro strands-agentcore-demo % uv run 20_rag_pipeline.py 
======================================================================
🔍 Complete RAG Pipeline Demo
======================================================================

📥 Ingesting documents into RAG system...

  ✅ Document 'company_policy' ingested successfully! Created 2 chunks.
  ✅ Document 'product_features' ingested successfully! Created 2 chunks.
  ✅ Document 'technical_specs' ingested successfully! Created 2 chunks.

======================================================================
📊 RAG System Status
======================================================================
RAG Pipeline Statistics:

📊 Total chunks stored: 6
🔍 Indexed terms: 169
💾 Storage: In-memory vector store

Configuration:
- Chunk size: 400 characters
- Chunk overlap: 50 characters
- Retrieval top-k: 3 by default


======================================================================
💬 Querying RAG-Powered Agent
======================================================================

❓ Question 1: What is the remote work policy?
----------------------------------------------------------------------
I'll search the knowledge base for information about the remote work policy.
Tool #1: search_knowledge_base
Let me search for more detailed information about the remote work policy to provide you with a complete answer.
Tool #2: search_knowledge_base
Based on the information found in the knowledge base, here's the remote work policy:

**Remote Work Policy** (Source: company_policy)

- **Eligibility**: All employees are eligible for remote work
- **Frequency**: Up to 3 days per week
- **Core Hours**: 10 AM to 3 PM EST for all team members
- **Requirements**: Employees must maintain a dedicated work space

The policy appears to allow flexibility while ensuring team coordination through required core hours when everyone should be available. However, the search results show that the full policy text was truncated. If you need more specific details about requirements, approval processes, or other aspects of the remote work policy, please let me know and I can search for more specific information.💡 Answer: Based on the information found in the knowledge base, here's the remote work policy:

**Remote Work Policy** (Source: company_policy)

- **Eligibility**: All employees are eligible for remote work
- **Frequency**: Up to 3 days per week
- **Core Hours**: 10 AM to 3 PM EST for all team members
- **Requirements**: Employees must maintain a dedicated work space

The policy appears to allow flexibility while ensuring team coordination through required core hours when everyone should be available. However, the search results show that the full policy text was truncated. If you need more specific details about requirements, approval processes, or other aspects of the remote work policy, please let me know and I can search for more specific information.



❓ Question 2: What are the API rate limits?
----------------------------------------------------------------------
I'll search the knowledge base for information about API rate limits.
Tool #3: search_knowledge_base
Let me search with more specific terms to find rate limit information.
Tool #4: search_knowledge_base
Let me try searching for technical specifications or API documentation.
Tool #5: search_knowledge_base
I wasn't able to find specific information about API rate limits in the knowledge base. The search results show technical specifications and product features, but don't contain details about rate limiting policies such as requests per minute, throttling thresholds, or API quotas.

To get information about API rate limits, you may need to:
1. Add this information to the knowledge base if it exists in other documentation
2. Check the API documentation directly
3. Contact the technical team for current rate limit specifications

Would you like me to search for any other specific technical details, or would you prefer to add API rate limit documentation to the knowledge base?💡 Answer: I wasn't able to find specific information about API rate limits in the knowledge base. The search results show technical specifications and product features, but don't contain details about rate limiting policies such as requests per minute, throttling thresholds, or API quotas.

To get information about API rate limits, you may need to:
1. Add this information to the knowledge base if it exists in other documentation
2. Check the API documentation directly
3. Contact the technical team for current rate limit specifications

Would you like me to search for any other specific technical details, or would you prefer to add API rate limit documentation to the knowledge base?



❓ Question 3: Tell me about the security features
----------------------------------------------------------------------
I'll search the knowledge base for information about security features.
Tool #6: search_knowledge_base
Let me try a broader search for security-related information.
Tool #7: search_knowledge_base
I can see there's a mention of "Security..." in the technical specifications. Let me search for more specific security terms to get the complete information.
Tool #8: search_knowledge_base
The search results show that there is security information in the technical specifications document (source: technical_specs), but the content appears to be truncated in the search results - I can only see "Security..." at the end.

Unfortunately, I cannot provide you with detailed information about the security features because the complete security section from the technical specifications isn't fully visible in my search results. The knowledge base contains a reference to security information, but the full details are not accessible through my current search.

To get complete information about security features, you may need to:
1. Access the full technical specifications document directly
2. Add more detailed security documentation to the knowledge base
3. Search for specific security aspects you're interested in (like authentication methods, encryption standards, etc.)

Is there a particular aspect of security you're most interested in? I can try searching for more specific terms that might yield better results.💡 Answer: The search results show that there is security information in the technical specifications document (source: technical_specs), but the content appears to be truncated in the search results - I can only see "Security..." at the end.

Unfortunately, I cannot provide you with detailed information about the security features because the complete security section from the technical specifications isn't fully visible in my search results. The knowledge base contains a reference to security information, but the full details are not accessible through my current search.

To get complete information about security features, you may need to:
1. Access the full technical specifications document directly
2. Add more detailed security documentation to the knowledge base
3. Search for specific security aspects you're interested in (like authentication methods, encryption standards, etc.)

Is there a particular aspect of security you're most interested in? I can try searching for more specific terms that might yield better results.



❓ Question 4: What database do we use?
----------------------------------------------------------------------
I'll search the knowledge base for information about the database we use.
Tool #9: search_knowledge_base
Let me try searching for technical specifications which might contain database information.
Tool #10: search_knowledge_base
Based on the information found in the knowledge base, here's what database we use:

**Database Information** (Source: technical_specs)

- **Primary Database**: PostgreSQL 14 with TimescaleDB
- **Cache**: Redis Cluster

The system uses PostgreSQL version 14 as the main database, enhanced with TimescaleDB (which is an extension for time-series data). Additionally, Redis Cluster is used for caching purposes.

TimescaleDB is particularly useful for handling time-series data efficiently, which suggests the system likely deals with time-based analytics or logging data.💡 Answer: Based on the information found in the knowledge base, here's what database we use:

**Database Information** (Source: technical_specs)

- **Primary Database**: PostgreSQL 14 with TimescaleDB
- **Cache**: Redis Cluster

The system uses PostgreSQL version 14 as the main database, enhanced with TimescaleDB (which is an extension for time-series data). Additionally, Redis Cluster is used for caching purposes.

TimescaleDB is particularly useful for handling time-series data efficiently, which suggests the system likely deals with time-based analytics or logging data.



❓ Question 5: What's the bonus structure?
----------------------------------------------------------------------
I'll search the knowledge base for information about the bonus structure.
Tool #11: search_knowledge_base
Let me search for more specific information about bonuses and compensation.
Tool #12: search_knowledge_base
Based on the information found in the knowledge base, here's what I can tell you about the bonus structure:

**Bonus Structure** (Source: company_policy)

- **Annual Bonus Potential**: 15-20% of base salary
- **Performance Reviews**: Conducted quarterly (which likely ties into bonus evaluations)

The company offers an annual bonus with a potential range of 15-20% of your base salary. The quarterly performance reviews suggest that bonus eligibility and amounts are likely tied to performance metrics evaluated throughout the year.

However, the search results appear to be truncated, so there may be additional details about the bonus structure (such as specific performance criteria, payout timing, or different bonus tiers) that aren't fully visible in my current results. If you need more specific information about bonus criteria or payout schedules, please let me know and I can search for more detailed terms.💡 Answer: Based on the information found in the knowledge base, here's what I can tell you about the bonus structure:

**Bonus Structure** (Source: company_policy)

- **Annual Bonus Potential**: 15-20% of base salary
- **Performance Reviews**: Conducted quarterly (which likely ties into bonus evaluations)

The company offers an annual bonus with a potential range of 15-20% of your base salary. The quarterly performance reviews suggest that bonus eligibility and amounts are likely tied to performance metrics evaluated throughout the year.

However, the search results appear to be truncated, so there may be additional details about the bonus structure (such as specific performance criteria, payout timing, or different bonus tiers) that aren't fully visible in my current results. If you need more specific information about bonus criteria or payout schedules, please let me know and I can search for more detailed terms.


======================================================================
✨ Demo complete!

📚 Production RAG Enhancements:

1. Vector Embeddings:
   - Use AWS Bedrock Titan embeddings
   - Use sentence-transformers (open source)
   - Use Cohere embeddings

2. Vector Databases:
   - Pinecone (managed)
   - Weaviate (open source)
   - Qdrant (open source)
   - ChromaDB (embedded)
   - pgvector (PostgreSQL extension)

3. Advanced Features:
   - Hybrid search (dense + sparse)
   - Query rewriting
   - Re-ranking
   - Multi-hop reasoning
   - Citation tracking
======================================================================
"""