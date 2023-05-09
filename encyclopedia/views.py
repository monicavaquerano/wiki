from django.http import HttpResponse
from django.shortcuts import render
from markdown2 import Markdown
from . import util


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
