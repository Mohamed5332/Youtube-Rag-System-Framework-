from langchain_community.document_loaders import YoutubeLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_ollama import OllamaEmbeddings , OllamaLLM
from joblib import load , dump
from langchain_core.prompts import PromptTemplate




def assign_ids(chunks):
    for index , chunk in enumerate(chunks):
        chunk.metadata['chunk_id'] = f"chunk_No:{index}"



def save_chunks(chunks , vid_name):
    dump(value = chunks , filename = vid_name)


Dataset_Generation_Prompt = PromptTemplate(
    template="""
You are an expert in creating evaluation datasets for Retrieval-Augmented Generation (RAG) systems.

Generate EXACTLY 10 diverse evaluation examples using ONLY the provided context.

RULES:
- Use ONLY information explicitly present in the context. Do NOT use external knowledge, do NOT invent facts.
- Copy chunk IDs EXACTLY as they appear in the context. Do NOT invent, modify, shorten, or reformat them.
- Every chunk ID you output MUST exist in the provided context.
- Questions must be diverse: mix factual, conceptual, how, why, comparison, and relationship questions.
- Avoid duplicate or overly similar questions.
- Avoid simple yes/no questions.
- ground_truth_answer must be concise, complete, and fully supported by the context. Do NOT hallucinate.
- relevant_chunk_ids must include ONLY chunks that directly support the answer (not every chunk that mentions the same topic).

OUTPUT FORMAT — CRITICAL:
Return ONLY a valid JSON array. Nothing else.
- No markdown, no ```json fences, no explanations, no headings, no comments.
- No text before the opening [ or after the closing ].
- The array MUST contain EXACTLY 10 objects.
- Each object MUST have EXACTLY these 3 fields, spelled exactly like this:
  "question" (string)
  "ground_truth_answer" (string)
  "relevant_chunk_ids" (array of strings)

Example structure (do not copy the values, only the shape):
[
  {{
    "question": "A question",
    "ground_truth_answer": "The answer",
    "relevant_chunk_ids": ["<exact_id_from_context>"]
  }}
]

Before answering, internally verify:
1. Output starts with [ and ends with ].
2. There are exactly 10 objects.
3. Every relevant_chunk_ids value exists verbatim in the context below.
4. No text exists outside the JSON array.

Context:
{context}
""",
    input_variables=["context"]
)




def get_context(chunks_file_path):

    chunks = load(filename = chunks_file_path)

    context = ""

    for chunk in chunks:
        context += "\n" + chunk.metadata['chunk_id'] + "\n" + chunk.page_content


    return context    




def get_ready_prompt(context):
    
    Ready_prompt = Dataset_Generation_Prompt.invoke(input= {
            'context' : context
    })

    return Ready_prompt.text.strip()    