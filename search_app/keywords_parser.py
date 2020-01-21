import requests
import codecs
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import collections
import spacy

language = "french"
#url = 'https://www.troyhunt.com/the-773-million-record-collection-1-data-reach/'
url = "https://openclassrooms.com/fr/courses/4668271-developpez-des-applications-web-avec-angular/5087065-structurez-avec-les-components"
search = "Collection"


def frequency(arr):
    return collections.Counter(arr)


def extract_text_from_url(url , remove_blank = True):
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
        'code'
    ]

    for t in document:
        if t.parent.name not in blacklist:
            text += '{} '.format(t)
    # removing duplicated spaces and puntctiontions
    if(remove_blank):
        text = remove_spaces(text)
    # unfortunate this quotes resisted
    text = text.replace('"', '')
    text = text.replace(' "', '')

    return text

def remove_spaces(text):
    text = " ".join(text.split())
    text = text.translate(str.maketrans('', '', string.punctuation))

    return text

def convert_verb_to_infinitif(text):
    steler = spacy.load("fr_core_news_md")
    word = steler(text)
    return word

def extract_stop_words(text):
    stop_words = set(stopwords.words(language)) 
  
    word_tokens = word_tokenize(text) 
    
    filtered_sentence = [w for w in word_tokens if not w in stop_words] 

    return filtered_sentence

def main():
    text = extract_text_from_url(url)
    conjugated_text = convert_verb_to_infinitif(text)
    words = extract_stop_words(conjugated_text)
    return words
    #return conjugated_text

def get_domains_url(full_domain_name):
    api = "https://api.hackertarget.com/pagelinks/?q={}"
    res = requests.get(api.format(full_domain_name))
    text = res.content
    #print(text)
    return text.decode()