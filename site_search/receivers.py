# -*- coding: utf-8 -*-
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from cms.models import Title
from cms.signals import post_publish, post_unpublish

from .helpers import get_request
from .indexers.cms_title import TitleIndexer
from .utils import add_indexed_object, remove_indexed_object


@receiver(post_publish, dispatch_uid='publish_cms_page')
def publish_cms_page(sender, instance, language, **kwargs):
    obj = instance.publisher_public.get_title_obj(language)
    request = get_request(language)
    indexer = TitleIndexer()
    search_text = indexer.get_search_data(obj, language, request)
    data = {
        'title': obj.title,
        'url': obj.page.get_absolute_url(),
        'pub_date': obj.page.publication_date,
        'login_required': obj.page.login_required,
        'site': obj.page.site,
        'description': obj.meta_description,
        'search_text': search_text,
        'language': language
    }
    add_indexed_object(obj, data)


@receiver(post_unpublish, dispatch_uid='unpublish_cms_page')
def unpublish_cms_page(sender, instance, language, **kwargs):
    obj = instance.publisher_public.get_title_obj(language)
    remove_indexed_object(obj)


@receiver(post_delete, sender=Title)
def post_delete_page(sender, instance, **kwargs):
    remove_indexed_object(instance)
