"""
First text analytics script using nltk.

Will load the text and then create a dictionary of words with the number of
occurences in the text.
"""

from nltk import pos_tag, word_tokenize


def load_book(filename):
    """Load the book's text from the file into memory."""
    with open(filename, 'r') as f:
        return f.read()


def unique_words_by_tag(tokens, tag_value):
    """Return a set of the words of the given tag value in the book."""
    nouns = []
    for word, tag in tokens:
        if tag == tag_value:
            nouns.append(word)
    return set(nouns)


# main loop
if __name__ == "__main__":
    # book = load_book('Texts/NonFreeTexts/InfiniteJest.txt')
    book = load_book('Texts/FreeTexts/Hamlet.txt')
    tokens = pos_tag(word_tokenize(book))
    unique_nouns = unique_words_by_tag(tokens, 'NNP')
    print(len(unique_nouns))
