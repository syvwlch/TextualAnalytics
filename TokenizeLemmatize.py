"""
Pre-process corpus using nltk.

Will unpickle the tokens and or lemmas for the text if they've already been
pickled, and generate and pickle them if not.
"""

import pickle
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


# main loop
if __name__ == "__main__":
    try:
        tokens = unpickle_tokens('Texts/NonFreeTexts/InfiniteJest')
    except FileNotFoundError:
        tokens = unpickle_tokens('Texts/FreeTexts/Hamlet')

    print('Number of tokens: ' + str(len(tokens)))
