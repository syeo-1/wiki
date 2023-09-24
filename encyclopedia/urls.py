from django.urls import path

from . import views

# order of the urls actually matters!!!
# if str:wiki_entry is before search, since search is a string and str:wiki_entry looks for
# any string, then it'll immediately just go for the wiki_entry view!!!!
urlpatterns = [
    path("", views.index, name="index"),
    path('search', views.search, name='search'),
    path('<str:wiki_entry>', views.wiki_entry, name='wiki_entry')
]
