def build_similarity_retriever(vector_db , k):

    retriever = vector_db.as_retriever(

                search_type="similarity",

                search_kwargs={"k": k} 

                )
    
    return retriever