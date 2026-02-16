import chromadb
from sentence_transformers import SentenceTransformer

class TalentVectorStore:
    def __init__(self, db_path="db/chroma_store"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="employees")

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def add_employee(self, emp_id: str, text: str):
        embedding = self.model.encode(text).tolist()

        self.collection.add(
            ids=[emp_id],
            documents=[text],
            embeddings=[embedding]
        )

    def query(self, query_text: str, top_k=5):
        query_embedding = self.model.encode(query_text).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        return results
