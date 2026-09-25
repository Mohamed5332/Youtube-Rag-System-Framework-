import json
import os 
from openai import AsyncOpenAI
import asyncio
from dotenv import load_dotenv

from ragas import SingleTurnSample

from ragas.llms import llm_factory
from ragas.embeddings.base import embedding_factory


from ragas.metrics.collections import ContextRecall , ContextPrecision , AnswerRelevancy , Faithfulness

load_dotenv()

groq_client = AsyncOpenAI(api_key = os.getenv(key = "Groq_api_key"), 
                          base_url = "https://api.groq.com/openai/v1", 
                          timeout = 300)

ollam_client = AsyncOpenAI(api_key = "ollama" , 
                           base_url = "http://localhost:11434/v1" ,
                           timeout= 300)


llm_evaluator = llm_factory(model = "openai/gpt-oss-20b",
                            provider = "openai", 
                            client = groq_client , 
                            max_tokens = 4096)

embeddings = embedding_factory(model = "bge-m3", 
                               client = ollam_client , 
                               provider = "openai")

context_precision = ContextPrecision(llm = llm_evaluator)

context_recall = ContextRecall(llm = llm_evaluator)

answer_relevancy = AnswerRelevancy(llm= llm_evaluator , embeddings = embeddings)

faithfullness = Faithfulness(llm= llm_evaluator)


async def Calc_faithfullness(sample):
    faithfullness_score = await  faithfullness.ascore(user_input = sample.user_input,
                                                       response = sample.response , 
                                                       retrieved_contexts = sample.retrieved_contexts)

    return {'faithfullness_score' : faithfullness_score.value}


async def Calc_answer_relevancy(sample):
    answer_relevancy_score = await answer_relevancy.ascore(user_input = sample.user_input,
                                                     response = sample.response)

    return {'answer_relevancy_score' : answer_relevancy_score.value} 


async def Calc_context_precision(sample):
    context_precision_score =  await context_precision.ascore(user_input = sample.user_input,
                                                              reference = sample.reference, 
                                                              retrieved_contexts = sample.retrieved_contexts)

    return {'context_precision_score' : context_precision_score.value}


async def Calc_context_recall(sample):
    context_recall_score = await context_recall.ascore(user_input = sample.user_input,
                                                       retrieved_contexts = sample.retrieved_contexts, 
                                                       reference = sample.reference)

    return {'context_recall_score' : context_recall_score.value}


async def Evaluate(sample):

    faithfullness_score , answer_relevancy_score , context_precision_score , context_recall_score =  await asyncio.gather(
        faithfullness.ascore(user_input = sample.user_input, 
                             response = sample.response , 
                             retrieved_contexts = sample.retrieved_contexts) , 

        answer_relevancy.ascore(user_input = sample.user_input,
                                response = sample.response), 

        context_precision.ascore(user_input = sample.user_input,
                                 reference = sample.reference, 
                                 retrieved_contexts = sample.retrieved_contexts),

        context_recall.ascore(user_input = sample.user_input,
                              retrieved_contexts = sample.retrieved_contexts, 
                              reference = sample.reference)
    )

    return {
        'context_recall' : context_recall_score.value ,

        'context_precision' : context_precision_score.value,

        'answer_relevancy' : answer_relevancy_score.value,

        'faithfullness' : faithfullness_score.value
    }



async def main():
    files = ['D:/Youtube rag system/Evaluation/Ragas_Eval_dataset1.json',
             'D:/Youtube rag system/Evaluation/Ragas_Eval_dataset2.json',
             'D:/Youtube rag system/Evaluation/Ragas_Eval_dataset3.json']
    
    print("Evaluation started successfully....")

    #for file in files :
    with open(file = files[2] , mode = 'r' , encoding = 'utf-8') as f :
        Ragas_dataset = json.load(fp= f)
        for index , example in enumerate(Ragas_dataset):
            sample = SingleTurnSample(user_input = example['question'], 
                                      retrieved_contexts = example['retrieved_contexts'], 
                                      retrieved_context_ids = example['retrieved_chunk_ids'],
                                      reference_context_ids = example['relevant_chunk_ids'], 
                                      response = example['response'],
                                      reference = example['ground_truth_answer'])

            result1 = await Calc_context_precision(sample = sample)
            


            print(f"question NO : {index+1} score => " , result1)
            print("\n" + "*" * 40)

    print("*" * 40)    



asyncio.run(main= main())