results.sort(key = lambda x : x['score'], reverse = True)

k = 2
top_chunks = results[:k]


def top_k_retrieve(index , query , embedder, k = 2):
    query_vector = list(embedder.embed([query]))[0]

    results = []

    for item in index:
        score = cosine_similarity(
            query_vector,
            item['embedding']
        )

        results.append({
            "text" : item['text'],
            "score" : score
        })

    results.sort(key = lambda x : x['score'], reverse = True)
    return results[:k]

def top_k_frequent_words(text, k):
    words = text.lower().split()

    freq = {}

    for word in words:
        freq[word] = freq.get(word , 0) + 1

    items = list(freq.items())
    items.sort(key = lambda x : x[1] , reverse = True)

    return items[:k]