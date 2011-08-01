
from collective.transmogrifier.transmogrifier import Transmogrifier
from zope.publisher.browser import BrowserPage

usage = 'Usage: curl http://admin:admin@localhost:8080/Plone/@@migrate/<pipeline>'

class TTWPipelineExecutor(BrowserPage):
    def __call__(self):
        return usage

    def publishTraverse(self, request, name):
        transmogrifier = Transmogrifier(self.context)
        try:
            transmogrifier(name)
            return 'Done: %s!' % name

        except:
            import sys, traceback
            return traceback.format_exc(sys.exc_info()[2])
