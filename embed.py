import os
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────

CHUNKS_DIR      = "documents/chunks"
CHROMA_DIR      = "documents/chroma_db"
COLLECTION_NAME = "solo_travel"
TOP_K           = 4

Path(CHROMA_DIR).mkdir(parents=True, exist_ok=True)

# ─────────────────────────────────────────
# LOAD EMBEDDING MODEL
# ─────────────────────────────────────────

print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✓ Model loaded\n")

# ─────────────────────────────────────────
# LOAD CHUNKS
# ─────────────────────────────────────────

def load_chunks(chunks_dir: str) -> list[dict]:
    """Parse all chunk files and return list of chunk dicts with metadata."""
    all_chunks = []

    for filename in sorted(os.listdir(chunks_dir)):
        if not filename.endswith("_chunks.txt"):
            continue

        filepath = os.path.join(chunks_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()

        # split on chunk delimiter
        blocks = raw.split("--- CHUNK ")
        for block in blocks:
            if not block.strip():
                continue

            lines      = block.strip().split("\n")
            chunk_num  = lines[0].replace("---", "").strip()
            metadata   = {}
            text_lines = []
            in_text    = False

            for line in lines[1:]:
                if line.startswith("SOURCE_ID:"):
                    metadata["source_id"] = line.split(":", 1)[1].strip()
                elif line.startswith("SOURCE_TYPE:"):
                    metadata["source_type"] = line.split(":", 1)[1].strip()
                elif line.startswith("URL:"):
                    metadata["url"] = line.split(":", 1)[1].strip()
                elif line == "":
                    in_text = True
                elif in_text:
                    text_lines.append(line)

            text = "\n".join(text_lines).strip()
            if not text:
                continue

            all_chunks.append({
                "id":          f"{filename}_chunk{chunk_num}",  # ← change this line
                "text":        text,
                "source_id":   metadata.get("source_id", "unknown"),
                "source_type": metadata.get("source_type", "unknown"),
                "url":         metadata.get("url", ""),
                "chunk_index": chunk_num,
                "filename":    filename,
            })

    return all_chunks


print("Loading chunks...")
chunks = load_chunks(CHUNKS_DIR)
print(f"✓ Loaded {len(chunks)} chunks from {CHUNKS_DIR}/\n")

# ─────────────────────────────────────────
# SET UP CHROMADB
# ─────────────────────────────────────────

print("Setting up ChromaDB...")
client = chromadb.PersistentClient(path=CHROMA_DIR)

# clear existing collection if it exists
try:
    client.delete_collection(COLLECTION_NAME)
except:
    pass

collection = client.create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}  # cosine similarity
)
print(f"✓ Collection '{COLLECTION_NAME}' created\n")

# ─────────────────────────────────────────
# EMBED + STORE
# ─────────────────────────────────────────

print(f"Embedding {len(chunks)} chunks...")

# batch embed for efficiency
texts = [c["text"] for c in chunks]
embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)

# add to chromadb in batches of 100
BATCH_SIZE = 100
for i in range(0, len(chunks), BATCH_SIZE):
    batch        = chunks[i:i+BATCH_SIZE]
    batch_embeds = embeddings[i:i+BATCH_SIZE]

    collection.add(
        ids        = [c["id"] for c in batch],
        embeddings = [e.tolist() for e in batch_embeds],
        documents  = [c["text"] for c in batch],
        metadatas  = [{
            "source_id":   c["source_id"],
            "source_type": c["source_type"],
            "url":         c["url"],
            "chunk_index": c["chunk_index"],
            "filename":    c["filename"],
        } for c in batch]
    )

print(f"\n✓ {len(chunks)} chunks embedded and stored in ChromaDB\n")

# ─────────────────────────────────────────
# RETRIEVAL FUNCTION
# ─────────────────────────────────────────

def retrieve(query: str, k: int = TOP_K) -> list[dict]:
    """Embed query and return top-k most relevant chunks with metadata."""
    query_embedding = model.encode([query])[0].tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"]
    )

    retrieved = []
    for i in range(len(results["documents"][0])):
        retrieved.append({
            "rank":        i + 1,
            "text":        results["documents"][0][i],
            "metadata":    results["metadatas"][0][i],
            "distance":    round(results["distances"][0][i], 4),
        })

    return retrieved

# ─────────────────────────────────────────
# TEST QUERIES
# ─────────────────────────────────────────

TEST_QUERIES = [
    "What do people say about the pros of solo travel?",
    "Why do people worry about traveling alone as a woman?",
    "How should one pack for a solo trip?",
]

for query in TEST_QUERIES:
    print("\n" + "=" * 60)
    print(f"QUERY: {query}")
    print("=" * 60)

    results = retrieve(query, k=TOP_K)

    for r in results:
        print(f"\n  Rank      : {r['rank']}")
        print(f"  Distance  : {r['distance']}  (lower = more similar)")
        print(f"  Source ID : {r['metadata']['source_id']}")
        print(f"  Type      : {r['metadata']['source_type']}")
        print(f"  URL       : {r['metadata']['url']}")
        print(f"  Text      :\n  {r['text'][:300]}...")
        print("  " + "-" * 56)

print("\n" + "=" * 60)
print("✓ Retrieval test complete")
print(f"  ChromaDB persisted to: {CHROMA_DIR}/")
print("=" * 60)