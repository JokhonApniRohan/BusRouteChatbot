
def get_similar_docs(vector_store, query, k=5):
    return vector_store.similarity_search(query, k=k)
