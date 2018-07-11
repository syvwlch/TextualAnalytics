"""
First text analytics script using nltk.

Will load the text and then create a dictionary of words with the number of
occurences in the text.
"""

import pickle
from collections import Counter
from nltk import pos_tag, word_tokenize, WordNetLemmatizer
from nltk.corpus import wordnet as wn

TAG_MAP = {
        'CC': None,  # coordin. conjunction (and, but, or)
        'CD': wn.NOUN,  # cardinal number (one, two)
        'DT': None,  # determiner (a, the)
        'EX': wn.ADV,  # existential ‘there’ (there)
        'FW': None,  # foreign word (mea culpa)
        'IN': wn.ADV,  # preposition/sub-conj (of, in, by)
        'JJ': wn.ADJ,  # adjective (yellow)
        'JJR': wn.ADJ,  # adj., comparative (bigger)
        'JJS': wn.ADJ,  # adj., superlative (wildest)
        'LS': None,  # list item marker (1, 2, One)
        'MD': None,  # modal (can, should)
        'NN': wn.NOUN,  # noun, sing. or mass (llama)
        'NNS': wn.NOUN,  # noun, plural (llamas)
        'NNP': wn.NOUN,  # proper noun, sing. (IBM)
        'NNPS': wn.NOUN,  # proper noun, plural (Carolinas)
        'PDT': wn.ADJ,  # predeterminer (all, both)
        'POS': None,  # possessive ending (’s )
        'PRP': None,  # personal pronoun (I, you, he)
        'PRP$': None,  # possessive pronoun (your, one’s)
        'RB': wn.ADV,  # adverb (quickly, never)
        'RBR': wn.ADV,  # adverb, comparative (faster)
        'RBS': wn.ADV,  # adverb, superlative (fastest)
        'RP': wn.ADJ,  # particle (up, off)
        'SYM': None,  # symbol (+,%, &)
        'TO': None,  # “to” (to)
        'UH': None,  # interjection (ah, oops)
        'VB': wn.VERB,  # verb base form (eat)
        'VBD': wn.VERB,  # verb past tense (ate)
        'VBG': wn.VERB,  # verb gerund (eating)
        'VBN': wn.VERB,  # verb past participle (eaten)
        'VBP': wn.VERB,  # verb non-3sg pres (eat)
        'VBZ': wn.VERB,  # verb 3sg pres (eats)
        'WDT': None,  # wh-determiner (which, that)
        'WP': None,  # wh-pronoun (what, who)
        'WP$': None,  # possessive (wh- whose)
        'WRB': None,  # wh-adverb (how, where)
        '$': None,  # dollar sign ($)
        '#': None,  # pound sign (#)
        '“': None,  # left quote (‘ or “)
        '”': None,  # right quote (’ or ”)
        '(': None,  # left parenthesis ([, (, {, <)
        ')': None,  # right parenthesis (], ), }, >)
        ',': None,  # comma (,)
        '.': None,  # sentence-final punc (. ! ?)
        ':': None  # mid-sentence punc (: ; ... – -)
    }


def tokenize_and_tag(filepath):
    """Load the book's text, tokenize and tag in memory."""
    with open(filepath+'.txt', 'r') as f:
        book = f.read()
    return pos_tag(word_tokenize(book))


def pickle_tokens(tokens, filepath):
    """Pickle the tokens to a file."""
    with open(filepath+'_tokens.pickle', 'wb') as f:
        pickle.dump(tokens, f)
    return


def unpickle_tokens(filepath):
    """Unpickle the tokens into memory."""
    try:
        with open(filepath+'_tokens.pickle', 'rb') as f:
            tokens = pickle.load(f)
    except FileNotFoundError:
        tokens = tokenize_and_tag(filepath)
        pickle_tokens(tokens, filepath)
    return tokens


def lemmatize(tokens):
    """Lemmatize the tokens in memory."""
    lemmas = []
    wnl = WordNetLemmatizer()
    for word, tag in tokens:
        if tag.startswith('NN') or tag.startswith('CD'):
            lemmas.append((wnl.lemmatize(word, pos=wn.NOUN), 'NN'))
        elif tag.startswith('EX') or tag.startswith('IN'):
            lemmas.append((wnl.lemmatize(word, pos=wn.ADV), 'RB'))
        elif tag.startswith('RB'):
            lemmas.append((wnl.lemmatize(word, pos=wn.ADV), 'RB'))
        elif tag.startswith('JJ'):
            lemmas.append((wnl.lemmatize(word, pos=wn.ADJ), 'JJ'))
        elif tag.startswith('PD') or tag.startswith('RP'):
            lemmas.append((wnl.lemmatize(word, pos=wn.ADJ), 'JJ'))
        elif tag.startswith('VB'):
            lemmas.append((wnl.lemmatize(word, pos=wn.VERB), 'VB'))
    return lemmas


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


def frequent_nouns_and_adjectives(tokens):
    """Print out 5 most frequence nouns, adjectives, and pairs."""
    DEPTH = 10

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
          + frequent_nouns[1][0] + "':")
    print(adjectives_before(tokens, frequent_nouns[0][0]).most_common(5))
    return


# main loop
if __name__ == "__main__":
    try:
        tokens = unpickle_tokens('Texts/NonFreeTexts/InfiniteJest')
    except FileNotFoundError:
        tokens = unpickle_tokens('Texts/FreeTexts/Hamlet')

    lemmas = lemmatize(tokens)

    frequent_nouns_and_adjectives(tokens)
    frequent_nouns_and_adjectives(lemmas)
