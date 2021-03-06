######################
Django CMS Site Search
######################

Django model based search for Django CMS

The reason I created this was simply to avoid the overhead of using third party applications such as haystack.
I was deploying an app on Amazons Elastic Beanstalk that will run on one or more instance and did not
want the hassle of trying to save the index results in a centralized storage. I also did not want another instance
just to act as a search endpoint like solr etc.

Doing it this way by saving the results in the database makes it extremely portable.

On publishing a page, an index item is added to the model.
On unpublishing or deleting its removed.


.. toctree::
   :maxdepth: 3

   general/installation
   general/setup
   reference/index
   general/contribute


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

