import logging
from os import environ

import click
import sentry_sdk
from flask import Flask
from flask.cli import with_appcontext
from flask_appbuilder import AppBuilder, SQLA
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
from sentry_sdk.integrations.flask import FlaskIntegration

from app.models.general import Question
from app.tools.mail import send_mail

db = SQLA()
appbuilder = AppBuilder()
migrate = Migrate()
toolbar = DebugToolbarExtension()


def create_app(config="app.config"):
    logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
    logging.getLogger().setLevel(logging.WARNING)

    traces_sample_rate = environ.get("SENTRY_TRACES_SAMPLE_RATE")
    traces_sample_rate = float(traces_sample_rate) if traces_sample_rate else None
    sentry_sdk.init(
        integrations=[FlaskIntegration()],
        traces_sample_rate=traces_sample_rate,
    )

    app = Flask(__name__)

    with app.app_context():
        app.config.from_object(config)
        app.config.from_envvar("APPLICATION_SETTINGS", silent=True)
        app.config.from_prefixed_env(loads=str)

        db.init_app(app)
        # TODO: check for alternative
        #  https://stackoverflow.com/questions/37908767/table-roles-users-is-already-defined-for-this-metadata-instance
        db.metadata.clear()

        migrate.init_app(app, db)
        appbuilder.init_app(app, db.session)
        toolbar.init_app(app)
        from app.models import general  # noqa
        from app.views import views  # noqa

        app.cli.add_command(send_mail_command)
        app.cli.add_command(init_db_command)

        appbuilder.post_init()
    return app

def init_db() -> None:
    # TODO: Only necessary until SQLAlchemy 2 is used.
    result = db.session.execute(
        "SELECT * FROM pg_collation WHERE collname = 'numeric';"
    )
    if not result.first():
        db.session.execute(
            "CREATE COLLATION numeric (provider = icu, locale = 'de_DE@colNumeric=yes');"
        )
    db.session.execute(
        f'ALTER TABLE "{Question.__tablename__}" '
        f'ALTER COLUMN "{Question.external_id.name}" type VARCHAR COLLATE numeric;'
    )

@click.command("send-mail")
@with_appcontext
def send_mail_command():
    send_mail()

@click.command("init-db")
@with_appcontext
def init_db_command() -> None:
    init_db()
    click.echo("Initialized the database.")