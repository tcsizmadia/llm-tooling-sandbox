from setuptools import setup, find_packages
from os import path

# Get the directory containing this file
HERE = path.abspath(path.dirname(__file__))

setup(
    name="boiler_api",
    version="0.1.0",
    packages=find_packages(where="."),
    package_dir={"": "."},
    install_requires=[
        "flask==3.1.0",
    ],
    author="Tamas Csizmadia",
    author_email="",
    description="A sample REST API project of an imaginary smart boiler",
    keywords="api, boiler, flask",
    python_requires=">=3.6",
)
