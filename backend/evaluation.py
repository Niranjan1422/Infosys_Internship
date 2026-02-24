def precision_at_k(retrieved, relevant, k=5):
    retrieved_k = retrieved[:k]
    relevant_set = set(relevant)
    return len([r for r in retrieved_k if r in relevant_set]) / k