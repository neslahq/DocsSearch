from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter, TokenTextSplitter
from langchain_core.documents import Document
from config import CHUNK_SIZE, CHUNK_OVERLAP

def get_text_splitter(algo):
    if algo == "recursive_character":
        return RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
        )
    elif algo == "character":
        return CharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
        )
    elif algo == "token":
        return TokenTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )
    else:
        raise ValueError(f"Unknown tokenization algorithm: {algo}")

def process_documents(docs, tokenization_algo):
    text_splitter = get_text_splitter(tokenization_algo)
    
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

            # processed_docs.append(
            #     Document(
            #     id=f"{doc['id']}-chunk-{i}",
            #     page_content=chunk,
            #     metadata={
            #         'doc_id': doc['id'],
            #         'doc_name': doc['name'],
            #         'doc_link': doc['link'],
            #         'chunk_index': i
            #     }
            #     ))
    
    return processed_docs
