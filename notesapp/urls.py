from django.conf.urls import patterns, url

from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.my_notes, name='my_notes'),
    url(r'^add/$', views.add_note, name='add_note'),
    url(r'^(?P<pk>\d+)/$', views.note_detail, name='note_detail'),
    url(r'^edit/(?P<pk>\d+)/$', views.edit_note, name='edit_note'),
    url(r'^delete/(?P<pk>\d+)/$', views.delete_note, name='delete_note'),
)
