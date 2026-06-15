import os
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ─────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────

INPUT_DIR  = "documents/raw_docs"
OUTPUT_DIR = "documents/chunks"
Path(OUTPUT_DIR).mkdir(exist_ok=True)

# chunking settings per source type
CHUNK_SETTINGS = {
    "reddit":  {"chunk_size": 400,  "chunk_overlap": 50},
    "blog":    {"chunk_size": 550, "chunk_overlap": 100},
    "article": {"chunk_size": 500, "chunk_overlap": 100},
}

# recursive separators — tries these in order before hard character split
SEPARATORS = ["\n\n", "\n", ". ", "! ", "? ", " ", ""]

# ─────────────────────────────────────────
# PARSE HEADER
# ─────────────────────────────────────────

def parse_header(text: str) -> tuple[dict, str]:
    """Extract SOURCE_ID, SOURCE_TYPE, URL from header and return metadata + body."""
    metadata = {}
    lines    = text.split("\n")
    body_start = 0

    for i, line in enumerate(lines):
        if line.startswith("SOURCE_ID:"):
            metadata["source_id"] = line.split(":", 1)[1].strip()
        elif line.startswith("SOURCE_TYPE:"):
            metadata["source_type"] = line.split(":", 1)[1].strip()
        elif line.startswith("URL:"):
            metadata["url"] = line.split(":", 1)[1].strip()
        elif line.startswith("=" * 20):
            body_start = i + 1
            break

    body = "\n".join(lines[body_start:]).strip()
    return metadata, body

# ─────────────────────────────────────────
# CHUNK
# ─────────────────────────────────────────

def chunk_text(text: str, source_type: str) -> list[str]:
    """Split text using recursive chunking based on source type."""
    settings = CHUNK_SETTINGS.get(source_type, CHUNK_SETTINGS["blog"])

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings["chunk_size"],
        chunk_overlap=settings["chunk_overlap"],
        separators=SEPARATORS,
        length_function=len,
    )

    return splitter.split_text(text)

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

all_chunks   = []  # list of dicts with metadata + chunk text
failed       = []
total_chunks = 0

for filename in sorted(os.listdir(INPUT_DIR)):
    if not filename.endswith(".txt"):
        continue

    filepath = os.path.join(INPUT_DIR, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    metadata, body = parse_header(raw)
    source_type    = metadata.get("source_type", "blog")

    if not body.strip():
        print(f"  ✗ Skipping {filename} — empty body")
        failed.append(filename)
        continue

    chunks = chunk_text(body, source_type)
    total_chunks += len(chunks)

    print(f"  ✓ {filename} → {len(chunks)} chunks  (type: {source_type})")

    # save chunks to output file
    out_path = os.path.join(OUTPUT_DIR, filename.replace(".txt", "_chunks.txt"))
    with open(out_path, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"--- CHUNK {i+1} ---\n")
            f.write(f"SOURCE_ID: {metadata.get('source_id', '?')}\n")
            f.write(f"SOURCE_TYPE: {source_type}\n")
            f.write(f"URL: {metadata.get('url', '?')}\n\n")
            f.write(chunk)
            f.write("\n\n")

    # store for representative sample
    for i, chunk in enumerate(chunks):
        all_chunks.append({
            "source_id":   metadata.get("source_id", "?"),
            "source_type": source_type,
            "url":         metadata.get("url", "?"),
            "chunk_index": i + 1,
            "total_chunks": len(chunks),
            "text":        chunk,
        })

# ─────────────────────────────────────────
# PRINT 5 REPRESENTATIVE CHUNKS
# ─────────────────────────────────────────

print("\n" + "=" * 60)
print("5 REPRESENTATIVE CHUNKS")
print("=" * 60)

# pick chunks spread across different source types
seen_types = set()
printed    = 0
sample     = []

# first pass — one of each type
for chunk in all_chunks:
    if chunk["source_type"] not in seen_types:
        sample.append(chunk)
        seen_types.add(chunk["source_type"])
    if len(sample) == 3:
        break

# second pass — fill remaining 2 from any type
for chunk in all_chunks:
    if len(sample) == 5:
        break
    if chunk not in sample:
        sample.append(chunk)

for chunk in sample:
    print(f"\nSource ID : {chunk['source_id']}")
    print(f"Type      : {chunk['source_type']}")
    print(f"Chunk     : {chunk['chunk_index']} of {chunk['total_chunks']}")
    print(f"URL       : {chunk['url']}")
    print(f"Length    : {len(chunk['text'])} chars")
    print(f"Text      :\n{chunk['text']}")
    print("-" * 60)

# ─────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────

print("\n" + "=" * 60)
print(f"Total files processed : {len(all_chunks) and len(set(c['source_id'] for c in all_chunks))}")
print(f"Total chunks produced : {total_chunks}")
print(f"Chunks saved to       : {OUTPUT_DIR}/")
if failed:
    print(f"Skipped               : {failed}")