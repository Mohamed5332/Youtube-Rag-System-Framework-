from langchain_classic.retrievers import EnsembleRetriever


def build_ensemble_retriever(retriever1 , retriever2):
    ensemble_retriever = EnsembleRetriever(retrievers= [retriever1 , retriever2] , weights= [0.5 , 0.5])
    return ensemble_retriever 
