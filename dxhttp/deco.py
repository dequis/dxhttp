import config

import functools

def content_type(type):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(environ, start_response, *args, **kwargs):
            start_response('200 OK', [('content-type', type)])
            return f(environ, start_response, *args, **kwargs)
        return wrapper
    return decorator

html = content_type(config.CONTENT_HTML)

def args(f):
    '''Expands dxhttp.args into actual function arguments'''
    @functools.wraps(f)
    def wrapper(environ, start_response, *args, **kwargs):
        return f(environ, start_response, *(environ['dxhttp.args'] + args), **kwargs)
    return wrapper



