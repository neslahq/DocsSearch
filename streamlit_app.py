import streamlit as st
from datetime import datetime, timedelta
from backend.google_docs import fetch_google_docs
from backend.document_processor import process_documents
from backend.vector_store import add_to_vector_store, query_vector_store
from backend.rag import generate_response
from backend.llm import get_llm

st.title("Google Docs RAG Search")

# Date range picker for manual indexing
st.subheader("Index Google Docs")
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
with col2:
    end_date = st.date_input("End Date", value=datetime.now())

if st.button("Index Documents"):
    with st.spinner("Indexing documents..."):
        docs = fetch_google_docs(start_date.isoformat(), end_date.isoformat())
        processed_docs = process_documents(docs)
        add_to_vector_store(processed_docs)
    st.success(f"Indexed {len(docs)} documents")

# Query input
st.subheader("Search Google Docs")
query = st.text_input("Enter your query")

if query:
    with st.spinner("Generating response..."):
        relevant_chunks = query_vector_store(query)
        llm = get_llm()
        response, source_docs = generate_response(query, relevant_chunks, llm)
    
    st.write("Response:")
    st.write(response)
    
    st.write("Sources:")
    for doc in source_docs:
        st.write(f"- [{doc.metadata['doc_name']}]({doc.metadata['doc_link']})")

# LLM Configuration
st.sidebar.subheader("LLM Configuration")
llm_model = st.sidebar.selectbox("Select LLM Model", ["llama3", "gpt4all", "other_model"])
if llm_model == "other_model":
    custom_model = st.sidebar.text_input("Enter custom model name")
    if custom_model:
        llm_model = custom_model

if st.sidebar.button("Update LLM"):
    with st.spinner("Updating LLM..."):
        llm = get_llm(llm_model)
    st.sidebar.success(f"LLM updated to {llm_model}")
