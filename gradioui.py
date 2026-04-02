import gradio as gr
from scraper import scrape_url
from utils import chunk_text
from embedder import VectorStore
from llm import generate_answer

def rag_pipeline(url, question):
    try:
        # 1. Scrape
        text = scrape_url(url)

        if not text.strip():
            return "❌ Failed to extract content. Try another site."

        # 2. Chunk
        chunks = chunk_text(text)

        if len(chunks) == 0:
            return "❌ No usable content found."

        # 3. Embed
        vector_store = VectorStore()
        vector_store.create_index(chunks)

        # 4. Retrieve
        context_chunks = vector_store.retrieve(question)
        context = "\n".join(context_chunks)

        # 5. Generate
        answer = generate_answer(context, question)

        return answer

    except Exception as e:
        return f"❌ Error: {str(e)}"


iface = gr.Interface(
    fn=rag_pipeline,
    inputs=[
        gr.Textbox(label="🌐 Website URL"),
        gr.Textbox(label="❓ Ask a Question")
    ],
    outputs=gr.Textbox(label="🤖 Answer"),
    title="🌐 Web RAG Chatbot",
    description="Ask questions about any website using AI"
)

if __name__ == "__main__":
    iface.launch()