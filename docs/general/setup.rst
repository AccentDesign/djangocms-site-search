#####
Setup
#####

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


