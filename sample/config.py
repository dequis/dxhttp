PORT = 8080
DEBUG = True

SERVER_MODULE = 'http' # http, fcgi, cgi

CONTENT_HTML = 'text/html'
TPL_ROOT = 'templates/'

from dxhttp.utils import module_default
module_default('config', '')
