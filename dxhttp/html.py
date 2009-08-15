from dxhttp.utils import extend
from config import TPL_ROOT

import xml.dom.minidom
import functools
import os.path

DOCTYPE = '<!DOCTYPE html>'

class Base(object):
    def __init__(self, basetag='html', template=None):

        if template:
            self.document = xml.dom.minidom.parse(os.path.join(TPL_ROOT, template))
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

def new(tag='html', template=None):
    return Base(tag, template)

def fix_attrs_names(f):
    '''Internal decorator that replaces kwargs
    with keys such as "class_" into "class"'''
    @functools.wraps(f)
    def wrapper(*args, **attrs):
        for attr in attrs.copy():
            if attr.endswith("_"):
                attrs[attr[:-1]] = attrs[attr]
                del attrs[attr]
        return f(*args, attrs=attrs)
    return wrapper

class Element(object):

    @fix_attrs_names
    def tag(self, name, text=None, attrs={}):
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

    def text(self, text):
        '''Appends to self a text node of content "text"'''
        if text:
            if isinstance(text, str):
                text = text.decode("utf-8")
            elif not isinstance(text, unicode):
                text = str(text).decode("utf-8")
            textnode = self.documentObject.createTextNode(text)
            self.appendChild(textnode)
        return self

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

        return [x for x in
            self.getElementsByTagName(tag)
            if matches(x)]

    def template(self, filename):
        '''Parses "filename" and appends it contents to self'''
        filename = os.path.join(TPL_ROOT, filename)
        self.appendChild(xml.dom.minidom.parse(filename).documentElement)

    def html(self, html):
        '''Appends html. Must be wrapped in some tag'''
        self.appendChild(xml.dom.minidom.parseString(html).documentElement)

extend(xml.dom.minidom.Element, Element)
