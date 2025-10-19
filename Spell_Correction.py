# Spell Checker using Levenshtein Distance

import nltk
import Levenshtein  
nltk.download('words', quiet=True)

from nltk.corpus import words

def load_dictionary():
    """
    English words from NLTK's word corpus.
    """
    word_list = [w.lower() for w in words.words()]
    return set(word_list)  


def correct_word(word, dictionary, max_distance=5):
    """
    Suggest the closest correct spelling for 'word'.
    """
    word = word.lower()
    best_word, best_dist = None, float('inf')

    for w in dictionary:
        dist = Levenshtein.distance(word, w)
        if dist < best_dist:
            best_word, best_dist = w, dist
        if best_dist == 0:
            break  # exact match found

    if best_dist <= max_distance:
        return best_word
    else:
        return None


def spell_check(text, dictionary):
    """
    Spell-check text and return suggestions for incorrect words.
    """
    words_in_text = text.split()
    corrections = {}
    for w in words_in_text:
        if w.lower() not in dictionary:
            suggestion = correct_word(w, dictionary)
            if suggestion:
                corrections[w] = suggestion
    return corrections

# Example usage with user input

if __name__ == "__main__":
    dictionary = load_dictionary()

    print("Enter your text below:")
    text = input(" ")

    results = spell_check(text, dictionary)

    if results:
        print("\nPossible corrections:")
        for wrong, right in results.items():
            print(f"  {wrong} → {right}")
    else:
        print("\n No spelling mistakes detected!")
