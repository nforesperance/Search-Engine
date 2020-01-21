from googleapiclient.discovery import build
import json
from search_engine.settings import BASE_DIR
import os
from .filter import *
import concurrent.futures
import urllib.request


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
    # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # # Start the load operations and mark each future with its URL
        # future_to_url = {executor.submit(load_url, item): item for item in items}
        # for future in concurrent.futures.as_completed(future_to_url):
        #     url = future_to_url[future]
        #     try:
        #         data = future.result()
        #     except Exception as exc:
        #         print('%r generated an exception: %s' % (url, exc))
        #     else:
        #         extrait = data.getPrincipalSection(query)
        #         structured_items.append({'link': data.url,
        #                             'htmlTitle': data.item['htmlTitle'],
        #                             'displayLink': data.item['displayLink'],
        #                             'htmlSnippet': extrait,
        #                             })

    for item in items:
        scraping_unit = ScrapingProcessorUnit(item=item, imediatly_fectch=True)
        extrait = scraping_unit.getPrincipalSection(query)
        print((extrait.split("\n")[0])[3:])
        if extrait:
            structured_items.append({'link': scraping_unit.url,
                                    'htmlTitle': scraping_unit.item['htmlTitle'],
                                    'displayLink': scraping_unit.item['displayLink'],
                                    'htmlSnippet': extrait,
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
