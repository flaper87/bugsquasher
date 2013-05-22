import os

from termcolor import colored
from launchpadlib import launchpad

from bugsquasher.utils import jsonutils


class LP(object):

    local_file = ".launchpad.json"

    @staticmethod
    def lp(config, section):
        cache = section.get("cache_dir",
                            "~/.bugsquasher/cache")

        return launchpad.Launchpad.login_anonymously('bugsquasher',
                                                     'production',
                                                     cache)

    @classmethod
    def on_take(cls, config, section, bug):
        lp = cls.lp(config, section)
        bug = lp.bugs[bug]

        summary = {
            "title": bug.title,
            "description": bug.description
        }

        for msg in bug.messages:
            comment = {
                "author": msg.owner.name,
                "content": msg.content,
                "time": msg.date_created.isoformat(),
            }
            summary.setdefault("comments", []).append(comment)

        with open(cls.local_file, 'wab') as f:
            f.write(jsonutils.dumps(summary, ensure_ascii=True, indent=4))

    @classmethod
    def on_show(cls, config, section, **kwargs):
        if os.path.exists(cls.local_file):
            with open(cls.local_file, "rb") as f:
                summary = jsonutils.loads(f.read())

            print colored("Bug Title: ", 'green') + summary["title"]
            #print "\tStatus: %s" % summary["status"]
            print "\t%s comments" % len(summary["comments"])

            if config.verbose:
                for idx, comment in enumerate(summary["comments"]):
                    print colored("\tComment: %s" % (idx + 1), 'yellow')
                    header = "\tAuthor: %s, Date %s" % \
                             (comment["author"], comment["time"])
                    print colored(header, 'yellow')
                    print "\t%s" % comment["content"].replace("\n", "\n\t")
                    print "\t"

    on_list = on_show
