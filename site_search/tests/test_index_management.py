# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from cms.api import create_page

from ..models import Index


class IndexTestCase(TestCase):

    def _create_page(self, **data):
        return create_page(
            title='test_page',
            reverse_id='testpage',
            template='test.html',
            language='en',
            **data
        )

    def test_creating_a_page_is_not_added(self):
        self._create_page()
        self.assertEqual(Index.objects.count(), 0)

    def test_published_page_is_added(self):
        page = self._create_page()
        page.publish('en')
        self.assertEqual(Index.objects.count(), 1)

    def test_unpublished_page_is_removed(self):
        page = self._create_page()
        page.publish('en')
        self.assertEqual(Index.objects.count(), 1)
        page.unpublish('en')
        self.assertEqual(Index.objects.count(), 0)

    def test_deleting_a_published_page_is_removed(self):
        page = self._create_page()
        page.publish('en')
        self.assertEqual(Index.objects.count(), 1)
        page.delete()
        self.assertEqual(Index.objects.count(), 0)

    def test_index_content_object_references_correct_object(self):
        page = self._create_page()
        page.publish('en')
        title = page.publisher_public.get_title_obj('en')
        title_type = ContentType.objects.get_for_model(title)
        index = Index.objects.get(content_type=title_type, object_id=title.pk)
        self.assertEqual(index.content_object, title)

    def test_index_title(self):
        page = self._create_page()
        page.publish('en')
        title = page.publisher_public.get_title_obj('en')
        title_type = ContentType.objects.get_for_model(title)
        index = Index.objects.get(content_type=title_type, object_id=title.pk)
        self.assertEqual(index.title, title.title)

    def test_index_pub_date(self):
        page = self._create_page(publication_date=datetime.now())
        page.publish('en')
        title = page.publisher_public.get_title_obj('en')
        title_type = ContentType.objects.get_for_model(title)
        index = Index.objects.get(content_type=title_type, object_id=title.pk)
        self.assertEqual(index.pub_date, page.publication_date)

    def test_index_login_required(self):
        page = self._create_page(login_required=True)
        page.publish('en')
        title = page.publisher_public.get_title_obj('en')
        title_type = ContentType.objects.get_for_model(title)
        index = Index.objects.get(content_type=title_type, object_id=title.pk)
        self.assertEqual(index.login_required, page.login_required)

    def test_index_site(self):
        page = self._create_page()
        page.publish('en')
        title = page.publisher_public.get_title_obj('en')
        title_type = ContentType.objects.get_for_model(title)
        index = Index.objects.get(content_type=title_type, object_id=title.pk)
        self.assertEqual(index.site.pk, page.site.pk)

    def test_index_description(self):
        page = self._create_page(meta_description='foo bar wiz bang')
        page.publish('en')
        title = page.publisher_public.get_title_obj('en')
        title_type = ContentType.objects.get_for_model(title)
        index = Index.objects.get(content_type=title_type, object_id=title.pk)
        self.assertEqual(index.description, title.meta_description)

    def test_index_url(self):
        page = self._create_page()
        page.publish('en')
        title = page.publisher_public.get_title_obj('en')
        title_type = ContentType.objects.get_for_model(title)
        index = Index.objects.get(content_type=title_type, object_id=title.pk)
        self.assertEqual(index.url, page.get_absolute_url())

    def test_index_language(self):
        page = self._create_page()
        page.publish('en')
        title = page.publisher_public.get_title_obj('en')
        title_type = ContentType.objects.get_for_model(title)
        index = Index.objects.get(content_type=title_type, object_id=title.pk)
        self.assertEqual(index.language, page.languages)
