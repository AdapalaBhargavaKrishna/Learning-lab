def cosine_similarity(a,b):
    dot = 0

    for x , y in zip(a , b):
        dot += x * y

    norm_a = 0
    norm_b = 0

    for x in a:
        norm_a = x * x

    for y in b:
        norm_b += y * y

    norm_a = norm_a ** 0.5
    norm_b = norm_b ** 0.5

    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot / (norm_a * norm_b)

def cosine_similarity(a , b):
    dot = sum(x * y for x , y in zip(a , b))

    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)