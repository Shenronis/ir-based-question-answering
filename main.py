from question_answering import IRQuestionAnswering
from utils.functions import *

if __name__ == "__main__":    
    questionAnswering = IRQuestionAnswering()

    query = 'người giàu nhất thế giới hiện nay 2022'
    answer_type = "PER"

    data = questionAnswering.search(query, answer_type)

    candidates = [p['ner'] for p in data]
    candidates = list(set([j for i in candidates for j in i]))
    candidates = [(c,0) for c in candidates]
    candidates = dict(candidates)
    for p in data:
        for ner in p['ner']:
            candidates[ner] += p['score']
    candidates = candidates.items()
    candidates = sorted(candidates, key = lambda x: x[1],reverse = True)
    candidates = candidates[:10]
    total_score = float(sum([c[1] for c in candidates[:5]]))
    for c in candidates:
        print(c[0], round((c[1] / total_score) * 100,2), "%")