##########
Pagination
##########

You can turn off pagination by setting::

    SITE_SEARCH_PAGINATION = None

Or change its default number of 10 to something else.


#################################
Modifying Searchable Placeholders
#################################

By default all placeholders within the cms will be indexed for searching.
This can be modified like so:

Suppose your template had the following placeholders::

    {% placeholder body %}
    {% placeholder hidden %}

the following will setting can be added so that when you add the
*unique identifier* in the page advanced settings of *only_show_body*, anything
in the hidden placeholder will be ignored::

    PLACEHOLDERS_SEARCH_LIST = {
        '*': {},
        'only_show_body': {
            'include': ['body'],
        }
    }

or the following will also only search the body placeholder::

    PLACEHOLDERS_SEARCH_LIST = {
        '*': {},
        'only_show_body': {
            'exclude': ['hidden'],
        }
    }

also::

    PLACEHOLDERS_SEARCH_LIST = {
        '*': {},
        'only_show_body': {
            'include': ['body'],
            'exclude': ['hidden'],
        }
    }

Any number of these can be setup.

IMPORTANT: the * option must be present if additional settings are added
and the {} donates everything is searched.