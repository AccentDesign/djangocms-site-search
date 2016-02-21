# -*- coding: utf-8 -*-
from django.test import TestCase

from ..models import Index


class ModelTestCase(TestCase):

    def test_str_method(self):
        index = Index(title='foo')
        self.assertEqual(index.__str__(), 'foo')

    def test_title(self):
        field = Index._meta.get_field("title")
        self.assertFalse(field.null)
        self.assertEqual(field.max_length, 255)

    def test_pub_date(self):
        field = Index._meta.get_field("pub_date")
        self.assertTrue(field.null)

    def test_login_required(self):
        field = Index._meta.get_field("login_required")
        self.assertFalse(field.null)

    def test_site(self):
        field = Index._meta.get_field("site")
        self.assertFalse(field.null)

    def test_description(self):
        field = Index._meta.get_field("description")
        self.assertTrue(field.null)

    def test_url(self):
        field = Index._meta.get_field("url")
        self.assertFalse(field.null)

    def test_search_text(self):
        field = Index._meta.get_field("search_text")
        self.assertTrue(field.null)

    def test_language(self):
        field = Index._meta.get_field("language")
        self.assertFalse(field.null)
        self.assertEqual(field.max_length, 255)

    def test_content_type(self):
        field = Index._meta.get_field("content_type")
        self.assertFalse(field.null)

    def test_object_id(self):
        field = Index._meta.get_field("object_id")
        self.assertFalse(field.null)

    def test_content_object(self):
        field = Index._meta.get_field("content_object")
        self.assertEqual(field.ct_field, 'content_type')
        self.assertEqual(field.fk_field, 'object_id')
