from fastembed import TextEmbedding
from chunking import chunk_text

# ============================================================
# 1. CHUNKING
# ============================================================

# def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:

#     if overlap >= chunk_size:
#         raise ValueError(
#             "overlap must be smaller than chunk_size"
#         )

#     words = text.split()

#     chunks = []

#     step = chunk_size - overlap

#     i = 0

#     while i < len(words):

#         chunk = words[i:i + chunk_size]

#         if len(chunk) < overlap:
#             break

#         chunks.append(" ".join(chunk))

#         i += step

#     return chunks


# ============================================================
# 2. COSINE SIMILARITY
# ============================================================

def cosine_similarity(a, b):

    dot = sum(
        x * y
        for x, y in zip(a, b)
    )

    norm_a = sum(
        x * x
        for x in a
    ) ** 0.5

    norm_b = sum(
        y * y
        for y in b
    ) ** 0.5

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


# ============================================================
# 3. BUILD VECTOR INDEX
# ============================================================

def build_index(chunks, embedder):

    embeddings = list(
        embedder.embed(chunks)
    )

    index = []

    for chunk, embedding in zip(
        chunks,
        embeddings
    ):

        index.append({
            "text": chunk,
            "embedding": embedding
        })

    return index


# ============================================================
# 4. TOP-K RETRIEVAL
# ============================================================

def top_k_retrieve(
    index,
    query,
    embedder,
    k=2
):

    query_vector = list(embedder.embed([query]))[0]
    results = []

    for item in index:

        score = cosine_similarity(
            query_vector,
            item["embedding"]
        )

        results.append({
            "text": item["text"],
            "score": score
        })

    results.sort(key=lambda x: x["score"],reverse=True)
    return results[:k]

# ============================================================
# 5. WORD FREQUENCY
# ============================================================

def top_k_frequent_words(text, k):

    words = text.lower().split()

    frequency = {}

    for word in words:

        frequency[word] = (
            frequency.get(word, 0) + 1
        )

    items = list(frequency.items())

    items.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return items[:k]


# ============================================================
# 6. WPM / READING TIME
# ============================================================

def analyze_text(text, wpm=200):

    if wpm <= 0:
        raise ValueError(
            "WPM must be greater than 0"
        )

    words = text.split()

    word_count = len(words)

    reading_time = word_count / wpm

    return {
        "words": words,
        "word_count": word_count,
        "reading_time_minutes": reading_time
    }

# ============================================================
# 7. MAIN PIPELINE
# ============================================================

documents = [

    """
    Python is a programming language.
    Python is widely used in artificial intelligence.
    Python is also popular for machine learning.
    """,

    """
    RAG stands for Retrieval Augmented Generation.
    RAG retrieves relevant information from documents.
    The retrieved information can be provided to a language model.
    """
]


# ------------------------------------------------------------
# INGESTION + CHUNKING
# ------------------------------------------------------------

chunks = []

for document in documents:

    document_chunks = chunk_text(
        document,
        chunk_size=10,
        overlap=3
    )

    chunks.extend(document_chunks)


print("CHUNKS:")
for chunk in chunks:
    print(chunk)
    print()


# ------------------------------------------------------------
# EMBEDDING MODEL
# ------------------------------------------------------------

embedding_model = TextEmbedding()

# ------------------------------------------------------------
# BUILD INDEX
# ------------------------------------------------------------

index = build_index(
    chunks,
    embedding_model
)


print("INDEX CREATED")
print("Number of vectors:", len(index))


# ------------------------------------------------------------
# QUERY
# ------------------------------------------------------------

query = "How is Python used in machine learning?"


# ------------------------------------------------------------
# RETRIEVE TOP K
# ------------------------------------------------------------

results = top_k_retrieve(
    index,
    query,
    embedding_model,
    k=2
)

print("\nTOP RESULTS:")

for result in results:

    print(
        f"Score: {result['score']:.4f}"
    )

    print(
        f"Text: {result['text']}"
    )

    print()


# ------------------------------------------------------------
# WORD FREQUENCY
# ------------------------------------------------------------

text = "Python Python AI AI AI RAG"

print(
    "Top frequent words:",
    top_k_frequent_words(text, 2)
)


# ------------------------------------------------------------
# WPM
# ------------------------------------------------------------

analysis = analyze_text(
    text,
    wpm=200
)

print(
    "Word count:",
    analysis["word_count"]
)

print(
    "Reading time:",
    analysis["reading_time_minutes"],
    "minutes"
)