import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from app.config import *
from openai import OpenAI
import numpy as np
import sqlite3

class Retrieval:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.client = OpenAI()

    def embed_query(self,query):
        resp = self.client.embeddings.create(
            input=query,
            model=EMBEDDING_MODEL
        )
        return np.array(resp.data[0].embedding)

    def cosine_similarity(self,vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def retrieve(self,query, top_k=5):
        query_embedding = self.embed_query(query)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT id, source, chunk_id, text, embedding FROM documents")
        rows = c.fetchall()
        results = []
        for row in rows:
            doc_id, source, chunk_id, text, embedding_blob = row
            embedding = np.frombuffer(embedding_blob, dtype=np.float32)
            similarity = self.cosine_similarity(query_embedding, embedding)
            results.append((similarity, source, chunk_id, text))
        conn.close()
        if len(results) == 0 or results == None:
            return []
        else:
            results.sort(reverse=True, key=lambda x: x[0])
            return results[:top_k]