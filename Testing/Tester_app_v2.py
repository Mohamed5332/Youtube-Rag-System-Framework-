import json
import os
import sys
import time

# مكان الملف الحالي + روت المشروع (Testing جوه المشروع، فبنطلع درجة واحدة)
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(THIS_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


from Ingestion.Vector_DB import load_vector_DB
from Retreivers.factory import build_retriever

from langchain_ollama import OllamaLLM , OllamaEmbeddings

config = {'embeddings' : OllamaEmbeddings(model = "bge-m3"), 
          'llm' : OllamaLLM(model = "qwen3:4b")}




def Test_rag(Evaluation_dataset_file_path , vector_db):

    # Load dataset.
    with open(Evaluation_dataset_file_path , "r" , encoding="utf-8") as f:
        dataset = json.load(f)

    recalls = []    
    precsions= []
    f1_scores = []

    latencies = []

    for item in dataset:
        retrieved_chunks = []
        print('question : ' , item['question'])
        print('relevant_chunk_ids : ' , item['relevant_chunk_ids'])


        retriever = build_retriever(vector_db = vector_db ,
                                    llm = config['llm'] , 
                                    search_type = 'similarity' , 
                                    k = len(item['relevant_chunk_ids']) ,
                                    fetch_k = len(item['relevant_chunk_ids']) * 2 , 
                                    lambda_mult = 0.5 ,
                                    multi_query = True , 
                                    compression = False )

        start = time.time()

        result = retriever.invoke(input = item['question'])

        end = time.time()

        retrieved_chunks = list( dict.fromkeys( doc.metadata['chunk_id'] for doc in result ) ) 


        print("retrieved_chunks : " , retrieved_chunks)    

        recall , precsion , f1_score = calc_recall_precesion_f1_score(relevant_chunks = item['relevant_chunk_ids'] , retrieved_chunks = retrieved_chunks)


        recalls.append(recall)
        latencies.append(end - start)
        precsions.append(precsion)
        f1_scores.append(f1_score)


        print("*" * 80)
        print("\n\n")

    print("Total report : ")    
    print("Total recall : " , sum(recalls) / len(recalls))
    #print("Total precsion : " , sum(precsions) / len(precsions))
    #print("Total F1_score : " , sum(f1_scores) / len(f1_scores))
    print("Total latency : " , sum(latencies) / len(latencies)) 


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



eval_dataset_path = os.path.join(PROJECT_ROOT , 'Evaluation' , 'Eval_dataset1.json')
vector_DB_path =os.path.join(PROJECT_ROOT , 'vid1_DB')


# Load Database..
vector_DB1 = load_vector_DB(persist_directory = vector_DB_path,
                            collection_name = "vid1_collection",
                            embeddings = config['embeddings'])


Test_rag(Evaluation_dataset_file_path = eval_dataset_path , 
         vector_db = vector_DB1)