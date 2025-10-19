import nltk
from nltk.corpus import words
import sys

# Make sure the NLTK 'words' corpus is downloaded
try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

# Load dictionary
dictionary = set(words.words())  # Use set for faster lookup


def levenshtein_distance(S: str, T: str) -> int:
    """Compute Levenshtein distance using two-row optimization."""
    m, n = len(S), len(T)

    # Ensure T is the shorter string to reduce space
    if n > m:
        S, T = T, S
        m, n = n, m

    prev = list(range(n + 1))
    cur = [0] * (n + 1)

    for i in range(1, m + 1):
        cur[0] = i
        for j in range(1, n + 1):
            cost = 0 if S[i - 1].lower() == T[j - 1].lower() else 1
            cur[j] = min(
                prev[j - 1] + cost,  # substitution/match
                prev[j] + 1,  # deletion
                cur[j - 1] + 1  # insertion
            )
        prev, cur = cur, prev  # swap rows
    return prev[n]


def spell_check(sentence: str):
    words_in_sentence = sentence.split()

    for word in words_in_sentence:
        word_lower = word.lower()
        # Exact match check
        if word_lower in dictionary:
            continue

        # Compute Levenshtein distances with all dictionary words
        min_dist = float('inf')
        suggestions = []
        for dict_word in dictionary:
            dist = levenshtein_distance(word_lower, dict_word.lower())
            if dist < min_dist:
                min_dist = dist
                suggestions = [dict_word]
            elif dist == min_dist:
                suggestions.append(dict_word)

        print(
            f"'{word}': Spelling error. Suggestions (distance {min_dist}): {suggestions[:10]}{'...' if len(suggestions) > 10 else ''}")


if __name__ == "__main__":
    sentence = input("Enter a sentence to spell-check: ").strip()
    spell_check(sentence)
