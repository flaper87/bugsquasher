# vim: tabstop=4 shiftwidth=4 softtabstop=4

import os

from termcolor import colored

from bugsquasher import commands


class Cmd(commands.BaseApp):
    name = "list"

    @classmethod
    def execute(cls, config, section):
        work_dir = os.path.expanduser(section.get('work_dir'))
        prefix = section.get('prefix', '')

        assert os.path.exists(work_dir), ("Work dir %s does not exist" %
                                          work_dir)

        for bug in os.listdir(work_dir):
            bug_dir = os.path.join(work_dir, bug)
            if not os.path.isdir(bug_dir) or not bug.startswith(prefix):
                continue

            os.chdir(bug_dir)
            bug = bug.lstrip(prefix)
            print colored("Bug: " + bug, 'red')
            print colored("Working Dir: ", 'green') + os.getcwd()
            cls.call_hooks(config, section, bug=bug)
            print
