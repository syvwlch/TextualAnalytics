"""Split the text by <ch> tags and save to separate files."""


def load_book(filepath):
    """Load the book's text, tokenize and tag in memory."""
    with open(filepath+'.txt', 'r') as f:
        book = f.read()
    return book


def save_book(filepath, book):
    """Save a string to a text file."""
    with open(filepath+'.txt', 'w') as f:
        f.write(book)
    return


# main loop
if __name__ == "__main__":

    book = load_book('Texts/NonFreeTexts/InfiniteJest_Chapters')
    chapters = book.split('<ch>')
    print('Number of chapters: ' + str(len(chapters)))

    index = 0
    for chapter in chapters:
        filename = 'Texts/NonFreeTexts/InfiniteJest_ch'+str(index)
        save_book(filename, chapter)
        index += 1
