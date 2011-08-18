Mr.Migrator: Drive-by transmogrification made easy!
***************************************************

mr.migrator is a transmogrifier pipeline runner, either
via the commandline or as a Plone add-on.

- Code repository: http://github.com/collective/mr.migrator
- Questions and comments to http://github.com/collective/mr.migrator/issues
- Report bugs at http://github.com/collective/mr.migrator/issues

.. contents::

Introduction
------------

Transmogrifier is a powerful tool for creating transformation processes called "pipelines".
Transmogrifier gives you the tools to create and share these pipelines but doesn't provide
an easy way to run the pipeline. Mr.migrator aims to bridge that gap.

Mr.Migrator provides the following:

- A buildout recipe with you can override a given pipeline and will also create a
  the commandline script to run the pipeline.
- A commandline script with help which lets you run pipelines and see their progress. This
  is useful used in conjunction with `transmogrify.ploneremote`_ or other blueprints which
  don't need expect to be run inside the `Plone`_ process.
- A Plone plugin which when installed lets you pick which pipeline you want to run,
  provides a form to override the pipeline options and then provides progress on the running
  pipeline. This is useful when you want to use `plone.app.transmogrifier`_ blueprints
  which expect to be run inside the `Plone`_ process.

Getting a pipeline
------------------

A pipeline is a concept from `collective.transmogrifier`_ where dictionary items pass there a series
of steps, each adding, removing or uploading information to an external source. A pipeline
is configured in configuration file using the INI style syntax. Mr.Migrator lets you run either
pipelines you built yourself, or

Build your own pipeline
~~~~~~~~~~~~~~~~~~~~~~~
see collective.transmogrifer `pipelines`_ for more details.

Once you've created your pipeline .cfg you can use it on the commandline via ::

 migrate --pipeline=mypipeline.cfg

or if installing via buildout ::

  [migrate]
  recipe = mr.migrator
  pipeline = mypipeline.cfg

If you're using blueprints in your pipeline you will need to ensure that zcml configuration
that registers them is executed. If you are using buildout you can use the following ::

  [buildout]
  parts += mr.migrator

  [migrator]
  recipe = mr.migrator
  pipeline = mypipeline.cfg
  eggs = transmogrify.sqlalchemy
  zcml = transmogrify.sqlalchemy

This will ensure that the package that contains the blueprints is downloaded and the zcml for it
is run before the pipeline is run so that the blueprints are registered.

If you aren't using buildout you can will need to tell the runner which packages to load zcml in via ::

 migrate --zcml=transmogrify.sqlalchemy,transmogrify.other

If you the blueprint package includes the following entry_point you can skip the zcml settings above ::

  entry-points = {"z3c.autoinclude.plugin":['target = transmogrify']}


There currently isn't a way to run a custom pipeline if using the Plone plugin. You will have
to register it as below.

Using a Registered Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If a pipeline has been registered inside another package via zcml such as ::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:transmogrifier="http://namespaces.plone.org/transmogrifier"
        i18n_domain="collective.transmogrifier">

    <transmogrifier:registerConfig
        name="exampleconfig"
        title="Example pipeline configuration"
        description="This is an example pipeline configuration"
        configuration="example.cfg"
        />

    </configure>

and the package has an entry point that will enable the zcml to be loaded such as ::

      entry_points = {"z3c.autoinclude.plugin":['target = transmogrify']}

Then you can get mr.migrator to run that pipeline via ::

  migrate --pipeline=exampleconfig

or ::

  [migrate]
  recipe = mr.migrator
  pipeline = exampleconfig

An example of a package which declares a pipeline designed to be overridden is `funnelweb`_.


Overriding pipeline values
--------------------------

Pipelines are organised as a series of steps through which crawled items pass before eventually being
uploaded. Each step as one or more configuration options so you can customise import process
for your needs. Almost all imports will require some level of configurations.

The first part of each configuration key is the step e.g. `crawler`. The second part is the particular
configuration option for that particular step. e.g. `url`. This is then followed by = and value or values.

The configuration options can either be given as part of the buildout part e.g. ::

  [buildout]
  parts += mr.migrator

  [mr.migrator]
  recipe = mr.migrator
  crawler-url=http://www.whitehouse.gov

or the same option can be overridden via the command line ::

 $> bin/migrate --crawler:url=http://www.whitehouse.gov

some options require multiple lines within a buildout part. These can be overridden
via the commandline by repeating the same argument e.g. ::

  $> bin/migrate --crawler:ignore=\.mp3 --crawler:ignore=\.pdf


You use the commandline help to view the list of available options ::

  $> bin/migrate --help



Controlling Logging
~~~~~~~~~~~~~~~~~~~

You can show additional debug output on any particular set by setting a debug commandline switch.
For instance to see see additional details about template matching failures ::

  $> bin/mr.migrator --template1:debug
  
  

Working directly with transmogrifier (advanced)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You might need to insert further transformation steps for your particular
conversion usecase. To do this, you can extend a plugins underlying
transmogrifier pipeline. mr.migrator uses a transmogrifier pipeline to perform the needed transformations and all
commandline and recipe options refer to options in the pipeline.


You can view pipeline and all its options via the following command ::

 $> bin/mr.migrator --show-pipeline

You can also save this pipeline and customise it for your own needs ::

 $> bin/mr.migrator --show-pipeline > pipeline.cfg
 $> {edit} pipeline.cfg
 $> bin/mr.migrator --pipeline=pipeline.cfg

Customising the pipeline allows you add your own personal transformations which
haven't been pre-considered by the standard mr.migrator tool.

See transmogrifier documentation to see how to add your own blueprints or add blueprints that
already exist to your custom pipeline.

Using external blueprints
~~~~~~~~~~~~~~~~~~~~~~~~~

If you have decided you need to customise your pipeline and you want to install transformation
steps that use blueprints not already included in mr.migrator or transmogrifier, you can include
them using the ``eggs`` option in a mr.migrator buildout part ::

  [mr.migrator]
  recipe = mr.migrator
  eggs = myblueprintpackage
  pipeline = mypipeline.cfg

However, this only works if your blueprint package includes the following setuptools entrypoint
in its ``setup.py`` ::

      entry_points="""
            [z3c.autoinclude.plugin]
            target = transmogrify
            """,
            )

.. NOTE:: Some transmogrifier blueprints assume they are running inside a Plone
   process such as those in `plone.app.transmogrifier` (see http://pypi.python.org/pypi/plone.app.transmogrifier).  mr.migrator
   doesn't run inside a Plone process so these blueprints won't work. If
   you want upload content into Plone, you can instead use
   transmogrify.ploneremote which provides alternative implementations
   which will upload content remotely via XML-RPC.
   ``transmogrify.ploneremote`` is already included in funnelweb as it is
   what funnelweb's default pipeline uses.

Help syntax for pipeline configuration
--------------------------------------

TODO

Mr.Migrator in Plone
--------------------

***under development***

Mr.Migrator needs to be combined with a package providing a registered pipeline.

1. Install mr.migrator into your buildout
2. Install a package providing your pipeline such as funnelweb or collective.jsonmigrator
3. Go to the place in your site where you want to import content and select Actions > Mr.Migrate here
4. Pick the pipeline you want from the drop down list
5. A form for filling in extra configuration for your pipeline will displayed
   (either autogenerated from the .cfg or a form designed by the pipeline author)
6. Click run
7. Popup a progress feedback dialog with a log of activity

TODO
----

- Finish autoform so works in all cases
- combine argsparse and autoform code
- do progress dialog
- hook point for packages to register form along with pipeline
- when no pipelines found: display help on where to find them and how to install them


Contributing
------------

- Code repository: http://github.com/collective/mr.migrator
- Questions and comments to http://github.com/collective/mr.migrator/issues
- Report bugs at http://github.com/collective/mr.migrator/issues


Thanks
------

- Alex Clark - for the name
- Rok Garbas - the original code for the z3cform
- Dylan Jay - the original code of the commandline runner


.. _`pipelines`: http://pypi.python.org/pypi/collective.transmogrifier/#pipelines
.. _`collective.transmogrifier`: http://pypi.python.org/pypi/collective.transmogrifier
.. _`funnelweb`: http://pypi.python.org/pypi/funnelweb
.. _`plone`: http://plone.org
.. _`plone.app.transmogrifier`: http://pypi.python.org/pypi/plone.app.transmogrifier
.. _`transmogrify.ploneremote`: http://pypi.python.org/pypi/transmogrify.ploneremote


