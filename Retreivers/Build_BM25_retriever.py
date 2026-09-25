from langchain_classic.retrievers import BM25Retriever

def build_BM25Retriever(documents , k):
    Bm25_retriever = BM25Retriever.from_documents(documents= documents , k = k)

    return Bm25_retriever