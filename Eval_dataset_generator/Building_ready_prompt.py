
from Ingestion.utils import assign_ids , save_chunks , get_context , get_ready_prompt 
from Ingestion.youtube_loader import load_documents
from Ingestion.chunker import chunk_documents


def build_ready_prompt(youtube_url , chunk_file_path , embeddings):

    documents = load_documents(youtube_url= youtube_url)

    chunks = chunk_documents(documents= documents , embeddings= embeddings)

    assign_ids(chunks = chunks)

    save_chunks(chunks = chunks , vid_name = chunk_file_path)
    
    context = get_context(chunks_file_path = chunk_file_path)

    ready_prompt = get_ready_prompt(context= context)

    return ready_prompt
