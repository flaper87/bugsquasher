#!/usr/bin/env python

import os
from pkg_resources import iter_entry_points

from bugsquasher.cfg import conf
from bugsquasher.commands import base

COMMANDS = []


def main(config_files):
    def load_commands(prefix):
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        for path in os.environ["PATH"].split(os.pathsep):

            if not os.path.exists(path) or not os.path.isdir(path):
                continue

            for program in os.listdir(path):
                if not program.startswith(prefix):
                    continue

                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    yield exe_file

    subparsers = conf.add_subparsers()

    for cmd in iter_entry_points("bugsquasher.commands"):
        cmd = cmd.load()
        COMMANDS.append(cmd)
        cmd.add_argument_parser(subparsers)

    for cmd in load_commands("bgsq-"):
        class NewCmd(base.BaseBash):
            name = cmd.split("-")[-1]
        COMMANDS.append(NewCmd)
        NewCmd.add_argument_parser(subparsers)

    conf.args.cmd_class.main()

if __name__ == '__main__':
    dev_conf = os.path.join(os.path.expanduser("~"), '.bgsqrc')

    config_files = None
    if os.path.exists(dev_conf):
        config_files = [dev_conf]

    main(config_files=config_files)