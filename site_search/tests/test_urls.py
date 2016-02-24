from django.conf.urls import url, patterns, include


urlpatterns = patterns(
    '',
    url(r'^', include('site_search.urls', 'search')),
)
