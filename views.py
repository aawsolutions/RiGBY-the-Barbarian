from django.shortcuts import HttpResponse, render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from datetime import datetime

from comicr.models import *
from comicr.defaults import *



def home(request):

    nav = {}

    books =  Book.objects.all().order_by('published')
    latest = Page.objects.latest('published')
    
    delta = datetime.now() - latest.published
    if delta.days <5:
        fresh = True
    else:
        fresh = False

    try:
        page_id =  request.session['my_page_id']
        welcome_back = True
        if page_id > 0:
            page = Page.objects.get(id=page_id)
        else:
            page = Page.objects.latest('published')
    except:
        page = Page.objects.all().order_by('published')[0]
        welcome_back = False

    for book in books:
        book.chapters = book.chapter_set.all().order_by('published')

    try:
        legacy = Page.objects.get(legacy_slug=request.GET['webcomic_page']).get_absolute_url()
    except:
        legacy = False

    try:
        test = request.GET['feed']
        print test
        return redirect('rss', permanent=True)
    except:
        pass    

    return render_to_response('home.html',{
        'books': books,
        'page': page,
        'latest': latest,
        'fresh': fresh,
        'welcome_back': welcome_back,
        'legacy': legacy,},
        context_instance=RequestContext(request))


def remember_page_id(request, page_id):
    request.session['my_page_id'] = page_id
    return HttpResponse('[{"success": %s,}]' % page_id, 'application/json')
    
