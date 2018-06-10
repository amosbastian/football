from setuptools import setup, find_packages

setup(
    name="football",
    version="0.2.0",
    packages=find_packages(),
    description="A Python wrapper around the football-data API.",
    url="https://github.com/amosbastian/football",
    author="Amos Bastian",
    author_email="amosbastian@googlemail.com",
    license="AGPL-3.0",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3.6"
    ],
    keywords="football football-data api",
    install_requires=["requests"],
    python_requires=">=3.6"
)
