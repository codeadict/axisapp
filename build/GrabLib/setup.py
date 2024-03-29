#!/usr/bin/python

import os, re

from setuptools import setup

description = "Utility for defining then downloading, concatenating and minifying your project's external library files"
docs_file = 'GrabLib/docs.txt'
try:
    long_description = open(docs_file, 'r').read()
except IOError:
    print '%s not found, long_description is short' % docs_file
    long_description = description

setup(name='GrabLib',
    version = '0.05',
    description = description,
    long_description = long_description,
    author = 'Samuel Colvin',
    license = 'MIT',
    author_email = 'S@muelColvin.com',
    url = 'https://github.com/samuelcolvin/GrabLib',
    packages = ['GrabLib'],
    platforms = 'any',
    scripts = ['GrabLib/bin/grablib'],
    install_requires=[
        'requests>=2.2.1',
        'termcolor>=1.1.0',
        'six>=1.6.1',
        'slimit>=0.8.1',
        'argparse>=1.2.1'
    ],
)