#!/usr/bin/python

import re
import sys
import cgi

import config
import dxhttp.utils
import dxhttp.exc

MAP = [
    (r'^$', 'index'),
    (r'^demo/([A-Za-z0-9\._\-]*)\.py$', 'get_demo'),
    (r'(^(img|css|js)/[A-Za-z0-9\._\-]*)', 'read'),
]

@dxhttp.exc.ExceptionMiddleware
def application(environ, start_response):
    query_string = cgi.parse_qs(environ.get('QUERY_STRING', None))
    environ['dxhttp.query_string'] = query_string

    import app
    reload(app)

    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, func in MAP:
        match = re.search(regex, path)
        if match is not None:
            environ['dxhttp.args'] = match.groups()
            return getattr(app, func)(environ, start_response)

    start_response('404 Not found', [('content-type', 'text/plain')])
    return '404 Not found'


def main():
    mod = (len(sys.argv) > 1) and sys.argv[1] or config.SERVER_MODULE
    dxhttp.utils.get_mod(mod, 'dxhttp.srv').WSGIServer().run(application)

if __name__ == '__main__':
    main()
