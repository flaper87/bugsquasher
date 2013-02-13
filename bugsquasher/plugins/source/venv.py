from bugsquasher.utils import misc


class VenvPlugin(object):

    def ensure_login(func):
        def wrapper(self):
            user = self.config.get('user')
            password = self.config.get('password')
            if (user and password) and not self.bugzilla.logged_in:
                self.bugzilla.login(user, password)
            return func(self)
        return wrapper

    @classmethod
    def on_take(cls, config, **kwargs):
        cmd = ["virtualenv"] + config.get("pyvenv_args", [])
        print misc.execute(*cmd)
