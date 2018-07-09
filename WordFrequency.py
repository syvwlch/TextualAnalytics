"""
First text analytics script using nltk.

Will load the text and then create a dictionary of words with the number of
occurences in the text.
"""

from collections import Counter
from nltk import pos_tag, word_tokenize


def load_book(filename):
    """Load the book's text from the file into memory."""
    with open(filename, 'r') as f:
        return f.read()


def unique_words_by_tag(tokens, tag_value='N/A'):
    """Return a counter of the tokens with the given tag value."""
    nouns = []
    for word, tag in tokens:
        if tag == tag_value or tag_value == 'N/A':
            nouns.append(word)
    return Counter(nouns)


# main loop
if __name__ == "__main__":
    # book = load_book('Texts/NonFreeTexts/InfiniteJest.txt')
    book = load_book('Texts/FreeTexts/Hamlet.txt')
    tokens = pos_tag(word_tokenize(book))
    unique_words = unique_words_by_tag(tokens, 'NNP')
    print(unique_words.most_common(20))
