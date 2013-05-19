from oslo.config import cfg

from bugsquasher import commands
from bugsquasher.utils import misc


class Cmd(commands.BaseApp):
    name = 'config'

    @classmethod
    def register_opts(cls, config):
        super(Cmd, cls).register_opts(config)
        config.register_cli_opt(cfg.StrOpt('shell', default=False))

    @classmethod
    def execute(cls, config, section):

        if config.shell:
            output = []
            for config in misc.config_to_bash(section).iteritems():
                output.append("export " + "=".join(config))
            section = "\n".join(output)

        print section
