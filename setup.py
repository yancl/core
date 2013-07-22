#!/usr/bin/env python
import os
import sys
from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload -r internal')
    sys.exit()

setup(
        name = "zhwcore",
        version = "0.10",
        description="python corelib for zhaohaowan project",
        long_description=open("README.md").read(),
        author="yancl",
        author_email="kmoving@gmail.com",
        url='https://github.com/yancl/core',
        classifiers=[
            'Programming Language :: Python',
        ],
        platforms='Linux',
        license='MIT License',
        zip_safe=False,
        install_requires=[
            'distribute',
            'MySQL-python',
            'torndb',
            'Pyrex',
            'python-libmemcached',
            'redis',
            'thrift_client',
        ],
        tests_require=[
            'nose',
        ],
        packages=['core', 'core.common', 'core.client', 'core.patch', 'core.test', 'core.utils']
)
