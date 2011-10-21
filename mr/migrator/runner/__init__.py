from collective.transmogrifier.transmogrifier import configuration_registry
from collective.transmogrifier.transmogrifier import Transmogrifier
from optparse import OptionParser, OptionGroup
from pkg_resources import resource_filename

import Products.GenericSetup
import logging
import mr.migrator
import sys

logging.basicConfig(level=logging.INFO)

try:
    import configparser
except ImportError:
    import ConfigParser as configparser
try:
    from Zope2.App.zcml import load_config
except:
    try:
        from Products.Five.zcml import load_config
    except:
        from zope.configuration.xmlconfig import XMLConfig as load_config
        load_config = lambda config, context: load_config(config, context)()


class Context:
    pass


class NoErrorParser(OptionParser):
    def error(self):
        pass


def runner(args={}, pipeline=None):
    # Make sure GS ZCML is loaded before we load ours
    load_config('autoinclude.zcml', mr.migrator)

    parser = OptionParser()

    parser.add_option("--pipeline", dest="pipeline",
                  help="Transmogrifier pipeline.cfg to use",
                  metavar="FILE")
    parser.add_option("--show-pipeline", dest="showpipeline",
                      action="store_true",
                      help="Show contents of the pipeline")
    parser.add_option("--zcml", dest="zcml",
                      action="store",
                      help="Load zcml")
    # Parse just the pipeline args
    ispipeline = lambda arg: [
        a for a in ['--pipeline', '--show-pipeline'] if arg.startswith(a)]
    pargs = [arg for arg in sys.argv[1:] if ispipeline(arg)]
    (options, cargs) = parser.parse_args(pargs)
    if options.pipeline is not None:
        config = options.pipeline
    elif pipeline is not None:
        config = pipeline
    else:
        config = resource_filename(__name__, 'pipeline.cfg')
    cparser = configparser.ConfigParser()
    context = Context()
    try:
        config_info = configuration_registry.getConfiguration(config)
        fp = open(config_info['configuration'])
        pipelineid = config
    except:
        fp = open(config)
        configuration_registry.registerConfiguration(
            u'transmogrify.config.mr.migrator',
            u"",
            u'', config)
        pipelineid = 'transmogrify.config.mr.migrator'

    try:
        # configparser
        cparser.read_file(fp)
    except:
        # ConfigParser
        cparser.read(config)

    fp.close()

    pipeline = [
        p.strip() for p in cparser.get('transmogrifier', 'pipeline').split()]
    for section in pipeline:
        if section == 'transmogrifier':
            continue
        if cparser.has_option(section, '@doc'):
            doc = cparser.get(section, '@doc')
        else:
            doc = ''
        group = OptionGroup(parser, section, doc)
        for key, value in cparser.items(section):
            if key.startswith('@'):
                if key == '@doc':
                    continue
                metavar, _, help = value.partition(': ')
                if metavar.upper() == metavar:
                    action = "store"
                else:
                    action = "store_true"
                    help = value
                group.add_option("--%s:%s" % (section, key[1:]), action=action,
                                             help=help,
                                             metavar=metavar)
        parser.add_option_group(group)
    pargs = [arg for arg in sys.argv[1:] if not arg.startswith('--template')]
    (options, cargs) = parser.parse_args(pargs)

    cargs = {}
    for k, _, v in [a.partition('=') for a in sys.argv[1:]]:
        k = k.lstrip('--')
        if ':' in k:
            part, _, key = k.partition(':')
            if key.lower() == 'debug':
                logger = logging.getLogger(part)
                logger.setLevel(logging.DEBUG)
            else:
                section = cargs.setdefault(part, {})
                if key in section:
                    section[key] = '%s\n%s' % (section[key], v)
                else:
                    section[key] = v
        else:
            pass
            #cargs[k] = v
    for k, v in cargs.items():
        args.setdefault(k, {}).update(v)

    overrides = {}
    if type(args) == type(''):
        for arg in args:
            section, keyvalue = arg.split(':', 1)
            key, value = keyvalue.split('=', 1)
            overrides.setdefault('section', {})[key] = value
    else:
        overrides = args

    if options.showpipeline:
        for section, values in overrides.items():
            for key,value in values.items():
                cparser.set(section, key, value)
        cparser.write(sys.stdout)
        return

    # delay this so arg processing not so slow
    load_config("meta.zcml", Products.GenericSetup)
    load_config("configure.zcml", Products.GenericSetup)

    load_config('configure.zcml', mr.migrator)

    if options.zcml:
        for zcml in options.zcml.split(','):
            if not zcml.strip():
                continue
            load_config('configure.zcml', __import__(zcml, fromlist=zcml.split('.')))

    transmogrifier = Transmogrifier(context)

    transmogrifier(pipelineid, **overrides)
