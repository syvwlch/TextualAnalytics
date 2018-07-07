"""
First text analytics script using nltk.

Will load the text and then create a dictionary of words with the number of
occurences in the text.
"""


def load_book(filename):
    """Load the book's text from the file into memory."""
    with open(filename, 'r') as f:
        book = f.read()
    return book


# main loop
if __name__ == "__main__":
    print(load_book('Texts/FreeTexts/hamlet.txt'))
