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

# Tokenization options
TOKENIZATION_OPTIONS = {
    "recursive_character": "RecursiveCharacterTextSplitter (Default)",
    "character": "CharacterTextSplitter",
    "token": "TokenTextSplitter",
}

# Retrieval options
RETRIEVAL_OPTIONS = {
    "similarity_score": "Similarity Search with Top-K (Default)",
    "mmr": "Maximum Marginal Relevance (MMR)",
}

# Descriptions for algorithms
ALGORITHM_DESCRIPTIONS = {
    "recursive_character": "Splits text recursively by different characters. Good for most use cases.",
    "character": "Splits text based on characters. Simple but may break words.",
    "token": "Splits text based on tokens. Useful for maintaining semantic meaning.",
    "similarity_score": "Retrieves documents based on similarity to the query. Fast and effective for most cases.",
    "mmr": "Balances relevance with diversity in results. Useful when you want to avoid redundant information.",
}