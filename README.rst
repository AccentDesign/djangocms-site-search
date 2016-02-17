========================================
Django Model Based Search For Django CMS
========================================

Project description


Installation
============
Installation with ``pip``::

    $ pip install djangocms-site-search

Setup
=====
Add the following apps to the ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'cms',
        'site_search',
    )

Add the url routes to the project in urls.py::

    urlpatterns = [
        url(r'^', include('site_search.urls', 'search')),
    ]

License
=======
The project is licensed under the MIT license.