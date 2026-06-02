#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevEnvSync 安装脚本
"""

from setuptools import setup, find_packages
import os

# 读取README
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, 'README.md')
long_description = ""
if os.path.exists(readme_path):
    with open(readme_path, encoding='utf-8') as f:
        long_description = f.read()

setup(
    name="devenvsync",
    version="1.0.0",
    author="DevEnvSync Team",
    author_email="",
    description="智能开发环境配置同步引擎 - Intelligent Development Environment Configuration Sync Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lobster8k/DevEnvSync",
    py_modules=["devenvsync"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Tools",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Natural Language :: English",
        "Natural Language :: Chinese (Simplified)",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "devenvsync=devenvsync:main",
            "des=devenvsync:main",
        ],
    },
    keywords="dotfiles, config, sync, backup, development, environment, cli, terminal",
    project_urls={
        "Bug Reports": "https://github.com/lobster8k/DevEnvSync/issues",
        "Source": "https://github.com/lobster8k/DevEnvSync",
    },
)
