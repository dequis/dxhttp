import config
from dxhttp import deco, html, utils

MAP = [
    (r'^$', 'index'),
    (r'^demo/([A-Za-z0-9\._\-]*)\.py$', 'get_demo'),
    (r'(^(img|css|js)/[A-Za-z0-9\._\-]*)', 'read'),
]

# in a real world app you would make a importer of "app", not "dxhttp"
# but the only external module that provides an app is dxhttp.read, so...
get = utils.make_importer(locals(), 'dxhttp', True)
get('read')

def navbar(tpl):
    ul = tpl.html.filter(tag="ul", id="navbar")[0]
    for mod in utils.get_mod_list("demos"):
        ul.tag("li").tag("a", href="/demo/%s" % mod).text(mod)

@deco.html
def index(environ, start_response):
    tpl = html.new(template='index.html')
    navbar(tpl)

    content = tpl.html.getElementById("content")
    content.text("Select one of the demos above")
    return tpl

@deco.html
@deco.args
def get_demo(environ, start_response, module):
    tpl = html.new(template='index.html')
    navbar(tpl)

    content = tpl.html.getElementById("content")
    utils.get_mod(module, "demos").main(environ, content)
    return tpl

