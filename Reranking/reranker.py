def Rerank(reranker_model , query , docs , Top_k):
    reranked_documents = []
    pairs = []
    for doc in docs: 
        pair = (query , doc.page_content)
        pairs.append(pair)

    scores = reranker_model.predict(inputs = pairs)

    docs_scores = list(zip(scores , docs))

    sorted_result = sorted(docs_scores , reverse = True)

    for _ , doc in sorted_result[:Top_k]:
        reranked_documents.append(doc)

    return reranked_documents