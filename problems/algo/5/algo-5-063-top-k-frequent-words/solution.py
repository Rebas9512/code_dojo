from collections import Counter
import heapq


def top_words(words: list[str], k: int) -> list[str]:
    counts = Counter(words)
    return heapq.nsmallest(k, counts, key=lambda word: (-counts[word], word))
