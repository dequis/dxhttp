from setuptools import setup, find_packages
setup(
    name = "dxhttp",
    version = "2.3",
    packages = ['dxhttp'],
    package_data = {
        '': ['.htaccess', 'dxhttp.fcgi', 'config.py', 'app.py']
    },
    entry_points = {
        'console_scripts': [
            'dxhttp_project = dxhttp.project:main',
        ]
    }
)

