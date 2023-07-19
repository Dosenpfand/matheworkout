import pytest
from dotenv import load_dotenv

from app import create_app, db

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Flask
    from flask.testing import FlaskClient


@pytest.fixture
def app() -> "Flask":
    # TODO: should be done?
    # db.drop_all()

    load_dotenv("testing.env")
    app = create_app()
    app.test_request_context().push()

    # Assure that we never delete the db in production
    assert app.config["TESTING"]
    assert not app.config["DEBUG"]

    # TODO: db.create_all()
    # engine = app.appbuilder.get_session.get_bind(mapper=None, clause=None)
    # from flask_appbuilder.models.sqla import Model

    # Model.metadata.create_all(engine)

    # Add admin
    admin_is_added = app.appbuilder.sm.add_user(
        "admin@matheworkout.at",
        "admin",
        "admin",
        "admin@matheworkout.at",
        app.appbuilder.sm.find_role(app.appbuilder.sm.auth_role_admin),
        "ahs",
        "password",
    )
    assert admin_is_added

    yield app

    db.session.remove()
    db.drop_all()


@pytest.fixture()
def client(app) -> "FlaskClient":
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_trivial_request_index(client: "FlaskClient"):
    response = client.get("/")
    assert b"matheworkout" in response.data


def test_trivial_request_achievements(client: "FlaskClient"):
    response = client.get("/achievements")
    assert b"Errungenschaften" in response.data


USER_FIRST_NAME = "test_first_name"
USER_LAST_NAME = "test_last_name"
USER_EMAIL = "test_user@matheworkout.at"
USER_PASSWORD = "test_password"
USER_ROLE = "Student"
USER_SCHOOL_TYPE = "ahs"


def test_register_user(client: "FlaskClient"):
    response = client.post(
        "/register/form",
        data=dict(
            first_name=USER_FIRST_NAME,
            last_name=USER_LAST_NAME,
            email=USER_EMAIL,
            password=USER_PASSWORD,
            conf_password=USER_PASSWORD,
            role=USER_ROLE,
            school_type=USER_SCHOOL_TYPE,
            submit=True,
        ),
        follow_redirects=True,
    )
    print(response.text)
    assert response.status_code == 200
    assert response.request.path == "/"
    assert (
        "Um den vollen Funktionsumfang zu nutzen, bestätige deine E-Mail-Adresse"
        in response.text
    )
