#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open("requirements.txt") as f:
    requirements = [req.strip() for req in f.readlines()]


setup(name='GoogleSearch_Advanced',
      version='1.0',
      url='https://github.com/TheProjectsX/GoogleSearch_Advanced',
      description='Get Advanced Google Search Results via Python',
      author='TheProjectsX',
      author_email='',
      license='MIT',
      packages=[
          'googlesearch_advanced'
      ],
      package_dir={'googlesearch_advanced': 'googlesearch_advanced'},
      install_requires=requirements,
      # Include additional files
      include_package_data=True,
      # Additional classifiers
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
      ],
      )
