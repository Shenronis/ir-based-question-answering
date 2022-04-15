from question_answering import IRQuestionAnswering
from utils.functions import *

def showResult(data):
    """
        Show possible results from IR-QA system
        The one with highest percentage% is the most possible answer
    """

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

if __name__ == "__main__":    
    questionAnswering = IRQuestionAnswering()

    # Inputs    
    # ANS_TYPE = [
    #   "PER",  - Person answer tag
    #   "LOC",  - Location answer tag
    #   "ORG"   - Organization answer tag
    # ]
    query = 'người giàu nhất thế giới hiện nay 2022'
    answer_type = "PER"

    data = questionAnswering.search(query, answer_type)    

    print("\n\n")
    showResult(data)