import importlib

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from . import settings


class Ukon(Flask):
    """A custom Flask app"""

    def __init__(self, *args, **kwargs):
        kwargs.update(
            {
                # "template_folder": settings.FLASK_TEMPLATE_PATH,
                # "static_folder": settings.STATIC_ASSETS_PATH,
                "static_url_path": "/static",
            }
        )
        super(Ukon, self).__init__(__name__, *args, **kwargs)
        # Make sure we get the right referral address even behind proxies like nginx.
        # self.wsgi_app = ProxyFix(self.wsgi_app, x_for=settings.PROXIES_COUNT, x_host=1)
        # Configure Redash using our settings
        self.config.from_object("backend.settings")


def create_app():
    from . import (
        migrate,
        routers
    )
    from .models import db
    from .settings.dynamic_settings import import_env

    app = Ukon()

    import_env(app, settings.ENV_FILE)

    db.init_app(app)
    migrate.init_app(app, db)
    routers.init_app(app)

    @app.errorhandler(404)
    def invalid_route(e):
        app.logger.error(e, {'http_code': 404}, exc_info=True)
        return e

    return app
