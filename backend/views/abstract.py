from functools import wraps
from werkzeug.exceptions import BadRequest
from flask import jsonify, current_app, has_request_context, request
import logging
from backend.utils import UkonRequestParser
from backend.utils.common import ERROR


class ViewMixin(object):
    def get_request(self):
        return request

    def raise_error(self, *args, **kwargs):
        raise NotImplementedError

    def is_get(self):
        return request.method == 'GET'

    def is_post(self):
        return request.method == 'POST'


def parse_arguments(*parse_args):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            parser = UkonRequestParser()
            try:
                arguments = dict()
                for argument in parse_args:
                    parser.add_argument(argument)
                if isinstance(request.get_json(silent=True), dict):
                    arguments.update(request.get_json(silent=True))
                if isinstance(request.args, dict):
                    arguments.update(request.args)
                if isinstance(request.form, dict):
                    arguments.update(request.form)
                arguments.update(parser.parse_args())
                return f(arguments=arguments, *args, **kwargs)
            except BadRequest as e:
                current_app.logger.error(str(e.description), {'http_code': 200, 'status_code': 10400}, exc_info=True)
                return jsonify({"success": False, "message": u"arguments error", "data": e.description, "code": 10400})
        return decorated_function

    return decorator


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.base_url = request.base_url
            record.host_url = request.host_url
            record.method = request.method
            try:
                try:
                    if isinstance(request.json, dict):
                        record.request_json = request.json
                    elif isinstance(request.args, dict):
                        record.request_json = request.args.to_dict()
                    else:
                        record.request_json = {}
                except Exception as e:
                    record.request_json = {}
                record.user_agent = request.user_agent
                record.version = request.headers.get('Version')
                record.system_version = request.headers.get('System-Version')
                record.device_name = request.headers.get('Device-Name')
                record.login_from = request.headers.get('login-from')
                record.user_id = request.headers.get('user-id')
                record.http_code = record.args.get('http_code')
                record.status_code = record.args.get('status_code')
                record.blueprint = request.blueprint
            except Exception as e:
                record.status_code = ERROR.PRINT_LOG_ERROR['status_code']
                record.message = ERROR.PRINT_LOG_ERROR['message']
        else:
            record.url = None
            record.remote_addr = None
        return super().format(record)

