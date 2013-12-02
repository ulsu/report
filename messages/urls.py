from django.conf.urls import *
from messages.views import *
from main.views import *

urlpatterns = patterns('',
                       url(r'^add/$', report_create),
                       url(r'^list/$', report_list),
                       url(r'^mylist/$', my_report_list),
                       url(r'^(?P<id>\d+)/$', report_view),
                       url(r'^(?P<id>\d+)/edit/$', report_edit),
                       url(r'^(?P<id>\d+)/save/$', save),
                       url(r'^(?P<id>\d+)/addcomment/$', comment_add),
                       )