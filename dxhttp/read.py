'''read.py
Reads static files, for the builtin http server
'''

from dxhttp import deco

import os
import mimetypes

@deco.args
def read(environ, start_response, filename, *args):
    if os.path.exists(filename):
        content, encoding = mimetypes.guess_type(filename)
        headers = [('Content-Type', content),
                   ('Content-Encoding', encoding)]
        start_response('200 OK', [x for x in headers if x[1]])
        return open(filename)
    else:
        start_response('404 Not found', [('Content-Type', 'text/plain')])
        return '404 Not found'
