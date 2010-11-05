# -*- coding: utf-8 -*-
"""
This module contains the tool of funnelweb
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0'

long_description = (
    read('README.rst')
    + '\n' +
    'Contributors\n' 
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' + 
    read('CHANGES.txt')
    + '\n' +
   'Download\n'
    '********\n'
    )
entry_point = 'funnelweb.recipe:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point],
                'console_scripts': ['funnelweb = funnelweb.runner:runner']}

tests_require=['zope.testing', 'zc.buildout']

setup(name='funnelweb',
      version=version,
      description="Parse static sites and import to CMS",
      long_description=long_description,
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Zope Public License',
        ],
      keywords='buildout crawler spider',
      author='Dylan Jay',
      author_email='software@pretaweb.com',
      url='http://svn.plone.org/svn/collective/',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['funnelweb'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout',
                        'z3c.recipe.scripts',
#                        'Zope2',
          'collective.transmogrifier',
                        'transmogrify.htmltesting',
                        'transmogrify.webcrawler',
                        'transmogrify.siteanalyser',
                        'transmogrify.htmlcontentextractor',
                        'transmogrify.pathsorter',
                        'transmogrify.ploneremote',
                        'Products.CMFCore',
                'zope.app.pagetemplate',
                'zope.app.component',
          'z3c.autoinclude'
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'funnelweb.recipe.funnelweb.tests.test_docs.test_suite',
      entry_points=entry_points,
      )
