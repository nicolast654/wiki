from random import choice

from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown

from . import util

markdown = Markdown()

class NewEntryForm(forms.Form):
	title = forms.CharField(label="New Entry")
	content = forms.CharField(widget=forms.Textarea)

class EditEntryForm(forms.Form):
    title = forms.CharField(label="Edit Entry")
    content = forms.CharField(widget=forms.Textarea)



def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if util.get_entry(title) is None:
                util.save_entry(title, content)

                return HttpResponseRedirect(title)

            else:
                return render(request, "encyclopedia/errornew.html", {"title": title})

    else:
        return render(request, "encyclopedia/new.html", {"form": NewEntryForm()})

def entry(request, entry):
    taken_entry = util.get_entry(entry)

    if taken_entry is not None:
        return render(request,"encyclopedia/entry.html",{"entry": markdown.convert(taken_entry), "name": entry})   
    else:
        return render(request, "encyclopedia/error.html", {"entry":entry})  

def random_pick(request):
    entries_list = util.list_entries()
    random_entry = choice(entries_list)
    entry_content = util.get_entry(random_entry)

    return render(request,"encyclopedia/entry.html",{"entry": markdown.convert(entry_content), "name": random_entry})


def edit(request, entryName):
    originContent = util.get_entry(entryName)

    if request.method == "POST":
        form = EditEntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if util.get_entry(entryName) is not None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"entry": title}))

    form = EditEntryForm({"title": entryName, "content": originContent})
    return render(request, "encyclopedia/edit.html", {"editForm": form})

def search(request):
    searchedName = request.GET["q"].capitalize()
    list_entries = util.list_entries()
    searchResult = []

    if searchedName in list_entries:
        return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={"entry": searchedName}))

    else:
        for entry in list_entries:
            if searchedName[:1] == entry[:1]:
                searchResult.append(entry)
            
        return render(request, "encyclopedia/search.html", {"searchResult": searchResult})        





