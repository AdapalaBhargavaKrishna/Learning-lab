index = []

for chunk, embedding in zip(chunks, embeddings):

    index.append({
        "text": chunk,
        "embedding": embedding
    })