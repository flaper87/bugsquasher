
import os
from termcolor import colored
from bugsquasher.cfg import conf
from bugzilla import RHBugzilla, Bugzilla
from bugsquasher.utils.jsonutils import loads, dumps


class BugzillaBackend(object):

    def __init__(self, _id, config):
        self._bug = None
        self.config = config

        self.id = _id
        self.url = config.get('bz_url')

        if "bugzilla.redhat.com" in self.url:
            self.bugzilla = RHBugzilla(url=self.url)
        else:
            self.bugzilla = Bugzilla(url=self.url)

    def ensure_login(func):
        def wrapper(self):
            user = self.config.get('user')
            password = self.config.get('password')
            if (user and password) and not self.bugzilla.logged_in:
                self.bugzilla.login(user, password)
            return func(self)
        return wrapper

    @property
    @ensure_login
    def bug(self):
        if not self._bug:
            self._bug = self.bugzilla.getbug(self.id)
        return self._bug

    @classmethod
    def on_take(cls, config, **kwargs):
        bugz = cls(kwargs.get("bug"), config)
        bug = bugz.bug.__dict__

        if bug:
            with open('.bugzilla.json', 'wab') as f:
                f.write(dumps(bug, ensure_ascii=True, indent=4))

    @classmethod
    def on_update(cls, config, **kwargs):
        def update_bug(bug):
            bugz = cls(bug, config)
            bug = bugz.bug.__dict__

            if bug:
                with open('.bugzilla.json', 'wab') as f:
                    f.write(dumps(bug, ensure_ascii=True, indent=4))

        if kwargs.get("bug"):
            return update_bug(kwargs.get("bug"))

        for sub in os.listdir("./"):
            bugdir = os.path.join("./", sub)

            if not os.path.exists(os.path.join(bugdir, '.bugzilla.json')):
                continue

            update_bug(sub.lstrip(config.get("prefix", "")))

    @classmethod
    def on_show(cls, config, **kwargs):
        if os.path.exists(".bugzilla.json"):
            with open(".bugzilla.json", "rb") as f:
                summary = loads(f.read())

            print colored("Bug Title: ", 'green') + summary["summary"]
            print "\tStatus: %s" % summary["status"]
            print "\t%s comments" % len(summary["comments"])

            # Check if conf.args has attr so we can reuse it for listing
            if hasattr(conf.args, "verbose") and conf.args.verbose:
                for idx, comment in enumerate(summary["comments"]):
                    print colored("\tComment: %s" % (idx + 1), 'yellow')
                    header = "\tAuthor: %s, Private: %s, Date %s" % (comment["author"],
                                                                  comment["is_private"],
                                                                  comment["time"])
                    print colored(header, 'yellow')
                    print "\t%s" % comment["text"].replace("\n", "\n\t")
                    print "\t"

    on_list = on_show
