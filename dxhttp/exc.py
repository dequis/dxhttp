import os
import cgi
import glob
import traceback
import cStringIO as StringIO

from dxhttp import utils
import config

class RogerExceptionMiddleware(object):
    '''Exception Middelware'''

    def __init__(self, app, _bool=True):
        self.app = app

    def __call__(self, environ, start_response):
        '''catch exceptions'''
        appiter = None
        try:
            appiter = self.app(environ, start_response)
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


if config.DEBUG:
    try:
        from werkzeug import DebuggedApplication
        # replace
        ExceptionMiddleware = DebuggedApplication
    except ImportError:
        ExceptionMiddleware = RogerExceptionMiddleware
else:
    # debug disabled
    ExceptionMiddleware = lambda app, _bool: app
