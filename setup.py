from setuptools import setup, find_packages

setup(
    name='djangocms-site-search',
    version='0.0.7',
    description='Django model based search for Django CMS',
    long_description=open('README.rst').read(),
    author='Stuart George',
    author_email='stuart.bigmassa@gmail.com',
    url='https://github.com/bigmassa/djangocms-site-search',
    download_url='https://pypi.python.org/pypi/djangocms-site-search',
    license='MIT',
    packages=find_packages(exclude=('example',)),
    install_requires=[
        'Django>=1.8,<=1.9',
        'django-cms>3.0',
    ],
    include_package_data=True,
    keywords = ['django', 'cms', 'search'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
    ],
)