#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
sentry-irc
==============

An extension for Sentry which integrates with Whatsapp�. It will send
notifications to whatsapp users and groups.

:copyright: (c) 2013 by Eduard Carreras, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from setuptools import setup, find_packages

# See http://stackoverflow.com/questions/9352656/python-assertionerror-when-running-nose-tests-with-coverage
# for why we need to do this.
from multiprocessing import util


tests_require = [
]

install_requires = [
    'sentry>=5.4.1',
]

setup(
    name='sentry-whatsapp',
    version='0.1.2',
    author='Eduard Carreras',
    author_email='ecarreras@gisce.net',
    url='https://github.com/ecarreras/sentry-whatsapp',
    description='A Sentry extension which integrates with Whatsapp™',
    long_description=__doc__,
    license='BSD',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    test_suite='nose.collector',
    entry_points={
        'sentry.plugins': [
            'whatsapp = sentry_whatsapp.plugin:WhatsappMessage'
        ],
    },
    include_package_data=True,
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
