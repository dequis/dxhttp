
def do(environ, url, status='302 Found'):
    environ['dxhttp.status'] = status
    environ.setdefault('dxhttp.headers', []).append(('Location', url))
