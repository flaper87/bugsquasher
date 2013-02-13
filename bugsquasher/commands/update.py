# vim: tabstop=4 shiftwidth=4 softtabstop=4

import os

from bugsquasher.cfg import conf
from bugsquasher.commands.base import BaseApp


class UpdateBugs(BaseApp):

    name = 'update'

    @classmethod
    def add_argument_parser(cls, subparsers):
        parser = super(UpdateBugs, cls).add_argument_parser(subparsers)
        parser.add_argument('-b', '--bug', required=False)
        return parser

    @classmethod
    def main(cls):
        """
        https://bugzilla.redhat.com/show_bug.cgi?id=894813
        """
        section = conf.args.section
        if not section:
            section = conf.config.get('section')

        config = conf.config.get(section)

        bug = conf.args.bug
        work_dir = config.get('work_dir')
        assert os.path.exists(work_dir), \
                "Work dir %s does not exist" % work_dir

        if bug:
            if bug.startswith(config.get('prefix', '')):
                bug = bug.lstrip(config.get('prefix', ''))

            work_dir = os.path.join(work_dir, "%s%s" % (config.get('prefix'), bug))

        os.chdir(work_dir)
        cls.call_hooks(config=config, bug=bug)
