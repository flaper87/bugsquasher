# vim: tabstop=4 shiftwidth=4 softtabstop=4

from bugsquasher.cfg import conf
from bugsquasher.commands.base import BaseApp
from bugsquasher.utils import misc


class Config(BaseApp):

    name = 'config'

    @classmethod
    def add_argument_parser(cls, subparsers):
        parser = super(Config, cls).add_argument_parser(subparsers)
        parser.add_argument('--shell',
                            action="store_true",
                            required=False)
        return parser

    @classmethod
    def main(cls):
        section = conf.args.section
        if not section:
            section = conf.config.get('section')

        config = conf.config.get(section)

        if conf.args.shell:
            output = []
            for config in misc.config_to_bash(config).iteritems():
                output.append("export " + "=".join(config))
            config = "\n".join(output)

        print config
