from django.core import serializers
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from comicr.models import *
from comicr.defaults import *

s = serializers.serialize

def payload_generator(is_ajax=True, book_slug=DEFAULT_BOOK_SLUG, chapter_slug=DEFAULT_CHAPTER_SLUG, page_number=int(DEFAULT_PAGE_NUMBER)):
    payload = {}

    print '%s, %s, %s\r' % (book_slug, chapter_slug, page_number)
    if not is_ajax:
        try:
            payload['book'] = Book.objects.get(slug=book_slug)
        except:
            raise Http404

    try:
        chapter = Chapter.objects.filter(book__slug=book_slug).order_by('published')[0]
        if not is_ajax:
            payload['chapter'] = chapter
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
            if is_ajax:
                payload = '{"currentPage": {%s}, "nextPage": {%s},"previousPage": 0}' % (
                    s('json', [pages[0],], use_natural_keys=True)[2:-2], 
                    s('json', [pages[1],], use_natural_keys=True)[2:-2])
            else:
                payload['currentPage'] = pages[0]
                payload['nextPage'] = pages[1]
        else:
            if is_ajax:
                payload = '{"currentPage": {%s}, "nextPage": 0,"previousPage": {%s}}' % (
                    s('json', [pages[1],], use_natural_keys=True)[2:-2], 
                    s('json', [pages[0],], use_natural_keys=True)[2:-2])
            else:
                payload['currentPage'] = pages[1]
                payload['previousPage'] = pages[0]

    else:
        if is_ajax:
            payload = '{"currentPage": {%s}, "nextPage": {%s},"previousPage": {%s}}' % (
                    s('json', [pages[1],], use_natural_keys=True)[2:-2], 
                    s('json', [pages[2],], use_natural_keys=True)[2:-2], 
                    s('json', [pages[0],], use_natural_keys=True)[2:-2])
        else:
            payload['currentPage'] = pages[1]
            payload['nextPage'] = pages[2]
            payload['previousPage'] = pages[0]
    print payload

    return payload


def get_book(request, book_slug='rigby-the-barbarian'):
    
    if 'json' in request.META['HTTP_ACCEPT']:
        return HttpResponse(payload_generator(True, book_slug), 'application/json')

    else:
        print 'Here'
        return render_to_response('reader.html',{
            'pages': payload_generator(False, book_slug)}, 
            context_instance=RequestContext(request))


def get_chapter(request, book_slug='rigby-the-barbarian', chapter_slug='savage-sword-of-rigby'):

    if 'json' in request.META['HTTP_ACCEPT']:
        return HttpResponse(payload_generator(True, book_slug, chapter_slug), 'application/json')

    else:
        return render_to_response('reader.html',{
            'pages': payload_generator(False, book_slug, chapter_slug)},
            context_instance=RequestContext(request))


def get_page(request, book_slug='rigby-the-barbarian', chapter_slug='savage-sword-of-rigby', page_number=1):

    if 'json' in request.META['HTTP_ACCEPT']:
        return HttpResponse(payload_generator(True, book_slug, chapter_slug, int(page_number)), 'application/json')

    else:
        return render_to_response('reader.html',{
            'pages': payload_generator(False, book_slug, chapter_slug, int(page_number))},
            context_instance=RequestContext(request))



def comicr_home(request):
    return HttpResponse('Nothing to see here yet; carry on.', 'text/plain')
