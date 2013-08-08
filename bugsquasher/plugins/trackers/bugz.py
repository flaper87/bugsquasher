import os
import prettytable
from termcolor import colored
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
        def wrapper(self, *args, **kwargs):
            user = self.config.get('bz_user')
            password = self.config.get('bz_password')
            if (user and password) and not self.bugzilla.logged_in:
                self.bugzilla.login(user, password)
            return func(self, *args, **kwargs)
        return wrapper

    @property
    @ensure_login
    def bug(self):
        if not self._bug:
            self._bug = self.bugzilla.getbug(self.id)
        return self._bug

    @ensure_login
    def search(self, query):
        q = self.config.get("bz_query", {}).copy()
        q.update(query)

        for k, v in q.items():
            if isinstance(v, basestring) and "," in v:
                q[k] = v.split(",")
        return self.bugzilla.query(q)

    @classmethod
    def on_search(cls, config, section, query, **kwargs):
        bugz = cls(None, section)
        results = bugz.search(query)

        headers = [
            'ID',
            'Component',
            'Status',
            'Summary',
            'Assignee']
        table = prettytable.PrettyTable(headers, header=False, border=False)

        for rst in results:
            bug = rst.__dict__
            table.add_row([
                        bug["id"],
                        colored(bug["component"], "green"),
                        colored(bug["status"], "red"),
                        bug["summary"],
                        bug["assigned_to"],
                    ])

        print table.get_string()

    @classmethod
    def on_take(cls, config, section, **kwargs):
        bugz = cls(kwargs.get("bug"), section)
        bug = bugz.bug.__dict__

        if bug:
            with open('.bugzilla.json', 'wab') as f:
                f.write(dumps(bug, ensure_ascii=True, indent=4))

    @classmethod
    def on_update(cls, config, section, **kwargs):
        def update_bug(bug):
            bugz = cls(bug, section)
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
    def on_show(cls, config, section, **kwargs):
        if os.path.exists(".bugzilla.json"):
            with open(".bugzilla.json", "rb") as f:
                summary = loads(f.read())

            print colored("Bug Title: ", 'green') + summary["summary"]
            print "\tStatus: %s" % summary["status"]
            print "\t%s comments" % len(summary["comments"])

            if config.verbose:
                for idx, comment in enumerate(summary["comments"]):
                    print colored("\tComment: %s" % (idx + 1), 'yellow')
                    header = "\tAuthor: %s, Private: %s, Date %s" % \
                             (comment["author"], comment["is_private"],
                              comment["time"])
                    print colored(header, 'yellow')
                    print "\t%s" % comment["text"].replace("\n", "\n\t")
                    print "\t"

    on_list = on_show
