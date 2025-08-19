#!/usr/bin/env python3
"""
Setup configuration for iflow package.

"""

import os
import re
from setuptools import setup, find_packages

def get_version():
    """Read version from __init__.py file."""
    init_file = os.path.join(os.path.dirname(__file__), 'sw', 'iflow', '__init__.py')
    with open(init_file, 'r') as f:
        content = f.read()
    match = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", content)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find version string in __init__.py")

setup(
    name="iflow",
    version=get_version(),
    description="Git-based artifact management system",
    author="Claudio Klingler",
    packages=find_packages(where="sw"),
    package_dir={"": "sw"},
    install_requires=[
        "flask>=2.0.0",
        "pyyaml>=5.0",
        "gitpython>=3.0.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "iflow=iflow.main:main",
        ],
    },
    python_requires=">=3.8",
)
