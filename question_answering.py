import requests
import re
import sys
from difflib import SequenceMatcher
from bs4 import BeautifulSoup
from underthesea import sent_tokenize
from utils.functions import *

API_KEY = ['AIzaSyBh7Kw9G3CH12L3KNe7d4eHkLfW9TJ8Yt0']
SEARCH_ENGINE_ID = "7dc162fa0b147c47c"

class IRQuestionAnswering():
    __instance = None
    
    def __init__(self):        
        if IRQuestionAnswering.__instance != None:
            return IRQuestionAnswering.__instance
        else:            
            IRQuestionAnswering.__instance = self

    def __googleSearch(self, query):
        print('Google Search...')

        page = 1
        start = (page - 1) * 10 + 1
        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY[0]}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"
        data = requests.get(url, timeout=4).json()

        return data

    def __extractResult(self, result):
        print("Extracting Result...")


        items = []
        searched_items = result.get("items")        
        for i, search_item in enumerate(searched_items, start=1):            
            items.append({
                'title': search_item.get("title"),
                'link': search_item.get("link")                
            })

        return items

    def __passageRetrievial(self, url):
        print('Passage Retrievial...')


        try:
            content = []

            html = requests.get(url, timeout=4)
            tree = BeautifulSoup(html.text,'lxml')
            for invisible_elem in tree.find_all(['script', 'style']):
                invisible_elem.extract()            

            content = []
            text_chunks = list(chunks(tree.get_text(),100000))
            for text in text_chunks:
                content += tokenize(text)           
            return content
        except:
            return ''
    
    def __processPassage(self, passages, topic_index):
        print('Process Passage...')


        res = []
        for sent in passages:
            sent = sent.strip()                
            sent = sent.replace("\n", "")            
            sent = filterSentence(sent)
            if not isMiscSentence(sent):
                sent_keywords = extractKeywords(sent)
                keyword_occurences = len(set(sent_keywords) & set(self.keywords))
                if keyword_occurences > 0:
                    ner = list(set(ner_extraction(sent)[self.answer_type]))
                    if len(ner) > 0:
                        res.append({
                            'sentence': sent,
                            'keyword': keyword_occurences,
                            'ner': ner,
                            'rank': topic_index
                        })
        return res

    def __filterByKeywordOccurence(self, passages_dict):
        print('Filtering...')


        max_keyword = 0
        min_num_passages = 20
        for p in passages_dict:
            if p['keyword'] > max_keyword:
                max_keyword = p['keyword']
        print("Filtering... maxKW = " + str(max_keyword))

        while (True):
            if (max_keyword == 0): break

            num_candidate_passages = 0
            for p in passages_dict:
                if p['keyword'] >= max_keyword:
                    num_candidate_passages += 1
            if (num_candidate_passages >= min_num_passages or max_keyword == 1):
                break
            else:
                max_keyword -=1        

        return [p for p in passages_dict if p['keyword'] >= max_keyword]

    def __rankPassages(self, passages_dict):
        print('Ranking...')


        for passage in passages_dict:
            score = 3
            score -= passage['rank']
            score -= len(passage['ner'])
            score += passage['keyword']
            score -= int(len(passage['sentence'].split()) / 50.0)

            token_query = tokenize(self.query)[0]
            x = token_query.lower().split()
            y = passage['sentence'].lower().split()
            s = SequenceMatcher(None, x, y)
            score += s.find_longest_match(0, len(x), 0, len(y)).size
            bigram_q = generateBigram(x)
            bigram_p = generateBigram(y)
            score += len(set(bigram_q) & set(bigram_p))
            passage['score'] = score

        return passages_dict

    def search(self, query, answer_type):        
        self.query = query        
        self.answer_type = answer_type
        self.keywords = extractKeywords(query)
        searchResult = self.__googleSearch(query)
        extractedResult = self.__extractResult(searchResult)
        
        result = []

        for topic_index, topic in enumerate(extractedResult):
            title = topic['title']
            link = topic['link']
            passages = self.__passageRetrievial(link)
            processed_passages = self.__filterByKeywordOccurence( self.__processPassage(passages, topic_index) )
            result += self.__rankPassages(processed_passages)             

        return result