from django.core import serializers
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from comicr.models import *
from comicr.defaults import *

s = serializers.serialize

#book_slug = DEFAULT_BOOK_SLUG
#chapter_slug = DEFAULT_CHAPTER_SLUG
#page_number = DEFAULT_PAGE_NUMBER

def payload_generator(is_ajax, book_slug, chapter_slug=False, page_number=1):

    payload = {}

    if not is_ajax:
        try:
            payload['book'] = Book.objects.get(slug=book_slug)
        except:
            raise Http404

    try:
        if not chapter_slug:
            chapter = Chapter.objects.filter(book__slug=book_slug).order_by('published')[0]
            try:
                next_chapter = chapter.get_next_by_published()
            except:
                next_chapter = False
        else:
            chapter = Chapter.objects.get(slug=chapter_slug)
            try:
                next_chapter = chapter.get_next_by_published()
            except:
                next_chapter = False

            try:
                prev_chapter = chapter.get_previous_by_published()
            except:
                prev_chapter = False

        
        if not is_ajax:
            payload['chapter'] = chapter
            if next_chapter:
                payload['next_chapter'] = next_chapter
            if prev_chapter:
                payload['pre_chapter'] = prev_chapter

    except:
        raise Http404

    try:
        pages = Page.objects.filter(chapter__slug=chapter.slug
                           ).filter(chapter__book__slug=book_slug
                           ).filter(pnumber__range=(page_number-1, page_number+1)
                           ).order_by('pnumber')
    except:
        raise Http404


    if len(pages)==2:
        if pages[0].pnumber == page_number:
            try:
                st = pages[0].soundtrack_set.all()[0]
                sts = st.mp3.url
            except:
                st = 0
                sts = 'None'
            if is_ajax:
                payload = '{"currentPage": {%s}, "nextPage": {%s},"previousPage": 0, "soundtrack": "%s"}' % (
                    s('json', [pages[0],], use_natural_keys=True)[2:-2], 
                    s('json', [pages[1],], use_natural_keys=True)[2:-2],
                    sts)
            else:
                payload['currentPage'] = pages[0]
                payload['nextPage'] = pages[1]
                payload['soundtrack'] = st
        else:
            try:
                st = pages[1].soundtrack_set.all()[0]
                sts = st.mp3.url
            except:
                st = 0
                sts = 'None'
            if is_ajax:
                payload = '{"currentPage": {%s}, "nextPage": 0,"previousPage": {%s}, "soundtrack": "%s"}' % (
                    s('json', [pages[1],], use_natural_keys=True)[2:-2], 
                    s('json', [pages[0],], use_natural_keys=True)[2:-2],
                    sts)
            else:
                payload['currentPage'] = pages[1]
                payload['previousPage'] = pages[0]
                payload['soundtrack'] = st

    else:
        try:
            st = pages[1].soundtrack_set.all()[0]
            sts = st.mp3.url
        except:
            st = 0
            sts = 'None'
        if is_ajax:
            payload = '{"currentPage": {%s}, "nextPage": {%s},"previousPage": {%s}, "soundtrack": "%s"}' % (
                    s('json', [pages[1],], use_natural_keys=True)[2:-2], 
                    s('json', [pages[2],], use_natural_keys=True)[2:-2], 
                    s('json', [pages[0],], use_natural_keys=True)[2:-2],
                    sts)
        else:
            payload['currentPage'] = pages[1]
            payload['nextPage'] = pages[2]
            payload['previousPage'] = pages[0]
            payload['soundtrack'] = st


    return payload


def get_book(request, book_slug='rigby-the-barbarian'):
    if 'json' in request.META['HTTP_ACCEPT']:
        return HttpResponse(payload_generator(True, book_slug), 'application/json')

    else:
        return render_to_response('reader.html',{
            'pages': payload_generator(False, book_slug)}, 
            context_instance=RequestContext(request))


def get_chapter(request, book_slug, chapter_slug):

    if 'json' in request.META['HTTP_ACCEPT']:
        return HttpResponse(payload_generator(True, book_slug, chapter_slug, int(DEFAULT_PAGE_NUMBER)), 'application/json')

    else:
        return render_to_response('reader.html',{
            'pages': payload_generator(False, book_slug, chapter_slug, int(DEFAULT_PAGE_NUMBER))},
            context_instance=RequestContext(request))


def get_page(request, book_slug, chapter_slug, page_number):
    if 'json' in request.META['HTTP_ACCEPT']:
        return HttpResponse(payload_generator(True, book_slug, chapter_slug, int(page_number)), 'application/json')

    else:
        return render_to_response('reader.html',{
            'pages': payload_generator(False, book_slug, chapter_slug, int(page_number))},
            context_instance=RequestContext(request))



def comicr_home(request):
    return HttpResponse('Nothing to see here yet; carry on.', 'text/plain')
