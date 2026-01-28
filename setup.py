from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zmenu",
    version="0.1.0",
    author="zmenu contributors",
    description="A flexible and reusable Python framework for building interactive console applications with nested menu support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clarithromycine/zmenu",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
