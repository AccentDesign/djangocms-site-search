# -*- coding: utf-8 -*-
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.template import Engine, RequestContext
from django.test import RequestFactory
from cms.toolbar.toolbar import CMSToolbar

from .conf import settings
from .utils import get_cleaned_text


def get_field_value(obj, name):
    fields = name.split('__')
    name = fields[0]

    try:
        obj._meta.get_field(name)
    except (AttributeError, models.FieldDoesNotExist):
        value = getattr(obj, name, None) or ''
    else:
        value = getattr(obj, name)

    if len(fields) > 1:
        remaining = '__'.join(fields[1:])
        return get_field_value(value, remaining)
    return value


def get_plugin_index_data(base_plugin, request):
    searchable_text = []
    instance, plugin_type = base_plugin.get_plugin_instance()

    if instance is None:
        return searchable_text

    search_fields = getattr(instance, 'search_fields', [])

    if not bool(search_fields):
        context = RequestContext(request)
        updates = {}

        engine = Engine.get_default()
        for processor in engine.template_context_processors:
            updates.update(processor(context.request))
        context.dicts[context._processors_index] = updates

        plugin_contents = instance.render_plugin(context=context)
        if plugin_contents:
            searchable_text = get_cleaned_text(plugin_contents)
    else:
        values = (get_field_value(instance, field) for field in search_fields)
        for value in values:
            cleaned_bits = get_cleaned_text(value or '')
            searchable_text.extend(cleaned_bits)

    return searchable_text


def get_request(language=None):
    request_factory = RequestFactory(HTTP_HOST=settings.ALLOWED_HOSTS[0])
    request = request_factory.get("/")
    request.session = {}
    request.LANGUAGE_CODE = language or settings.LANGUAGE_CODE
    request.current_page = None
    request.user = AnonymousUser()
    request.toolbar = CMSToolbar(request)
    return request
