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


@json_view
def change_state(*args, **kwargs):
    with open(settings.state_file, 'r+') as f:
        try:
            state = json.loads(f.read())
        except ValueError:
            state = {}



def get_state(state):
    def lol(*args, **kwargs):
        return state.state
    return json_view(lol)





class Api(object):


    endpoints = {
        'ph' : ('get_ph', ('GET',)),
        'temp' : ('get_temp', ('GET',)),
        'level' : ('get_level', ('GET',)),
        'state' : ('change_state', ('POST',)),
    }

    def __init__(self, app, state):
        base = '/api/%s'
        for route, endpoint in self.endpoints.iteritems():
            cb, methods = endpoint
            app.add_url_rule(base % route, view_func = LazyView('api.api.%s' % cb), methods = methods)

        app.add_url_rule(base % 'state', view_func = get_state(state))