from setuptools import setup, find_packages

setup(
    name='djangocms-site-search',
    version='0.2.2',
    description='Django model based search for Django CMS',
    long_description=open('README.rst').read(),
    author='Stuart George',
    author_email='stuart.bigmassa@gmail.com',
    url='https://github.com/bigmassa/djangocms-site-search',
    download_url='https://pypi.python.org/pypi/djangocms-site-search',
    license='MIT',
    packages=find_packages(exclude=('example',)),
    install_requires=[
        'Django>=1.8,<1.10',
        'django-cms>=3.1,<3.3',
    ],
    include_package_data=True,
    keywords = ['djangocms', 'django', 'cms', 'search', 'site'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
