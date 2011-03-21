# -*- coding: utf-8 -*-
"""
This module contains the tool of funnelweb
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0b1'

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
entry_point = ''
entry_points = {"zc.buildout": ["default = mr.migrator.recipe:Recipe"],
                'console_scripts': ['migrate = mr.migrator.runner:runner'],
                "z3c.autoinclude.plugin": ["target = plone"],
                }

tests_require=['zope.testing', 'zc.buildout']

setup(name='mr.migrator',
      version=version,
      description="Your friend in helping you migrate content",
      long_description=long_description,
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Zope Public License',
        ],
      keywords='buildout crawler spider plone transmogrifierless',
      author='Dylan Jay',
      author_email='software@pretaweb.com',
      url='http://pypi.python.org/pypi/migrator',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['mr'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout',
                        'zc.recipe.egg',
                        'collective.transmogrifier',
                        'Products.CMFCore', # cause transmogrifier needs it
                'zope.app.pagetemplate',
                'zope.app.component',
          'z3c.autoinclude'
                        # -*- Extra requirements: -*-
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'mr.migrator.recipe.tests.test_docs.test_suite',
      entry_points=entry_points,
      )
