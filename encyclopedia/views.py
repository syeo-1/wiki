from django.shortcuts import render
from django.http import HttpResponse
import markdown2
from django import forms

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label='Page Title')
    entry = forms.CharField(label='Entry Markdown', widget=forms.Textarea)

def get_entry_html(entry_markdown, entry):
    markdown_to_html = markdown2.markdown(entry_markdown)
    return HttpResponse(f'<title>{entry}</title>'+markdown_to_html)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def wiki_entry(request, wiki_entry):
    markdown_page = util.get_entry(wiki_entry)
    if markdown_page == None:
        return render(request, 'encyclopedia/error.html')
    else:
        return get_entry_html(markdown_page, wiki_entry)

def search(request):

    query_string = request.GET.get('q')
    available_entries = [entry.lower() for entry in util.list_entries()]

    # check for an exact match for the query string in available entries
    if query_string in available_entries:
        entry_to_render = util.list_entries()[available_entries.index(query_string)]
        markdown_page = util.get_entry(entry_to_render)
        return get_entry_html(markdown_page, entry_to_render)


    # get all entries in which query_string is a substring if no exact match found. returned list may be empty
    filtered_entries = [entry for entry in util.list_entries() if query_string.lower() in entry.lower()]
    return render(request, 'encyclopedia/search_results.html', {
        "entries": filtered_entries
    })

def new_entry(request):
    return render(request, 'encyclopedia/new_page.html', {
        'form': NewEntryForm()
    })
    

