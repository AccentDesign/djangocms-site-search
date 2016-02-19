# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _


class SearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label=_('Search'),
        widget=forms.TextInput(attrs={'type': 'search'}))
