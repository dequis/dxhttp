import re
import cgi
import sys
import Cookie
import dxhttp.exc
import dxhttp.utils

@dxhttp.exc.ExceptionMiddleware
def application(environ, start_response):
    get = environ.get
    environ['dxhttp.query_string'] = cgi.parse_qs(get('QUERY_STRING', ''))
    environ['dxhttp.cookies'] = Cookie.BaseCookie(get('HTTP_COOKIE', ''))
    environ['dxhttp.status'] = "200 OK"
    environ['dxhttp.headers'] = []

    import app
    reload(app)

    if hasattr(app, 'app_plug'):
        app.app_plug(environ, start_response)

    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex, func in app.MAP:
        match = re.search(regex, path)
        if match is not None:
            environ['dxhttp.args'] = match.groups()
            return getattr(app, func)(environ, start_response)

    start_response('404 Not found', [('content-type', 'text/plain')])
    return '404 Not found'

def start_server(module):
    dxhttp.utils.get_mod(module, 'dxhttp.srv').WSGIServer().run(application)

def main():
    import config
    mod = (len(sys.argv) > 1) and sys.argv[1] or config.SERVER_MODULE
    start_server(mod)

if __name__ == '__main__':
    main()
