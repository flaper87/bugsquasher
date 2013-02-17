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
        "bin/bugsq.py",
        "bin/bugsq-venv"
    ],
    entry_points={
        'bugsquasher.commands': [
            'list=bugsquasher.commands.ls:LsBugs',
            'search=bugsquasher.commands.search:Search',
            'show=bugsquasher.commands.show:ShowBug',
            'take=bugsquasher.commands.take:TakeBug',
            'config=bugsquasher.commands.config:Config',
            'update=bugsquasher.commands.update:UpdateBugs',
            'destroy=bugsquasher.commands.destroy:DestroyBug',
        ],
        'bugsquasher.plugins': [
            'pyvenv=bugsquasher.plugins.source.venv:VenvPlugin',
            'vagrant=bugsquasher.plugins.hypervisors.vagrant:Vagrant',
            'bugzilla=bugsquasher.plugins.trackers.bugz:BugzillaBackend',
        ],
    },
)
