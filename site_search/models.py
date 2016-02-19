# -*- coding: utf-8 -*-
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models


class Index(models.Model):

    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField(null=True)
    login_required = models.BooleanField()
    site = models.ForeignKey(Site)
    description = models.TextField(blank=True, null=True)
    url = models.URLField()
    search_text = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=255)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()


from site_search import receivers  # leave unused import
