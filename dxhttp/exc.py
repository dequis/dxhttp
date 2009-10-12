import os
import cgi
import glob
import traceback
import functools
import cStringIO as StringIO

from dxhttp import sendmail
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


def MailExceptionMiddleware(mail, error_message):
    '''Sends the traceback to (mail)
    and displays (error_message) to the user'''

    def decorator(app):
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
                    pass
                yield error_message

                subject = "%s: %s" % (environ["SERVER_NAME"], exception.strip().split("\n")[-1])
                dump =  '\n'.join([': '.join(map(str, x)) for x in environ.items()])
                text = '%s\n\nEnviron dump:\n%s' % (exception, dump)
                sendmail.mail(to=mail, subject=subject, text=text, html=False)

        return wrapper
    return decorator


if config.DEBUG:
    try:
        from werkzeug import DebuggedApplication as ExceptionMiddleware
    except ImportError:
        ExceptionMiddleware = RogerExceptionMiddleware
else:
    # debug disabled
    ExceptionMiddleware = lambda app: app
