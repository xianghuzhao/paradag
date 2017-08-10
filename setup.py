import sys
import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'paradag', 'VERSION')) as version_file:
    version = version_file.read().strip()

with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

setup(
    name = 'paradag',
    version = version,
    description = 'A robust DAG implementation',
    long_description = long_description,
    url = 'https://github.com/xianghuzhao/paradag',
    author = 'Xianghu Zhao',
    author_email = 'xianghuzhao@gmail.com',
    license = 'MIT',

    classifiers = [
        'Development Status :: 2 - Pre-Alpha',

        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: System :: Software Distribution',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    keywords = 'DAG',
    packages = find_packages(exclude=[]),
    include_package_data = True,
    tests_require = [
        'pytest',
    ],
)
