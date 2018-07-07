"""
First text analytics script using nltk.

Will load the text and then create a dictionary of words with the number of
occurences in the text.
"""

from nltk import word_tokenize


def load_book(filename):
    """Load the book's text from the file into memory."""
    with open(filename, 'r') as f:
        return f.read()


def tokenize_book(book):
    """Tokenize a book using word_tokenize function from nltk."""
    return word_tokenize(book)


# main loop
if __name__ == "__main__":
    print(word_tokenize(load_book('Texts/FreeTexts/hamlet.txt')))
