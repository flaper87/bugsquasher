import json
import os
import sys

from oslo.config import cfg
from stevedore import driver

from bugsquasher.utils import misc, plugins


command_opts = [
    cfg.StrOpt('verbose', short='v', help='Verbose Mode'),
    cfg.StrOpt('section', short='s', help='Section to use'),
    cfg.ListOpt('exclude', short='e', default=[], help='Exclude plugins'),
    cfg.ListOpt('include', short='i', default=[], help='Include plugins')
]


class BaseApp(object):

    name = None

    @classmethod
    def main(cls):
        """
        Called whenever a command is executed.
        """
        config = cfg.CONF
        cls.register_opts(config)
        config(sys.argv[1:], project='bugsquasher')

        sfile = config.find_file("%s.json" % config.section)
        section = json.load(open(sfile))
        cls.execute(config, section)

    @classmethod
    def register_opts(cls, config):
        config.register_cli_opts(command_opts)

    @classmethod
    def execute(cls, config):
        raise NotImplementedError()

    @classmethod
    def call_hooks(cls, config, section, **kwargs):
        """
        Called by main. This method calls hooks that were
        configured in the config file or enabled in the cli.

        It also excludes hooks specified in the cli using `-e`

        NOTE: Hooks enabled using `-i` will be called after the
        ones configured in the config file.

        :params config: Dictionary containing section's configs.
        :params kwargs: Any extra keyword that should be passed
        to the final method.
        """

        hooks = section.get("%s_hooks" % cls.name, []) + config.include
        filtered = filter(lambda x: x not in config.exclude, set(hooks))

        for hook in filtered:
            try:
                mgr = driver.DriverManager('bugsquasher.plugins', hook)
                meth = getattr(mgr.driver, "on_%s" % cls.name)
                meth(config, section, **kwargs)
            except AttributeError:
                pass


class BaseBug(BaseApp):
    """
    Base command class for bug related
    commands.
    """

    @classmethod
    def register_opts(cls, config):
        super(BaseBug, cls).register_opts(config)
        config.register_cli_opt(cfg.StrOpt('bug',
                                           required=True,
                                           positional=True))

    @staticmethod
    def get_bug_dir(config, section):
        """
        Returns the bug directory
        """
        bug = config.bug
        if bug.startswith(section.get('prefix', '')):
            bug = bug.lstrip(section.get('prefix', ''))

        base_work_dir = os.path.expanduser(section.get('work_dir'))
        assert os.path.exists(base_work_dir), "Work dir %s does not exist" % \
                                              base_work_dir
        return os.path.join(base_work_dir, "%s%s" %
                            (section.get('prefix'), bug))

    @classmethod
    def execute(cls, config, section):
        """
        This implementation makes sure a folder for
        the given bug exists and cd'es it before executing
        hooks chain.
        """
        work_dir = cls.get_bug_dir(config, section)
        if not os.path.exists(work_dir):
            os.mkdir(work_dir)
        os.chdir(work_dir)
        cls.call_hooks(config, section, bug=config.bug)
