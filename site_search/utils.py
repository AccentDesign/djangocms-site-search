# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import striptags
from django.utils.text import smart_split
from django.utils.encoding import force_text as force_unicode

from .models import Index


def clean_join(separator, iterable):
    return separator.join(filter(None, iterable))


def get_cleaned_text(data):
    decoded = force_unicode(data)
    stripped = striptags(decoded)
    return smart_split(stripped)


def add_indexed_object(obj, data):
    obj_type = ContentType.objects.get_for_model(obj)
    data['content_type'] = obj_type
    index, created = Index.objects.update_or_create(
        content_type__id=obj_type.id,
        object_id=obj.id,
        defaults=data)
    return index, created


def remove_indexed_object(obj):
    obj_type = ContentType.objects.get_for_model(obj)
    try:
        index = Index.objects.get(
            content_type__id=obj_type.id,
            object_id=obj.id,
        )
        index.delete()
    except Index.DoesNotExist:
        pass
