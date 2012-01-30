from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'rigby.views.home', name='home'),
    url(r'^wall/', 'rigby.views.home', name='home'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^reader/', include('comicr.urls')),
    
    url(r'^session/remember/(?P<page_id>\d+)/$', 'rigby.views.remember_page_id', name='session_remember'),
)

urlpatterns += patterns('comicr.views',
    url(r'^rss/$', 
        view='rss',
        name='rss'),
)


    
