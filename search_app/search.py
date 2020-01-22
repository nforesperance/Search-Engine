from googleapiclient.discovery import build
import json
from search_engine.settings import BASE_DIR
import os
from .filter import *
import concurrent.futures
import urllib.request
from multiprocessing import Pool

# new stuffs
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import nltk
from nltk.tokenize import RegexpTokenizer 
import matplotlib.pyplot as plt
import json
from nltk.stem.snowball import FrenchStemmer
import collections
import spacy
from sklearn.utils import shuffle
import pickle


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return more_structured_items([res['items'][0], res['items'][1]], query=search_term)
    # return more_structured_items(res['items'], query=search_term)

def load_url(item):
    return ScrapingProcessorUnit(item=item, imediatly_fectch=True)


def more_structured_items(items, query):
# We can use a with statement to ensure threads are cleaned up promptly
    structured_items = []
    

    for item in items:
        scraping_unit = ScrapingProcessorUnit(item=item, imediatly_fectch=True)
        extrait = scraping_unit.getPrincipalSection(query)
        if extrait:
            heading = (extrait.split("\n")[0])[3:65]
            structured_items.append({'link': scraping_unit.url,
                                    'htmlTitle': scraping_unit.item['htmlTitle'],
                                    'displayLink': scraping_unit.item['displayLink'],
                                    'htmlSnippet': extrait[10:],
                                    'heading':heading,
                                    })
        else:
            structured_items.append({'link': scraping_unit.url,
                                    'htmlTitle': scraping_unit.item['htmlTitle'],
                                    'displayLink': scraping_unit.item['displayLink'],
                                    'htmlSnippet': scraping_unit.item['htmlSnippet'],
                                    })

    return structured_items



def load_best_platforms():

    with open(os.path.join(BASE_DIR, 'best_platform.json')) as json_file:
        data = json.load(json_file)
    return data

def google_search1(pool,search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    rep = res['items']
    # rep = [res['items'][0],res['items'][1]]
    results = [pool.apply(fetch, args=(item,search_term)) for item in rep]
    return results
    # return more_structured_items([res['items'][0], res['items'][1]], query=search_term)
    # return more_structured_items(res['items'], query=search_term)    

def fetch(item,query):
    if getData(item['link'])==1:
        scraping_unit = ScrapingProcessorUnit(item=item, imediatly_fectch=True)
        extrait = scraping_unit.getPrincipalSection(query)
        if extrait:
            heading = (extrait.split("\n")[0])[3:65]
            result ={'link': scraping_unit.url,
                    'htmlTitle': scraping_unit.item['htmlTitle'],
                    'displayLink': scraping_unit.item['displayLink'],
                    'htmlSnippet': extrait,
                    'heading':heading,
                    }
        else:
            heading = (scraping_unit.item['htmlSnippet'][:60]).replace("<b>", "")
            heading = heading.replace("</b>","")
            result ={'link': scraping_unit.url,
                    'htmlTitle': scraping_unit.item['htmlTitle'],
                    'displayLink': scraping_unit.item['displayLink'],
                    'htmlSnippet': scraping_unit.item['htmlSnippet'],
                    'heading':heading,
                    }
        # print(result)
        return result
    else:
        return ""







# filtering functions
tokenizer = RegexpTokenizer('\w+')
freq_totale = nltk.Counter()
stemmer = FrenchStemmer()
with open('stopwords-fr.json', encoding='utf-8') as json_file:
    sw = set(json.load(json_file))

KEYWORDS = []

g = open('keywords.txt', 'r', encoding="utf-8")
for y in g:
    KEYWORDS.append(stemmer.stem(y.rstrip("\n\r")))
KEYWORDS = set(KEYWORDS)

def convert_verb_to_infinitif(text):
    return stemmer(text)

def format_text(text):
    # removing duplicated spaces and punctuations
    text = " ".join(text.split())
    text ="".join([i for i in text if not i.isdigit()])
    punct = '!"#$%&\()*+,-./:;’<=>?@[\\]^_`«{|}~»—'
    text = text.translate(str.maketrans('', '', punct))
    # unfortunate this quotes resisted
    text = text.replace('"', '')
    text = text.replace("'", "' ")
    
    #get the tokens
    tokens = tokenizer.tokenize(text)
    
    #lowercase all tokens
    words = []
    for word in tokens:
        words.append(word.lower())
    return words

def scrapText(url):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    document = soup.find_all(text=True)
    text = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
        'style',
        'img',
        'video',
        'code',
        'span',
        'li',
    ]

    for t in document:
        if t.parent.name not in blacklist:
            text += '{} '.format(t)
    # removing duplicated spaces and punctuations
    text = " ".join(text.split())
    text ="".join([i for i in text if not i.isdigit()])
    punct = '!"#$%&\()*+,-./:;’<=>?@[\\]^_`«{|}~»—'
    text = text.translate(str.maketrans('', '', punct))
    # unfortunate this quotes resisted
    text = text.replace('"', '')
    text = text.replace("'", "' ")
    
    #get the tokens
    tokens = tokenizer.tokenize(text)
    
    #lowercase all tokens
    words = []
    for word in tokens:
        words.append(word.lower())
    return words

def normalizeVector(words):
    filtered_words = []
    for word in words:
        if word not in sw:
            filtered_words.append(word) 
    resulti = [x for x in filtered_words if not(x.isdigit() or x[0].isdigit() or (x[0] == '-' and x[1:].isdigit()))]
    return resulti

def stemming(words):
    stemmed_words = [stemmer.stem(word) for word in words]
    return stemmed_words

def clean_text(words):
    resulto = normalizeVector(words)
    resultis = stemming(resulto)
    return resultis

def is_keyword(el):
    return el in KEYWORDS

def format_url_site(url):
    resultat = scrapText(url)
    resultats = clean_text(resultat)
    return collections.Counter(resultats)
def getData(url):
    vector = format_url_site(url)
    dictio = dict(vector)
    good_dictio = {}
    for keys in KEYWORDS:
        if keys in dictio:
            good_dictio[keys]= dictio[keys]
        else:
            good_dictio[keys]= 0
    vector_data = list(good_dictio.values())
    f = open('my_classifier.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()
    response = classifier.predict(np.array([vector_data]))
    return response[0]
