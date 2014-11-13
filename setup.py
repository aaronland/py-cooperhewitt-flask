#!/usr/bin/env python

from setuptools import setup

setup(name='cooperhewitt-flask',
      version='0.2',
      description='Cooper Hewitt utility functions for Flask applications',
      author='Cooper Hewitt Smithsonian Design Museum',
      url='https://github.com/cooperhewitt/py-flask',
      requires=[
        'flask',
        'flaskcors',
        'werkzeug',
        'werkzeug.security',
        ],
      packages=[
          'cooperhewitt',
          'cooperhewitt.flask'
      ],
      scripts=[],
      download_url='https://github.com/cooperhewitt/py-cooperhewitt-flask/releases/tag/v0.2',
      license='BSD')
