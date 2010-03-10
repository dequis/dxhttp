import config
from dxhttp import deco, html
from dxhttp.read import read

MAP = [
    (r'^$', 'index'),
    (r'(^(img|css|js)/[A-Za-z0-9\._\-]*)', 'read'),
]

@deco.html
def index(environ, start_response):
    tpl = html.new('html')
    tpl.html.add('head').add('title', 'dxhttp')
    tpl.html.add('body').add('h1', 'It works!')
    return tpl
