from googleapiclient.discovery import build
from numpy import random
import requests
from bs4 import BeautifulSoup
import timeout_decorator
from underthesea import sent_tokenize
from multiprocessing import Pool
import re
import sys

API_KEY = ['AIzaSyBh7Kw9G3CH12L3KNe7d4eHkLfW9TJ8Yt0']
SEARCH_ENGINE_ID = "7dc162fa0b147c47c"

class GoogleSearch():
    __instance = None
    
    def __init__(self):        
        if GoogleSearch.__instance != None:
            return GoogleSearch.__instance
        else:            
            GoogleSearch.__instance = self

    def __googleSearch(self, query):
        page = 1
        start = (page - 1) * 10 + 1
        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY[0]}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"
        data = requests.get(url, timeout=4).json()

        return data

    def __extractResult(self, result):
        items = []
        searched_items = result.get("items")        
        for i, search_item in enumerate(searched_items, start=1):            
            items.append({
                'title': search_item.get("title"),
                'link': search_item.get("link")                
            })

        return items

    def __chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def __getContent(self, url):
        try:
            html = requests.get(url, timeout=4)
            tree = BeautifulSoup(html.text,'lxml')
            for invisible_elem in tree.find_all(['script', 'style']):
                invisible_elem.extract()

            paragraphs = [p.get_text() for p in tree.find_all("p")]

            for para in tree.find_all('p'):
                para.extract()

            for href in tree.find_all(['a','strong']):
                href.unwrap()

            tree = BeautifulSoup(str(tree.html),'lxml')

            text = tree.get_text(separator='\n\n')
            text = re.sub('\n +\n','\n\n',text)

            paragraphs += text.split('\n\n')
            paragraphs = [re.sub(' +',' ',p.strip()) for p in paragraphs]
            paragraphs = [p for p in paragraphs if len(p.split()) > 10]

            for i in range(0,len(paragraphs)):
                sents = []
                text_chunks = list(self.__chunks(paragraphs[i],100000))
                for chunk in text_chunks:
                    sents += sent_tokenize(chunk)

                sents = [s for s in sents if len(s) > 2]
                sents = ' . '.join(sents)
                paragraphs[i] = sents

            return paragraphs
        except:
            return ''
    
    def search(self, query):
        result = [            
            # {
            #    title: the title of the site            
            #    link: url of the site
            #    content: the content (paragraphs, texts) in the site
            # }           
        ]        
        searchResult = self.__googleSearch(query)
        extractedResult = self.__extractResult(searchResult)

        for topic in extractedResult:
            title = topic['title']
            link = topic['link']
            content = self.__getContent(topic['link'])

            result.append({
                'title': title,
                'link': link,
                'content': [d for d in content if len(d) > 20]
            })            

        return result