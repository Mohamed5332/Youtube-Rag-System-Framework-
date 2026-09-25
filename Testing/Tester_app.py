import json
import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(THIS_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)






from Ingestion.Vector_DB import load_vector_DB
from langchain_ollama import OllamaLLM , OllamaEmbeddings


config = {'embeddings' : OllamaEmbeddings(model = "nomic-embed-text"), 
          'llm' : OllamaLLM(model = "qwen3:4b")}

def Test_rag(Evaluation_dataset_file_path , vector_DB):
    # Load dataset.
    with open(Evaluation_dataset_file_path , "r" , encoding="utf-8") as f:
        dataset = json.load(f)

    recalls = []    


    for item in dataset:
        retrieved_chunks = []
        print('question : ' , item['question'])
        print('relevant_chunk_ids : ' , item['relevant_chunk_ids'])

        retriever = vector_DB.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": len(item['relevant_chunk_ids']) , 
            #'fetch_k' : len(item['relevant_chunk_ids']) * 2, 
            #'lambda_mult' : 0.5
        }
    )
        #MQ_retriever = MultiQueryRetriever.from_llm(retriever = retriever , llm = LLM)
        result = retriever.invoke(input = item['question'])
        for doc in result :
            retrieved_chunks.append(doc.metadata['chunk_id'])

        print("retrieved_chunks : " , retrieved_chunks)    

        recall = calc_recall_precesion_f1_score(relevant_chunks= item['relevant_chunk_ids'] , retrieved_chunks= retrieved_chunks)
        recalls.append(recall)

        print("*" * 80)
        print("\n\n")
    print("Total recall is : " , sum(recalls) / len(recalls))    



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

    return recall     



eval_dataset_path = os.path.join(PROJECT_ROOT , 'Evaluation' , 'Eval_dataset3.json')
vector_DB_path =os.path.join(PROJECT_ROOT , 'vid3_DB')

vector_DB1 = load_vector_DB(persist_directory = vector_DB_path,
                            collection_name = "vid3_collection",
                        embeddings = config['embeddings'])


Test_rag(Evaluation_dataset_file_path = eval_dataset_path , vector_DB = vector_DB1)