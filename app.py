import config
from dxhttp import deco, html, utils

# static files
from dxhttp.read import read

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

