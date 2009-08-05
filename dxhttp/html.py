from dxhttp.utils import extend
from config import TPL_ROOT

import xml.dom.minidom
import os.path

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
        return ['<!DOCTYPE html>', self.write_function(encoding="utf-8")].__iter__()

def new(tag='html', template=None):
    return Base(tag, template)

class Element(object):
    def tag(self, name, text=None, **attrs):
        '''Appends to self a child tag of "name", with content "text"
        and attributes "kwds"'''

        tag = self.documentObject.createElement(name)
        tag.text(text)
        tag.attrs(**attrs)
        self.appendChild(tag)
        return tag

    def attrs(self, **attrs):
        if 'class_' in attrs:
            attrs['class'] = attrs['class_']
            del attrs['class_']

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

    def filter(self, tag="*", **attrs):
        if 'class_' in attrs:
            attrs['class'] = attrs['class_']
            del attrs['class_']
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

extend(xml.dom.minidom.Element, Element)
