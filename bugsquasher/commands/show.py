# vim: tabstop=4 shiftwidth=4 softtabstop=4

from bugsquasher.commands.base import BaseBug

class ShowBug(BaseBug):

    name = 'show'

    @classmethod
    def add_argument_parser(cls, subparsers):
        parser = super(ShowBug, cls).add_argument_parser(subparsers)
        parser.add_argument('-v', '--verbose',
                            action="store_true",
                            help="Verbose output")
        parser.add_argument('--vm',
                            help="Virtual machine's OS")
        return parser