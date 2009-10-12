import os
import cgi
import glob
import traceback
import functools
import cStringIO as StringIO

from dxhttp import utils
import config

STATUS = '500 INTERNAL SERVER ERROR'
HEADERS = [('Content-Type', 'text/plain')]

def RogerExceptionMiddleware(app):
    @functools.wraps(app)
    def wrapper(environ, start_response):
        try:
            appiter = app(environ, start_response)
            for item in appiter:
                yield item
        except:
            exception = traceback.format_exc()
            try:
                start_response(STATUS, HEADERS)
            except:
                yield '<pre>\n'

            yield exception
    return wrapper

if config.DEBUG:
    try:
        from werkzeug import DebuggedApplication as ExceptionMiddleware
    except ImportError:
        ExceptionMiddleware = RogerExceptionMiddleware
else:
    # debug disabled
    ExceptionMiddleware = lambda app: app
