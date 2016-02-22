# -*- coding: utf-8 -*-
from django.db import models
from django.test import TestCase
from cms.api import add_plugin, create_page
from cms.models import CMSPlugin
from cms.models.placeholdermodel import Placeholder
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from ..helpers import get_request
from ..indexers.cms_title import TitleIndexer
from ..models import Index


class ValidSearchFieldsModel(CMSPlugin):

    body = models.TextField()
    additional_text = models.TextField()

    search_fields = ('body', 'additional_text',
                     'cmsplugin_ptr__placeholder__slot')

    class Meta:
        app_label = 'tests'


class InvalidSearchFieldsModel(CMSPlugin):

    body = models.TextField()
    additional_text = models.TextField()

    search_fields = ('body', 'additional_text_foo',
                     'cmsplugin_ptr__placeholder__slot')

    class Meta:
        app_label = 'tests'


class ValidSearchFieldsPlugin(CMSPluginBase):
    model = ValidSearchFieldsModel


plugin_pool.register_plugin(ValidSearchFieldsPlugin)


class InvalidSearchFieldsPlugin(CMSPluginBase):
    model = InvalidSearchFieldsModel


plugin_pool.register_plugin(InvalidSearchFieldsPlugin)


class SearchFieldsTestCase(TestCase):

    def setUp(self):
        self.index = TitleIndexer()
        self.request = get_request(language='en')

    def test_valid_search_fields_in_search_text_shows_as_expected(self):
        page = create_page(title='page', template='test.html', language='en')
        placeholder = page.placeholders.get(slot='body')
        add_plugin(
            placeholder, 'ValidSearchFieldsPlugin', 'en', body='Lorem ipsum',
            additional_text='additional text')
        page.publish('en')
        indexed = Index.objects.all()[0]
        self.assertEqual(
            'Lorem ipsum additional text body', indexed.search_text)

    def test_invalid_search_fields_in_search_text_shows_as_expected(self):
        page = create_page(title='page', template='test.html', language='en')
        placeholder = page.placeholders.get(slot='body')
        add_plugin(
            placeholder, 'InvalidSearchFieldsPlugin', 'en', body='Lorem ipsum',
            additional_text='additional text')
        page.publish('en')
        indexed = Index.objects.all()[0]
        self.assertEqual(
            'Lorem ipsum body', indexed.search_text)
