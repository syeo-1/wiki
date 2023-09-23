from django.shortcuts import render
from django.http import HttpResponse
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki_entry(request, wiki_entry):
    markdown_page = util.get_entry(wiki_entry)
    if markdown_page == None:
        return render(request, 'encyclopedia/error.html')
    else:
        markdown_to_html = markdown2.markdown(markdown_page)
        return HttpResponse(markdown_to_html)

