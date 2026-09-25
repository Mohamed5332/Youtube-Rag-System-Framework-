from langchain_chroma import Chroma


def creat_vector_DB(collection_name , 
                    persist_directory , 
                    embedding_function,
                    chunks):

    vector_DB = Chroma.from_documents(documents= chunks,
                                      collection_name= collection_name , 
                                      persist_directory= persist_directory , 
                                      embedding= embedding_function)

    return vector_DB




def load_vector_DB(persist_directory ,collection_name , embeddings):

    vector_DB = Chroma(persist_directory = persist_directory,
                       collection_name = collection_name, 
                       embedding_function= embeddings)

    return vector_DB

