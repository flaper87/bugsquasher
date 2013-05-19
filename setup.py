import os
from setuptools import setup, find_packages

from bugsquasher import version


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="bugsquasher",
    version=version,
    author="Flavio Percoco",
    author_email="flaper87@flaper87.org",
    description=("A pluggable tool for squashing bugs and tracking down issues"),
    license="BSD",
    url="https://github.com/FlaPer87/bugsquasher",
    packages=find_packages('.'),
    include_package_data=True,
    long_description=read('README.md'),
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    scripts=[
        "bin/bugsq",
        "bin/bugsq-venv"
    ],
    entry_points={
        'bugsquasher.plugins': [
            'pyvenv=bugsquasher.plugins.source.venv:VenvPlugin',
            'vagrant=bugsquasher.plugins.hypervisors.vagrant:Vagrant',
            'bugzilla=bugsquasher.plugins.trackers.bugz:BugzillaBackend',
            'launchpad=bugsquasher.plugins.trackers.lp:LP',
        ],
        "console_scripts": [
            'bugsq-list = bugsquasher.cmd.ls:Cmd.main',
            'bugsq-show = bugsquasher.cmd.show:Cmd.main',
            'bugsq-take = bugsquasher.cmd.take:Cmd.main',
            'bugsq-update = bugsquasher.cmd.update:Cmd.main',
            'bugsq-search = bugsquasher.cmd.search:Cmd.main',
            'bugsq-destroy = bugsquasher.cmd.destroy:Cmd.main',
        ]
    },
)
