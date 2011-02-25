from django.conf.urls.defaults import *
from django_commander import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^panel/$', views.panel, name='panel'),
    url(r'^view/(?P<filename>.*)$', views.view, name ='file'),
    url(r'^edit/(?P<filename>.*)$', views.edit, name ='edit'),

)