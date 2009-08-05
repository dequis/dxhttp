#!/usr/bin/env python

import urllib
import xml.dom.minidom

API_KEY = "b25b959554ed76058ac220b7b2e0a026"
BASE_URL = "http://ws.audioscrobbler.com/2.0/?"

params = {
    "method": "tasteometer.compare",
    "type1": "user",
    "type2": "user",
    "limit": 200,
    "api_key": API_KEY,
}

def main(environ, node):
    node.tag("p", "last.fm compat list. Params:")
    ul = node.tag("ul")
    ul.tag("li", "v1: last.fm username")
    ul.tag("li", "v2: last.fm username")
    
    query_string = environ['dxhttp.query_string']
    try:
        params['value1'] = query_string['v1'][0]
        params['value2'] = query_string['v2'][0]
    except KeyError:
        return

    url = BASE_URL + urllib.urlencode(params)
    xmlstring = urllib.urlopen(url).read()
    doc = xml.dom.minidom.parseString(xmlstring)

    p = node.tag("p")
    p.tag("b", params['value1'])
    p.text(" and ")
    p.tag("b", params['value2'])
    
    ul = node.tag("ul")
    for artist in doc.getElementsByTagName("artist"):
        ul.tag("li", artist.getElementsByTagName("name")[0].firstChild.nodeValue)
