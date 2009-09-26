import cgi

def is_post_request(environ):
    if environ['REQUEST_METHOD'].upper() != 'POST':
        return False
    content_type = environ.get('CONTENT_TYPE', 'application/x-www-form-urlencoded')
    return (content_type.startswith('application/x-www-form-urlencoded')
            or content_type.startswith('multipart/form-data'))

def get_post_form(environ):
    if not is_post_request(environ):
        return None

    input = environ['wsgi.input']
    post_form = environ.get('wsgi.post_form')
    if post_form:
        return post_form

    # This must be done to avoid a bug in cgi.FieldStorage
    environ.setdefault('QUERY_STRING', '')

    fs = cgi.FieldStorage(fp=input,
                          environ=environ,
                          keep_blank_values=1)
    new_input = InputProcessed()
    environ['wsgi.post_form'] = fs
    environ['wsgi.input'] = new_input
    return fs

class InputProcessed(object):
    def read(self, *args):
        raise EOFError('The wsgi.input stream has already been consumed')
    readline = readlines = __iter__ = read


