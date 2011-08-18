# -*- coding: utf-8 -*-
"""Recipe mr.migrator"""

from zc.recipe.egg.egg import Scripts

import logging
import os
import re
import shutil

logging.basicConfig(level=logging.DEBUG)


class Recipe(Scripts):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        args = {}
        for k, v in self.options.items():
            if '-' in k:
                part, key = k.split('-', 1)
                args.setdefault(part, {})[key] = v

        self.options['scripts'] = 'migrate=%s' % name

        self.options['eggs'] = """
                mr.migrator
                """ + self.options.get('eggs', '')
        pipeline = self.options['pipeline']
        if ':' in pipeline:
            package, pipeline_name = pipeline.split(':')
            self.options['eggs'] += "  %s" % package

        pipeline = self.options.get('pipeline', None)
        if pipeline:
            self.options['arguments'] = str(args) + ',"' + pipeline + '"'
        else:
            self.options['arguments'] = str(args)

        # Process zcml
        partsdir = self.buildout['buildout']['parts-directory']
        newdir = partsdir + '/migrate'
        if not os.path.exists(newdir):
            os.mkdir(newdir)

        newdir = partsdir + '/migrate/etc'
        if not os.path.exists(newdir):
            os.mkdir(newdir)

        self.options['location'] = self.buildout['buildout']['parts-directory'] + '/migrate'
        if 'zcml' in options:
            self.build_package_includes()

        return Scripts.__init__(self, buildout, name, options)

    def install(self):
        """Installer"""
        # XXX Implement recipe functionality here
        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return Scripts.install(self)

    def update(self):
        """Updater"""
        return Scripts.update(self)

    # Borrowed from p.r.zope2instance
    def build_package_includes(self):
        """Create ZCML slugs in etc/package-includes
        """
        location = self.options['location']
        sitezcml_path = os.path.join(location, 'etc', 'site.zcml')
        zcml = self.options.get('zcml')
        site_zcml = self.options.get('site-zcml')
        additional_zcml = self.options.get("zcml-additional")
        resources = self.options.get("resources")

        if site_zcml:
            open(sitezcml_path, 'w').write(site_zcml)
            return

        if zcml:
            zcml = zcml.split()

        if additional_zcml or resources or zcml:
            includes_path = os.path.join(location, 'etc', 'package-includes')

            if not os.path.exists(includes_path):
                # Zope 2.9 does not have a package-includes so we
                # create one.
                os.mkdir(includes_path)
            else:
                if zcml and '*' in zcml:
                    zcml.remove('*')
                else:
                    shutil.rmtree(includes_path)
                    os.mkdir(includes_path)

        if additional_zcml:
            path=os.path.join(includes_path, "999-additional-overrides.zcml")
            open(path, "w").write(additional_zcml.strip())

        if resources:
            resources_path = resources.strip()
            path=os.path.join(includes_path, "998-resources-configure.zcml")
            open(path, "w").write(
                resources_zcml % dict(directory=resources_path)
                )

            if not os.path.exists(resources_path):
                os.mkdir(resources_path)

        if zcml:
            n = 0
            package_match = re.compile('\w+([.]\w+)*$').match
            for package in zcml:
                n += 1
                orig = package
                if ':' in package:
                    package, filename = package.split(':')
                else:
                    filename = None

                if '-' in package:
                    package, suff = package.split('-')
                    file_suff = suff
                    if suff not in ('configure', 'meta', 'overrides'):
                        file_suff = '%s-configure' % suff
                else:
                    suff = file_suff = 'configure'

                if filename is None:
                    filename = suff + '.zcml'

                if not package_match(package):
                    raise ValueError('Invalid zcml', orig)

                path = os.path.join(
                    includes_path,
                    "%3.3d-%s-%s.zcml" % (n, package, file_suff),
                    )
                open(path, 'w').write(
                    '<include package="%s" file="%s" />\n'
                    % (package, filename)
                    )

