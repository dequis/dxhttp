import os
import cgi
import glob
import traceback
import functools
import cStringIO as StringIO

from dxhttp import utils
import config

def RogerExceptionMiddleware(app):
    @functools.wraps(app)
    def wrapper(environ, start_response):
        appiter = None
        try:
            appiter = app(environ, start_response)
            for item in appiter:
                yield item
        except:
            exception = traceback.format_exc()
            try:
                start_response('500 INTERNAL SERVER ERROR', [
                               ('Content-Type', 'text/plain')])
            except:
                yield '<pre>\n'

            yield exception

        if hasattr(appiter, 'close'):
            appiter.close()
    return wrapper

if config.DEBUG:
    try:
        from werkzeug import DebuggedApplication as ExceptionMiddleware
    except ImportError:
        ExceptionMiddleware = RogerExceptionMiddleware
else:
    # debug disabled
    ExceptionMiddleware = lambda app: app
