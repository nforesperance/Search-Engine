from django.shortcuts import render

from .search import google_search , load_best_platforms

from search_engine.settings import API_KEY, ENGINE_ID
from django.http import JsonResponse
import json

from .form import SearchForm

# Create your views here.


def index2(request):
    form = SearchForm(request.POST or None)
    if form.is_valid():
        page = form.cleaned_data.get('page')
        page = int(page)
        query = form.cleaned_data.get("query")
        if page > 0:
            result = google_search(
                query, API_KEY, ENGINE_ID, start=int(page)*10)
        else:
            result = google_search(query, API_KEY, ENGINE_ID)
        return render(request, template_name='search_app/index.html', context={'result': result, 'form': form})
    else:
        return render(request=request, template_name="search_app/index.html", context={'form': form})


def index(request):
    total_page = range(1 , 11)
    form = SearchForm(request.GET or None)
    page = request.GET.get('page' , None)
    if form.data == {} :
        platforms = load_best_platforms()
        return render(request, template_name='search_app/search.html', context={'form': form , "platforms" : platforms})
    try:
        page = int(page)
    except:
        page = 0
    query = request.GET.get("query")
    if not query:
        return render(request, template_name='search_app/result2.html', context={"total": total_page, 'result': [], 'form': form , "query" : query})
    if page > 0:
        result = google_search(query, API_KEY, ENGINE_ID, start=int(page)*10)
    else:
        result = google_search(query, API_KEY, ENGINE_ID)
    return render(request, template_name='search_app/result2.html', context={"total": total_page, 'result': result, 'form': form , "query" : query})


