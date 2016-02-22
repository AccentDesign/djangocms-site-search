# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.utils.translation import get_language_from_request
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

try:
    from cms.cms_menus import get_visible_pages
except:
    from cms.menu import get_visible_pages

from cms.utils.page_resolver import get_page_queryset

from .conf import settings
from .forms import SearchForm
from .models import Index


class SearchResultsView(FormMixin, ListView):
    form_class = SearchForm
    model = Index
    template_name = 'site_search/search_results.html'

    paginate_by = settings.SITE_SEARCH_PAGINATION

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        return super(SearchResultsView, self).get(request, *args, **kwargs)

    def get_language(self):
        return get_language_from_request(self.request, check_path=True)

    def get_site(self):
        return get_current_site(self.request)

    def get_viewable_pages(self):
        site = self.get_site()
        page_queryset = get_page_queryset(self.request).published()
        pages = page_queryset.filter(site=site)
        return get_visible_pages(self.request, pages, site)

    def check_authenticated(self, queryset):
        if not self.request.user.is_authenticated():
            queryset = queryset.exclude(login_required=True)
        return queryset

    def check_view_permission(self, queryset):
        title_type = ContentType.objects.get(app_label="cms", model="title")
        cms_queryset = queryset.filter(content_type=title_type)
        viewable_pages = self.get_viewable_pages()
        for cms_object in cms_queryset:
            if cms_object.content_object.page_id not in viewable_pages:
                queryset = queryset.exclude(pk=cms_object.pk)
        return queryset

    def get_queryset(self):
        queryset = super(SearchResultsView, self).get_queryset()
        search = self.request.GET.get('q', '').strip()
        if search == '':
            return []
        queryset = self.check_authenticated(queryset)
        language = self.get_language()
        site = self.get_site()
        queryset = queryset.filter(
            Q(search_text__icontains=search) | Q(title__icontains=search),
            Q(language=language) & Q(site__pk=site.id),
            Q(pub_date__lte=datetime.now()) | Q(pub_date__isnull=True))
        queryset = self.check_view_permission(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context
