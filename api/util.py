import json
from flask import Response
from decimal import Decimal
from werkzeug import import_string, cached_property
from flask import request

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def json_view(fn):
    def wrapped(*args, **kwargs):
        res = fn(*args, **kwargs)
        if type(res) == list or len(res) == 1:
            result = res
            status = 200
        else:
            result, status = res

        js = json.dumps(result, cls = Encoder)
        resp = Response(js, mimetype="application/json")
        resp.status_code = status
        return resp
    return wrapped



def paginate(fn):
    def wrapped(*args, **kwargs):
        res = fn(*args, **kwargs)
        try:
            count = int(request.args.get('count', 60))
            offset = int(request.args.get('offset', 0))
        except ValueError:
            count = 60
            offset = 0
        return res[offset:(offset+count)]
    return wrapped



class LazyView(object):

    def __init__(self, import_name):
        self.__module__, self.__name__ = import_name.rsplit('.', 1)
        self.import_name = import_name

    @cached_property
    def view(self):
        return import_string(self.import_name)

    def __call__(self, *args, **kwargs):
        return self.view(*args, **kwargs)