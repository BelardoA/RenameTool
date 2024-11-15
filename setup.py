#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""imports"""
import sys
from pathlib import Path

from setuptools import find_packages, setup

from rename_tool import __version__

# make sure to keep python version in numerical order
SUPPORTED_PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12", "3.13"]
CLASSIFIERS = [
    "Operating System :: OS Independent",
] + ["Programming Language :: Python :: " + version for version in SUPPORTED_PYTHON_VERSIONS]
CWD = Path(__file__).resolve().parent
long_description = (CWD / "README.md").read_text(encoding="utf-8")

if f"{sys.version_info.major}.{sys.version_info.minor}" not in SUPPORTED_PYTHON_VERSIONS:
    raise RuntimeError(
        f"Unsupported version of Python detected: {sys.version_info.major}.{sys.version_info.minor}\n"
        f"RegScale-CLI requires Python {', '.join(SUPPORTED_PYTHON_VERSIONS)}."
    )


def _strip(file_name: str) -> str:
    """
    Strip text from a file
    :param str file_name: path to the filename to strip
    :return: stripped text from the provided file
    :rtype: str
    """
    return (CWD / file_name).read_text(encoding="utf-8").strip()


# Define requirement lists and append synqly to the list
INSTALL_REQUIRES = _strip("requirements.txt").split()
DEV_REQUIRES = [
    "pytest>=5",
    "pylint",
]

setup(
    name="RenameTool",
    version=__version__,
    author="Anthony Belardo",
    author_email="livintodie4e@gmail.com",
    license="MIT",
    description="Command Line Interface (CLI) Rename Tool for renaming files within Season subdirectories with SXXEXX prefix for plex parsing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BelardoA/RenameTool",
    packages=find_packages(exclude=["tests"]),
    include_package_data=False,
    package_data={},
    setup_requires=["rich==12.6.0", "cython"],
    install_requires=INSTALL_REQUIRES,
    extras_require={"dev": DEV_REQUIRES + INSTALL_REQUIRES},
    # parse and increase the minor version number of the last item in SUPPORTED_PYTHON_VERSIONS
    python_requires=f">={SUPPORTED_PYTHON_VERSIONS[0]}, <{str(int(SUPPORTED_PYTHON_VERSIONS[-1].split('.')[0]) + 1)}",
    classifiers=CLASSIFIERS,
    entry_points={
        "console_scripts": [
            "rename_tool = rename_tool.main:cli",
        ],
    },
)