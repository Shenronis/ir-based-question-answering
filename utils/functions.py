import string
from underthesea import word_tokenize, ner, sent_tokenize, word_tokenize
from collections import defaultdict

VIETNAMESE_STOPWORDS = set(open('resources\\vietnamese-stopwords.txt', mode='r', encoding='utf8').read().split('\n'))
PUNCTUATION_CHARACTERS = set([char for char in string.punctuation])
EXCLUSIVE = set.union(VIETNAMESE_STOPWORDS, PUNCTUATION_CHARACTERS)

def chunks(l, n):
    """
        Split big list into smaller lists (chunk == smol piece)
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]

def tokenize(text):
    """
        Sentence tokenizing with words tokenized
    """
    sents = sent_tokenize(text)
    sents = [word_tokenize(s,format = 'text') for s in sents]
    return sents

def get_entities(seq):
    """
        Get chunks that have prefixes from B- to I-
    """
    i = 0
    chunks = []
    seq = seq + ['O']  # add sentinel
    types = [tag.split('-')[-1] for tag in seq]
    while i < len(seq):
        if seq[i].startswith('B'):
            for j in range(i+1, len(seq)):
                if seq[j].startswith('I') and types[j] == types[i]:
                    continue
                break
            chunks.append((types[i], i, j))
            i = j
        else:
            i += 1
    return chunks

def get_chunks(words, tags):
    """
        Return dict of chunk_type
    """
    chunks = get_entities(tags)
    res = defaultdict(list)
    for chunk_type, chunk_start, chunk_end in chunks:
        res[chunk_type].append(' '.join(words[chunk_start: chunk_end]))
    return res

def ner_extraction(text):
    """
        Get NER using underthesea.ner()
        from underthesea import ner
        text = 'Chưa tiết lộ lịch trình tới Việt Nam của Tổng thống Mỹ Donald Trump'
        ner(text)
        >>  [('Chưa', 'R', 'O', 'O'),
            ('tiết lộ', 'V', 'B-VP', 'O'),
            ('lịch trình', 'V', 'B-VP', 'O'),
            ('tới', 'E', 'B-PP', 'O'),
            ('Việt Nam', 'Np', 'B-NP', 'B-LOC'),
            ('của', 'E', 'B-PP', 'O'),
            ('Tổng thống', 'N', 'B-NP', 'O'),
            ('Mỹ', 'Np', 'B-NP', 'B-LOC'),
            ('Donald', 'Np', 'B-NP', 'B-PER'),
            ('Trump', 'Np', 'B-NP', 'I-PER')]

        To extract NER type like
            -PER
            -LOC
            -ORG

        and Inside–outside–beginning (tagging)
            - prefix I - inside of chunk
            - prefix B  - begining of chunk
            - an O - does not belong to any chunk
    """
    res = ner(text)
    words = [r[0] for r in res]
    tags = [t[3] for t in res]
    
    return get_chunks(words,tags)

def generateBigram(words):
    """
        Return bigram from word tokens (sentence)
    """
    bigrams = [words[i] + '_' + words[i+1] for i in range(0,len(words) - 1)]
    return bigrams

def extractKeywords(sentence):
    """
        Remove stopwords, punctuations
    """
    filtered_sw = ' '.join([word for word in sentence.split() if word not in EXCLUSIVE])    
    return word_tokenize(filtered_sw)

def filterSentence(sentence):    
    """
        Remove only punctuations
    """
    return ' '.join([word for word in sentence.split() if word not in PUNCTUATION_CHARACTERS])    

def isMiscSentence(sent):
    """
        Check if sentence is noisy (not worth retrieving - contains no valuable information)
    """

    # Too less or too much line/ newline
    if len(sent.split()) <= 3 or len(sent.split()) > 100:
        return True
    
    # Too short
    if len(sent) <= 30:
        return True

    # Contains character outside 128
    if all(ord(c) < 128 for c in sent):
        return True
    
    # Don't contain any letter
    if not any(c.isalpha() for c in sent):
        return True