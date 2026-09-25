import os
import sys
import warnings

from dotenv import load_dotenv
from joblib import dump, load
from urllib.parse import urlparse, parse_qs

from fastapi import FastAPI
from pydantic import BaseModel

from langchain_ollama import OllamaEmbeddings
from langchain_groq import ChatGroq
from sentence_transformers import CrossEncoder
from langchain_openai import ChatOpenAI

from Ingestion.chunker import chunk_documents , chunk_documents_by_characters
from Ingestion.youtube_loader import load_documents , load_documents_v2
from Ingestion.Vector_DB import creat_vector_DB, load_vector_DB
from Pipeline.rag_pipeline import rag_pipeline
from Retreivers.factory import build_retriever
from langchain_huggingface import HuggingFaceEndpointEmbeddings


warnings.filterwarnings(action="ignore")

load_dotenv()

print("User story testing in action....")

os.environ["GROQ_API_KEY"] = os.getenv("Groq_api_key")


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(THIS_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)



DATASETS_DIR = "/app/Datasets"
CHUNKS_DIR = "/app/Temp_Chunks"



app = FastAPI()



rag_pipeline_v1 = None
video_id_current = None



config = {

    "LLM": ChatGroq(
        model_name = "openai/gpt-oss-120b",
        temperature = 0.2
    ),

    "LLM1" : ChatOpenAI(
        model = "openai/gpt-oss-120b" , 
        temperature = 0.2,
        api_key = os.getenv(key = "CEREBRAS_API_KEY")
    ),
    "embeddings": OllamaEmbeddings(
        model = "bge-m3",
        keep_alive = -1,
        base_url = "http://host.docker.internal:11434"
    ),
    "embeddings_production" : HuggingFaceEndpointEmbeddings(
        model = "intfloat/multilingual-e5-large",
        huggingfacehub_api_token = os.getenv("HF_TOKEN") 
    ),
    "reranker": CrossEncoder(
        model_name_or_path = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )
}


def extract_url(youtube_url: str) -> str:

    parsed_url = urlparse(youtube_url)

    video_id = parse_qs(
        parsed_url.query
    )["v"][0]

    return video_id



def get_rag_pipeline(
    video_id: str,
    youtube_url: str
):

    database_path = os.path.join(
        DATASETS_DIR,
        f"new_vid_{video_id}"
    )


    if os.path.exists(database_path):

        print(
            "True, Database exists already..."
        )

        # Load Vector DB
        vector_DB = load_vector_DB(
            persist_directory=database_path,

            collection_name=f"new_vid_{video_id}",

            embeddings=config["embeddings_production"]
        )

        # Load previously saved chunks
        chunks_path = os.path.join(
            CHUNKS_DIR,
            video_id
        )

        docs = load(
            filename=chunks_path
        )

        # Build retriever
        retriever = build_retriever(

            vector_db=vector_DB,

            llm=config["LLM"],

            search_type="mmr_hybrid",

            k=3,

            fetch_k=5,

            lambda_mult=0.5,

            documents=docs,

            multi_query=None,

            compression=True
        )

        # Build RAG pipeline
        rag_pipeline_v1 = rag_pipeline(

            llm=config["LLM"],

            retriever=retriever
        )


    else:

        print(
            "False, Database does not exist."
        )

        print(
            "Building initial process..."
        )

        # Load YouTube transcript/documents
        docs = load_documents_v2( # use version 2 of retrieval instead of first version for better performance...
            youtube_url=youtube_url
        )

        """
        # Chunk documents
        chunks = chunk_documents(

            documents=docs,

            embeddings=config["embeddings"],

            breakpoint_threshold_type="standard_deviation",

            breakpoint_threshold_amount=1
        )
        """

        chunks = chunk_documents_by_characters(documents= docs , 
                                               chunk_size = 1000 , 
                                               chunk_overlap = 150)

        # Create Vector DB
        vector_DB = creat_vector_DB(

            collection_name = f"new_vid_{video_id}",

            persist_directory=database_path,

            embedding_function=config["embeddings_production"],

            chunks=chunks
        )

        # Build retriever
        retriever = build_retriever(

            vector_db=vector_DB,

            llm=config["LLM"],

            search_type="mmr_hybrid",

            k=3,

            fetch_k=5,

            lambda_mult=0.5,

            documents=chunks,

            multi_query=None,

            compression=None
        )

        # Make sure chunks directory exists
        os.makedirs(
            CHUNKS_DIR,
            exist_ok=True
        )

        # Save chunks for future use
        chunks_path = os.path.join(
            CHUNKS_DIR,
            video_id
        )

        dump(
            value=chunks,

            filename=chunks_path
        )

        # Build RAG pipeline
        rag_pipeline_v1 = rag_pipeline(

            llm=config["LLM"],

            retriever=retriever
        )

    return rag_pipeline_v1



class QuestionRequest(BaseModel):

    question: str



@app.get("/Youtube_url")
def predict(url: str):

    global rag_pipeline_v1
    global video_id_current

    print(
        "Received YouTube URL:",
        url
    )

    # Extract video ID
    video_id_current = extract_url(
        youtube_url=url
    )

    print(
        "Video ID:",
        video_id_current
    )

    # Build / load RAG pipeline
    rag_pipeline_v1 = get_rag_pipeline(

        video_id=video_id_current,

        youtube_url=url
    )

    print(
        "RAG pipeline is ready."
    )

    return {

        "video_id": video_id_current,

        "status": "ready"
    }



@app.post("/ask")
def ask(request: QuestionRequest):

    global rag_pipeline_v1

    # Check whether RAG pipeline is ready
    if rag_pipeline_v1 is None:

        return {

            "error":
            "Please enter a YouTube URL first."
        }

    print(
        "Question:",
        request.question
    )


    # Run RAG pipeline
    result = rag_pipeline_v1.invoke(

        question=request.question
    )

    return {

        "answer": result.content
    }