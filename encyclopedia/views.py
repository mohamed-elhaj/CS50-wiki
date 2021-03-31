from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
from random import randint
from django import forms
from . import util
import re

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control col-md-6 col-lg-8', 'style': 'margin: 5px'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 3, 'style': 'height: 300px; resize: none'}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)
    


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    

def entry(request, entry):

    markdowner = Markdown()
    page = util.get_entry(entry)
    if page is None:
        return render(request, "encyclopedia/error.html", {
            "error_type": "Error 404",
            "error_content": "Page not found!"
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
    page = util.get_entry(random_page)
    return render(request, "encyclopedia/entry.html", {
        "title": random_page,
        "content": markdowner.convert(page)
    })        

def edit(request, entry):
    page = util.get_entry(entry)
    if not page:
        return render(request, "encyclopedia/error.html", {
            "error_type": "",
            "error_content": "Page Not Found!"
        }) 
    else:
        form = NewPageForm()
        form.fields["title"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
        # Dsipaly the content of the page
        form.fields["content"].initial = page 
        # Set "edit" = True to pass "new" function's condition
        form.fields["edit"].initial = True
        # Let "new" function deals with the logic
        return render(request, "encyclopedia/new_page.html", {
            "form": form,
            "entry": entry
        })





def new(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # if the page is not existed and (edit is not required)
            if title.upper() in util.list_entries() and form.cleaned_data["edit"] == False:
                return render(request, "encyclopedia/error.html", {
                    "error_type": "",
                    "error_content": title.capitalize() + " is already exsisted!"
                })
                # if the page is not existed or edit is required 
            else:                
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
        else:
            return render(request, "encyclopedia/new_page.html", {
                "form": form,
                "edit": True
            })            
        
    else:        
        return render(request, "encyclopedia/new_page.html", {
            "form": NewPageForm()
        })

def search(request):
    page = request.GET.get('q')
    # Check for a perfect match
    if page.upper() in util.list_entries():
        return HttpResponseRedirect(reverse("entry", kwargs={"entry": page}))
    # if there is no perfect match        
    else:
        results = []
        for entry in util.list_entries():
            if page.upper() in entry:
                results.append(entry)
        if len(results) > 0:                
            return render(request, "encyclopedia/search.html", {
                "results": results
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })            
    

