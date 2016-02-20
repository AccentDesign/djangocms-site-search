# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import SearchResultsView


urlpatterns = patterns(
    '',

    url(r'^$',
        SearchResultsView.as_view(),
        name='search_results'),

)
