'''html_etree.py. ElementTree-based implementation of dxhtml
Features:
    -Much less nitpicky about unicode, base tags in templates, html entities.

API differences:
    -tag() is now add()
    -text() is now addtext()
'''

from dxhttp.utils import extend
from dxhttp.replacer import Replacer 
from config import TPL_ROOT

from subprocess import Popen, PIPE
from xml.parsers.expat import ExpatError
import xml.etree.ElementTree as ET
import xml.etree.cElementTree as cET
import xml.dom.minidom
import functools
import os.path
import re

DOCTYPE = '<!DOCTYPE html>'

class Base(object):
    def __init__(self, basetag='html', template=None, vars={}):
        
        if template:
            f = Replacer(os.path.join(TPL_ROOT, template), vars)
            self.document = ET.parse(f)
        else:
            self.document = ET.ElementTree(ET.Element(basetag))

        # make it global
        xml.dom.minidom.Element.documentObject = self.document
        
        # <html>
        self.html = self.document.getroot()
        
        self.write_function = ET.tostring

    def write(self, file):
        '''Writes to a file-like object'''
        file.write(self.write_function(self.document, encoding="utf-8"))

    def __iter__(self):
        '''Returns the value of this object as an iterator'''
        return [DOCTYPE, self.write_function(self.html, encoding="utf-8")].__iter__()

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

XMLNS_RE = re.compile('^<html xmlns.*$', re.M)

def XML_safe(html, filename=None):
    '''Tries to read a string with ET.XML, and if it fails, pass it
    through html tidy, addressing common xml parsing errors.
    If a filename is specified, html is read from there, and written back.
    If the html string is clean (no ExpatError), this is the same as ET.XML'''
    
    try:
        return ET.XML(html)  
    except ExpatError:
        pass
        
    if filename:
        # don't save back replaced variables
        # caveat: we output without replacement...
        html = open(filename).read()
    
    # -n numeric entities, -q quiet
    # --input-encoding utf8, but still output as numeric entities
    # --output-xml 1, close tags such as <br />, but don't enforce XHTML            
    tidy = Popen(['tidy', '-nq', '--input-encoding', 'utf8', '--output-xml', '1'], stdin=PIPE, stdout=PIPE, stderr=PIPE)    
    stdout, stderr = tidy.communicate(html)

    # remove xmlns to avoid having it in every attribute
    # ...and parse that string as XML
    newxml = ET.XML(XMLNS_RE.sub('<html>', stdout))
    
    # ignore html and head
    body = newxml.find("body")
    body.tag = 'div'
    if len(body) == 1 and body[0].tag == 'div':
        # avoid having multiple divs as body
        body = body[0]
    
    if filename:
        # write the clean document back
        open(filename, "w").write(ET.tostring(body))
        
    return body        

class Element:
    @fix_attrs_names
    def add(self, name, text=None, attrs={}):
        '''Appends to self a child tag of "name", with content "text"
        and attributes "kwds"'''
        tag = ET.SubElement(self, name, attrs)
        tag.text = text
        return tag

    def addtext(self, text):
        # this function sucks a lot
        if len(self):
            if self[-1].tail is None:
                self[-1].tail = ''
            self[-1].tail += text
        else:
            if self.text is None:
                self.text = ''
            self.text += text
        return self

    @fix_attrs_names
    def attrs(self, attrs={}):
        for (name, value) in attrs.iteritems():
            self.set(name, value)
        
        return self

    def getElementById(self, id):
        return self.filter(id=id)[0]

    @fix_attrs_names
    def filter(self, tag='*', attrs={}):
        def matches(element):
            for key, value in attrs.iteritems():
                if element.get(key) == value:
                    return True
            return False
        
        if not attrs:
            matches = lambda x: True

        return [x for x in self.getiterator(tag) if matches(x)]

    def template(self, filename, vars={}):
        '''Parses "filename" and appends it contents to self'''
        path = os.path.join(TPL_ROOT, filename) 
        if os.path.exists(path):
            f = Replacer(path, vars)
            self.append(XML_safe(f.read(), path))
            return True
        else:
            return False

    def html(self, html):
        '''Appends html. Must be wrapped in some tag'''
        self.append(XML_safe(html))

extend(ET._ElementInterface, Element)
