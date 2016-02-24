# -*- coding: utf-8 -*-
from copy import deepcopy
import mock

from django.conf import settings
from django.template import Template
from django.test import TestCase
from cms.api import add_plugin, create_page
from cms.models import CMSPlugin
from cms.models.placeholdermodel import Placeholder
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from ..helpers import get_plugin_index_data, get_request
from ..indexers.cms_title import TitleIndexer
from ..models import Index


class BasePlugin(CMSPluginBase):
    model = CMSPlugin
    plugin_content = 'some plugin content'
    render_template = Template(plugin_content)

    def render(self, context, instance, placeholder):
        return context


plugin_pool.register_plugin(BasePlugin)


class NoContentPlugin(CMSPluginBase):
    model = CMSPlugin
    plugin_content = ''
    render_template = Template(plugin_content)

    def render(self, context, instance, placeholder):
        return context


plugin_pool.register_plugin(NoContentPlugin)


class HiddenPlugin(CMSPluginBase):
    model = CMSPlugin
    plugin_content = 'some hidden content'
    render_template = Template(plugin_content)

    def render(self, context, instance, placeholder):
        return context


plugin_pool.register_plugin(HiddenPlugin)


class SearchTextTestCase(TestCase):

    def setUp(self):
        self.index = TitleIndexer()
        self.request = get_request(language='en')

    def get_plugin(self):
        instance = CMSPlugin(
            language='en',
            plugin_type="BasePlugin",
            placeholder=Placeholder(id=1111)
        )
        instance.cmsplugin_ptr = instance
        instance.pk = 1110
        return instance

    def test_plugin_indexing_enabled(self):
        cms_plugin = self.get_plugin()
        indexed_content = self.index.get_plugin_search_text(
            cms_plugin, self.request)
        self.assertEqual(BasePlugin.plugin_content, indexed_content)

    def _create_page(self, **data):
        data['reverse_id'] = data.get('reverse_id', 'testpage')
        return create_page(
            title='test_page',
            template='test.html',
            language='en',
            **data
        )

    def test_page_with_plugin_is_indexed_in_search_text(self):
        page = self._create_page()
        add_plugin(page.placeholders.get(slot='body'), BasePlugin, 'en')
        page.publish('en')
        indexed = Index.objects.all()[0]
        self.assertEqual('test_page', indexed.title)
        self.assertEqual('some plugin content', indexed.search_text)

    def test_page_with_plugin_without_content(self):
        page = self._create_page()
        add_plugin(page.placeholders.get(slot='body'), NoContentPlugin, 'en')
        page.publish('en')
        indexed = Index.objects.all()[0]
        self.assertEqual('', indexed.search_text)

    def test_page_with_meta_is_indexed_in_search_text(self):
        page = self._create_page(meta_description='foo bar')
        add_plugin(page.placeholders.get(slot='body'), BasePlugin, 'en')
        page.publish('en')
        indexed = Index.objects.all()[0]
        self.assertEqual('foo bar', indexed.description)
        self.assertEqual('some plugin content foo bar', indexed.search_text)

    def test_page_with_hidden_content_not_in_search_text(self):
        page = self._create_page()
        add_plugin(page.placeholders.get(slot='body'), BasePlugin, 'en')
        add_plugin(page.placeholders.get(slot='hidden'), HiddenPlugin, 'en')
        page.publish('en')
        indexed = Index.objects.all()[0]
        self.assertEqual('some plugin content', indexed.search_text)

    def test_page_search_text_for_testpage1(self):
        page = self._create_page(reverse_id='testpage1')
        add_plugin(page.placeholders.get(slot='body'), BasePlugin, 'en')
        add_plugin(page.placeholders.get(slot='hidden'), HiddenPlugin, 'en')
        page.publish('en')
        indexed = Index.objects.all()[0]
        self.assertEqual('some plugin content some hidden content',
                         indexed.search_text)

    def test_page_search_text_for_testpage2(self):
        page = self._create_page(reverse_id='testpage2')
        add_plugin(page.placeholders.get(slot='body'), BasePlugin, 'en')
        add_plugin(page.placeholders.get(slot='hidden'), HiddenPlugin, 'en')
        page.publish('en')
        indexed = Index.objects.all()[0]
        self.assertEqual('',
                         indexed.search_text)

    def test_page_search_text_for_testpage3(self):
        page = self._create_page(reverse_id='testpage3')
        add_plugin(page.placeholders.get(slot='body'), BasePlugin, 'en')
        add_plugin(page.placeholders.get(slot='hidden'), HiddenPlugin, 'en')
        page.publish('en')
        indexed = Index.objects.all()[0]
        self.assertEqual('some plugin content',
                         indexed.search_text)

    def test_page_search_text_for_testpage4(self):
        page = self._create_page(reverse_id='testpage4')
        add_plugin(page.placeholders.get(slot='body'), BasePlugin, 'en')
        add_plugin(page.placeholders.get(slot='hidden'), HiddenPlugin, 'en')
        page.publish('en')
        indexed = Index.objects.all()[0]
        self.assertEqual('some hidden content',
                         indexed.search_text)

    def test_page_search_text_for_testpage5(self):
        page = self._create_page(reverse_id='testpage5')
        add_plugin(page.placeholders.get(slot='body'), BasePlugin, 'en')
        add_plugin(page.placeholders.get(slot='hidden'), HiddenPlugin, 'en')
        page.publish('en')
        indexed = Index.objects.all()[0]
        self.assertEqual('some plugin content some hidden content',
                         indexed.search_text)

    def test_page_search_text_for_testpage6(self):
        page = self._create_page(reverse_id='testpage6')
        add_plugin(page.placeholders.get(slot='body'), BasePlugin, 'en')
        add_plugin(page.placeholders.get(slot='hidden'), HiddenPlugin, 'en')
        page.publish('en')
        indexed = Index.objects.all()[0]
        self.assertEqual('some hidden content',
                         indexed.search_text)

    def test_page_search_text_for_testpage7_invalid_settings(self):
        page = self._create_page(reverse_id='testpage7')
        add_plugin(page.placeholders.get(slot='body'), BasePlugin, 'en')
        add_plugin(page.placeholders.get(slot='hidden'), HiddenPlugin, 'en')
        page.publish('en')
        indexed = Index.objects.all()[0]
        self.assertEqual('some plugin content', indexed.search_text)

    def test_page_search_text_for_testpage7(self):
        page = self._create_page(reverse_id='testpage7')
        add_plugin(page.placeholders.get(slot='body'), BasePlugin, 'en')
        add_plugin(page.placeholders.get(slot='hidden'), HiddenPlugin, 'en')
        page.publish('en')
        indexed = Index.objects.all()[0]
        self.assertEqual('some plugin content', indexed.search_text)

    def test_invalid_reverse_id_uses_all(self):
        page = self._create_page(reverse_id='testpage8')
        add_plugin(page.placeholders.get(slot='body'), BasePlugin, 'en')
        add_plugin(page.placeholders.get(slot='hidden'), HiddenPlugin, 'en')
        page.publish('en')
        indexed = Index.objects.all()[0]
        self.assertEqual('some plugin content some hidden content',
                         indexed.search_text)

    def test_blank_reverse_id_uses_all(self):
        page = self._create_page(reverse_id='')
        add_plugin(page.placeholders.get(slot='body'), BasePlugin, 'en')
        add_plugin(page.placeholders.get(slot='hidden'), HiddenPlugin, 'en')
        page.publish('en')
        indexed = Index.objects.all()[0]
        self.assertEqual('some plugin content some hidden content',
                         indexed.search_text)

    @mock.patch('django.conf.settings.PLACEHOLDERS_SEARCH_LIST', None)
    def test_none_setting_uses_all(self):
        page = self._create_page()
        add_plugin(page.placeholders.get(slot='body'), BasePlugin, 'en')
        add_plugin(page.placeholders.get(slot='hidden'), HiddenPlugin, 'en')
        page.publish('en')
        indexed = Index.objects.all()[0]
        self.assertEqual('some plugin content some hidden content',
                         indexed.search_text)

    @mock.patch('django.conf.settings.PLACEHOLDERS_SEARCH_LIST', {})
    def test_empty_setting_uses_all(self):
        page = self._create_page()
        add_plugin(page.placeholders.get(slot='body'), BasePlugin, 'en')
        add_plugin(page.placeholders.get(slot='hidden'), HiddenPlugin, 'en')
        page.publish('en')
        indexed = Index.objects.all()[0]
        self.assertEqual('some plugin content some hidden content',
                         indexed.search_text)

    search_list = deepcopy(settings.PLACEHOLDERS_SEARCH_LIST)
    del search_list['*']

    @mock.patch('django.conf.settings.PLACEHOLDERS_SEARCH_LIST', search_list)
    def test_missing_all_and_invalid_placeholder_raises_error(self):
        page = self._create_page(reverse_id='foo')
        add_plugin(page.placeholders.get(slot='body'), BasePlugin, 'en')
        add_plugin(page.placeholders.get(slot='hidden'), HiddenPlugin, 'en')
        try:
            page.publish('en')
            return False
        except AttributeError:
            return True

    @mock.patch('cms.models.pluginmodel.CMSPlugin.get_plugin_instance')
    def test_none_plugin_instance_returns_blank(self, mocked):
        mocked.return_value = None, None
        cms_plugin = self.get_plugin()
        indexed_content = self.index.get_plugin_search_text(
            cms_plugin, self.request)
        self.assertEqual('', indexed_content)
