#!/usr/bin/env python

from os import path
from setuptools import setup

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md')) as file:
    README = file.read()

setup(
    name='hoare',
    version='0.1.0',
    description='Testing framework to ease the development of Connect EaaS Processors.',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords='connect testing framework cloudblue ingram micro ingrammicro cloud automation test bdd tdd',
    packages=['hoare'],
    url='https://github.com/othercodes/hoare',
    license='MIT'
)
