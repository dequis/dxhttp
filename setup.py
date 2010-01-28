from setuptools import setup, find_packages
setup(
    name = "dxhttp",
    version = "2.2",
    packages = find_packages(),
    package_data = {
        '': ['.htaccess', 'dxhttp.fcgi', 'main.py', 'config.py', 'app.py']
    },
    entry_points = {
        'console_scripts': [
            'dxhttp_project = util.project:main',
        ]
    }
)

