
import os

from oslo.config import cfg

from bugsquasher import commands


class Cmd(commands.BaseApp):
    name = 'update'

    @classmethod
    def register_opts(cls, config):
        super(Cmd, cls).register_opts(config)
        config.register_cli_opt(cfg.StrOpt('bug', positional=True))

    @classmethod
    def execute(cls, config, section):
        bug = config.bug
        work_dir = config.get('work_dir')
        assert (os.path.exists(work_dir),
                "Work dir %s does not exist" % work_dir)

        if bug:
            if bug.startswith(config.get('prefix', '')):
                bug = bug.lstrip(config.get('prefix', ''))

            work_dir = os.path.join(work_dir, "%s%s" %
                                    (config.get('prefix'), bug))

        os.chdir(work_dir)
        cls.call_hooks(config=config, bug=bug)
