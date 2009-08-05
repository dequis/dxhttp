import config

pre = lambda text: "<pre>%s</pre>" % text

def get_mod(name, path=config.APPDIR):
    return reload(__import__('.'.join([path, name]), globals(), locals(), ['main']))

def get_mod_list(path=config.APPDIR):
    import glob, os
    return [''.join(x.split("/")[1:]) for x in
            glob.glob(os.path.join(path, "*.py"))
            if not x.count("__init__.py")]

def list_mods():
    import glob, os
    return ', '.join(get_mod_list())

def get_qs(raw):
    return '?'.join(raw.split(" ")[1].split("?", 1)[1:])


def extend(base, new):
    '''Sets the defined methods in "new" to "base", where the latter
    is a class like xml.dom.minidom.Element'''
    import inspect

    for method in [name for (name, value) in inspect.getmembers(new)
                                          if inspect.ismethod(value)]:
        setattr(base, method, new.__dict__[method])
