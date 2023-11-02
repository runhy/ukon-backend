import os
import warnings
import re
import logging
import sentry_sdk
from collections import defaultdict
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration


def import_env(app, env_file):
    if not os.path.exists(env_file):
        warnings.warn("can't read {0} - it doesn't exist".format(env_file))
    else:
        with open(env_file, "r") as f:
            for line in f:
                try:
                    line = line.lstrip()
                    key, value = line.strip().split('=', 1)
                except ValueError:
                    pass
                else:
                    app.config[key] = re.sub(r"\A[\"']|[\"']\Z", "", value)
                    os.environ[key] = app.config[key]


def database_key_definitions(default):
    definitions = defaultdict(lambda: default)
    definitions.update({})
    return definitions


def strip_sensitive_data(event, hint):
    # modify event here
    return event


def import_sentry(app):
    print(app.config['SENTRY_URL'], app.config['ENV_NAME'])
    sentry_sdk.init(
        dsn="{SENTRY_URL}",
        integrations=[FlaskIntegration()],
        environment=app.config['ENV_NAME'],
        # before_send=strip_sensitive_data
    )
