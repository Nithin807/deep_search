from dotenv import load_dotenv
load_dotenv()
from app.config import *
from app.generation import Generation
from app.ingest import Ingest
from app.retrieval import Retrieval
from fastapi import FastAPI,File, UploadFile
from pydantic import BaseModel
import uvicorn


# class UploadRequest(BaseModel):
#     filename: str
#     content: bytes

app = FastAPI()
ingest = Ingest()
retrieval = Retrieval()
generation = Generation()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    ingest.file_upload(file.filename, content)
    return {"status": "file uploaded", "filename": file.filename}

@app.post("/query")
def query_file(query: str):
    # contexts = retrieval.retrieve(query)
    answer = generation.generate_answer(query)
    return {"answer": answer}



if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)

