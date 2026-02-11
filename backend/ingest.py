"""
Document Ingestion Pipeline for Maya Voice SDR RAG
====================================================
CLI tool to load knowledge-base documents into the ChromaDB vector store.

Supports: .txt, .md, .pdf
Usage:
    python ingest.py                     # ingest from default dir
    python ingest.py --dir ./my_docs     # custom directory
    python ingest.py --reset             # wipe & re-ingest
"""

import argparse
import logging
import os
import sys
from pathlib import Path

from rag_engine import RAGEngine, chunk_text

logger = logging.getLogger("ingest")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"}
DEFAULT_KB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge_base")


def _read_pdf(path: str) -> str:
    """Extract text from a PDF file."""
    try:
        from pypdf import PdfReader

        reader = PdfReader(path)
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(pages)
    except ImportError:
        logger.warning("pypdf not installed — skipping %s", path)
        return ""
    except Exception as e:
        logger.error("Failed to read PDF %s: %s", path, e)
        return ""


def _read_text(path: str) -> str:
    """Read a plain text or markdown file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error("Failed to read %s: %s", path, e)
        return ""


def _infer_category(filename: str) -> str:
    """Infer a category tag from the filename for metadata filtering."""
    name_lower = filename.lower()
    if "pricing" in name_lower or "plan" in name_lower:
        return "pricing"
    if "case" in name_lower or "success" in name_lower or "story" in name_lower:
        return "case_study"
    if "faq" in name_lower or "question" in name_lower:
        return "faq"
    if "competitor" in name_lower or "comparison" in name_lower or "vs" in name_lower:
        return "competitor"
    if "product" in name_lower or "feature" in name_lower or "overview" in name_lower:
        return "product"
    return "general"


def load_and_ingest(kb_dir: str, reset: bool = False) -> dict:
    """Load all supported documents from a directory and ingest into RAG.

    Returns summary stats.
    """
    kb_path = Path(kb_dir)
    if not kb_path.exists():
        logger.error("Knowledge base directory not found: %s", kb_dir)
        sys.exit(1)

    # Collect files
    files = sorted(
        f
        for f in kb_path.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    if not files:
        logger.warning("No supported files found in %s", kb_dir)
        return {"documents": 0, "chunks": 0}

    logger.info("Found %d document(s) in %s", len(files), kb_dir)

    # Init RAG engine
    rag = RAGEngine()

    if reset:
        logger.info("Resetting collection...")
        rag.reset_collection()

    total_chunks = 0
    for filepath in files:
        ext = filepath.suffix.lower()
        if ext == ".pdf":
            text = _read_pdf(str(filepath))
        else:
            text = _read_text(str(filepath))

        if not text.strip():
            logger.warning("Skipping empty file: %s", filepath.name)
            continue

        category = _infer_category(filepath.name)
        chunks = chunk_text(text)
        n = rag.ingest_chunks(chunks, source=filepath.name, category=category)
        total_chunks += n
        logger.info(
            "  ✓ %s — %d chunks (category: %s)", filepath.name, n, category
        )

    stats = rag.stats()
    logger.info(
        "Ingestion complete — %d chunks from %d documents (total in store: %d)",
        total_chunks,
        len(files),
        stats["total_chunks"],
    )
    return {"documents": len(files), "chunks": total_chunks}


def main():
    parser = argparse.ArgumentParser(
        description="Ingest knowledge-base documents into Maya RAG vector store"
    )
    parser.add_argument(
        "--dir",
        default=DEFAULT_KB_DIR,
        help=f"Path to knowledge base directory (default: {DEFAULT_KB_DIR})",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Wipe existing collection before ingesting",
    )
    args = parser.parse_args()
    load_and_ingest(args.dir, args.reset)


if __name__ == "__main__":
    main()
