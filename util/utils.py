import json


def obj2json(obj):
    return json.dumps(obj, default=lambda o: o.__dict__)


def json2obj(json_str, hook=None):
    return json.loads(json_str, object_hook=hook)
