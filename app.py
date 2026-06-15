import os
import gradio as gr
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import chromadb
from groq import Groq

load_dotenv()

# ── setup ──────────────────────────────────────────────────
print("Loading model and database...")

model      = SentenceTransformer("all-MiniLM-L6-v2")
client     = chromadb.PersistentClient(path="documents/chroma_db")
collection = client.get_collection("solo_travel")
groq       = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("✓ Ready\n")

# ── retrieval ──────────────────────────────────────────────
def retrieve(query: str, k: int = 4) -> list[dict]:
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

# ── build grounded prompt ──────────────────────────────────
def build_prompt(query: str, chunks: list[dict]) -> str:
    """Build a prompt that strictly grounds the model to retrieved context."""

    context_blocks = []
    for i, chunk in enumerate(chunks):
        meta = chunk["metadata"]
        source_label = f"[Source {i+1}: {meta.get('url', 'unknown')}]"
        context_blocks.append(f"{source_label}\n{chunk['text']}")

    context = "\n\n".join(context_blocks)

    prompt = f"""You are a helpful assistant for solo female travelers.

STRICT GROUNDING RULES:
- Answer ONLY using the information in the provided sources below.
- Do NOT use any outside knowledge or general information.
- If the sources do not contain enough information to answer the question, you MUST respond with exactly: "I don't have enough information on that."
- Do NOT make up, infer, or assume anything not explicitly stated in the sources.
- Every claim in your answer must be traceable to one of the sources below.

SOURCES:
{context}

QUESTION:
{query}

ANSWER (cite sources inline using [Source N] notation):"""

    return prompt

# ── generation ─────────────────────────────────────────────
def generate(query: str, chunks: list[dict]) -> str:
    """Call Groq with grounded prompt. Returns answer string."""
    if not chunks:
        return "I don't have enough information on that."

    prompt = build_prompt(query, chunks)

    response = groq.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a grounded retrieval assistant. "
                    "You answer questions strictly from provided source documents. "
                    "You never use outside knowledge. "
                    "If the documents don't contain the answer, say: "
                    "'I don't have enough information on that.'"
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.0,  # deterministic — no creativity, just grounded answers
        max_tokens=1000,
    )

    return response.choices[0].message.content.strip()

# ── format sources ─────────────────────────────────────────
def format_sources(chunks: list[dict]) -> str:
    """Programmatically build source list from chunk metadata."""
    if not chunks:
        return "No sources retrieved."

    lines = []
    for i, chunk in enumerate(chunks):
        meta        = chunk["metadata"]
        source_type = meta.get("source_type", "unknown").capitalize()
        source_id   = meta.get("source_id", "?")
        url         = meta.get("url", "N/A")
        distance    = chunk.get("distance", "?")
        lines.append(
            f"[Source {i+1}] {source_type} | ID: {source_id} | Score: {distance}\n{url}"
        )

    return "\n\n".join(lines)

# ── main pipeline ──────────────────────────────────────────
def answer(query: str):
    if not query.strip():
        return "Please enter a question.", ""

    chunks   = retrieve(query)
    response = generate(query, chunks)
    sources  = format_sources(chunks)

    return response, sources

# ── UI ─────────────────────────────────────────────────────
with gr.Blocks(title="Solo Female Travel Assistant") as demo:
    gr.Markdown("# 🧳 Solo Female Travel Assistant")
    gr.Markdown(
        "Ask anything about solo female travel — safety, packing, destinations, and more. "
        "Answers are grounded in retrieved sources only."
    )

    with gr.Row():
        query_box = gr.Textbox(
            label="Your question",
            placeholder="e.g. What are the safest countries for solo female travel?",
            lines=2
        )

    submit_btn = gr.Button("Ask", variant="primary")

    with gr.Row():
        answer_box = gr.Textbox(label="Answer", lines=10)

    with gr.Row():
        sources_box = gr.Textbox(label="Sources", lines=6)

    submit_btn.click(answer, inputs=query_box, outputs=[answer_box, sources_box])
    query_box.submit(answer, inputs=query_box, outputs=[answer_box, sources_box])

# ── end to end test ────────────────────────────────────────
def run_tests():
    TEST_QUERIES = [
        "What do people say about the pros of solo travel?",
        "Why do people worry about traveling alone as a woman?",
        "What is the best cryptocurrency to invest in right now?",  # out of scope
    ]

    for query in TEST_QUERIES:
        print("\n" + "=" * 60)
        print(f"QUERY: {query}")
        print("=" * 60)
        chunks   = retrieve(query)
        response = generate(query, chunks)
        sources  = format_sources(chunks)
        print(f"\nANSWER:\n{response}")
        print(f"\nSOURCES:\n{sources}")
        print("=" * 60)

if __name__ == "__main__":
    run_tests()
    print("\nLaunching Gradio app...")
    demo.launch()