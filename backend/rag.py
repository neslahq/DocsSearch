from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings

def generate_response(query, relevant_chunks, llm, retriever):
    # Create a Chroma vector store from the relevant chunks
    # embeddings = HuggingFaceEmbeddings()
    
    # documents = [chunk['document'] for chunk in relevant_chunks]
    # metadatas = [chunk['metadata'] for chunk in relevant_chunks]
    
    # vectorstore = Chroma.from_texts(
    #     documents,
    #     embeddings,
    #     metadatas=metadatas
    # )
    
    # # Create a retriever
    # retriever = vectorstore.as_retriever()
    
    # Create a prompt template
    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}
    Answer:"""
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
    
    # Create a RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    
    # Generate the response
    response = qa_chain({"query": query})
    
    # Remove duplicate sources
    unique_sources = []
    seen_doc_ids = set()
    for doc in response['source_documents']:
        doc_id = doc.metadata['doc_id']
        if doc_id not in seen_doc_ids:
            unique_sources.append(doc)
            seen_doc_ids.add(doc_id)
    
    return response['result'], unique_sources
