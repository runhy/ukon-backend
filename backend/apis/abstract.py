import json, ast
from flask import make_response, jsonify, current_app
from werkzeug.wrappers import Response
from flask_restful import Resource
from backend.views.abstract import ViewMixin
from .exceptions import ApiUserError, UserError


class ActionApi(Resource, ViewMixin):
    def __init__(self, model_class=None, **kwargs):
        self.model_class = model_class

    def raise_error(self, *args, **kwargs):
        raise ApiUserError(*args, **kwargs)

    def raise404(self, msg=u"Interface not found"):
        current_app.logger.error(msg, {'http_code': 404}, exc_info=True)
        self.raise_error(msg)

    def dispatch_action(self, action, server_hostname=None, *args, **kwargs):
        try:
            if not hasattr(self, action):
                self.raise404()
            # try:
            return getattr(self, action)(*args, **kwargs)
            # return self.user_fail(e)

        except UserError as err:
            return self.fail(err.message, err.status_code)
        except NotImplementedError:
            return self.fail(u"Interface is pending...")
        except Exception:
            return self.fail(u"Interface not found", code=10404)

    def get(self, action=None, server_hostname=None, **kwargs):
        return self.dispatch_action(action, **kwargs)

    def post(self, action=None, server_hostname=None, **kwargs):
        return self.dispatch_action(action, **kwargs)

    def done(self, data=None):
        current_app.logger.info('', {'http_code': 200, 'status_code': 200})
        if isinstance(data, Response):
            return data
        return json.loads(json.dumps({"success": True, "data": data}))

    def user_fail(self, e):
        message = e.message
        code = e.status_code
        try:
            current_app.logger.info(e, {'http_code': 200, 'status_code': code})
        finally:
            if hasattr(e, 'user_id'):
                return {"success": False, "message": message, "code": code, 'user_id': e.user_id}
            return {"success": False, "message": message, "code": code}

    def fail(self, e, message="", code=400):
        try:
            if not message:
                message = str(e)
            current_app.logger.error(e, {'http_code': 200, 'status_code': code}, exc_info=True)
            # current_app.logger.error(message, exc_info=True)
        finally:
            # if isinstance(message, Response):
            #     return message
            if hasattr(e, 'user_id'):
                return {"success": False, "message": message, "code": code, 'user_id': e.user_id}
            return {"success": False, "message": message, "code": code}
            # return self.make_error_response(code, message)

    def make_error_response(self, code, message):
        resp = make_response(jsonify(success=False, message=message, code=code))
        resp.status_code = code
        return resp.json

    def pagination_done(self, result):
        data, pagination_dict = result
        r = self.done(data)
        r['paginationMeta'] = pagination_dict
        return r


def list_type(value):
    return ast.literal_eval(value)


def dict_type(value):
    return ast.literal_eval(value)


def pagination(q_base, page=1, size=100):
    pagination_dict = dict()
    if page and size:
        q_base = q_base.paginate(int(page), int(size), error_out=False)
        q_all = q_base.items
        pagination_dict['currentPage'] = q_base.page
        pagination_dict['nextPage'] = q_base.next_num
        pagination_dict['perPage'] = q_base.per_page
        pagination_dict['previousPage'] = q_base.prev_num
        pagination_dict['totalCount'] = q_base.total
        pagination_dict['totalPages'] = q_base.pages
    else:
        q_all = q_base.all()
    return q_all, pagination_dict
