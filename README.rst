****************************************
Django model based search for Django CMS
****************************************

|PyPI_Version| |Build_Status| |Coverage_Status|

The reason I created this was simply to avoid the overhead of using third party applications such as haystack.
I was deploying an app on Amazons Elastic Beanstalk that will run on one or more instance and did not
want the hassle of trying to save the index results in a centralized storage. I also did not want another instance
just to act as a search endpoint like solr etc.

Doing it this way by saving the results in the database makes it extremely portable.

On publishing a page, an index item is added to the model.
On unpublishing or deleting its removed.


************
Installation
************

Installation with ``pip``::

    $ pip install djangocms-site-search


*****
Setup
*****

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


*************
Documentation
*************

Please head over to our `documentation <https://djangocms-site-search.readthedocs.org/>`_ for all
the details on how to install and use the django CMS site search.


*******
License
*******

The project is licensed under the MIT license.



.. |PyPI_Version| image:: http://img.shields.io/pypi/v/djangocms-site-search.svg
   :target: https://pypi.python.org/pypi/djangocms-site-search
.. |Build_Status| image:: https://circleci.com/gh/AccentDesign/djangocms-site-search.svg?style=svg
   :target: https://circleci.com/gh/AccentDesign/djangocms-site-search
.. |Coverage_Status| image:: http://img.shields.io/coveralls/AccentDesign/djangocms-site-search/master.svg
   :target: https://coveralls.io/r/AccentDesign/djangocms-site-search?branch=master