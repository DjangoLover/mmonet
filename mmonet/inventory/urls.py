from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'inventory.views.index'),
    url(r'^/delete$', 'inventory.views.delete'),
    url(r'^/connect$', 'inventory.views.connect'),
    url(r'^/add$', 'inventory.views.add'),

    )
