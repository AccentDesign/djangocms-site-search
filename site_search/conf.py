# -*- coding: utf-8 -*-
from django.conf import settings

from appconf import AppConf


class SiteSearchAppConf(AppConf):

    CMS_PAGE = True
    DEFAULT_LANGUAGE = settings.LANGUAGE_CODE
    PAGINATION = 10

    class Meta:
        prefix = 'SITE_SEARCH'
