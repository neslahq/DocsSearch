from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def generate_response(query, relevant_chunks, llm):
    # Create a Chroma vector store from the relevant chunks
    embeddings = HuggingFaceEmbeddings()
    
    # # Adjust this part based on the actual structure of relevant_chunks
    # documents = relevant_chunks['documents'] if isinstance(relevant_chunks, dict) else relevant_chunks

    documents = [chunk['document'] for chunk in relevant_chunks]
    metadatas = [chunk['metadata'] for chunk in relevant_chunks]
    
    print(documents)
    print(type(documents))

    # documents = []

    vectorstore = Chroma.from_texts(
        documents,
        embeddings,
        metadatas=metadatas
        # metadatas=[{"source": f"chunk_{i}"} for i in range(len(documents))]
    )
    
    # Create a retriever
    retriever = vectorstore.as_retriever()
    
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
    
    return response['result'], response['source_documents']
