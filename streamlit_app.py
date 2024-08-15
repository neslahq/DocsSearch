import streamlit as st
from datetime import datetime, timedelta
from backend.google_docs import fetch_google_docs
from backend.document_processor import process_documents
from backend.vector_store import add_to_vector_store, query_vector_store, get_vector_store_retriever
from backend.rag import generate_response
from backend.llm import get_llm
from config import TOKENIZATION_OPTIONS, RETRIEVAL_OPTIONS, ALGORITHM_DESCRIPTIONS

st.title("DocsSearch")

# Sidebar for configurations
st.sidebar.title("Configuration")

# Algorithm Selection (moved to sidebar)
st.sidebar.subheader("Algorithm Selection")
tokenization_algo = st.sidebar.selectbox(
    "Select Tokenization Algorithm",
    options=list(TOKENIZATION_OPTIONS.keys()),
    format_func=lambda x: TOKENIZATION_OPTIONS[x]
)
st.sidebar.info(ALGORITHM_DESCRIPTIONS[tokenization_algo])

retrieval_algo = st.sidebar.selectbox(
    "Select Retrieval Algorithm",
    options=list(RETRIEVAL_OPTIONS.keys()),
    format_func=lambda x: RETRIEVAL_OPTIONS[x]
)
st.sidebar.info(ALGORITHM_DESCRIPTIONS[retrieval_algo])

# LLM Configuration (already in sidebar)
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

# Main area
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
        processed_docs = process_documents(docs, tokenization_algo)
        add_to_vector_store(processed_docs)
    st.success(f"Indexed {len(docs)} documents")

# Query input
st.subheader("Search Google Docs")
query = st.text_input("Enter your query")

if query:
    with st.spinner("Generating response..."):
        relevant_chunks = query_vector_store(query, retrieval_algo)
        llm = get_llm()
        retriever = get_vector_store_retriever()
        response, source_docs = generate_response(query, relevant_chunks, llm, retriever)
    
    st.write("Response:")
    st.write(response)
    
    st.write("Sources:")
    for doc in source_docs:
        st.write(f"- [{doc.metadata['doc_name']}]({doc.metadata['doc_link']})")
