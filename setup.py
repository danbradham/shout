try:
    from distutils.core import setup
except ImportError:
    from setuptools import setup
import os
import sys
import shout

if sys.argv[-1] == 'cheeseit!':
    os.system('python setup.py sdist upload')
    sys.exit()

with open("README.rst") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="shout",
    version=shout.__version__,
    description=shout.__description__,
    long_description=readme,
    author=shout.__author__,
    author_email=shout.__email__,
    url=shout.__url__,
    include_package_data=True,
    license=license,
    zip_safe=False,
    package_data={"": ["LICENSE"]},
    packages=[],
    install_requires = [],
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
)
