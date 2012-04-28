try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {

    'description': 'A variety of handy utilities to do simple Python tests. NOTE: testing coverage is low, use at your own risk and contribute fixes. Contributors always welcome on github',
    'author': 'Jeffrey Tratner',
    'url': 'jeffreytratner.com',
    'download_url': 'on pypi',
    'author_email': 'jeffrey.tratner@gmail.com',
    'version': '0.1',
    'install_requires': [],
    'packages': ['simpleutils'],
    'scripts': [],
    'name': 'simpleutils',
    'license': 'GPL license v3.0'
}

setup(**config)
