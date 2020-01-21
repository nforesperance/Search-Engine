from googleapiclient.discovery import build
import json
from search_engine.settings import BASE_DIR
import os
from .filter import *
import concurrent.futures
import urllib.request
from multiprocessing import Pool


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
    results = [pool.apply(fetch, args=(item,search_term)) for item in rep]
    return results
    # return more_structured_items([res['items'][0], res['items'][1]], query=search_term)
    # return more_structured_items(res['items'], query=search_term)    

def fetch(item,query):
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
        result ={'link': scraping_unit.url,
                'htmlTitle': scraping_unit.item['htmlTitle'],
                'displayLink': scraping_unit.item['displayLink'],
                'htmlSnippet': scraping_unit.item['htmlSnippet'],
                }
    print(result)
    return result
