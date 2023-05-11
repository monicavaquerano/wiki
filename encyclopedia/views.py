from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from markdown2 import Markdown
from . import util
import os
from random import choice


def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    html = convert_md_to_html(title)
    if html == None:
        return render(
            request, "encyclopedia/error.html", {"message": "This entry does not exist"}
        )
    else:
        return render(
            request, "encyclopedia/entry.html", {"title": title, "html": html}
        )


def search(request):
    if request.method == "POST":
        entry_search = request.POST["q"]
        html = convert_md_to_html(entry_search)
        if html is not None:
            return render(
                request,
                "encyclopedia/entry.html",
                {"title": entry_search, "html": html},
            )
        else:
            allEntries = util.list_entries()
            recommendations = []
            for entry in allEntries:
                if entry_search.lower().strip() in entry.lower():
                    recommendations.append(entry)
            return render(
                request,
                "encyclopedia/search.html",
                {"recommendations": recommendations},
            )


def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST["title"].strip()
        content = request.POST["content"].strip()
        if util.get_entry(title):
            return render(
                request,
                "encyclopedia/error.html",
                {"message": "This entry already exists."},
            )
        else:
            util.save_entry(title, content)
            return entry(request, title)


def edit(request):
    if request.method == "POST":
        title = request.POST["title"].strip()
        content = util.get_entry(title)
        return render(
            request, "encyclopedia/edit.html", {"title": title, "content": content}
        )


def save(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        return redirect(f"/wiki/{title}")


def delete(request):
    if request.method == "POST":
        title = request.POST["title"]
        if os.path.exists(f"entries/{title}.md"):
            os.remove(f"entries/{title}.md")
            return render(
                request, "encyclopedia/index.html", {"entries": util.list_entries()}
            )
        else:
            return render(
                request,
                "encyclopedia/error.html",
                {"message": "This entry doesn't exists."},
            )


def random(request):
    entries = util.list_entries()
    title = choice(entries)
    return redirect(f"/wiki/{title}")
