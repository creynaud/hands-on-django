from django.conf.urls import patterns, url

from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.my_notes, name='my_notes'),
    url(r'^(?P<pk>\d+)/$', views.note_detail, name='note_detail'),
)
