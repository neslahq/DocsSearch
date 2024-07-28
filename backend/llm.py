from langchain.llms import Ollama
from config import DEFAULT_LLM, OLLAMA_BASE_URL

def get_llm(model_name=DEFAULT_LLM):
    return Ollama(base_url=OLLAMA_BASE_URL, model=model_name)
