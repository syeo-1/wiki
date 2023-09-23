from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('<str:wiki_entry>', views.wiki_entry, name='wiki_entry')
]
