from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class VectorStore:
    def __init__(self):
        self.index = None
        self.chunks = []
        self.model = None  # lazy load

    def load_model(self):
        if self.model is None:
            print("Loading model...")
            self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def create_index(self, chunks):
        self.load_model()

        self.chunks = chunks
        embeddings = self.model.encode(chunks)

        if len(embeddings.shape) == 1:
            embeddings = np.array([embeddings])
        else:
            embeddings = np.array(embeddings)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

    def retrieve(self, query, k=3):
        self.load_model()

        query_embedding = self.model.encode([query])

        if len(query_embedding.shape) == 1:
            query_embedding = np.array([query_embedding])

        distances, indices = self.index.search(query_embedding, k)
        return [self.chunks[i] for i in indices[0]]