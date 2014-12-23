
# Add these early to avoid spurious ConfigurationErrors

try:
    eval("1 if True else 2")  # http://stackoverflow.com/questions/446052
    from Zope2.App.zcml import load_config
    import Products.Five
    load_config("configure.zcml", Products.Five)
    import Products.GenericSetup
    load_config("meta.zcml", Products.GenericSetup)
    load_config("configure.zcml", Products.GenericSetup)
except SyntaxError:
    # doesn't have ternary
    pass
