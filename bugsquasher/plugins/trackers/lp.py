try:
    from launchpadlib.launchpad import Launchpad
except ImportError:
    print "launchpadlib is missing."

from bugsquasher.utils import jsonutils


class LP(object):

    @staticmethod
    def lp(config, section):
        cache = section.get("cache_dir",
                            "~/.bugsquasher/cache")

        return Launchpad.login_anonymously('bugsquasher',
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

        with open('.launchpad.json', 'wab') as f:
            f.write(jsonutils.dumps(summary, ensure_ascii=True, indent=4))
