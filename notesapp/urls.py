from django.conf.urls import patterns, url

from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.notes, name='notes'),
)
