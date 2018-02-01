#!/usr/bin/env python
# http://docs.python.org/distutils/setupscript.html
# http://docs.python.org/2/distutils/examples.html
from setuptools import setup, find_packages
import re
import os
from codecs import open


name = "transcribe"

def read(path):
    if os.path.isfile(path):
        with open(path, encoding='utf-8') as f:
            return f.read()
    return ""


vpath = os.path.join(name, "__init__.py")
if not os.path.isfile(vpath): vpath = os.path.join("{}.py".format(name))
version = re.search("^__version__\s*=\s*[\'\"]([^\'\"]+)", read(vpath), flags=re.I | re.M).group(1)

long_description = read('README.rst')

tests_modules = []
install_modules = list(filter(None, read("requirements.txt").splitlines(False)))


setup(
    name=name,
    version=version,
    description='Convert images or audio files to plain text on the command line',
    long_description=long_description,
    author='Jay Marcyes',
    author_email='jay@marcyes.com',
    url='http://github.com/Jaymon/{}'.format(name),
    #py_modules=[name], # files
    packages=find_packages(), # folders
    license="MIT",
    install_requires=install_modules,
    tests_require=tests_modules,
    classifiers=[ # https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Text Processing',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],
    entry_points = {
        'console_scripts': [
            '{} = {}.__main__:console'.format(name, name),
        ],
    }
)

