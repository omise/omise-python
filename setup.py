#!/usr/bin/env python
import os
from io import open

# Workaround for hardlink problem in Python 2.7+
# See also: http://bugs.python.org/issue8876
if os.environ.get('USER', '') == 'vagrant':
    del os.link

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(name='omise',
      long_description=long_description,
      long_description_content_type='text/markdown',
      version='0.15.0',
      description='Omise Python client',
      author='Omise',
      author_email='support@omise.co',
      url='https://www.omise.co/',
      packages=['omise', 'omise.test'],
      install_requires=['requests >= 2.12.1'],
      test_suite='omise.test',
      extras_require={
        "tests": ['nose >= 1.3.4', 'mock >= 1.0.1', 'coverage >= 7.0.0'],
      },
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Programming Language :: Python :: 3.12",
          "Programming Language :: Python :: 3.13",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ])
