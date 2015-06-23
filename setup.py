import os
from setuptools import setup


setup(
    name = "deflake",
    version = "0.1.2",
    author = "NCBI",
    author_email = "",
    description = ("Helps debug a non determinate test (or any flaky program) by running it until it exits with a non-zero exit code. See https://github.com/ncbi/deflake for more details"),
    license = "Public Domain",
    keywords = "testing flaky",
    url = "http://packages.python.org/deflake",
    entry_points = {
        'console_scripts': 
            ['deflake=deflake.cli:main']
    },
    packages = ["deflake"]
)
