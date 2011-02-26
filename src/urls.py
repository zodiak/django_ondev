from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^robots.txt$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'path': "static/robots.txt"}),
    url(r'^favicon.ico$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'path': "static/favicon.ico"}),
)

if settings.DEBUG:
    urlpatterns+= patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', 
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )

urlpatterns += patterns('',
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/sentry/', include('sentry.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
    url(r'commander/', include('django_commander.urls', namespace='django_commander')),
    url(r'backups/', include('django_backup.urls', namespace='django_backup')),
    url(r'^', include('cms.urls')),
)