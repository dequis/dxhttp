import html

def main(environ, node):
    lol = node.tag('div', id="lol")
    lol.tag("h1", "lol")
    lol.tag("p", "ololol: ").tag("b", "LOL")
    node.tag("hr")
    node.tag("h2", "lol'd").tag("sup", "tm")
