import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent))
from app.config import *
from openai import OpenAI
import numpy as np
import sqlite3
from PyPDF2 import PdfReader
from io import BytesIO

class Ingest:
    def __init__(self):
        self.data_path = DATA_PATH
        self.db_path = DATABASE_PATH
        self.client = OpenAI()

    def check_text(self,text,chunk_size=500,overlap=50):
        words = text.split()
        chunks, i = [], 0
        while i < len(words):
            chunks.append(" ".join(words[i:i+chunk_size]))
            i += chunk_size - overlap
        return chunks
    
    def embed_text(self,texts):
        response = self.client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=texts
        )
        return [np.array(d.embedding, dtype=np.float32) for d in response.data]

    def init_db(self):
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            chunk_id INTEGER,
            text TEXT,
            embedding BLOB
        )""")
        conn.commit()
        conn.close()
    
    def file_upload(self,filename,content):
        self.init_db()
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        if filename.endswith('.txt'):
            text = content.decode('utf-8')
            chunks = self.check_text(text)
            embeddings = self.embed_text(chunks)
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                c.execute("INSERT INTO documents (source, chunk_id, text, embedding) VALUES (?, ?, ?, ?)",
                          (filename, i, chunk, embedding.tobytes()))
            conn.commit()
        elif filename.endswith('.pdf'):
            pdf_file = BytesIO(content)
            reader = PdfReader(pdf_file)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text() + "\n"
            chunks = self.check_text(full_text)
            embeddings = self.embed_text(chunks)
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                c.execute("INSERT INTO documents (source, chunk_id, text, embedding) VALUES (?, ?, ?, ?)",
                          (filename, i, chunk, embedding.tobytes()))
            conn.commit()
        conn.close()
        return {"status": "success", "message": f"File {filename} processed and stored."}
    
    def current_file_upload(self):
        data_file = self.data_path
        with open(data_file, "rb") as f:
            self.file_upload("AWSCertifiedMLSlides.pdf", f)
        return {"status": "success", "message": f"File AWSCertifiedMLSlides.pdf processed and stored."}

        

    

    



        