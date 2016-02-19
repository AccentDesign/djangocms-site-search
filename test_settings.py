#!/usr/bin/env python
# -*- coding: utf-8 -*-


def gettext(s):
    return s


HELPER_SETTINGS = {
    'TEMPLATE_DIRS': ('example/templates/cms/layouts/',),
    'CMS_TEMPLATES': (
        ('fullwidth.html', 'Fullwidth'),
    ),
    'ALLOWED_HOSTS': ['localhost'],
    'CMS_LANGUAGES': {1: [{'code': 'en', 'name': 'English'}]},
    'LANGUAGES': (('en', 'English'),),
    'LANGUAGE_CODE': 'en',
    'CMS_PERMISSION': True,
    'CMS_PLACEHOLDER_CONF': {
        'content': {},
    },
    'PLACEHOLDERS_SEARCH_LIST': {
        '*': {},
    },
    'SITE_SEARCH_PAGINATION': 10,
}


def run():
    from djangocms_helper import runner
    runner.cms('site_search')

if __name__ == '__main__':
    run()