# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.utils.translation import get_language_from_request
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

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

    def get_queryset(self):
        queryset = super(SearchResultsView, self).get_queryset()
        search = self.request.GET.get('q', '').strip()
        if search == '':
            return []
        if not self.request.user.is_authenticated():
            queryset = queryset.exclude(login_required=True)
        language = get_language_from_request(self.request, check_path=True)
        site = get_current_site(self.request)
        queryset = queryset.filter(
            Q(search_text__icontains=search) | Q(title__icontains=search),
            Q(language=language) & Q(site__pk=site.id),
            Q(pub_date__lte=datetime.now()) | Q(pub_date__isnull=True))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context
