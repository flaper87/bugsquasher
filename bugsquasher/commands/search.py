# vim: tabstop=4 shiftwidth=4 softtabstop=4

from bugsquasher.cfg import conf
from bugsquasher.commands.base import BaseApp


class Search(BaseApp):

    name = 'search'

    @classmethod
    def add_argument_parser(cls, subparsers):
        parser = super(Search, cls).add_argument_parser(subparsers)
        parser.add_argument('-q', '--query',
                            nargs="+",
                            action="append",
                            required=False)
        return parser

    @classmethod
    def main(cls):
        section = conf.args.section
        if not section:
            section = conf.config.get('section')

        config = conf.config.get(section)

        query = {}

        if conf.args.query:
            for param in conf.args.query:
                param = " ".join(param)
                k, v = param.split("=")
                query[k] = v
        cls.call_hooks(config=config, query=query)
