========================================
Django model based search for Django CMS
========================================

A model based search app for Django CMS.

The reason I created this was simply to avoid the overhead of using third party applications such as haystack.
I was deploying an app on Amazons Elastic Beanstalk that will run on one or more instance and did not
want the hassle of trying to save the index results in a centralized storage. I also did not want another instance
just to act as a search endpoint like solr etc.

Doing it this way by saving the results in the database makes it extremely portable.

Its early days in the project and needs nore work such as unit testing, pagination etc.


Installation
============
Installation with ``pip``::

    $ pip install djangocms-site-search


Get Going
=====
On publishing a page, an index item is added to the model.
On unpublishing or deleting its removed. Simple!

You could even create more receivers to easily populate for non cms models.
Take a look at the ones for the cms at https://github.com/bigmassa/djangocms-site-search/blob/master/site_search/receivers.py.
You just need to provide the data.

There is a sample app included in the repo.


Setup
=====
Add the following apps to the ``INSTALLED_APPS`` ensuring its below cms::

    INSTALLED_APPS = (
        ...
        'cms',
        'site_search',
    )

Add the url routes to the project in urls.py::

    urlpatterns = [
        url(r'^', include('site_search.urls', 'search')),
    ]

You can turn off pagination by setting::

    SITE_SEARCH_PAGINATION = None

Or change its default number of 10 to something else.


License
=======
The project is licensed under the MIT license.
