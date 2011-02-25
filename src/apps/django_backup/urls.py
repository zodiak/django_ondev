from django.conf.urls.defaults import *
from django_backup import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^backup/$', views.backup, name='backup'),
    url(r'^restore/$', views.restore, name='restore'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^delete_selected/$', views.delete_selected, name='delete_selected'),
    url(r'^download/(?P<file>(\w|[\.\-]){1,50})$', views.download, name='download'),
)