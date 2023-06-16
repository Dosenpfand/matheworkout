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

from app.models.general import Achievement, Question
from app.tools.mail import send_mail

db = SQLA()
appbuilder = AppBuilder()
migrate = Migrate()
toolbar = DebugToolbarExtension()


def create_app(config="config"):
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

        # Init achievements
        # TODO: move to config?
        achievements = [
            Achievement(
                name="beginner",
                title="Anfänger(in)???",
                description="Eine Aufgabe richtig beantwortet",
            ),
            Achievement(
                name="intermediate",
                title="Fortgeschritten???",
                description="100 Aufgaben richtig beantwortet",
            ),
            Achievement(
                name="pro",
                title="Profi???",
                description="100 Aufgaben richtig beantwortet",
            ),
            Achievement(
                name="bad-luck",
                title="Pechsträhne",
                description="5 Aufgaben nacheinander falsch beantwortet",
            ),
            Achievement(
                name="board",
                title="Bereit für die Matura",
                description="Alle Aufgaben einer Matura richtig beantwortet",
            ),
            Achievement(
                name="brain",
                title="Mathematik durchgespielt",
                description="Alle Aufgaben richtig beantwortet",
            ),
            Achievement(
                name="first",
                title="Klassenbeste(r)",
                description="Platz 1 in deiner Klasse, gewertet nach richtig beantworteten Fragen",
            ),
            Achievement(
                name="third",
                title="Klassenpodest",
                description="Unter den Top 3 in deiner Klasse, gewertet nach richtig beantworteten Fragen",
            ),
            Achievement(
                name="night-owl",
                title="Nachteule",
                description="10 Aufgaben zu später Stunde beantwortet",
            ),
            Achievement(
                name="nth-root",
                title="Wurzelente",
                description="Eine Aufgabe als erstes richtig beantwortet",
            ),
            Achievement(
                name="infinity-rat",
                title="Matheratte",
                description="Alle Aufgaben einer Matura als erstes richtig beantwortet",
            ),
            Achievement(
                name="see-no-evil",
                title="Selbstüberschätzung",
                description="5 Selbstkontrolle-Aufgaben hintereinander richtig beantwortet",
            ),
            Achievement(
                name="speed",
                title="Marathon",
                description="50 Aufgaben an einem Tag richtig beantwortet",
            ),
            Achievement(
                name="star",
                title="Top 1 %",
                description="Unter den Top 1 Prozent auf matheworkout, gewertet nach richtig beantworteten Aufgaben",
            ),
            Achievement(
                name="math",
                title="Alter Hase",
                description="Übt schon länger als ein Jahr",
            ),
        ]

        for achievement in achievements:
            result = (
                db.session.query(Achievement).filter_by(name=achievement.name).first()
            )
            if not result:
                db.session.add(achievement)
            else:
                # TODO: Update
                pass

        migrate.init_app(app, db)
        appbuilder.init_app(app, db.session)
        toolbar.init_app(app)
        from app.models import general  # noqa
        from app.views import views  # noqa

        app.cli.add_command(send_mail_command)

        appbuilder.post_init()
    return app


@click.command("send-mail")
@with_appcontext
def send_mail_command():
    send_mail()
