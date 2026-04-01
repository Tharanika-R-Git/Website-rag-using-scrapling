from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

class VectorStore:
    def __init__(self):
        self.index = None
        self.chunks = []

    def create_index(self, chunks):
        self.chunks = chunks

        embeddings = model.encode(chunks)

        # ✅ FIX: force 2D array
        if len(embeddings.shape) == 1:
            embeddings = np.array([embeddings])

        else:
            embeddings = np.array(embeddings)

        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

    def retrieve(self, query, k=3):
        query_embedding = model.encode([query])

        if len(query_embedding.shape) == 1:
            query_embedding = np.array([query_embedding])

        distances, indices = self.index.search(query_embedding, k)

        return [self.chunks[i] for i in indices[0]]