
import functools
from dxhttp.post import *


class FormValidationException(Exception):
    pass


def post(fields=[], ints=[], notnull=[]):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(environ, start_response, *args, **kwargs):
            if not is_post_request(environ):
                raise FormValidationException('POST only')
            
            form = get_post_form(environ)
            newform = {}
            for field in fields:
                try:
                    newform[field] = form[field].value
                except KeyError:
                    newform[field ] = ''

                if newform[field] is None or len(str(newform[field])) == 0:
                    raise FormValidationException('Field %s required' % field)

                if field in ints:
                    try:
                        newform[field] = int(newform[field])
                    except ValueError:
                        raise FormValidationException('Field %s must be int' % field)

            return f(environ, start_response, newform, *args, **kwargs)
        return wrapper
    return decorator
