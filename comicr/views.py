from django.core import serializers
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from comicr.models import *
from comicr.defaults import *

s = serializers.serialize

#book_slug = DEFAULT_BOOK_SLUG
#chapter_slug = DEFAULT_CHAPTER_SLUG
#page_number = DEFAULT_PAGE_NUMBER

def reader(request, book_slug=DEFAULT_BOOK_SLUG, chapter_slug=DEFAULT_CHAPTER_SLUG, page_number=DEFAULT_PAGE_NUMBER):
    try:
        book = Book.objects.select_related().get(slug=book_slug)
        chapter = book.chapter_set.get(slug=chapter_slug)
        try:
            next_chapter = chapter.get_next_by_published()
        except:
            next_chapter = False
        try:
            prev_chapter = chapter.get_previous_by_published()
        except:
            prev_chapter = False
        pages = chapter.page_set.extra(select={'current':"pnumber = %s" % page_number}).all().order_by('pnumber')
    except:
        raise Http404


    return render_to_response('reader.html', {
        'book': book,
        'chapter': chapter,
        'next_chapter': next_chapter,
        'prev_chapter': prev_chapter,
        'pages': pages,
        'current_index': int(page_number)-1},
        context_instance=RequestContext(request))

def read_book(request, book_slug, chapter_slug=DEFAULT_CHAPTER_SLUG):
    try:
        book = Book.objects.select_related().get(slug=book_slug)
        chapter = book.chapter_set.all().order_by('published')[0]
        page = chapter.page_set.order_by('pnumber')[0]
        return redirect(page)
    except:
        raise Http404

def comicr_home(request):
    return HttpResponse('Nothing to see here yet; carry on.', 'text/plain')


def rss(request):
    pages = Page.objects.all().order_by('-published')[0:10]

    return render_to_response('rss.xml', {
        'pages': pages,
        'lastBuildDate': pages[0].published.strftime('%a, %d %b %Y %H:%M:%S GMT'),
    })

def toc(request):
    pages = s("json", Page.objects.all())
    return HttpResponse(pages, mimetype="application/json")

def home2(request):
    return render_to_response('2base.html', {
        'motd': 'hello world'
    })




