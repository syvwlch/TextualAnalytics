"""
First text analytics script using nltk.

Will load the text and then create a dictionary of words with the number of
occurences in the text.
"""

import pickle
from collections import Counter
from nltk import pos_tag, word_tokenize


def tokenize_and_tag(filepath):
    """Load the book's text, tokenize and tag in memory."""
    with open(filepath+'.txt', 'r') as f:
        book = f.read()
    return pos_tag(word_tokenize(book))


def pickle_tokens(tokens, filepath):
    """Pickle the tokens to a file."""
    with open(filepath+'.pickle', 'wb') as f:
        pickle.dump(tokens, f)
    return


def unpickle_tokens(filepath):
    """Unpickle the tokens into memory."""
    try:
        with open(filepath+'.pickle', 'rb') as f:
            tokens = pickle.load(f)
    except FileNotFoundError:
        tokens = tokenize_and_tag(filepath)
        pickle_tokens(tokens, filepath)
    return tokens


def unique_words_by_tag(tokens, tag_value='N/A'):
    """Return a counter of the tokens with the given tag value."""
    nouns = []
    for word, tag in tokens:
        if tag == tag_value or tag_value == 'N/A':
            nouns.append(word.lower())
    return Counter(nouns)


def adjective_noun_pairs(tokens):
    """Return a counter of the adjective+noun pairs in the text."""
    pairs = []
    last_word = ''
    last_tag = ''
    for word, tag in tokens:
        if last_tag.startswith('JJ') and tag.startswith('NN'):
            pairs.append(last_word.lower()+' '+word.lower())
        last_word = word
        last_tag = tag
    return Counter(pairs)


def adjectives_before(tokens, target_word):
    """Return a counter of the adjectives which precede the target_word."""
    adjectives = []
    last_word = ''
    last_tag = ''
    target_word = target_word.lower()
    for word, tag in tokens:
        if word.lower() == target_word and last_tag.startswith('JJ'):
            adjectives.append(last_word.lower())
        last_word = word
        last_tag = tag
    return Counter(adjectives)


def nouns_after(tokens, target_word):
    """Return a counter of the nouns which follow the target_word."""
    nouns = []
    last_word = ''
    target_word = target_word.lower()
    for word, tag in tokens:
        if last_word.lower() == target_word and tag.startswith('NN'):
            nouns.append(word.lower())
        last_word = word
    return Counter(nouns)


# main loop
if __name__ == "__main__":
    try:
        tokens = unpickle_tokens('Texts/NonFreeTexts/InfiniteJest')
    except FileNotFoundError:
        tokens = unpickle_tokens('Texts/FreeTexts/Hamlet')

    DEPTH = 5

    frequent_adjectives = unique_words_by_tag(tokens, 'JJ').most_common(DEPTH)
    frequent_nouns = unique_words_by_tag(tokens, 'NN').most_common(DEPTH)
    frequent_noun_pairs = adjective_noun_pairs(tokens).most_common(DEPTH)

    print('Most frequent adjectives:')
    print(frequent_adjectives)
    print('Most frequent nouns:')
    print(frequent_nouns)
    print('Most frequent adjective/noun pairs:')
    print(frequent_noun_pairs)
    print("Most frequent nouns after the adjective '"
          + frequent_adjectives[0][0] + "':")
    print(nouns_after(tokens, frequent_adjectives[0][0]).most_common(5))
    print("Most frequent adjectives before the noun '"
          + frequent_nouns[0][0] + "':")
    print(adjectives_before(tokens, frequent_nouns[0][0]).most_common(5))
