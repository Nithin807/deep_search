from dotenv import load_dotenv
load_dotenv()
from app.config import *
from app.generation import Generation
from app.ingest import Ingest
from app.retrieval import Retrieval
from app.track_user import TrackUser
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
track_user = TrackUser()

class QueryRequest(BaseModel):
    query: str

class ChatInput(BaseModel):
    user_name: str
    session_id: str
    message: str

class SignupRequest(BaseModel):
    user_name: str
    password: str

class LoginRequest(BaseModel):
    user_name: str
    password: str


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

@app.post("/chat")
def chat_endpoint(chat_input: ChatInput):
    history = track_user.get_messages(chat_input.user_name, chat_input.session_id)
    history_conversation = [{"role":role, "content":message} for role, message in history]
    history_conversation.append({"role":"user", "content":chat_input.message})
    answer = generation.generate_with_history(chat_input.message, history_conversation )
    track_user.add_message(chat_input.user_name, chat_input.session_id, "user", chat_input.message)
    track_user.add_message(chat_input.user_name, chat_input.session_id, "assistant", answer)
    return {"answer": answer}

@app.post("/signup")
def signup(request: SignupRequest):
    success = track_user.create_user(request.user_name, request.password)
    if success:
        return {"status": "user created"}
    else:
        return {"status": "user already exists"}

@app.post("/login")
def login(request: SignupRequest):
    success = track_user.authenticate_user(request.user_name, request.password)
    if success:
        return {"status": "login successful"}
    else:
        return {"status": "invalid credentials"}
    

@app.get("/sessions/{user_name}")
def get_sessions(user_name: str):
    sessions = track_user.get_sessions(user_name)
    return {"sessions": sessions}

@app.get("/messages/{user_name}/{session_id}")
def get_messages(user_name: str, session_id: str):
    history = track_user.get_messages(user_name, session_id)
    # history is probably a list of (role, message) tuples
    return {
        "messages": [{"role": role, "content": msg} for role, msg in history]
    }



if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=8000)

