# vim: tabstop=4 shiftwidth=4 softtabstop=4

import os
import shutil
from bugsquasher.commands.base import BaseBug


class DestroyBug(BaseBug):

    name = 'destroy'

    @classmethod
    def main(cls):
        super(DestroyBug, cls).main()
        bug_dir = os.getcwd()
        os.chdir("../")
        shutil.rmtree(bug_dir)
