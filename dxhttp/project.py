import os
import sys
import shutil
import urllib
import optparse

from pkg_resources import Requirement, resource_filename, resource_string

LIBS = {
    'jquery': ('http://ajax.googleapis.com/ajax/libs/jquery/%s/jquery.min.js', '1.3'),
    'jqueryui': ('http://ajax.googleapis.com/ajax/libs/jqueryui/%s/jquery-ui.min.js', '1.7'),
}

SKELETON = {
    'dirs': ['', 'templates', 'css', 'images', 'js'],
    'files': ['config.py', 'app.py'],
}

FCGI_MODE = 0755

def main():
    parser = optparse.OptionParser()
    parser.add_option("-n", "--new", action="store_true")
    parser.add_option("-d", "--directory")
    parser.add_option("-l", "--jslib", action="append", default=[])
    parser.add_option("-p", "--python-binary")

    options, args = parser.parse_args()

    if len(args) == 0:
        parser.error('Project name required')
    
    project = args[0]
    
    # do the changes 
    projectpath = options.directory or project

    for dirname in SKELETON['dirs']:
        path = os.path.join(projectpath, dirname)
        if not os.path.exists(path):
            os.makedirs(path)
            print "Created dir %s" % path

    if options.new:
        dxhttp = Requirement.parse("dxhttp")
        for name in SKELETON['files']:
            source = resource_filename(dxhttp, name)
            dest = os.path.join(projectpath, name)
            print "Copied dxhttp/%s to %s" % (name, dest)
            shutil.copy(source, dest)
        
        projectfcgi = '%s.fcgi' % project
        dxhttpfcgi = 'dxhttp.fcgi'
        
        fcgi = resource_string(dxhttp, dxhttpfcgi)
        if options.python_binary:
            fcgi = fcgi.replace('/usr/bin/env python', options.python_binary)
        
        projectfcgipath = os.path.join(projectpath, projectfcgi)
        open(projectfcgipath, "w").write(fcgi)
        print "Created %s" % projectfcgi
        
        os.chmod(projectfcgipath, FCGI_MODE)
        print "Set mode %o for %s" % (FCGI_MODE, projectfcgi)
        
        htaccess = resource_string(dxhttp, '.htaccess').replace(dxhttpfcgi, projectfcgi)
        open(os.path.join(projectpath, '.htaccess'), "w").write(htaccess)
        print "Created .htaccess"
        
    for lib in options.jslib:
        version = None
        if lib.find("-") != -1:
            lib, version = lib.split("-", 1)

        if lib not in LIBS:
            parser.error('Library not found: %s' % lib)
        
        url, defversion = LIBS[lib]
        if version is None:
            version = defversion

        dest = os.path.join(projectpath, 'js', '%s.js' % lib)
        shutil.copyfileobj(urllib.urlopen(url % version), open(dest, "w"))
        print "Downloaded %s-%s to %s" % (lib, version, dest)
        
        
            
    return 0
