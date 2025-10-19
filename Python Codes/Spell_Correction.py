#!/usr/bin/env python3
"""
Simple Levenshtein-based spell checker using NLTK words corpus.
"""

import nltk
from nltk.corpus import words
import sys

# Make sure the NLTK 'words' corpus is downloaded
try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

# Load dictionary
DICTIONARY = set(words.words())  # Use set for faster lookup

# --- Levenshtein Distance Function ---
def levenshtein_distance(a: str, b: str) -> int:
    """Compute the Levenshtein distance between two strings."""
    m, n = len(a), len(b)
    if m == 0:
        return n
    if n == 0:
        return m

    prev = list(range(n + 1))
    curr = [0] * (n + 1)

    for i in range(1, m + 1):
        curr[0] = i
        for j in range(1, n + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            curr[j] = min(
                prev[j - 1] + cost,  # substitution/match
                prev[j] + 1,         # deletion
                curr[j - 1] + 1      # insertion
            )
        prev, curr = curr, prev

    return prev[n]


# --- Main Spell Checker ---
def spell_check():
    # Step 1: Take input
    text = input("Enter a sentence to spell-check: ").strip().lower()

    # Step 2: Assume all are wrong initially
    wrong_words = text.split()

    # Step 3–4: Remove words that exist in dictionary
    wrong_words = [w for w in wrong_words if w not in DICTIONARY]

    # Step 5: If no wrong words
    if not wrong_words:
        print("No spelling errors found.")
        return

    # Step 6: For each wrong word, find closest dictionary matches
    for w in wrong_words:
        min_dist = float("inf")
        suggestions = []

        for dict_word in DICTIONARY:
            dict_word=dict_word.lower()
            dist = levenshtein_distance(w, dict_word)
            if dist < min_dist:
                min_dist = dist
                suggestions = [dict_word]
            elif dist == min_dist:
                suggestions.append(dict_word)

        print(f"‘{w}’: Spelling error. Suggestions (distance {min_dist}): {suggestions[:10]}{'...' if len(suggestions) > 10 else ''}")
        wrong_words.remove(w)
# --- Run ---
if __name__ == "__main__":
    spell_check()
