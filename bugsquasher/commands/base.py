import os

from bugsquasher.cfg import conf
from bugsquasher.utils import misc, plugins


class BaseApp(object):

    name = None

    @classmethod
    def add_argument_parser(cls, subparsers):
        parser = subparsers.add_parser(cls.name, help=cls.__doc__)
        parser.set_defaults(cmd_class=cls)
        parser.add_argument('-s', '--section',
                            help='Section to use')
        parser.add_argument('-e', '--exclude', default="",
                            help='Exclude plugins (Comma separated)')
        parser.add_argument('-i', '--include', default="",
                            help='Include plugins (Comma separated)')
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
        cls.call_hooks(config=config)

    @classmethod
    def call_hooks(cls, config={}, **kwargs):
        for hook in config.get("%s_hooks" % cls.name, []):
            hook_type, hook = hook.split(":")
            if hook in conf.args.exclude.split(","):
                continue
            getattr(cls, "_%s" % hook_type)(hook, config=config, **kwargs)

        if conf.args.include:
            for hook in conf.args.include.split(","):
                if not hasattr(cls, "_%s" % hook.split(":")[0]):
                    hook_type = "egg"
                    hook = "bugsquasher#" + hook
                else:
                    hook_type, hook = hook.split(":")

                getattr(cls, "_%s" % hook_type)(hook, config=config, **kwargs)

    @classmethod
    def _egg(cls, hook, config={}, **kwargs):
        plugin = plugins.load_plugin("egg:%s" % hook)
        getattr(plugin, "on_%s" % cls.name)(config=config, **kwargs)

    @classmethod
    def _cmd(cls, hook, config={}, **kwargs):
        misc.execute(hook, config=config)


class BaseBash(BaseApp):

    @classmethod
    def main(cls):
        section = conf.args.section
        if not section:
            section = conf.config.get('section')

        config = conf.config.get(section)

        misc.execute("bgsq-%s" % cls.name, config=config)


class BaseBug(BaseApp):

    @classmethod
    def add_argument_parser(cls, subparsers):
        parser = super(BaseBug, cls).add_argument_parser(subparsers)
        parser.add_argument('bug')
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
        if bug.startswith(config.get('prefix', '')):
            bug = bug.lstrip(config.get('prefix', ''))

        base_work_dir = os.path.expanduser(config.get('work_dir'))
        assert os.path.exists(base_work_dir), "Work dir %s does not exist" % \
                                              base_work_dir
        work_dir = os.path.join(base_work_dir, "%s%s" %
                                               (config.get('prefix'), bug))

        if not os.path.exists(work_dir):
            os.mkdir(work_dir)
        os.chdir(work_dir)
        cls.call_hooks(config=config, bug=bug)
