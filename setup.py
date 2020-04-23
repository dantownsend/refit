#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup

from refit import __VERSION__ as VERSION


directory = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(directory, "requirements.txt")) as f:
    contents = f.read()
    REQUIREMENTS = [i.strip() for i in contents.strip().split("\n")]


with open(os.path.join(directory, "README.md")) as f:
    LONG_DESCRIPTION = f.read()


setup(
    name="refit",
    version=VERSION,
    description="Simple remote server configuration, using asyncio.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Daniel Townsend",
    author_email="dan@dantownsend.co.uk",
    python_requires=">=3.7.0",
    url="https://github.com/dantownsend/refit",
    packages=find_packages(exclude=("tests",)),
    package_data={
        'refit': [
            'scaffold/files/*.md',
            'scaffold/templates/*.jinja'
        ]
    },
    install_requires=REQUIREMENTS,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Development Status :: 2 - Pre-Alpha",
    ],
    entry_points={"console_scripts": ["refit = refit.main:command_line"]},
)
