import sys
import os

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.append(PROJECT_ROOT)

print("Building Ragas dataset in action....")

import json
from joblib import load , dump
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaEmbeddings , OllamaLLM
from Ingestion.Vector_DB import load_vector_DB
from Retreivers.factory import build_retriever
from Reranking.reranker import Rerank
from sentence_transformers import CrossEncoder
from langchain_groq import ChatGroq

load_dotenv()

os.getenv(key= "Groq_api_key")
config = {'llm' : ChatGroq(model_name = "openai/gpt-oss-120b" ,
                           api_key= os.getenv(key="Groq_api_key"),  
                           temperature= 0.2) , 
          'embeddings' : OllamaEmbeddings(model = 'bge-m3') , 
          'reranker' : CrossEncoder(model_name_or_path = 'cross-encoder/ms-marco-MiniLM-L-6-v2')}


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


def build_retrieved_generated_dataset(Evaluation_dataset_file_path , vector_DB , output_file , documents = None):
    # Load dataset.
    with open(Evaluation_dataset_file_path , "r" , encoding="utf-8") as f:
        dataset = json.load(f)

    recalls = []    
    precisions = []
    f1_scores = []

    for item in dataset:
        retrieved_chunks = []
        print('question : ' , item['question'])
        print('relevant_chunk_ids : ' , item['relevant_chunk_ids'])

        retriever = build_retriever(vector_db= vector_DB , 
                                    llm= config['llm'] , 
                                    search_type= 'mmr_hybrid' , 
                                    k= len(item['relevant_chunk_ids']) , 
                                    fetch_k = len(item['relevant_chunk_ids']) * 2,
                                    lambda_mult= 0.5 , 
                                    documents = documents,
                                    multi_query= None , 
                                    compression= None)


        result = retriever.invoke(input = item['question'])

        # reranker works here...
        reranked_docs = Rerank(reranker_model = config['reranker'] ,
                               query = item['question'] ,
                               docs = result, 
                               Top_k = len(item['relevant_chunk_ids']))


        for doc in reranked_docs :
            retrieved_chunks.append(doc.metadata['chunk_id'])


        prompt = PromptTemplate(

            template="""Answer the question using only the provided context.

            Context:
            {context}

            Question:
            {question}

            Answer:
            """,
            input_variables=['question', 'context']
        )
        context = ""

        for doc in reranked_docs :
            context += "\n" + doc.page_content 

        ready_prompt = prompt.invoke(input={'context' : context , 'question' : item['question']})

        generated_answer = config['llm'].invoke(input = ready_prompt)

        retrieved_contexts = [doc.page_content for doc in reranked_docs]
                
        print("retrieved_chunks : " , retrieved_chunks)    

        print("generated answer : " , generated_answer.content)

        print("Ground truth answer : " , item['ground_truth_answer'])

        print("retrieved_contexts : " , retrieved_contexts)

        item['response'] = generated_answer.content
        item['retrieved_contexts'] = retrieved_contexts
        item['retrieved_chunk_ids'] = retrieved_chunks
        
        recall , precision , f1_score = calc_recall_precesion_f1_score(relevant_chunks= item['relevant_chunk_ids'] , retrieved_chunks= retrieved_chunks)
        recalls.append(recall)
        precisions.append(precision)
        f1_scores.append(f1_score)

        print("*" * 80)
        print("\n\n")
    print("Average recall : " , sum(recalls) / len(recalls))    
    print("Average precision : " , sum(precisions) / len(precisions))
    print("Average f1_score : " , sum(f1_scores) / len(f1_scores))

    with open(file= output_file , mode='w' , encoding='utf-8') as f :
        json.dump(dataset , f , ensure_ascii= False , indent= 4)



DB_VID1 = load_vector_DB(persist_directory = 'D:/Youtube rag system/Databases/vid1_DB', 
                         collection_name = 'vid1_collection', 
                         embeddings = config['embeddings'])

DB_VID2 = load_vector_DB(persist_directory = 'D:/Youtube rag system/Databases/vid2_DB', 
                         collection_name = 'vid2_collection', 
                         embeddings = config['embeddings'])

DB_VID3 = load_vector_DB(persist_directory = 'D:/Youtube rag system/Databases/vid3_DB', 
                         collection_name = 'vid3_collection', 
                         embeddings = config['embeddings'])

combinations = [
    (
        'D:/Youtube rag system/Evaluation/Eval_dataset1.json',
        DB_VID1,
        'D:/Youtube rag system/Evaluation/Ragas_Eval_dataset1.json',
        'D:/Youtube rag system/Chunks/chunks_file1'
    ),

    (
        'D:/Youtube rag system/Evaluation/Eval_dataset2.json',
        DB_VID2,
        'D:/Youtube rag system/Evaluation/Ragas_Eval_dataset2.json',
        'D:/Youtube rag system/Chunks/chunks_file2'
    ),

    (
        'D:/Youtube rag system/Evaluation/Eval_dataset3.json',
        DB_VID3,
        'D:/Youtube rag system/Evaluation/Ragas_Eval_dataset3.json',
        'D:/Youtube rag system/Chunks/chunks_file3'
    )
]


# Build Ragas datasets for 3 videos and 
for item in combinations:
    build_retrieved_generated_dataset(Evaluation_dataset_file_path = item[0], 
                                      vector_DB = item[1], 
                                      output_file = item[2], 
                                      documents =  load(item[3]))