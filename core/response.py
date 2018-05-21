from bson.json_util import dumps
from flask import make_response
from flask_mongoengine import BaseQuerySet, Document, DynamicDocument


def make_json_response(obj, code, headers=None):
    """
    Translate MongoDB types to JSON.
    """
    def obj_serialize(o):
        if isinstance(o, Document) or isinstance(o, DynamicDocument):
            return o.to_mongo()
        else:
            return o

    if isinstance(obj, BaseQuerySet) or isinstance(obj, list):
        resp = make_response(dumps([obj_serialize(o) for o in obj]), code)
    elif isinstance(obj, dict):
        resp = make_response(dumps(obj), code)
    else:
        resp = make_response(dumps(obj_serialize(obj)), code)

    resp.headers.extend(headers or {})

    return resp
