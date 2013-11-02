from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^login/$', 'django.contrib.auth.views.login', name='login' ),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login/'}, name='logout' ),

    url(r'^$', 'apps.timing.views.timing', {'page_slug': 'tickets'}, name='timing'),
    url(r'^(?P<page_slug>[-\w]+)/$', 'apps.timing.views.timing', name='timing'),

    url(r'^timing/', include('apps.timing.urls')),
)

urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )
