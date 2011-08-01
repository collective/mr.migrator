
import urllib
from zope.interface import Interface
from zope.schema import URI
from zope.schema import Int
from zope.schema import List
from zope.schema import Choice
from zope.schema import TextLine
from zope.schema import ASCIILine
from zope.schema import Bool
from zope.schema import Text
from zope.schema import URI
from zope.schema import Password
from zope.schema.vocabulary import SimpleVocabulary
from z3c.form import form
from z3c.form import field
from z3c.form import button
from z3c.form import group
from z3c.form import interfaces
from z3c.form.browser import multi
from plone.app.z3cform.layout import wrap_form
from collective.transmogrifier.transmogrifier import Transmogrifier
from collective.transmogrifier.transmogrifier import configuration_registry
from collective.transmogrifier.transmogrifier import _load_config
from mr.migrator.browser import MigratorMessageFactory as _
from mr.migrator.browser import logger




groupforms = {}

def formfactory(configname):
    if configname in groupforms:
        return groupforms[configname]
    groups = []
    config = _load_config(configname)
    sections = config['transmogrifier']['pipeline'].splitlines()
    print sections
    for section_id in sections:
        if not section_id:
            continue
        if section_id == 'transmogrifier':
            continue
        cparser = config[section_id]
        g = type(section_id, (group.Group,),dict(label=section_id.capitalize()))
        fields = []
        doc = cparser.get('@doc','')
        for key,value in cparser.items():
            if key in ['@doc','blueprint']:
                continue 
            if key.startswith('@'):
                key = key[1:]
                metavar,_,help = value.partition(':')
                default = unicode(cparser.get(key,''))
                help = value
            else:
                if '@'+key in cparser:
                    # let the @option line be used instead
                    continue
                else:
                    metavar = 'LINE'
                    default = unicode(value)
                    help = ''
            title = key.capitalize().replace('-',' ').replace('_',' ')
#                name = "%s:%s"%(section_id,key[1:])
            if metavar == 'HIDDEN':
                continue
            elif metavar == 'PASSWORD':
                ftype = Password()
            elif metavar == 'INT':
                ftype = Int()
                if default:
                    default = int(default)
                else:
                    default = 0
            #elif metavar == 'URL':
            #    ftype = URI()
            elif metavar == 'LIST' or '\n' in default:
                ftype = List(
                    value_type=TextLine(),)
                #ftype = Text()
                #if type(default) == type(""):
                default = default.splitlines()
                ftype.widgetFactory = multi.multiFieldWidgetFactory
            elif metavar.upper() != metavar:
                ftype = Bool()
                default = len(default)
            else:
                ftype = TextLine()
            ftype.__name__ = "%s-%s"%(section_id,key.replace('-', '_'))
            ftype.title=unicode(title)
            ftype.description=unicode(help)
            ftype.required=False
            ftype.default = default
            print (key,value,ftype,default)
            fields.append(ftype)
        if fields:
            g.fields = field.Fields(*fields)
            groups.append(g)
    groupforms[configname]=groups
    return groups

class IMigratorRun(Interface):
    """ remote source interface
    """

    config = ASCIILine  ()


class MigratorRun(group.GroupForm, form.Form):

    label = _(u"Synchronize and migrate")
    fields = field.Fields(IMigratorRun)
    ignoreContext = True

    def update(self):
        configname = self.request.get('form.widgets.config')
        self.groups = formfactory(configname)
        return super(MigratorRun, self).update()

    def updateWidgets(self):
        super(MigratorRun, self).updateWidgets()
        self.widgets['config'].mode = interfaces.HIDDEN_MODE

    @button.buttonAndHandler(u'Run')
    def handleRun(self, action):
        data, errors = self.extractData()
        if errors:
            return False

        overrides = {}
        for key, value in data.items():
            if '-' not in key:
                continue
            elif value is None:
                continue
            elif type(value) is list:
                value = '\n'.join(value)
            elif type(value) is bool:
                value = value and 'True' or 'False'
            else:
                value = str(value)
            section,key = key.split('-')
            overrides.setdefault(section, {})[key] = value

#        import ipdb; ipdb.set_trace()
        logger.info("Start importing profile: " + data['config'])
        Transmogrifier(self.context)(data['config'], **overrides)
        logger.info("Stop importing profile: " + data['config'])


class MigratorConfigurations(object):

    def __call__(self, context):
        terms = []
        for conf_id in configuration_registry.listConfigurationIds():
            print conf_id
            conf_file = _load_config(conf_id)
            for section_id in conf_file.keys():
                section = conf_file[section_id]
                if section.get('blueprint', '') == 'plone.app.transmogrifier.atschemaupdater':
                    conf = configuration_registry.getConfiguration(conf_id)
                    terms.append(SimpleVocabulary.createTerm(
                            conf_id, conf_id, conf['title']))
                    break
        return SimpleVocabulary(terms)


class IMigrator(Interface):
    """ remote source interface """

    config = Choice(
            title=_(u"Select configuration"),
            description=_(u"Registered configurations to choose from."),
            vocabulary=u"collective-migrator-configurations",
            )


class Migrator(form.Form):

    label = _(u"Synchronize and migrate")
    fields = field.Fields(IMigrator)

    ignoreContext = True

    @button.buttonAndHandler(u'Select')
    def handleSelect(self, action):
        data, errors = self.extractData()
        if errors:
            return False
        self.request.RESPONSE.redirect('%s/@@mr.migrator-run?form.widgets.%s' %
                (self.context.absolute_url(), urllib.urlencode(data)))


MigratorConfigurationsFactory = MigratorConfigurations()
MigratorRunView = wrap_form(MigratorRun)
MigratorView = wrap_form(Migrator)

