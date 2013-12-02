from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from main.views import *
from messages.views import *
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', report_list),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^account/', include('main.urls')),
                       url(r'^report/', include('messages.urls')),
                       url(r'^send/$', send),
                       url(r'^media/(?P<path>.*)$', mediaserver),
)

urlpatterns += staticfiles_urlpatterns()