from django.conf.urls.defaults import *
from django.conf import settings

import filedrop.views
import django.contrib.auth.views

urlpatterns = patterns('',
    url(r'^$', filedrop.views.home, name='home'),
    url(r'^dropoff/$', filedrop.views.dropoff, name='dropoff'),
    url(r'^dropoff/(?P<key>[a-zA-Z0-9]+)/upload/$', filedrop.views.upload, name='dropoff_upload'),
    url(r'^dropoff/(?P<key>[a-zA-Z0-9]+)/$', filedrop.views.dropoff),
    url(r'^pickup/(?P<key>[a-zA-Z0-9]+)/$', filedrop.views.pickup, name='pickup'),
    url(r'^pickup/(?P<key>[a-zA-Z0-9]+)/(?P<file_id>[0-9]+)/(?P<filename>[\W]+)$', filedrop.views.download, name='download'),
    url(r'^upload/$', filedrop.views.upload, name='upload'),
)

if settings.DEBUG:
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns = patterns('',
        # Debug Administration
        (r'^admin/', include(admin.site.urls)),
        # Debug User Authentication
        url(r'^accounts/login/', django.contrib.auth.views.login),
        url(r'^accounts/logout/', django.contrib.auth.views.logout),
        # Debug Files
        (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s/images/' % settings.MEDIA_ROOT, 'show_indexes': True}),
        (r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s/css/' % settings.MEDIA_ROOT, 'show_indexes': True}),
        (r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s/js/' % settings.MEDIA_ROOT, 'show_indexes': True}),
    ) + urlpatterns
