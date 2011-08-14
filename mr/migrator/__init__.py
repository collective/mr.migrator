
# Add these early to avoid spurious ConfigurationErrors

import Products.Five
from Zope2.App.zcml import load_config

load_config("configure.zcml", Products.Five)
