# vim: tabstop=4 shiftwidth=4 softtabstop=4

import os

from termcolor import colored

from bugsquasher.cfg import conf
from bugsquasher.commands.base import BaseApp


class LsBugs(BaseApp):

    name = 'list'

    @classmethod
    def main(cls):
        section = conf.args.section
        if not section:
            section = conf.config.get('section')

        config = conf.config.get(section)

        work_dir = os.path.expanduser(config.get('work_dir'))
        prefix = config.get('prefix', '')

        assert os.path.exists(work_dir), "Work dir %s does not exist" % \
                                          work_dir
        for bug in os.listdir(work_dir):
            bug_dir = os.path.join(work_dir, bug)
            if not os.path.isdir(bug_dir) or not bug.startswith(prefix):
                continue

            os.chdir(bug_dir)
            bug = bug.lstrip(prefix)
            print colored("Bug: " + bug, 'red'), \
                  colored("Working Dir: ", 'green') + os.getcwd()
            cls.call_hooks(config=config, bug=bug)
