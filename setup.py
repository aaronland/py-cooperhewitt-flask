#!/usr/bin/env python

from setuptools import setup, find_packages

packages = find_packages()
desc = open("README.md").read(),

print packages

setup(name='cooperhewitt-flask',
      version='0.3',
      description='Cooper Hewitt utility functions for Flask applications',
      long_description=desc,
      author='Cooper Hewitt Smithsonian Design Museum',
      url='https://github.com/cooperhewitt/py-flask',
      requires=[
        'flask',
        'flaskcors',
        'werkzeug',
        'werkzeug.security',
        ],
      packages=packages,
      scripts=[],
      download_url='https://github.com/cooperhewitt/py-cooperhewitt-flask/releases/tag/v0.3',
      license='BSD')
