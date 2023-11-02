from flask.cli import AppGroup
from flask import current_app
from backend.models.base import db, Version

manager = AppGroup(help="Initialize data.")


@manager.command()
def data():
    """"""
    print("init data...")


def init_common_func(model_name, ver, func):
    print("init {0}...".format(model_name.__tablename__))
    if not db.session.query(model_name).first():
        func()
        db.session.add(Version(classifies=model_name.__tablename__, ver=ver))
    else:
        q = (
            db.session.query(Version)
            .filter(Version.classifies == model_name.__tablename__)
            .first()
        )
        if not q:
            # db.session.query(model_name).delete()
            func()
            db.session.add(Version(classifies=model_name.__tablename__, ver=ver))
        else:
            if ver != q.ver:
                # db.session.query(model_name).delete()
                func()
                q.ver = ver
            else:
                print("Don't need init.")
    print("success {0} done.".format(model_name.__tablename__))
    db.session.commit()
