#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()


requirements = [
    'starlette',
    'PyJWT',
]

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
    'pytest-cov',
    'coverage',
    'requests'
]

setup(
    name='starlette_jwt',
    version='0.1.7',
    description="A JSON Web Token Middleware for Starlette",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Amit Ripshtos",
    url='https://github.com/amitripshtos/starlette-jwt',
    packages=find_packages(include=['starlette_jwt']),
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='starlette_jwt',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
