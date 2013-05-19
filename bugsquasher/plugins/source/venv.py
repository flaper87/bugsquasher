from bugsquasher.utils import misc


class VenvPlugin(object):

    @classmethod
    def on_take(cls, config, section, **kwargs):
        cmd = ["virtualenv"] + section.get("pyvenv_args", [])
        print misc.execute(*cmd)
