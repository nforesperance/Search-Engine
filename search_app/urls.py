
from django.urls import path
from .views import index
from django.conf.urls import url

urlpatterns = [
    path('', index , name = "search"),
]
