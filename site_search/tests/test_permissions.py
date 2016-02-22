# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from cms.api import assign_user_to_page, create_page

from ..helpers import get_request
from ..views import SearchResultsView


class PermissionsTestCase(TestCase):

    def setUp(self):
        self.view = SearchResultsView()
        self.request = get_request('en')
        self.request.GET = self.request.GET.copy()
        self.request.GET['q'] = 'test_page'
        self.view.request = self.request
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')
        self.other_user = User.objects.create_user(
            username='fred', email='fred@…', password='top_secret')

    def _create_page(self, **data):
        return create_page(
            title='test_page',
            reverse_id='testpage',
            template='test.html',
            language='en',
            **data
        )

    ####################################################################
    # login_required                                                   #
    ####################################################################

    def test_not_included_when_login_required_and_user_anonymous(self):
        page = self._create_page(login_required=True)
        page.publish('en')
        self.assertEqual(len(self.view.get_queryset()), 0)

    def test_included_when_login_required_when_user_logged_in(self):
        self.view.request.user = self.user
        page = self._create_page(login_required=True)
        page.publish('en')
        self.assertEqual(len(self.view.get_queryset()), 1)

    ####################################################################
    # page permissions                                                 #
    ####################################################################

    def test_included_when_perm_set_and_this_user_included(self):
        self.view.request.user = self.user
        page = self._create_page(login_required=True)
        page.publish('en')
        assign_user_to_page(page, self.user, can_view=True)
        self.assertEqual(len(self.view.get_queryset()), 1)

    def test_not_included_when_perm_set_and_this_user_not_included(self):
        self.view.request.user = self.user
        page = self._create_page(login_required=True)
        page.publish('en')
        assign_user_to_page(page, self.other_user, can_view=True)
        self.assertEqual(len(self.view.get_queryset()), 0)

    def test_included_when_no_perm_set(self):
        self.view.request.user = self.user
        page = self._create_page(login_required=True)
        page.publish('en')
        self.assertEqual(len(self.view.get_queryset()), 1)

    ####################################################################
    # ensure perms still valid when login_required was not ticked      #
    ####################################################################

    def test_included_when_perm_set_and_this_user_included_2(self):
        self.view.request.user = self.user
        page = self._create_page(login_required=False)
        page.publish('en')
        assign_user_to_page(page, self.user, can_view=True)
        self.assertEqual(len(self.view.get_queryset()), 1)

    def test_not_included_when_perm_set_and_this_user_not_included_2(self):
        self.view.request.user = self.user
        page = self._create_page(login_required=False)
        page.publish('en')
        assign_user_to_page(page, self.other_user, can_view=True)
        self.assertEqual(len(self.view.get_queryset()), 0)

    def test_included_when_no_perm_set_2(self):
        self.view.request.user = self.user
        page = self._create_page(login_required=False)
        page.publish('en')
        self.assertEqual(len(self.view.get_queryset()), 1)
