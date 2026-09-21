def analyze_text(text, wpm=200):

    if wpm <= 0:
        raise ValueError('WPM must be greater than 0')
    words = text.split()

    word_count = len(words)

    reading_time = word_count / wpm

    return {
        "words": words,
        "word_count": word_count,
        "reading_time": reading_time
    }

paragraph = """
Python is a programming language.
It is widely used in artificial intelligence
and machine learning.
"""
result = analyze_text(paragraph, 200)

print(result)

