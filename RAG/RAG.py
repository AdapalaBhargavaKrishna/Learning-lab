"""
================================================================================
COGNIZANT ACE - RAG PIPELINE STUDY FILE (single-file, runnable)
================================================================================
Covers, in order:
    1. Chunking (fixed-size, overlapping)
    2. Embedding (FastEmbed-shaped interface + dependency-free simulated embedder)
    3. In-memory vector index + hand-rolled cosine similarity
    4. Top-k retrieval
    5. Word-frequency helper (in case "top-k frequent elements" means literal
       word counts rather than similarity ranking - build both, cheap insurance)
    6. WPM / text-processing helper (paragraph -> word list -> length -> time
       to read, matches the Reddit-reported pattern)
    7. End-to-end demo tying everything together

Run directly:  python3 rag_study.py
Every section's logic is independently testable - see the demo functions
under each heading and the __main__ block at the bottom.
================================================================================
"""

import math
import hashlib
from abc import ABC, abstractmethod


# ==============================================================================
# SECTION 1: CHUNKING
# ==============================================================================
# Fixed-size chunker with overlap. Splits on words (not raw characters) so
# each chunk stays semantically readable and lines up with how a real
# tokenizer-based embedder would consume text.
#
# Key invariants:
#   - step = chunk_size - overlap  ->  must be > 0, else the sliding window
#     never advances (infinite loop). Enforce overlap < chunk_size.
#   - Guard against tiny leftover tail chunks (near-duplicate junk that can
#     pollute the index with spuriously high similarity).

def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """
    Split `text` into overlapping chunks of `chunk_size` words, advancing
    the window by (chunk_size - overlap) words each step.

    Raises ValueError if overlap >= chunk_size.
    """
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    step = chunk_size - overlap
    words = text.split()
    chunks = []

    i = 0
    while i < len(words):
        piece = words[i:i + chunk_size]
        if len(piece) < overlap:
            # tail fragment too small to be meaningful on its own - stop
            break
        chunks.append(" ".join(piece))
        i += step

    return chunks


# ==============================================================================
# SECTION 2: EMBEDDING
# ==============================================================================
# Real FastEmbed usage (memorize this shape - matches the graded interface):
#
#     from fastembed import TextEmbedding
#     model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
#     vectors = list(model.embed(["text one", "text two"]))  # generator -> list
#     # each vector is a fixed-size np.ndarray, e.g. shape (384,)
#
# FastEmbed needs to download its ONNX model from HuggingFace on first use.
# If that's blocked (no internet in the grading sandbox), fall back to a
# deterministic, dependency-free SimulatedEmbedder with the SAME interface,
# so nothing else in the pipeline needs to change.

class BaseEmbedder(ABC):
    """Common interface - makes real/simulated embedders interchangeable."""

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        ...


class FastEmbedEmbedder(BaseEmbedder):
    """Real FastEmbed wrapper. Requires network access to fetch the model."""

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        from fastembed import TextEmbedding  # imported lazily
        self.model = TextEmbedding(model_name=model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [vec.tolist() for vec in self.model.embed(texts)]


class SimulatedEmbedder(BaseEmbedder):
    """
    Deterministic, dependency-free stand-in for FastEmbed.

    Method: hash each word into `dim` pseudo-random-but-deterministic floats,
    sum per chunk, then L2-normalize. Same text -> same vector every time.
    Different text -> different vector. Not semantically meaningful, but
    structurally identical to a real embedder (fixed dimension, normalized),
    which is all the downstream index/retrieval code needs.
    """

    def __init__(self, dim: int = 128):
        self.dim = dim

    def _word_vector(self, word: str) -> list[float]:
        vec = [0.0] * self.dim
        h = hashlib.sha256(word.lower().encode("utf-8")).digest()
        for i in range(self.dim):
            byte = h[i % len(h)]
            vec[i] = (byte / 255.0) * 2 - 1  # spread into [-1, 1]
        return vec

    def _embed_one(self, text: str) -> list[float]:
        words = text.split()
        if not words:
            return [0.0] * self.dim

        summed = [0.0] * self.dim
        for w in words:
            wv = self._word_vector(w)
            for i in range(self.dim):
                summed[i] += wv[i]

        norm = math.sqrt(sum(x * x for x in summed))
        if norm == 0:
            return summed
        return [x / norm for x in summed]

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_one(t) for t in texts]


def get_embedder(use_real: bool = False, dim: int = 128) -> BaseEmbedder:
    """Factory - swap embedders here, nothing downstream changes."""
    if use_real:
        return FastEmbedEmbedder()
    return SimulatedEmbedder(dim=dim)


# ==============================================================================
# SECTION 3: IN-MEMORY VECTOR INDEX + COSINE SIMILARITY (from scratch)
# ==============================================================================
# cosine_similarity(A, B) = (A . B) / (||A|| * ||B||)
#   - dot product over product of magnitudes
#   - range -1..1 for arbitrary vectors, usually 0..1 for text embeddings
#   - guard against division by zero for empty/zero vectors

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    if len(vec_a) != len(vec_b):
        raise ValueError("vectors must be the same dimension")

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(a * a for a in vec_a))
    magnitude_b = math.sqrt(sum(b * b for b in vec_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


class InMemoryVectorIndex:
    """Stores (chunk_text, embedding) pairs. No external vector DB."""

    def __init__(self):
        self._chunks: list[str] = []
        self._vectors: list[list[float]] = []

    def add(self, chunk: str, vector: list[float]) -> None:
        self._chunks.append(chunk)
        self._vectors.append(vector)

    def add_many(self, chunks: list[str], vectors: list[list[float]]) -> None:
        if len(chunks) != len(vectors):
            raise ValueError("chunks and vectors must be the same length")
        for c, v in zip(chunks, vectors):
            self.add(c, v)

    def __len__(self) -> int:
        return len(self._chunks)

    def all_items(self):
        """Yield (chunk, vector) pairs - used by retrieval."""
        return zip(self._chunks, self._vectors)


# ==============================================================================
# SECTION 4: TOP-K RETRIEVAL (by similarity)
# ==============================================================================

def retrieve_top_k(
    query_vector: list[float],
    index: InMemoryVectorIndex,
    k: int = 3,
) -> list[tuple[str, float]]:
    """Return top-k (chunk, score) pairs sorted by cosine similarity, descending."""
    scored = []
    for chunk, vec in index.all_items():
        score = cosine_similarity(query_vector, vec)
        scored.append((chunk, score))

    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:k]


def retrieve_top_k_heap(
    query_vector: list[float],
    index: InMemoryVectorIndex,
    k: int = 3,
) -> list[tuple[str, float]]:
    """
    Same result as retrieve_top_k, but O(n log k) instead of O(n log n) using
    a min-heap of size k - useful to mention if asked about scaling to large
    corpora. heapq is a MIN-heap, so we negate scores to simulate a max-heap.
    """
    import heapq
    heap: list[tuple[float, str]] = []  # (score, chunk) - negated score

    for chunk, vec in index.all_items():
        score = cosine_similarity(query_vector, vec)
        if len(heap) < k:
            heapq.heappush(heap, (score, chunk))
        elif score > heap[0][0]:
            heapq.heapreplace(heap, (score, chunk))

    heap.sort(key=lambda pair: pair[0], reverse=True)
    return [(chunk, score) for score, chunk in heap]


# ==============================================================================
# SECTION 5: WORD-FREQUENCY HELPER
# ==============================================================================
# In case "top-k frequent elements" in the assessment means literal word/
# token frequency counting rather than embedding similarity - cheap to have
# both ready. Classic top-k frequent pattern (same shape as LeetCode 347).

def word_frequency(text: str) -> dict[str, int]:
    """Return a {word: count} map, case-insensitive, punctuation-stripped."""
    counts: dict[str, int] = {}
    for raw_word in text.split():
        word = raw_word.strip(".,!?;:\"'()[]{}").lower()
        if not word:
            continue
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_k_frequent_words(text: str, k: int) -> list[tuple[str, int]]:
    """Return the k most frequent words as (word, count), most frequent first."""
    counts = word_frequency(text)
    # sort by count descending; ties broken alphabetically for determinism
    ranked = sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))
    return ranked[:k]


# ==============================================================================
# SECTION 6: WPM / TEXT-PROCESSING HELPER
# ==============================================================================
# Matches the Reddit-reported pattern: "convert a paragraph into a list and
# return the length of the list, then using it return time required to
# process it (words per minute given)".

def paragraph_to_word_list(paragraph: str) -> list[str]:
    """Split a paragraph into a list of words."""
    return paragraph.split()


def estimate_reading_time_minutes(paragraph: str, words_per_minute: int) -> float:
    """
    Given a paragraph and a reading speed (words per minute), estimate the
    time in minutes required to read/process it.
    """
    if words_per_minute <= 0:
        raise ValueError("words_per_minute must be positive")

    word_list = paragraph_to_word_list(paragraph)
    word_count = len(word_list)
    return word_count / words_per_minute


def estimate_reading_time_seconds(paragraph: str, words_per_minute: int) -> float:
    return estimate_reading_time_minutes(paragraph, words_per_minute) * 60


# ==============================================================================
# SECTION 7: END-TO-END DEMO
# ==============================================================================

DOCUMENT = """
The Reserve Bank of India regulates monetary policy and oversees the
banking system in India. It sets the repo rate, which influences how
much banks charge for loans across the economy. Inflation targeting is
one of its primary mandates under the current policy framework.

Cognizant is a multinational information technology services and
consulting company headquartered in the United States. It provides
services in digital, technology, consulting, and operations, working
with clients across banking, healthcare, and retail sectors.

Retrieval Augmented Generation, or RAG, combines a retrieval step over
a knowledge base with a generative language model. Instead of relying
purely on parameters learned during training, the model is given
relevant retrieved text chunks as context before generating an answer,
which reduces hallucination and allows use of up-to-date information.
"""


def build_pipeline(document: str, chunk_size: int = 30, overlap: int = 8):
    """Ingest + chunk + embed + index a document. Returns (index, embedder)."""
    chunks = chunk_text(document, chunk_size=chunk_size, overlap=overlap)
    embedder = get_embedder(use_real=False, dim=128)
    vectors = embedder.embed(chunks)

    index = InMemoryVectorIndex()
    index.add_many(chunks, vectors)
    return index, embedder


def answer_query(query: str, index: InMemoryVectorIndex, embedder, k: int = 2):
    query_vector = embedder.embed([query])[0]
    return retrieve_top_k(query_vector, index, k=k)


# ==============================================================================
# MAIN - run every section's self-test
# ==============================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SECTION 1: CHUNKING")
    print("=" * 70)
    sample_text = "the quick brown fox jumps over the lazy dog and then runs away very fast into the dark forest"
    chunks = chunk_text(sample_text, chunk_size=5, overlap=2)
    for i, c in enumerate(chunks):
        print(f"  [{i}] {c!r}")
    try:
        chunk_text(sample_text, chunk_size=3, overlap=3)
    except ValueError as e:
        print(f"  edge case (overlap >= chunk_size) correctly raised: {e}")

    print()
    print("=" * 70)
    print("SECTION 2: EMBEDDING")
    print("=" * 70)
    embedder = get_embedder(use_real=False, dim=64)
    vecs = embedder.embed(["the quick brown fox", "the quick brown fox", "completely different text"])
    print("  vector length:", len(vecs[0]))
    print("  identical text -> identical vector:", vecs[0] == vecs[1])
    print("  different text -> different vector:", vecs[0] != vecs[2])

    print()
    print("=" * 70)
    print("SECTION 3: COSINE SIMILARITY + INDEX")
    print("=" * 70)
    a, b, c, d = [1.0, 0.0], [1.0, 0.0], [0.0, 1.0], [-1.0, 0.0]
    print("  identical vectors (expect  1.0):", cosine_similarity(a, b))
    print("  orthogonal vectors (expect 0.0):", cosine_similarity(a, c))
    print("  opposite vectors  (expect -1.0):", cosine_similarity(a, d))

    idx_demo = InMemoryVectorIndex()
    idx_demo.add_many(["chunk one", "chunk two"], [[1.0, 0.0], [0.0, 1.0]])
    print("  index size:", len(idx_demo))

    print()
    print("=" * 70)
    print("SECTION 4: TOP-K RETRIEVAL")
    print("=" * 70)
    idx_demo2 = InMemoryVectorIndex()
    idx_demo2.add_many(
        chunks=["cats and dogs", "space rockets", "cats are great pets"],
        vectors=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.9, 0.1, 0.0]],
    )
    query_vec = [1.0, 0.0, 0.0]
    for chunk, score in retrieve_top_k(query_vec, idx_demo2, k=2):
        print(f"  {score:.3f}  {chunk}")
    print("  (heap version, same result):")
    for chunk, score in retrieve_top_k_heap(query_vec, idx_demo2, k=2):
        print(f"  {score:.3f}  {chunk}")

    print()
    print("=" * 70)
    print("SECTION 5: WORD FREQUENCY / TOP-K FREQUENT")
    print("=" * 70)
    freq_text = "the cat sat on the mat the cat was happy"
    print("  top-3 frequent words:", top_k_frequent_words(freq_text, k=3))

    print()
    print("=" * 70)
    print("SECTION 6: WPM / READING TIME")
    print("=" * 70)
    paragraph = "This is a sample paragraph used to test the word per minute reading time calculation logic."
    word_list = paragraph_to_word_list(paragraph)
    print("  word list length:", len(word_list))
    print("  estimated reading time (200 wpm):",
          round(estimate_reading_time_minutes(paragraph, 200), 4), "minutes")
    print("  estimated reading time (200 wpm):",
          round(estimate_reading_time_seconds(paragraph, 200), 2), "seconds")

    print()
    print("=" * 70)
    print("SECTION 7: END-TO-END PIPELINE")
    print("=" * 70)
    index, pipeline_embedder = build_pipeline(DOCUMENT, chunk_size=30, overlap=8)
    print(f"  Indexed {len(index)} chunks.")

    test_query = "What does RAG do for language models?"
    results = answer_query(test_query, index, pipeline_embedder, k=2)
    print(f"  Query: {test_query}")
    for rank, (chunk, score) in enumerate(results, start=1):
        print(f"  [{rank}] score={score:.4f}")
        print(f"      {chunk.strip()}")