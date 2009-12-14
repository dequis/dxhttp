import config

import functools

def headers(**kwds):
    '''Appends the headers specified in **kwds to start_response.
    These may be overriden by the app using environ['dxhttp.headers']
    Underscores in kwds are turned into dashes, as in "Content_Type"
    There are two shortcuts below: @content_type and @html
    '''

    baseheaders = []
    for key, value in kwds.iteritems():
        key = key.replace("_", "-")
        baseheaders.append((key, value))

    def merge_headers(e):
        e.setdefault('dxhttp.headers', [])
        
        for key, value in baseheaders:
            if key.lower() not in [x[0].lower() for x in e['dxhttp.headers']]:
                e['dxhttp.headers'].append((key, value))

        return e['dxhttp.headers']

    def decorator(f):
        @functools.wraps(f)
        def wrapper(environ, start_response, *args, **kwargs):
            appiter = f(environ, start_response, *args, **kwargs)
            headers = merge_headers(environ)

            if 'dxhttp.decorated' in environ:
                return appiter
            environ['dxhttp.decorated'] = True
            
            status = environ.get('dxhttp.status', '200 OK')
            
            if appiter is None:
                appiter = ['None']

            start_response(status, headers)
            return appiter
        return wrapper
    return decorator

content_type = lambda x: headers(Content_Type=x)
html = headers(Content_Type=config.CONTENT_HTML)

def args(f):
    '''Expands dxhttp.args into actual function arguments'''
    @functools.wraps(f)
    def wrapper(environ, start_response, *args, **kwargs):
        return f(environ, start_response, *(environ['dxhttp.args'] + args), **kwargs)
    return wrapper



