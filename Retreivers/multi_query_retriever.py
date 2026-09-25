from langchain_classic.retrievers.multi_query import MultiQueryRetriever

def build_multi_query_retriever(llm , retriever):


    Multi_query_retriever = MultiQueryRetriever.from_llm(llm = llm , retriever = retriever)


    return Multi_query_retriever    
