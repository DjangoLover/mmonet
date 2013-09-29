from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^$', 'monitor.views.index'),

    url(r'^/delete$', 'monitor.views.delete'),
    url(r'^/add_measure$', 'monitor.views.add_measure'),
    url(r'^/add_trigger$', 'monitor.views.add_trigger'),
    )
