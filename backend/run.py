from dotenv import load_dotenv
load_dotenv()
from app.config import *
from app.generation import Generation
from app.ingest import Ingest
from app.retrieval import Retrieval
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


# class UploadRequest(BaseModel):
#     filename: str
#     content: bytes

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
ingest = Ingest()
retrieval = Retrieval()
generation = Generation()

class QueryRequest(BaseModel):
    query: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    filename = file.filename
    ingest.file_upload(filename, content)
    return {"status": "file uploaded", "filename": filename}

@app.post("/query")
def query_file(request: QueryRequest):
    # contexts = retrieval.retrieve(query)
    answer = generation.generate_answer(request.query)
    return {"answer": answer}



if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)

