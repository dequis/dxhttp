'''Higher-level form parser that ensures that required fields are there
and converts specified fields to ints. The parsed form is passed to the
function as a third parameter, "form".

If there are errors, the original function is not called and an error
message is returned instead (if doraise=False) or FormValidationException
is raised (if doraise=True, duh)

File uploads not supported yet, but are easy to implement.

Usage:
    
    @deco.html
    @validate.post(fields=['name', 'address', 'age', 'comments'],
                   ints=['age'],
                   notnull=['name', 'address', 'age'])
    def submit_something(environ, start_response, form):
        if form['age'] < 13:
            return ['this is illegal']
        return ['right']
'''

import cgi
import functools
import dxhttp.post

class FormValidationException(Exception):
    pass

def _validate(environ, method, fields, ints, notnull, dicts):
    '''Validates a form a returns a dict with the values
    
    -method: POST or GET
    -fields: keys to include in the dict. Missing fields default to ''
    -ints: fields that are converted to int
    -notnull: required fields

    Not meant to be used directly, try the "post" and "get" decorators instead
    '''
    
    if method == 'POST':
        if not dxhttp.post.is_post_request(environ):
            raise FormValidationException('POST only')
        form = dxhttp.post.get_post_form(environ)
    else:
        form = cgi.FieldStorage(environ=environ, keep_blank_values=1)

    newform = {}
    for field in fields:
        try:
            if type(form[field]) == list:
                newform[field] = form[field][0].value
            else:
                newform[field] = form[field].value
        except KeyError:
            newform[field] = ''

        if field in notnull and \
           (newform[field] is None or len(str(newform[field])) == 0):
            raise FormValidationException('Field %s required' % field)

        if field in ints:
            try:
                newform[field] = int(newform[field])
            except ValueError:
                if len(str(newform[field])) != 0:
                    raise FormValidationException('Field %s must be int' % field)
    
    for basename in dicts:
        newform[basename] = {}
        for field in form.keys():
            if field.startswith(basename + "["):
                key = field.split("[")[1].split("]")[0]
                newform[basename][key] = form[field].value
    return newform

def deco(method, fields=[], ints=[], notnull=[], dicts=[], doraise=False):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(environ, start_response, *args, **kwargs):
            try:
                newform = _validate(environ, method, fields, ints, notnull, dicts)
            except FormValidationException, e:
                if doraise:
                    raise
                else:
                    return ['Form validation error: %s' % e]
            return f(environ, start_response, newform, *args, **kwargs)
        return wrapper
    return decorator

def post(fields=[], ints=[], notnull=[], dicts=[], doraise=False):
    return deco('POST', fields, ints, notnull, dicts, doraise)

def get(fields=[], ints=[], notnull=[], dicts=[], doraise=False):
    return deco('GET', fields, ints, notnull, dicts, doraise)
