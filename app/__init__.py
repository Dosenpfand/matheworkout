import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from app.models.general import Question

db = SQLA()
appbuilder = AppBuilder()
migrate = Migrate()
toolbar = DebugToolbarExtension()


def create_app(config="config"):
    logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    logging.getLogger().setLevel(logging.WARNING)
    sentry_sdk.init(integrations=[FlaskIntegration()])

    app = Flask(__name__)

    with app.app_context():
        app.config.from_object(config)
        app.config.from_envvar("APPLICATION_SETTINGS", silent=True)
        app.config.from_prefixed_env(loads=str)

        db.init_app(app)

        # TODO: Only necessary until SQLAlcchemy 2 is used.
        result = db.session.execute(
            "SELECT * FROM pg_collation WHERE collname = 'numeric';"
        )
        if not result.first():
            db.session.execute(
                "CREATE COLLATION numeric (provider = icu, locale = 'de_DE@colNumeric=yes');"
            )
        db.session.execute(
            f'ALTER TABLE "{Question.__tablename__}" ALTER COLUMN "{Question.external_id.name}" type VARCHAR COLLATE numeric;'
        )

        migrate.init_app(app, db)
        appbuilder.init_app(app, db.session)
        toolbar.init_app(app)
        from app.models import general  # noqa
        from app.views import views  # noqa

        appbuilder.post_init()
    return app
