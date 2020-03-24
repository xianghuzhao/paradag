'''setup information for paradag'''

import os

from setuptools import setup, find_packages


HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, 'paradag', 'VERSION')) as version_file:
    VERSION = version_file.read().strip()

with open(os.path.join(HERE, 'README.md')) as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='paradag',
    version=VERSION,
    description='A robust DAG implementation for parallel programming',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/xianghuzhao/paradag',
    author='Xianghu Zhao',
    author_email='xianghuzhao@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],

    keywords=['DAG', 'parallel programming'],
    packages=find_packages(exclude=[]),
    include_package_data=True,
    tests_require=[
        'pytest',
    ],
)
