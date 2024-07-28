from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

def process_documents(docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    
    processed_docs = []
    for doc in docs:
        chunks = text_splitter.split_text(doc['content'])
        for i, chunk in enumerate(chunks):
            processed_docs.append({
                'id': f"{doc['id']}-chunk-{i}",
                'content': chunk,
                'metadata': {
                    'doc_id': doc['id'],
                    'doc_name': doc['name'],
                    'doc_link': doc['link'],
                    'chunk_index': i
                }
            })
    
    return processed_docs
