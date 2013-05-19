import os
import shutil
from bugsquasher import commands


class Cmd(commands.BaseBug):
    name = 'destroy'

    @classmethod
    def execute(cls, config, section):
        bug_dir = os.getcwd()
        os.chdir("../")
        shutil.rmtree(bug_dir)
