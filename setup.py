#!/usr/bin/env python3
"""
TermAssist - Terminal AI Command Assistant
智能终端命令助手
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="termassist",
    version="1.0.0",
    author="TermAssist Team",
    author_email="termassist@example.com",
    description="Terminal AI Command Assistant - 智能终端命令助手",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/termassist",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "termassist=termassist.main:main",
            "tai=termassist.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
