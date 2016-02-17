from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.template import RequestContext
from django.test import RequestFactory
from cms.toolbar.toolbar import CMSToolbar

from .utils import get_cleaned_bits


def get_field_value(obj, name):
    """
    Given a model instance and a field name (or attribute),
    returns the value of the field or an empty string.
    """
    fields = name.split('__')

    name = fields[0]

    try:
        obj._meta.get_field(name)
    except (AttributeError, models.FieldDoesNotExist):
        # we catch attribute error because obj will not always be a model
        # specially when going through multiple relationships.
        value = getattr(obj, name, None) or ''
    else:
        value = getattr(obj, name)

    if len(fields) > 1:
        remaining = '__'.join(fields[1:])
        return get_field_value(value, remaining)
    return value


def get_plugin_index_data(base_plugin, request):
    text_bits = []

    instance, plugin_type = base_plugin.get_plugin_instance()

    if instance is None:
        # this is an empty plugin
        return text_bits

    search_fields = getattr(instance, 'search_fields', [])

    if hasattr(instance, 'search_fulltext'):
        # check if the plugin instance has search enabled
        search_contents = instance.search_fulltext
    elif hasattr(base_plugin, 'search_fulltext'):
        # now check in the base plugin instance (CMSPlugin)
        search_contents = base_plugin.search_fulltext
    elif hasattr(plugin_type, 'search_fulltext'):
        # last check in the plugin class (CMSPluginBase)
        search_contents = plugin_type.search_fulltext
    else:
        # disabled if there's search fields defined,
        # otherwise it's enabled.
        search_contents = not bool(search_fields)

    if search_contents:
        context = RequestContext(request)

        from django.template import Engine
        updates = {}
        engine = Engine.get_default()

        for processor in engine.template_context_processors:
            updates.update(processor(context.request))
        context.dicts[context._processors_index] = updates

        plugin_contents = instance.render_plugin(context=context)

        if plugin_contents:
            text_bits = get_cleaned_bits(plugin_contents)
    else:
        values = (get_field_value(instance, field) for field in search_fields)

        for value in values:
            cleaned_bits = get_cleaned_bits(value or '')
            text_bits.extend(cleaned_bits)
    return text_bits


def get_request(language=None):
    """
    Returns a Request instance populated with cms specific attributes.
    """
    request_factory = RequestFactory(HTTP_HOST=settings.ALLOWED_HOSTS[0])
    request = request_factory.get("/")
    request.session = {}
    request.LANGUAGE_CODE = language or settings.LANGUAGE_CODE
    # Needed for plugin rendering.
    request.current_page = None
    request.user = AnonymousUser()
    request.toolbar = CMSToolbar(request)
    return request
