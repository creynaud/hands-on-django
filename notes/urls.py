from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'notes.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^notes/', include('notesapp.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
