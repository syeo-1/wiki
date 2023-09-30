from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import markdown2
from django.urls import reverse
from django import forms
import os

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label='Page Title')
    entry = forms.CharField(label='Entry Markdown', widget=forms.Textarea)

def get_entry_html(entry_markdown, entry):
    markdown_to_html = markdown2.markdown(entry_markdown)
    return f'<title>{entry}</title>'+markdown_to_html

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def wiki_entry(request, wiki_entry):
    print('aweofihawe')
    markdown_page = util.get_entry(wiki_entry)
    if markdown_page == None:
        return render(request, 'encyclopedia/error.html')
    else:
        print('test')
        print(repr(markdown_page))
        return render(request, 'encyclopedia/entry.html', {
            'entry_title': wiki_entry,
            'entry_html': get_entry_html(markdown_page, wiki_entry)
        })

def search(request):

    query_string = request.GET.get('q').lower()
    available_entries = [entry.lower() for entry in util.list_entries()]

    # check for an exact match for the query string in available entries
    print(query_string)
    print(available_entries)
    if query_string in available_entries:
        print('test')
        entry_to_render = util.list_entries()[available_entries.index(query_string)]
        markdown_page = util.get_entry(entry_to_render)
        return render(request, 'encyclopedia/entry.html', {
            'entry_title': entry_to_render,
            'entry_html': get_entry_html(markdown_page, entry_to_render)
        })


    # get all entries in which query_string is a substring if no exact match found. returned list may be empty
    filtered_entries = [entry for entry in util.list_entries() if query_string.lower() in entry.lower()]
    return render(request, 'encyclopedia/search_results.html', {
        "entries": filtered_entries
    })

def new_entry(request):
    if request.method == 'GET':
        return render(request, 'encyclopedia/new_page.html', {
            'form': NewEntryForm()
        })
    elif request.method == 'POST':
        user_title = request.POST.get('new_title')
        user_entry = request.POST.get('new_markdown_entry')

        # create the markdown file in the entries directory if it doesn't exist
        util.save_entry(user_title, user_entry)

        return render(request, 'encyclopedia/entry.html', {
            'entry_title': wiki_entry,
            'entry_html': get_entry_html(user_entry, wiki_entry)
        })

def edit_entry(request, wiki_entry):
    # retrieve the entry that the user wants to edit
    entry_markdown = util.get_entry(wiki_entry)

    # render the form with the contents

    # create it so it's like the new entry thing except that the title doesn't change
        
    return render(request, "encyclopedia/edit.html", {
        'title': wiki_entry,
        'entry': entry_markdown
    })

