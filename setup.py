#!/usr/bin/env python
# vim: fenc=utf-8

from distutils.core import setup

import os


def find_packages():
    packages = []

    for dir, dnames, fnames in os.walk('.'):
        split_path = dir.split(os.sep)
        if '.git' in split_path:
            continue

        if '__init__.py' in fnames:
            pkg_path = os.path.join(*split_path[1:])
            packages.append(pkg_path)

    return packages


setup(
    name='barbados',
    version='0.0.1',
    description='Harbo(u)r management system',
    url='https://github.com/codento/barbados/',
    author=u'Barbados Team / Codento',
    author_email='barbados@codento.com',
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('share/barbados/', ['requirements.txt', 'README.md']),
    ],
)

