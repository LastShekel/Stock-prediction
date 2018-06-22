from django.conf.urls import url

from . import views

app_name = 'prediction'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<riddle_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<riddle_id>[0-9]+)/answer/$', views.answer, name='answer')
]