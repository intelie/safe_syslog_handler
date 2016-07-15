#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()


requirements = [
]

test_requirements = [
    'mock',
]

setup(
    name='safe_syslog_handler',
    version='0.1.0',
    description="SafeSysLogHandler recreates the connection to a remote logging server when the connection is lost, avoiding the `[errno 32] Broken Pipe` error which would occur when using the `SysLogHandler`.",
    long_description=readme,
    author="Felipe Arruda Pontes",
    author_email='felipe.arruda@intelie.com.br',
    url='https://github.com/intelie/safe_syslog_handler',
    packages=[
        'safe_syslog_handler',
    ],
    package_dir={'safe_syslog_handler':
                 'safe_syslog_handler'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='safe SysLogHandler broken pipe errno32',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: System :: Logging',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
