from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper import scrape_url
from utils import chunk_text
from embedder import VectorStore
from llm import generate_answer

app = FastAPI()

# ✅ CORS (for Next.js frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Web RAG API is running 🚀"}


@app.post("/ask")
def ask(url: str, question: str):
    try:
        # 1. Scrape
        text = scrape_url(url)
        print("TEXT LENGTH:", len(text))

        if not text or len(text.strip()) == 0:
            return {
                "error": "Unable to extract content. This site may be JavaScript-heavy."
            }

        # 2. Chunk
        chunks = chunk_text(text)
        print("CHUNKS:", len(chunks))

        if len(chunks) == 0:
            return {
                "error": "No usable content found after processing."
            }

        # 3. Create vector store (per request)
        vector_store = VectorStore()
        vector_store.create_index(chunks)

        # 4. Retrieve
        context_chunks = vector_store.retrieve(question)

        if not context_chunks:
            return {
                "error": "No relevant context found."
            }

        context = "\n".join(context_chunks)

        # 5. Generate Answer
        answer = generate_answer(context, question)

        return {
            "question": question,
            "answer": answer,
            "context_used": context_chunks
        }

    except Exception as e:
        print("ERROR:", e)
        return {
            "error": str(e)
        }