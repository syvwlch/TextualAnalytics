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


def tag_tokens(book):
    """Tokenize and tag the book's text."""
    return pos_tag(word_tokenize(book))


# main loop
if __name__ == "__main__":
    # book = load_book('Texts/NonFreeTexts/InfiniteJest.txt')
    book = load_book('Texts/FreeTexts/Hamlet.txt')
    print(tag_tokens(book))
