import shutil
from bugsquasher import commands


class Cmd(commands.BaseBug):
    name = 'destroy'

    @classmethod
    def execute(cls, config, section):
        bug_dir = cls.get_bug_dir(config, section)
        shutil.rmtree(bug_dir)
