# -*- coding: utf-8 -*-
"""Setup file.

:copyright: (c) 2019, Serge Émond
:license: BSD 3-Clause, http://opensource.org/licenses/BSD-3-Clause

"""

from setuptools import setup

setup(
    name="golden-borders",
    # version=version_from_git(),
    author=u"Serge Émond",
    author_email="serge@sergeemond.com",
    zip_safe=True,
    packages=["golden_borders"],
    url="https://bitbucket.org/greyw/golden-borders",
    description="Compute the mat size and borders so the window is optically"
    "and the area follows the golden ratio",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: BSD License",
        "Topic :: Utilities",
    ],
    install_requires=["click", "mpmath"],
    extras_requires={
        "dev": [
            "flake8",
            "flake8",
            "flake8-docstrings",
            "flake8-import-order",
            "black",
            "isort",
        ]
    },
    version_format='{tag}.dev{commitcount}+{gitsha}',
    setup_requires=['setuptools-git-version'],
    entry_points="""
    [console_scripts]
    golden-borders=golden_borders:main
    """,
)
