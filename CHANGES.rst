Changelog
=========

1.3 (unreleased)
----------------

- Python 3 compatibility [ksuess]
- Fix ComponentLookupError (permission problem) on script launch : #16
  [laulaz]


1.2 (2017-05-15)
----------------

- Add Spanish translation.
  [macagua]

- Added more improvements about i18n support.
  [macagua]

- Added Buildout configuration file for Plone 4.3.x version.
  [macagua]

- Fix IOError: [Errno 2] No such file or directory: mr/migrator/autoinclude.zcml missing file.
  [macagua]

- Updated Buildout configuration file for Plone 3.3.x version.
  [macagua]

- Fix form problem with security hotfix 20160830
  [agitator]


1.1 (2015-10-22)
----------------

- Remove browserlayer registration, so the ``mr.migrator`` doesn't have to be
  installed to be used. Calling ``/@@mr.migrator`` is enough.

- Add uninstallation profile.
  [thet]

- Allow any pipeline configuration to be imported through the web at the
  ``@@mr.migrator`` view. Previously, only those pipelines were shown, which
  had a ``plone.app.transmogrifier.atschemaupdater`` blueprint included. Now
  any pipelines can be used, e.g. those which handle only Dexterity objects.
  [thet]

- Pep8.
  [thet]


1.0.1 (2012-09-18)
------------------

- put back in manual zcml loading [djay]

1.0 (2012-04-28)
----------------
- fix setup.py issue breaking buildout [djay]
- fixed NameError: global name 'cparser' is not defined, issue #6 [gborelli]
- fix default profile [toutpt]
- fix import error [toutpt]

1.0b11 (2012-04-25)
-------------------
- support pipeline includes [djay]

1.0b10 (2012-01-23)
-------------------

- Revert portion of ec799dcd3d, causing ConfigurationErrors
  [aclark]

1.0b9 (2012-01-23)
------------------

- Fix brown bag release (bad MANIFEST)
  [aclark]

1.0b8 (2012-01-23)
------------------

- Fix brown bag release (missing zcml)
  [aclark]

1.0b7 (2012-01-23)
------------------

- Look for pipeline.cfg in cwd
  [aclark]

1.0b6 (2012-01-23)
------------------

- Fix brown bag release
  [aclark]

1.0b5 (2012-01-22)
------------------

- Bug fix: support for --zcml arguments
  [aclark]

1.0b4 (2011-08-14)
------------------

- Bug fix: ZCML config
  [aclark]

1.0b3 (2011-08-14)
------------------

- Bug fix: ZCML config
  [aclark]

1.0b2 (2011-08-14)
------------------

- Bug fix: Python 2.4 compat
  [aclark]

1.0b1 (2011-06-29)
------------------

- allow way of running zcml for blueprint packages in commandline
  [djay]

- split out commandline runner from funnelweb
  [djay]

- add start of form for running transmogrifier inside plone
  [djay]
