import string
from underthesea import word_tokenize, ner, sent_tokenize, word_tokenize
from collections import defaultdict

VIETNAMESE_STOPWORDS = set(open('resources\\vietnamese-stopwords.txt', mode='r', encoding='utf8').read().split('\n'))
PUNCTUATION_CHARACTERS = set([char for char in string.punctuation])
EXCLUSIVE = set.union(VIETNAMESE_STOPWORDS, PUNCTUATION_CHARACTERS)

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def tokenize(text):
    sents = sent_tokenize(text)
    sents = [word_tokenize(s,format = 'text') for s in sents]
    return sents

def get_entities(seq):
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
    chunks = get_entities(tags)
    res = defaultdict(list)
    for chunk_type, chunk_start, chunk_end in chunks:
        res[chunk_type].append(' '.join(words[chunk_start: chunk_end]))
    return res

def ner_extraction(text):
    res = ner(text)
    words = [r[0] for r in res]
    tags = [t[3] for t in res]
    
    return get_chunks(words,tags)

def generateBigram(words):
    bigrams = [words[i] + '_' + words[i+1] for i in range(0,len(words) - 1)]
    return bigrams

def extractKeywords(sentence):
    filtered_sw = ' '.join([word for word in sentence.split() if word not in EXCLUSIVE])    
    return word_tokenize(filtered_sw)

def filterSentence(sentence):    
    return ' '.join([word for word in sentence.split() if word not in PUNCTUATION_CHARACTERS])    

def isMiscSentence(sent):
    if len(sent.split()) <= 3 or len(sent.split()) > 100:
        return True
    
    if len(sent) <= 30:
        return True
    
    if all(ord(c) < 128 for c in sent):
        return True
    
    if not any(c.isalpha() for c in sent):
        return True