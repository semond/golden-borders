# -*- coding: utf-8 -*-
"""

:copyright: © 2014, Serge Émond
:license: BSD 3-Clause, http://opensource.org/licenses/BSD-3-Clause

"""

import os
import subprocess
from setuptools import setup


def version_from_git():
    """Fetch version from git tags, and write to version.py.

    Also, when git is not available (PyPi package), use stored version.py.

    Source: http://blogs.nopcode.org/brainstorm/2013/05/20/pragmatic-python-versioning-via-setuptools-and-git-tags/)
    """
    version_py = os.path.join(os.path.dirname(__file__), 'version.py')

    try:
        version_git = subprocess.check_output(["git", "describe"]).rstrip()
    except:
        with open(version_py, 'r') as fh:
            version_git = open(version_py).read().strip().split('=')[-1].replace('"','')

    version_msg = "# Do not edit this file, pipeline versioning is governed by git tags"
    with open(version_py, 'w') as fh:
        fh.write(version_msg + os.linesep + "__version__=" + version_git)

    return version_git


setup_opts = dict(
    name='golden-borders',
    version=version_from_git(),
    author=u'Serge Émond',
    author_email='serge@sergeemond.com',
    zip_safe=True,
    packages=['golden_borders'],
    url='https://bitbucket.org/greyw/golden-borders',
    description="Compute the mat size and borders so the window is optically"
    "and the area follows the golden ratio",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Topic :: Utilities',
    ],
    install_requires=[
        'click',
        'mpmath',
    ],
    entry_points="""
    [console_scripts]
    golden-borders=golden_borders:main
    """,
    )

if __name__ == '__main__':
    setup(**setup_opts)