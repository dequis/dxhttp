# does not require python2.5

import dxhttp.fcgi

class WSGIServer(object):
    '''Wrapper for Allan Saddi's fcgi.py to pass the app
    in the run() method instead of __init__()'''

    def run(self, app):
        dxhttp.fcgi.WSGIServer(app).run()
