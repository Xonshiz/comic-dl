#!/usr/bin/env python
# coding: utf-8

import os
import sys
import comic_dl

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('ReadMe.md').read()
history = open('Changelog.md').read()

exec(compile(open('comic_dl/version.py').read(),
             'comic_dl/version.py', 'exec'))

setup(
    name='comic-dl',
    version=__version__,
    description='Comic-dl is a command line tool to download Comics and Manga from various Manga and Comic sites easily.',
    long_description=readme + '\n\n' + history,
    author='Xonshiz',
    author_email='xonshiz@psychoticelites.com',
    url='https://github.com/Xonshiz/comic-dl',
    packages=[
        'comic_dl',
        'comic_dl.sites',
    ],
    package_dir={'comic_dl': 'comic_dl'},
    include_package_data=True,
    install_requires=["clint",
                      "requests",
                      "cloudscraper",
                      "bs4"
    ],
    entry_points={
        'console_scripts': [
            'comic_dl = comic_dl:comic_dl'
        ],
    },
    license="MIT Licence",
    zip_safe=False,
    keywords = ['comic-dl', 'cli', 'comic downloader','manga downloader','mangafox','batoto','kissmanga','readcomiconline.to'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: Public Domain',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Graphics'
    ],
    #test_suite='tests',
)
