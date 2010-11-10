# bootstrap easy_install
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup

setup(
    name = 'qdupe',
    version = '0.1',
    description = "A command-line utility to quickly find duplicate files",
    author = "Chris Wilper",
    author_email = "cwilper@gmail.com",
    url = "http://github.com/cwilper/qdupe",
    py_modules = ['qdupe', 'ez_setup'],
    test_suite = '',
    scripts = ['bin/qdupe'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: System :: Archiving',
        'Topic :: System :: Filesystems',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
    ]
)
