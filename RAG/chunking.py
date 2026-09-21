def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    words = text.split()
    chunks = []

    step = chunk_size - overlap

    i = 0

    while i < len(words):
        chunk = words[i:i + chunk_size]

        if len(chunk) < overlap:
            break

        chunks.append(" ".join(chunk))
        i += step

    return chunks