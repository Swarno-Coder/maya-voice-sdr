"""
Low-Latency RAG Engine for Maya Voice SDR
==========================================
In-process vector retrieval using ChromaDB + sentence-transformers.
Designed for sub-50ms query latency — critical for real-time voice agents.

Architecture:
  User speech → STT → RAG query (this module) → context injection → LLM → TTS
"""

import os
import logging
import hashlib
from typing import Optional

import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer

logger = logging.getLogger("rag-engine")

# ---------------------------------------------------------------------------
# Defaults (overridable via env vars)
# ---------------------------------------------------------------------------
DEFAULT_COLLECTION = os.getenv("RAG_COLLECTION_NAME", "maya_knowledge")
DEFAULT_TOP_K = int(os.getenv("RAG_TOP_K", "3"))
DEFAULT_CHUNK_SIZE = int(os.getenv("RAG_CHUNK_SIZE", "512"))
DEFAULT_CHUNK_OVERLAP = int(os.getenv("RAG_CHUNK_OVERLAP", "64"))
DEFAULT_EMBED_MODEL = os.getenv("RAG_EMBED_MODEL", "all-MiniLM-L6-v2")
DEFAULT_DB_PATH = os.getenv(
    "RAG_DB_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "chroma_db"),
)

# ---------------------------------------------------------------------------
# Text chunking utility
# ---------------------------------------------------------------------------

def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    """Split text into overlapping chunks by character count.

    Uses a simple sliding-window approach optimised for speed.
    For voice-agent RAG the chunks are intentionally small so that
    retrieved context stays concise and doesn't bloat the LLM prompt.
    """
    words = text.split()
    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk.strip())
        start += chunk_size - overlap
    return chunks if chunks else [text.strip()] if text.strip() else []


def _stable_id(text: str, source: str, index: int) -> str:
    """Deterministic ID for a chunk — allows idempotent upserts."""
    h = hashlib.sha256(f"{source}::{index}::{text[:64]}".encode()).hexdigest()[:16]
    return f"{source}_{index}_{h}"


# ---------------------------------------------------------------------------
# RAG Engine (singleton-friendly)
# ---------------------------------------------------------------------------

class RAGEngine:
    """In-process, low-latency Retrieval-Augmented Generation engine.

    - Uses ChromaDB with persistent storage (no external server needed).
    - Embeds with sentence-transformers locally on CPU (~15 ms / query).
    - Returns formatted context strings ready for LLM prompt injection.

    Usage::

        rag = RAGEngine()                    # init once in prewarm
        context = await rag.query("pricing") # call per user turn
    """

    _instance: Optional["RAGEngine"] = None

    def __new__(cls, *args, **kwargs):
        """Singleton — reuse across agent sessions to avoid re-loading."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(
        self,
        db_path: str = DEFAULT_DB_PATH,
        collection_name: str = DEFAULT_COLLECTION,
        embed_model: str = DEFAULT_EMBED_MODEL,
    ):
        if self._initialized:
            return
        logger.info("Initializing RAG engine (model=%s, db=%s)", embed_model, db_path)

        # Load embedding model (cached after first download)
        self._embedder = SentenceTransformer(embed_model)

        # Persistent ChromaDB client — data survives restarts
        self._client = chromadb.PersistentClient(
            path=db_path,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

        self._initialized = True
        doc_count = self._collection.count()
        logger.info(
            "RAG engine ready — %d chunks in collection '%s'",
            doc_count,
            collection_name,
        )

    # ----- Ingestion (called by ingest.py) --------------------------------

    def ingest_chunks(
        self,
        chunks: list[str],
        source: str,
        category: str = "general",
    ) -> int:
        """Upsert pre-chunked texts into the vector store.

        Returns the number of chunks upserted.
        """
        if not chunks:
            return 0

        ids = [_stable_id(c, source, i) for i, c in enumerate(chunks)]
        embeddings = self._embedder.encode(chunks, show_progress_bar=False).tolist()
        metadatas = [
            {"source": source, "chunk_index": i, "category": category}
            for i in range(len(chunks))
        ]

        self._collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
        )
        return len(chunks)

    def reset_collection(self):
        """Drop and recreate the collection (for clean re-ingestion)."""
        name = self._collection.name
        meta = self._collection.metadata
        self._client.delete_collection(name)
        self._collection = self._client.get_or_create_collection(
            name=name, metadata=meta
        )
        logger.info("Collection '%s' reset.", name)

    # ----- Retrieval (called per user turn) --------------------------------

    async def query(
        self,
        text: str,
        top_k: int = DEFAULT_TOP_K,
        category: Optional[str] = None,
    ) -> str:
        """Retrieve the most relevant knowledge chunks for a user query.

        Returns a formatted string ready for prompt injection, or empty
        string if nothing relevant is found (distance > threshold).
        """
        if not text or not text.strip():
            return ""

        if self._collection.count() == 0:
            logger.debug("RAG collection is empty — skipping retrieval.")
            return ""

        # Embed the query (sync but fast: ~15ms on CPU)
        query_embedding = self._embedder.encode(
            [text], show_progress_bar=False
        ).tolist()

        where_filter = {"category": category} if category else None

        results = self._collection.query(
            query_embeddings=query_embedding,
            n_results=min(top_k, self._collection.count()),
            where=where_filter,
            include=["documents", "metadatas", "distances"],
        )

        if not results or not results["documents"] or not results["documents"][0]:
            return ""

        # Filter out low-relevance results (cosine distance > 0.75)
        RELEVANCE_THRESHOLD = 0.75
        context_parts: list[str] = []

        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            if dist > RELEVANCE_THRESHOLD:
                continue
            source = meta.get("source", "unknown")
            context_parts.append(f"[Source: {source}]\n{doc}")

        if not context_parts:
            return ""

        return "\n\n---\n\n".join(context_parts)

    # ----- Stats -----------------------------------------------------------

    def stats(self) -> dict:
        """Return collection statistics."""
        return {
            "collection": self._collection.name,
            "total_chunks": self._collection.count(),
            "db_path": DEFAULT_DB_PATH,
        }
