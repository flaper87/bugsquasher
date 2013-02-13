import os
import subprocess


def confirm_before(prompt, func, *args, **kwargs):
    sure = raw_input(prompt)

    if not sure or sure.lower() == "n":
        return

    func(*args, **kwargs)


def config_to_bash(config):
    environ = {}

    for conf, value in config.iteritems():
        if isinstance(value, (list, tuple, set)):
            value = ";".join(value)
        environ["BGSQ_%s" % conf.upper()] = value

    return environ


def execute(*args, **kwargs):
    environ = config_to_bash(kwargs.get("config", {}))
    environ.update(os.environ)
    command = [arg for arg in args if arg is not None]
    return subprocess.check_output(command,
                    env=environ,
                    stderr=subprocess.STDOUT,
                    shell=False, **kwargs)
