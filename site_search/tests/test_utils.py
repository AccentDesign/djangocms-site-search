# -*- coding: utf-8 -*-
from django.test import TestCase
from cms.api import create_page

from ..models import Index
from ..utils import (
    add_indexed_object,
    clean_join,
    get_cleaned_text,
    remove_indexed_object
)


class UtilsTestCase(TestCase):

    ##############################
    # clean_join                 #
    ##############################

    def test_clean_join(self):
        iterable = ['hello', 'there']
        retult = clean_join(' ', iterable)
        self.assertEqual(retult, 'hello there')

    def test_clean_join_with_none(self):
        iterable = ['hello', None, 'there']
        retult = clean_join(' ', iterable)
        self.assertEqual(retult, 'hello there')

    ##############################
    # get_cleaned_text           #
    ##############################

    def test_get_cleaned_text(self):
        html = '<p>foo</p> <a herf="/">bar</a> wiz pop'
        result = get_cleaned_text(html)
        self.assertListEqual([i for i in result], ['foo', 'bar', 'wiz', 'pop'])

    ##############################
    # add_indexed_object         #
    ##############################

    def _create_page(self, **data):
        return create_page(
            title='test_page',
            reverse_id='testpage',
            template='test.html',
            language='en',
            published=True,
            **data
        )

    def test_add_indexed_object(self):
        page = self._create_page()
        Index.objects.all().delete()
        obj = page.publisher_public.get_title_obj('en')
        data = {
            'title': obj.title,
            'url': obj.page.get_absolute_url(),
            'pub_date': obj.page.publication_date,
            'login_required': obj.page.login_required,
            'site': obj.page.site,
            'description': obj.meta_description,
            'search_text': 'foo',
            'language': 'en'
        }
        index, created = add_indexed_object(obj, data)
        self.assertTrue(created)
        self.assertEqual(Index.objects.all()[0], index)

    ##############################
    # remove_indexed_object      #
    ##############################

    def test_remove_indexed_object(self):
        page = self._create_page()
        obj = page.publisher_public.get_title_obj('en')
        remove_indexed_object(obj)
        self.assertEqual(Index.objects.count(), 0)

    def test_remove_indexed_object_doesnt_fail_if_not_there(self):
        page = self._create_page()
        obj = page.publisher_public.get_title_obj('en')
        remove_indexed_object(obj)
        self.assertEqual(Index.objects.count(), 0)
        remove_indexed_object(obj)
