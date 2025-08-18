#!/usr/bin/env python3
"""
Setup configuration for iflow package.
"""

import re
import os
from setuptools import setup, find_packages

def get_version():
    """Get version from __init__.py file."""
    init_file = os.path.join(os.path.dirname(__file__), 'sw', 'iflow', '__init__.py')
    with open(init_file, 'r') as f:
        content = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name="iflow",
    version=get_version(),
    description="Git-based project artifact management system",
    author="iflow team",
    packages=find_packages(where="sw"),
    package_dir={"": "sw"},
    install_requires=[
        "flask",
        "gitpython",
        "pyyaml",
        "typer"
    ],
    entry_points={
        "console_scripts": [
            "iflow=iflow.main:main",
        ],
    },
    python_requires=">=3.8",
)
