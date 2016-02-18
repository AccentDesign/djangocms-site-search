# -*- coding: utf-8 -*-
from appconf import AppConf


class SiteSearchAppConf(AppConf):

    PAGINATION = 10

    class Meta:
        prefix = 'SITE_SEARCH'
