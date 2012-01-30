from django.conf.urls.defaults import *

from comicr.models import *
#from comicr.feeds import *

urlpatterns = patterns('comicr.views',
    
    url(r'^$',
        view='comicr_home',
        name='comicr_home'),

    url(r'^(?P<book_slug>[-\w]+)/$',
        view='read_book',
        name='read_book'),

    url(r'^(?P<book_slug>[-\w]+)/(?P<chapter_slug>[-\w]+)/$',
        view='reader',
        name='read_chapter'),

    url(r'^(?P<book_slug>[-\w]+)/(?P<chapter_slug>[-\w]+)/#!(?P<page_number>\d+)$',
        view='reader',
        name='read_page'),
)
