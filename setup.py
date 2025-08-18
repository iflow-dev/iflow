#!/usr/bin/env python3
"""
Setup script for iflow package.
"""

from setuptools import setup, find_packages
import os
import re

def get_version():
    """Read version from __init__.py file."""
    init_file = os.path.join(os.path.dirname(__file__), 'sw', 'iflow', '__init__.py')
    with open(init_file, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)
    return "0.0.0"

# Read the README file
def read_readme():
    """Read the README file."""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "iflow - Project Artifact Manager"

setup(
    name="iflow",
    version=get_version(),
    description="A tool for managing project artifacts like requirements, tasks, test cases, and issues",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="iflow team",
    author_email="",
    url="",
    packages=find_packages(where="sw"),
    package_dir={"": "sw"},
    package_data={
        "iflow": ["static/*", "static/*/*"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Project Managers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pywebview>=4.0",
        "PyYAML>=6.0",
        "GitPython>=3.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=5.0",
            "mypy>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "iflow=iflow.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="project management, artifacts, requirements, tasks, test cases, issues, git",
    project_urls={
        "Bug Reports": "",
        "Source": "",
        "Documentation": "",
    },
)
