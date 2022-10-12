import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_migrate import Migrate

db = SQLA()
appbuilder = AppBuilder()
migrate = Migrate()


def create_app(config="config"):
    logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    logging.getLogger().setLevel(logging.WARNING)

    app = Flask(__name__)

    with app.app_context():
        app.config.from_object(config)
        app.config.from_envvar("APPLICATION_SETTINGS", silent=True)
        app.config.from_prefixed_env(loads=str)
        db.init_app(app)
        migrate.init_app(app, db)
        appbuilder.init_app(app, db.session)
        from app.models import general  # noqa
        from app.views import views  # noqa

        appbuilder.post_init()
    return app
