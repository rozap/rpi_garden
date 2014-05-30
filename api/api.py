import settings
import json
from util import json_view, LazyView, paginate
from flask import request

@json_view
@paginate
def get_ph(*args, **kwargs):
    with open(settings.ph_file, 'r') as f:
        parsed = json.loads(f.read())
        return parsed
    return 500, 'you broke it'

@json_view
@paginate
def get_temp(*args, **kwargs):
    with open(settings.temp_file, 'r') as f:
        parsed = json.loads(f.read())
        return parsed
    return 500, 'you broke it'

@json_view
@paginate
def get_level(*args, **kwargs):
    with open(settings.level_file, 'r') as f:
        parsed = json.loads(f.read())
        return parsed
    return 500, 'you broke it'



class Api(object):


    endpoints = {
        'ph' : 'get_ph',
        'temp' : 'get_temp',
        'level' : 'get_level'
    }

    def __init__(self, app):
        base = '/api/%s'
        for route, cb in self.endpoints.iteritems():
            app.add_url_rule(base % route, view_func = LazyView('api.api.%s' % cb), methods = ('GET',))