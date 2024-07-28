import os
from dotenv import load_dotenv
from backend.google_docs import fetch_google_docs
from backend.document_processor import process_documents
from backend.vector_store import add_to_vector_store, query_vector_store
from backend.rag import generate_response
from backend.llm import get_llm

load_dotenv()

def main():
    # Fetch Google Docs
    docs = fetch_google_docs(start_date, end_date)
    
    # Process documents
    processed_docs = process_documents(docs)
    
    # Add to vector store
    add_to_vector_store(processed_docs)
    
    # Get user query
    query = input("Enter your query: ")
    
    # Retrieve relevant chunks
    relevant_chunks = query_vector_store(query)
    
    # Generate response using RAG
    llm = get_llm()
    response = generate_response(query, relevant_chunks, llm)
    
    print(response)

if __name__ == "__main__":
    main()
