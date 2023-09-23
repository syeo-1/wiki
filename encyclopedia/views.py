from django.shortcuts import render
from django.http import HttpResponse
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki_entry(request, wiki_entry):
    try:
        markdown_file_path = f'entries/{wiki_entry}.md'
        html_from_markdown = markdown2.markdown_path(markdown_file_path)
        return HttpResponse(html_from_markdown)
    except FileNotFoundError as e:
        return HttpResponse('<p>markdown file not found</p>')
    

