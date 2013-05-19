from oslo.config import cfg
from bugsquasher import commands


class Cmd(commands.BaseApp):
    name = 'search'

    @classmethod
    def register_opts(cls, config):
        super(Cmd, cls).register_opts(config)
        config.register_cli_opt(cfg.MultiStrOpt('query', short='q'))

    @classmethod
    def execute(cls, config, section):
        query = {}
        if config.query:
            for param in config.query:
                k, v = param.split("=")
                query[k] = v
        import pdb; pdb.set_trace() ### XXX BREAKPOINT
        cls.call_hooks(config=config, section=section, query=query)
