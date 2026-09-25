

def build_mmr_retrievers(vector_db , k  , fetch_k , lambda_mult):

    retriever = vector_db.as_retriever(
            search_type = "mmr",
            search_kwargs = {"k": k , 'fetch_k' : fetch_k, 'lambda_mult' : 0.5}
    )

    return retriever