from bugsquasher.utils import misc


class VenvPlugin(object):

    @classmethod
    def on_take(cls, config, **kwargs):
        cmd = ["virtualenv"] + config.get("pyvenv_args", [])
        print misc.execute(*cmd)
