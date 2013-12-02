from django.conf.urls import *
from main.views import *

urlpatterns = patterns('',

                       url(r'^login/$', login_form),
                       url(r'^login/auth/$', login),
                       url(r'^logout/$', logout),
                       url(r'^change/$', account_change_form),
                       url(r'^change/set/$', account_change),
                       )
