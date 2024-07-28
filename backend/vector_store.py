from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import CHROMA_DB_DIR

embeddings = HuggingFaceEmbeddings()
vectorstore = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)

def add_to_vector_store(processed_docs):
    texts = [doc['content'] for doc in processed_docs]
    metadatas = [doc['metadata'] for doc in processed_docs]
    ids = [doc['id'] for doc in processed_docs]
    
    vectorstore.add_texts(texts=texts, metadatas=metadatas, ids=ids)
    vectorstore.persist()

def query_vector_store(query, n_results=5):
    results = vectorstore.similarity_search_with_score(query, k=n_results)
    return [{"document": doc.page_content, "metadata": doc.metadata, "score": score} for doc, score in results]
