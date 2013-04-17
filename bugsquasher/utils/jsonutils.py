import json
from functools import partial

try:
    from xmlrpclib import DateTime
except ImportError:
    pass


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, DateTime):
            return str(obj)

        #return super(JSONEncoder, self).default(obj)


dumps = partial(json.dumps, cls=JSONEncoder)
loads = json.loads
