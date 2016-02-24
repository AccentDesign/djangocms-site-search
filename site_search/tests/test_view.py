# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from cms.api import create_page

from ..helpers import get_request
from ..views import SearchResultsView


class URLTestCase(TestCase):

    @override_settings(ROOT_URLCONF='site_search.tests.test_urls')
    def test_search_url_view(self):
        response = self.client.get(reverse('search:search_results'))
        self.assertEqual(response.status_code, 200)


class ViewTestCase(TestCase):

    def setUp(self):
        self.view = SearchResultsView()
        self.request = get_request('en')
        self.request.GET = self.request.GET.copy()
        self.request.GET['q'] = 'test_page'
        self.view.request = self.request
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def _create_page(self, **data):
        return create_page(
            title='test_page',
            reverse_id='testpage',
            template='test.html',
            language='en',
            **data
        )

    def test_view_returns_ok_response(self):
        response = SearchResultsView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_view_returns_object_list(self):
        page = self._create_page()
        page.publish('en')
        self.assertEqual(len(self.view.get_queryset()), 1)

    def test_view_returns_blank_object_list_for_blank_search(self):
        page = self._create_page()
        page.publish('en')
        self.view.request.GET['q'] = ''
        self.assertEqual(len(self.view.get_queryset()), 0)

    def test_view_excludes_future_publications(self):
        page = self._create_page(
            publication_date=datetime.today() + timedelta(days=1))
        page.publish('en')
        self.assertEqual(len(self.view.get_queryset()), 0)

    def test_view_includes_past_publications(self):
        page = self._create_page(
            publication_date=datetime.today() - timedelta(days=1))
        page.publish('en')
        self.assertEqual(len(self.view.get_queryset()), 1)
