"""
First text analytics script using nltk.

Will load the tokens and then create a dictionary of words with the number of
occurences in the text.
"""

from TokenizeLemmatize import unpickle_tokens
from collections import Counter


def count_names(tokens):
    """Return a counter of the continuous chains of NNPs."""
    names = []
    name = None
    for word, tag in tokens:
        if word == '’':
            tag = '’'
        if name is None and tag.startswith('NNP'):
            name = word
        elif name is not None and tag.startswith('NNP'):
            name = name + ' ' + word
        elif name is not None and not tag.startswith('NNP'):
            names.append(name)
            name = None
    return Counter(names)


def filter_names(names, target):
    """Filter out the names which do not contain the target name."""
    hits = []
    for name, count in names.most_common():
        if target in name:
            hits.append((name, count))
    return hits


# main loop
if __name__ == "__main__":
    try:
        tokens = unpickle_tokens('Texts/NonFreeTexts/InfiniteJest')
    except FileNotFoundError:
        tokens = unpickle_tokens('Texts/FreeTexts/Hamlet')

    # print(count_names(tokens))
    print(filter_names(count_names(tokens), 'Group'))
