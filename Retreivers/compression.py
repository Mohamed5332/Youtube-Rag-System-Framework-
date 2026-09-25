from langchain_classic.retrievers.contextual_compression import (
    ContextualCompressionRetriever
)

from langchain_classic.retrievers.document_compressors import (
    LLMChainExtractor
)


def build_compression_retriever(llm , base_retriever):

    base_compressor = LLMChainExtractor.from_llm(llm = llm)

    compressor_retriever = ContextualCompressionRetriever(base_compressor = base_compressor, 
                                                          base_retriever = base_retriever)

    return compressor_retriever
