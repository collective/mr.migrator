
# Add these early to avoid spurious ConfigurationErrors

try:
    eval("1 if True else 2")  # http://stackoverflow.com/questions/446052
    import Products.Five
    from Zope2.App.zcml import load_config
    load_config("configure.zcml", Products.Five)
    load_config("configure.zcml", Products.GenericSetup)
except:
    pass
