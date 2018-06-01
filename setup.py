#!/usr/bin/env python

import os
import sys
import shutil

setup = os.path.abspath(sys.argv[0])
parent = os.path.dirname(setup)
pkg = os.path.basename(parent)

if pkg.startswith("py-cooperhewitt"):
    pkg = pkg.replace("py-", "")
    pkg = pkg.replace("-", ".")

    egg_info = "%s.egg-info" % pkg
    egg_info = os.path.join(parent, egg_info)

    if os.path.exists(egg_info):
        shutil.rmtree(egg_info)

from setuptools import setup, find_packages

packages = find_packages()
desc = open("README.md").read()
version = open("VERSION").read()

setup(
    name='cooperhewitt.flask',
    namespace_packages=['cooperhewitt'],
    version=version,
    description='Cooper Hewitt utility functions for Flask applications',
    long_description=desc,
    author='Cooper Hewitt Smithsonian Design Museum',
    url='https://github.com/cooperhewitt/py-cooperhewitt-flask',
    packages=packages,
    download_url='https://github.com/cooperhewitt/py-cooperhewitt-flask/releases/tag/' + version,
    license='BSD')
