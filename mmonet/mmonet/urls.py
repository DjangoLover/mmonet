from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'mmonet.views.index'),
    url(r'^inventory', include('inventory.urls')),

    url(r'^monitor', include('monitor.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
