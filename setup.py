# -*- coding: utf-8 -*-
"""
This module contains mr.migrator
"""
from setuptools import setup, find_packages

version = '1.1'

install_requires = [
    'collective.transmogrifier',
    'setuptools',
    'z3c.autoinclude',
    'zc.recipe.egg'
]

try:
    # If we are using Python 2.5 or greater we can require configparser
    eval("1 if True else 2")  # http://stackoverflow.com/questions/446052
    install_requires.append('configparser')
    install_requires.append('zope.app.component')  # BBB Only needed in
    # Plone >= 4?
except SyntaxError:
    # If we are using Python 2.4 or lower we cannot require configparser
    pass


long_description = (
    open('README.rst').read()
    + '\n' +
    open('CONTRIBUTORS.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
)
entry_point = ''
entry_points = {"zc.buildout": ["default = mr.migrator.recipe:Recipe"],
                'console_scripts': ['migrate = mr.migrator.runner:runner'],
                "z3c.autoinclude.plugin": ["target = plone"],
                }

tests_require = ['zope.testing', 'zc.buildout']

setup(
    name='mr.migrator',
    version=version,
    description="Drive-by transmogrifiction made easy!",
    long_description=long_description,
    classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Zope Public License',
    ],
    keywords='buildout crawler spider plone transmogrifierless',
    author='Dylan Jay',
    author_email='software@pretaweb.com',
    maintainer='Alex Clark',
    maintainer_email='aclark@aclark.net',
    url='https://github.com/collective/mr.migrator',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['mr'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    #      tests_require=tests_require,
    #      extras_require=dict(tests=tests_require),
    #      test_suite='mr.migrator.recipe.tests.test_docs.test_suite',
    entry_points=entry_points,
)
