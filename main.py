#!/usr/bin/python

import re
import sys
import cgi
import Cookie

import config
import dxhttp.utils
import dxhttp.exc

@dxhttp.exc.ExceptionMiddleware
def application(environ, start_response):
    get = environ.get
    environ['dxhttp.query_string'] = cgi.parse_qs(get('QUERY_STRING', ''))
    environ['dxhttp.cookies'] = Cookie.BaseCookie(get('HTTP_COOKIE', ''))
    environ['dxhttp.status'] = "200 OK"
    environ['dxhttp.headers'] = []

    import app
    reload(app)

    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, func in app.MAP:
        match = re.search(regex, path)
        if match is not None:
            environ['dxhttp.args'] = match.groups()
            return getattr(app, func)(environ, start_response)

    start_response('404 Not found', [('content-type', 'text/plain')])
    return '404 Not found'


def main(mod=None):
    if mod is None:
        mod = (len(sys.argv) > 1) and sys.argv[1] or config.SERVER_MODULE
    dxhttp.utils.get_mod(mod, 'dxhttp.srv').WSGIServer().run(application)

if __name__ == '__main__':
    main()
