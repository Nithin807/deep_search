import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

DATABASE_PATH = "backend/data/rag.sqlite"
DATA_PATH = "backend/data/AWSCertifiedMLSlides.pdf"