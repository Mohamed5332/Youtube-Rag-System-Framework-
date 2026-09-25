import json
import os
import sys
import time

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(THIS_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM , OllamaEmbeddings
from Retreivers.mmr import build_mmr_retrievers
from Ingestion.Vector_DB import load_vector_DB
from Retreivers.factory import build_retriever
from langchain_huggingface import HuggingFaceEndpointEmbeddings


config = {'llm' : OllamaLLM(model = "qwen3:1.7b"),
          'embeddings_locall' : OllamaEmbeddings(model = "bge-m3"), 
          'embeddings_production' : HuggingFaceEndpointEmbeddings(
                                    model="intfloat/multilingual-e5-large",
                                    huggingfacehub_api_token=os.getenv("HF_TOKEN") )}


class rag_pipeline:
    
    def __init__(self , llm , retriever):
        self.llm = llm 
        self.retriever = retriever


    def invoke(self , question):
        # result = retriever.invoke(input = item['question'])
        
        retrieval_start = time.time()
        docs = self.retriever.invoke(input = question)
        retrieval_end = time.time()

        

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        ) 

        prompt = PromptTemplate(
            template="""
        Answer the question using only the provided context.

        Important instructions:
            - Answer in the same language as the question.
            - If the question is in Arabic, answer in Arabic.
            - If the question is in English, answer in English.
            - Do not use information that is not present in the context.
            - If the answer cannot be found in the context, say that the information is not available in the provided context.
        
        Language and terminology rules:
            - Answer in the same language as the user's question.
            - If the question is primarily Arabic, use Arabic as the main language and sentence structure.
            - Keep technical, scientific, professional, and domain-specific terms in their original English form when English is the natural or standard terminology.
            - Do not translate, transliterate, or write both the Arabic and English versions of the same term.
            - Use English terms naturally within the Arabic sentence, without starting the sentence in English unless the user asks for an English answer.
            - Preserve important terminology from the provided context whenever possible.
            - If the question is primarily English, answer naturally in English.
            - If the question mixes Arabic and English, use the dominant language as the main language while preserving English terminology naturally.        Context:
        {context}

        Question:
        {question}

        Answer:
        """,
            input_variables=["question", "context"]
        )

        start_build_prompt = time.time()
        ready_prompt = prompt.invoke(input = {'question' : question ,
                                              'context' : context})
        end_build_prompt = time.time()

        start_generation = time.time()
        answer = self.llm.invoke(input = ready_prompt)
        end_generation = time.time()


        print("Retrieval latency : " , retrieval_end - retrieval_start)
        print("Build prompt latency : " , end_build_prompt - start_build_prompt)
        print("Generation latency : " , end_generation - start_generation)
        
        return answer