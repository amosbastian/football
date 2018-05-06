from setuptools import setup, find_packages

setup(
    name="football",
    version="0.1.0",
    description="A python wrapper around the football-data API.",
    url="https://github.com/amosbastian/football",
    author="Amos Bastian",
    author_email="amosbastian@googlemail.com",
    license="AGPL-3.0",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python"
    ],
    keywords="football",
    install_requires=["requests"]
)
