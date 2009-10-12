pre = lambda text: "<pre>%s</pre>" % text

def get_mod(name, path=None, attrs=[]):
    import config
    if path:
        mod = __import__('.'.join([path, name]), fromlist=[''])
    else:
        mod = __import__(name)

    if config.DEBUG:
        mod = reload(mod)

    if not attrs:
        return mod
    else:
        return [getattr(mod, x) for x in attrs]

def make_importer(locals, path=None, selftitled=False):
    def get(name, *attrs):
        if not attrs and selftitled:
            attrs = [name]
        ret = get_mod(name, path, attrs)
        if attrs:
            for attr in attrs:
                locals[attr] = ret.pop(0)
        else:
            return ret
    return get

def get_mod_list(path):
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

def module_default(name, default):
    '''name should be __name__. Hack from:
    http://mail.python.org/pipermail/python-list/2007-January/062929.html
    '''

    class Wrapper(object):
        def __init__(self, wrapped):
            self.wrapped = wrapped

        def __repr__(self):
            return '<Module wrapper of %s, default=%s>' % (repr(self.wrapped), repr(default))

        def __getattr__(self, attr):
            return getattr(self.wrapped, attr, default)

    import sys
    sys.modules[name] = Wrapper(sys.modules[name])

