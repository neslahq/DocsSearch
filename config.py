import os
from dotenv import load_dotenv

load_dotenv()

# Google API credentials
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

# ChromaDB settings
CHROMA_DB_DIR = "chroma_db"

# LLM settings
DEFAULT_LLM = "llama3"
OLLAMA_BASE_URL = "http://localhost:11434"

# RAG settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
