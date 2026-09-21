from fastembed import TextEmbedding

# Initialize the model
embedding_model = TextEmbedding()

documents = [
    "passage: This is an example passage.",
    "passage: another chunk of text here"
]

#  .embed() return a GENERATOR, not a list directly
embeddings_generator = embedding_model.embed(documents)

# convert to list to use the vectors
embeddings_list = list(embeddings_generator)

print(len(embeddings_list[0]))

class SimpleEmbedder:
    def __init__(self):
        self.vocabulary = ["python", "java", "ai", "rag"]

    def embed(self , texts):
        for text in texts:

            words = text.lower().split()

            vector = []

            for word in self.vocabulary:
                vector.append(words.count(word))

            yield vector

model = SimpleEmbedder()

texts = [
    "Python is useful for AI",
    "RAG is used in AI",
    "Java is a programming language"
]

embeddings = list(model.embed(texts))
print(embeddings)