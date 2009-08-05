# requires python2.5 (wsgiref)

import config
from wsgiref.simple_server import make_server

class WSGIServer(object):
    '''Wrapper to use simple_server like the other servers'''

    def run(self, app):
        print "Listening at http://0.0.0.0:" + str(config.PORT)
        make_server('', config.PORT, app).serve_forever()
