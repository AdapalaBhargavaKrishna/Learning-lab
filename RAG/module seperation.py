def load_and_clean(raw_text: str) -> str:
    """Ingestion + preprocessing: clean raw text."""
    ...

def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split cleaned text into overlapping chunks."""
    ...

def generate_embeddings(chunks: list[str]) -> list:
    """Use FastEmbed to convert chunks into vectors."""
    ...

def build_index(chunks: list[str], embeddings: list) -> list[dict]:
    """Pair chunks with their embeddings into an in-memory index."""
    ...

def cosine_similarity(vec_a, vec_b) -> float:
    """Compute cosine similarity between two vectors."""
    ...

def retrieve_top_k(query: str, index: list[dict], k: int) -> list[dict]:
    """Embed the query, rank all indexed chunks by similarity, return top k."""
    ...