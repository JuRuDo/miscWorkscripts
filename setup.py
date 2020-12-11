#!/bin/env python

from setuptools import setup, find_packages


setup(
    name="workScripts",
    version="0.1",
    python_requires='>=3.7.0',
    description="Just some work scripts",
    author="Julian Dosch",
    author_email="Dosch@bio.uni-frankfurt.de",
    url="https://github.com/JuRuDo/miscWorkscripts",
    packages=find_packages(),
    package_data={'': ['*']},
    install_requires=[],
    entry_points={
        'console_scripts': ["IDmapper = miscWorkScripts.uniprot.IDmapperUNIPROT:main",
                            "oma.getgroup = miscWorkScripts.oma.getGroup:main"
],
    },
    license="GPL-3.0",
    classifiers=[
        "Environment :: Console",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
    ],
)
