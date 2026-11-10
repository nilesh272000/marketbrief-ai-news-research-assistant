"""Article chunking and FAISS index construction."""
from dataclasses import dataclass

@dataclass
class Chunk:
    page_content: str
    metadata: dict

def articles_to_chunks(articles, chunk_size=1000, chunk_overlap=150):
    if chunk_size <= 0 or chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("Require chunk_size > chunk_overlap >= 0.")
    chunks=[]
    step=chunk_size-chunk_overlap
    for article in articles:
        text=article.text.strip()
        for start in range(0,len(text),step):
            piece=text[start:start+chunk_size]
            if piece.strip():
                chunks.append(Chunk(piece,{"source":article.url,"title":article.title}))
            if start+chunk_size >= len(text):
                break
    return chunks

def build_faiss_index(chunks,api_key,embedding_model="text-embedding-3-small"):
    if not chunks:
        raise ValueError("No article chunks available to index.")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required.")
    from langchain_core.documents import Document
    from langchain_openai import OpenAIEmbeddings
    from langchain_community.vectorstores import FAISS
    docs=[Document(page_content=c.page_content,metadata=c.metadata) for c in chunks]
    embeddings=OpenAIEmbeddings(model=embedding_model,api_key=api_key)
    return FAISS.from_documents(docs,embeddings)
