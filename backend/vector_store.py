# from langchain_community.vectorstores import Chroma
from langchain_chroma import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from config import CHROMA_DB_DIR

embeddings = HuggingFaceEmbeddings()
vectorstore = Chroma(persist_directory=CHROMA_DB_DIR, embedding_function=embeddings)

def add_to_vector_store(processed_docs):
    texts = [doc['content'] for doc in processed_docs]
    metadatas = [doc['metadata'] for doc in processed_docs]
    ids = [doc['id'] for doc in processed_docs]

    result = vectorstore.add_texts(
        texts=texts,
        metadatas=metadatas,
        ids=ids
    )

    print(f'Insert result is: [ {result} ] ------')
    print(f' ----- Total count of docs in collect is: [{vectorstore._collection.count()}] ------ ')

    # texts = [doc['content'] for doc in processed_docs]
    # metadatas = [doc['metadata'] for doc in processed_docs]
    # ids = [doc.id for doc in processed_docs]

    # # # Use update method for upsert-like functionality
    # # vectorstore.update_documents(
    # #     ids=ids,
    # #     documents=texts,
    # #     # metadatas=metadatas
    # # )

    # print(f"Sample doc is to insert: --- ID {processed_docs[0].id} --> [ {processed_docs[0]} ] --- ")
    # vectorstore._collection.upsert(
    #     ids=ids, 
    #     documents=processed_docs
    # )
    # vectorstore.upsert(processed_docs)
    
    # vectorstore.persist()

def query_vector_store(query, retrieval_algo, n_results=5):
    if retrieval_algo == "similarity_score":
        results = vectorstore.similarity_search_with_score(query, k=n_results)

        print(f"Sample doc retrieved: --- [ {results[0]} ] --- ")

        return [{"document": doc.page_content, "metadata": doc.metadata, "score": score} for doc, score in results]
    elif retrieval_algo == "mmr":
        results = vectorstore.max_marginal_relevance_search(query, k=n_results)
        # MMR doesn't return scores, so we'll set it to None
        return [{"document": doc.page_content, "metadata": doc.metadata, "score": None} for doc in results]
    else:
        raise ValueError(f"Unknown retrieval algorithm: {retrieval_algo}")


def get_vector_store_retriever():
    return vectorstore.as_retriever()

