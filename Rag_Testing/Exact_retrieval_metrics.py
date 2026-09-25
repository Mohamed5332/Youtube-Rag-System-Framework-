import sys
import os

from joblib import load

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(PROJECT_ROOT)

from dotenv import load_dotenv
import time
import json
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM , OllamaEmbeddings
from sentence_transformers import CrossEncoder

from langchain_groq import ChatGroq

from Ingestion.Vector_DB import load_vector_DB
from Retreivers.factory import build_retriever
from Reranking.reranker import Rerank


load_dotenv()


config = {
    'LLM': ChatGroq(model_name = 'qwen/qwen3.8-27b', 
                    api_key = os.getenv(key= "Groq_api_key"),
                    temperature = 0.2 , 
                    ),
    'embeddings' : OllamaEmbeddings(model = 'bge-m3'),
    'reranker' : CrossEncoder(model_name_or_path = 'cross-encoder/ms-marco-MiniLM-L-6-v2')
}


def calc_recall_precesion_f1_score(relevant_chunks , retrieved_chunks):
    intersection = set(relevant_chunks) & set(retrieved_chunks)

    if len(intersection) != 0 : 
        recall = len(intersection) / len(relevant_chunks) * 100 
        precesion = len(intersection) / len(retrieved_chunks) * 100
        f1_score = 2 * (recall * precesion) / (recall + precesion)
        print("recall : " , recall,"%")
        print("precesion : " , precesion,"%")
        print("f1_score : " , f1_score,"%")

    else :
        precesion = 0 
        recall = 0 
        f1_score = 0    

    return recall , precesion , f1_score




def Test_Retrieval_process(Evaluation_dataset_file_path , vector_DB , documents = None):
    # Load dataset.
    with open(Evaluation_dataset_file_path , "r" , encoding="utf-8") as f:
        dataset = json.load(f)

    recalls = []    
    precisions = []
    f1_scores = []
    latencies = []


    for item in dataset:
        retrieved_chunks = []
        print('question : ' , item['question'])
        print('relevant_chunk_ids : ' , item['relevant_chunk_ids'])



        retriever = build_retriever(vector_db= vector_DB , 
                                    llm= config['LLM'] , 
                                    search_type= 'mmr_hybrid' , 
                                    k= len(item['relevant_chunk_ids']) , 
                                    fetch_k = len(item['relevant_chunk_ids']) * 2,
                                    lambda_mult= 0.5 , 
                                    documents = documents,
                                    multi_query= None , 
                                    compression= None)
        
        start = time.time()
        result = retriever.invoke(input = item['question'])

        reranked_docs = Rerank(reranker_model = config['reranker'] ,
                               query = item['question'] , 
                               docs = result, 
                               Top_k = len(item['relevant_chunk_ids']))
        
        for i, doc in enumerate(reranked_docs):
            print("\nRESULT", i)
            print("chunk_id:", doc.metadata.get("chunk_id"))
            print("metadata:", doc.metadata)
            print("content:", doc.page_content[:500])

        end = time.time()

        latency = end - start

        for doc in reranked_docs :
            retrieved_chunks.append(doc.metadata['chunk_id'])


        context = ""

        for doc in reranked_docs :
            context += "\n" + doc.page_content 

       
        print("retrieved_chunks : " , retrieved_chunks)
        print("Retireval time is : " , end - start)    

        
        recall , precision , f1_score = calc_recall_precesion_f1_score(relevant_chunks= item['relevant_chunk_ids'] , retrieved_chunks= retrieved_chunks)

        recalls.append(recall)
        precisions.append(precision)
        f1_scores.append(f1_score)
        latencies.append(latency)

        print("*" * 80)
        print("\n\n")
    print("Average  recall is : " , sum(recalls) / len(recalls)) 
    print("Average  precision is : " , sum(precisions) / len(precisions))    
    print("Average  f1_score is : " , sum(f1_scores) / len(f1_scores))   
    print("Average  retrieval time per 10 questions : " , sum(latencies) / len(latencies)) 

       

DB_VID1 = load_vector_DB(persist_directory = 'D:/Youtube rag system/Databases/vid1_DB' , 
               collection_name = 'vid1_collection', 
               embeddings = config['embeddings'])

DB_VID2 = load_vector_DB(persist_directory = 'D:/Youtube rag system/Databases/vid2_DB' , 
               collection_name = 'vid2_collection', 
               embeddings = config['embeddings'])

DB_VID3 = load_vector_DB(persist_directory = 'D:/Youtube rag system/Databases/vid3_DB' , 
               collection_name = 'vid3_collection', 
               embeddings = config['embeddings'])


combinations = [
    (
        'D:/Youtube rag system/Evaluation/Eval_dataset1.json', # Evaluation Dataset
         DB_VID1, # Vector_Database..
        'D:/Youtube rag system/Chunks/chunks_file1' # Documents
    ),
    (
        'D:/Youtube rag system/Evaluation/Eval_dataset2.json',
        DB_VID2,
        'D:/Youtube rag system/Chunks/chunks_file2',
    ),
    (
        'D:/Youtube rag system/Evaluation/Eval_dataset3.json',
        DB_VID3,
        'D:/Youtube rag system/Chunks/chunks_file3',
    )
]

for item  in combinations:
    Test_Retrieval_process(Evaluation_dataset_file_path = item[0], 
                           vector_DB = item[1],
                           documents = load(item[2]))