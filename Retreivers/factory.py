from Retreivers.mmr import build_mmr_retrievers
from Retreivers.similarity import build_similarity_retriever
from Retreivers.multi_query_retriever import build_multi_query_retriever
from Retreivers.compression import build_compression_retriever
from Retreivers.hybrid_search_retriever import build_ensemble_retriever
from Retreivers.Build_BM25_retriever import build_BM25Retriever

def build_retriever(vector_db , 
                    llm  , 
                    search_type , 
                    k  , 
                    fetch_k , 
                    lambda_mult  , 
                    documents = None,
                    multi_query = None , 
                    compression = None):


    if search_type == "similarity":

        retriever = build_similarity_retriever(vector_db= vector_db ,
                                                k=k)

    elif search_type == "mmr" :

        retriever = build_mmr_retrievers(vector_db= vector_db , 
                                         k= k , 
                                         fetch_k= fetch_k , 
                                         lambda_mult= lambda_mult)


    elif search_type == "similarity_hybrid":
        similarity_retriever = build_similarity_retriever(vector_db = vector_db , k = k)
        Bm25_retriever = build_BM25Retriever(documents = documents, k = k)
        retriever = build_ensemble_retriever(retriever1 = similarity_retriever , retriever2 = Bm25_retriever)

        
    elif search_type == "mmr_hybrid":
        mmr_retriever = build_mmr_retrievers(vector_db = vector_db , 
                                             k = k , 
                                             fetch_k= fetch_k , 
                                             lambda_mult= lambda_mult)

        Bm25_retriever = build_BM25Retriever(documents = documents, k = k)

        retriever = build_ensemble_retriever(retriever1 = mmr_retriever , retriever2 = Bm25_retriever) 
        

    else :    
        raise ValueError(f"No search type called {search_type}")


    if multi_query:
        retriever = build_multi_query_retriever(llm = llm , retriever = retriever)


    if compression :
        retriever = build_compression_retriever(llm = llm , base_retriever = retriever)


    return retriever    

        
