#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages
import os

from __init__ import __version__

__requires = filter(None, open('requirements.txt').read().splitlines())

exclusion = [
    'ajenti.plugins.elements',
    'ajenti.plugins.ltfs',
    'ajenti.plugins.ltfs*',
    'ajenti.plugins.vh',
    'ajenti.plugins.vh*',
    'ajenti.plugins.custom*',
    'ajenti.plugins.test*',
]


on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:
    data_files = []
else:
    data_files = []


setup(
    name            = 'ajenti-mdadm',
    version         = __version__,
    install_requires= __requires,
    description     = 'The MDADM administration panel',
    author          = 'Marc Bertens',
    author_email    = 'm.bertens@pe2mbs.nl',
    url             = 'http://www.pe2mbs.nl/ajenti-mdadm',
    packages        = find_packages(exclude=['reconfigure', 'reconfigure.*'] + exclusion),
    # Need to check if this works properly.
    package_dir     = '/var/lib/ajenti/plugins/mdadm',
    package_data    = {'': ['content/*.*', 'content/*/*.*', 'content/*/*/*.*', 'layout/*.*', 'locales/*/*/*.mo']},
    scripts         = [],
    data_files      = data_files,
)
