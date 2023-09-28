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
    markdown_page = util.get_entry(wiki_entry)
    if markdown_page == None:
        return render(request, 'encyclopedia/error.html')
    else:
        print('test')
        # return HttpResponse(get_entry_html(markdown_page, wiki_entry))
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
        # return HttpResponse(get_entry_html(markdown_page, entry_to_render))
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
    # on submission what should happen?
    # it should go to the add endpoint? and then call some function to generate html for the given markdown contents provided
    # then it should return the html for the markdown
    
    # at the same time, it should generate a new markdown file within the entries directory

    # upon saving the created markdown file to the entries directory, it should then bring the user to their newly created page!

    ####
    # for now, try to make sure when a title and entry are given, they are printed to console
    # on submission, the user will just be brought back to the home page
    if request.method == 'GET':
        return render(request, 'encyclopedia/new_page.html', {
            'form': NewEntryForm()
        })
    elif request.method == 'POST':
        user_title = request.POST.get('new_title')
        user_entry = request.POST.get('new_markdown_entry')

        # create the markdown file in the entries directory if it doesn't exist
        if not os.path.exists(f'entries/{user_title}.md'):
            user_entry = user_entry.replace('\r\n\r\n', '\r\n') # remove double newline that somehow gets added in
            file = open(f'entries/{user_title}.md', 'w+')
            file.write(user_entry)
        else:
            print('file already exists!')
            return render(request, 'encyclopedia/new_page.html', {
                'form': NewEntryForm()
            })

        markdown = util.get_entry(user_title)
        return HttpResponse(get_entry_html(markdown, user_title))
        

