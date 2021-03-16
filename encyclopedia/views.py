from django.shortcuts import render
from markdown2 import Markdown
from random import randint

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    

def entry(request, entry):

    markdowner = Markdown()
    page = util.get_entry(entry)
    if page is None:
        return render(request, "encyclopedia/error.html", {
            "name": entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": entry,
            "content": markdowner.convert(page)
        })

def random(request):
    markdowner = Markdown()
    entries = util.list_entries()
    random_page = entries[randint(0, len(entries) - 1)]
    random_page = util.get_entry(random_page)
    return render(request, "encyclopedia/entry.html", {
        "title": "random_page",
        "content": markdowner.convert(random_page)
    })        

