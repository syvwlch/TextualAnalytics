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


def adjective_noun_pairs(tokens):
    """Return a counter of the adjective+noun pairs in the text."""
    pairs = []
    last_word = ''
    last_tag = ''
    for word, tag in tokens:
        if last_tag == 'JJ' and tag == 'NN':
            pairs.append(last_word.lower()+' '+word.lower())
        last_word = word
        last_tag = tag
    return Counter(pairs)


# main loop
if __name__ == "__main__":
    # book = load_book('Texts/NonFreeTexts/InfiniteJest.txt')
    book = load_book('Texts/FreeTexts/Hamlet.txt')
    tokens = pos_tag(word_tokenize(book))
    unique_pairs = adjective_noun_pairs(tokens)
    print(unique_pairs.most_common(20))
