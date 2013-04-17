import os
import sys
import json
import argparse


class Configuration(argparse.ArgumentParser):
    _conf = None
    _parsed = None

    @property
    def args(self):
        if not self._parsed:
            self._parsed = self.parse_args(sys.argv[1:])
        return self._parsed

    @property
    def config(self):
        if not self._conf:
            with open(os.path.join(os.path.expanduser("~"), '.bgsqrc')) as cfg:
                self._conf = json.load(cfg)
        return self._conf

conf = Configuration()
