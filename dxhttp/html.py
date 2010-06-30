from dxhttp.utils import extend
from dxhttp.replacer import Replacer 
from config import TPL_ROOT

import xml.dom.minidom
import functools
import os.path

DOCTYPE = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'

class Base(object):
    def __init__(self, basetag='html', template=None, vars={}):

        if template:
            f = Replacer(os.path.join(TPL_ROOT, template), vars)
            self.document = xml.dom.minidom.parse(f)
        else:
            self.document = xml.dom.minidom.getDOMImplementation() \
                .createDocument(None, basetag, None)

        # make it global
        xml.dom.minidom.Element.documentObject = self.document
        
        # <html>
        self.html = self.document.documentElement
        
        self.write_function = self.html.toxml

    def write(self, file):
        '''Writes to a file-like object'''
        file.write(self.write_function(encoding="utf-8"))

    def __iter__(self):
        '''Returns the value of this object as an iterator'''
        return [DOCTYPE, self.write_function(encoding="utf-8")].__iter__()

def new(tag='html', template=None, vars={}):
    return Base(tag, template, vars)

def fix_attrs_names(f):
    '''Internal decorator that replaces kwargs
    with keys such as "class_" into "class"'''
    @functools.wraps(f)
    def wrapper(*args, **attrs):
        for attr in attrs.copy():
            if attr.endswith("_"):
                attrs[attr[:-1]] = attrs[attr]
                del attrs[attr]
        return f(attrs=attrs, *args)
    return wrapper

class Element(object):

    @fix_attrs_names
    def add(self, name, text=None, attrs={}):
        '''Appends to self a child tag of "name", with content "text"
        and attributes "kwds"'''

        tag = self.documentObject.createElement(name)
        tag.text(text)
        tag.attrs(**attrs)
        self.appendChild(tag)
        return tag

    @fix_attrs_names
    def attrs(self, attrs={}):
        for (name, value) in attrs.iteritems():
            self.setAttribute(name, value)
        
        return self

    def addtext(self, text):
        '''Appends to self a text node of content "text"'''
        if text:
            if isinstance(text, str):
                text = text.decode("utf-8", "replace")
            elif not isinstance(text, unicode):
                text = str(text).decode("utf-8", "replace")
            textnode = self.documentObject.createTextNode(text)
            self.appendChild(textnode)
        return self
     
    # backwards compatibility, these do not work with etree implementation
    tag = add
    text = addtext

    def getElementById(self, id):
        return self.filter(id=id)[0]

    @fix_attrs_names
    def filter(self, tag="*", attrs={}):
        def matches(x):
            for key, value in attrs.iteritems():
                if x.getAttribute(key) == value:
                    if key == "title":
                        x.setAttribute(key, "")
                    return True
            return False

        if not attrs:
            matches = lambda x: True

        return [x for x in
            self.getElementsByTagName(tag)
            if matches(x)]

    def template(self, filename, vars={}):
        '''Parses "filename" and appends it contents to self'''
        path = os.path.join(TPL_ROOT, filename) 
        if os.path.exists(path):
            f = Replacer(path, vars)
            self.appendChild(xml.dom.minidom.parse(f).documentElement)
            return True
        else:
            return False

    def html(self, html):
        '''Appends html. Must be wrapped in some tag'''
        self.appendChild(xml.dom.minidom.parseString(html).documentElement)

extend(xml.dom.minidom.Element, Element)
