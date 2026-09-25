from langchain_experimental.text_splitter import SemanticChunker 
from langchain_text_splitters import TokenTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(documents , embeddings , breakpoint_threshold_type , breakpoint_threshold_amount):

    chunker = SemanticChunker(embeddings = embeddings , 
                              breakpoint_threshold_type = breakpoint_threshold_type, 
                              breakpoint_threshold_amount = breakpoint_threshold_amount) 

    chunks = chunker.split_documents(documents = documents)

    return chunks


def chunk_documents_by_tokens(documents , chunk_size = 500 , chunk_overlap = 50):
    
    chunker = TokenTextSplitter(chunk_size = chunk_size , chunk_overlap = chunk_overlap)

    chunks = chunker.split_documents(documents)

    return chunks


def chunk_documents_by_characters(documents , chunk_size=500 , chunk_overlap=50):

    chunker = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n","\n","؟","!",".","،"," ",""])

    chunks = chunker.split_documents(documents)

    return chunks