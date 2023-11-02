import simplejson
import binascii
import datetime
import decimal
import uuid
from sqlalchemy.orm.query import Query
from flask_restful.reqparse import RequestParser, Namespace
from flask_restful.reqparse import Argument


# def make_celery():
#     app.config.from_object('settings.common')
#     app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
#     app.config['REDIS_URL'] = REDIS_URL
#     app.config['BROKER_URL'] = BROKER_URL
#     app.config['BACKEND_URL'] = BACKEND_URL
#     import_env(app.config['CELERY_ENV_FILE'])
#     db.init_app(app)
#     celery = Celery(
#         "MZ",
#         backend=app.config['BACKEND_URL'],
#         broker=app.config['BROKER_URL']
#     )
#     celery.conf.update({"ENV_CONFIG": app.config})
#
#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)
#
#     celery.Task = ContextTask
#     return celery
#
#
# def import_env(env_file):
#     if not os.path.exists(env_file):
#         pass
#     else:
#         with open(env_file, "r") as f:
#             for line in f:
#                 try:
#                     line = line.lstrip()
#                     key, value = line.strip().split('=', 1)
#                 except ValueError:
#                     pass
#                 else:
#                     temp = re.sub(r"\A[\"']|[\"']\Z", "", value)
#                     app.config[key] = temp


class JSONEncoder(simplejson.JSONEncoder):
    """Adapter for `simplejson.dumps`."""

    def default(self, o):
        # Some SQLAlchemy collections are lazy.
        if isinstance(o, Query):
            result = list(o)
        elif isinstance(o, decimal.Decimal):
            result = float(o)
        elif isinstance(o, (datetime.timedelta, uuid.UUID)):
            result = str(o)
        # See "Date Time String Format" in the ECMA-262 specification.
        elif isinstance(o, datetime.datetime):
            result = o.strftime("%Y-%m-%d %H:%M:%S")
            # if o.microsecond:
            #     result = result[:23] + result[26:]
            # if result.endswith("+00:00"):
            #     result = result[:-6] + "Z"
        elif isinstance(o, datetime.date):
            result = o.isoformat()
        elif isinstance(o, datetime.time):
            if o.utcoffset() is not None:
                raise ValueError("JSON can't represent timezone-aware times.")
            result = o.isoformat()
            if o.microsecond:
                result = result[:12]
        elif isinstance(o, memoryview):
            result = binascii.hexlify(o).decode()
        elif isinstance(o, bytes):
            result = binascii.hexlify(o).decode()
        else:
            result = super(JSONEncoder, self).default(o)
        return result


def json_dumps(data, *args, **kwargs):
    """A custom JSON dumping function which passes all parameters to the
    simplejson.dumps function."""
    kwargs.setdefault("cls", JSONEncoder)
    kwargs.setdefault("encoding", None)
    # Float value nan or inf in Python should be render to None or null in json.
    # Using ignore_nan = False will make Python render nan as NaN, leading to parse error in front-end
    kwargs.setdefault('ignore_nan', True)
    return simplejson.dumps(data, *args, **kwargs)


class UkonArgument(Argument):
    def source(self, request):
        """Pulls values off the request in the provided location
        :param request: The flask request object to parse arguments from
        """
        import six
        from werkzeug.datastructures import MultiDict

        if isinstance(self.location, six.string_types):
            if self.location in {"json", "get_json"}:
                value = request.get_json(silent=True)
            else:
                value = getattr(request, self.location, MultiDict())
                if callable(value):
                    value = value()
            if value is not None:
                return value
        else:
            values = MultiDict()
            for l in self.location:
                if l in {"json", "get_json"}:
                    value = request.get_json(silent=True)
                else:
                    value = getattr(request, l, None)
                    if callable(value):
                        value = value()
                if value is not None:
                    values.update(value)
            return values

        return MultiDict()


class UkonRequestParser(RequestParser):
    def __init__(self, argument_class=UkonArgument):
        super().__init__(argument_class)
        self.argument_class = argument_class
