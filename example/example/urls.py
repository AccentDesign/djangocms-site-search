from django.conf import settings
from django.conf.urls import patterns, include, static, url
from django.contrib import admin


urlpatterns = patterns(
    '',

    url(r'^admin/',
        include(admin.site.urls)),

    url(r'^search/',
        include('site_search.urls', 'search')),

    url(r'',
        include('cms.urls')),

)

if settings.DEBUG:
    # media url for when dev storage
    urlpatterns += static.static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
