#!/usr/bin/env python
import os

# Workaround for hardlink problem in Python 2.7+
# See also: http://bugs.python.org/issue8876
if os.environ.get('USER','') == 'vagrant':
    del os.link

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='omise',
      version='0.6.0',
      description='Omise Python client',
      author='Omise',
      author_email='support@omise.co',
      url='https://www.omise.co/',
      packages=['omise', 'omise.test'],
      install_requires=['requests >= 2.12.1'],
      tests_require=['nose >= 1.3.4', 'mock >= 1.0.1'],
      test_suite='omise.test',
      package_data={'omise': ['data/ca_certificates.pem']},
      classifiers=[
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ])
