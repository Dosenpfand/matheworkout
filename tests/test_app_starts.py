import os

import pytest

os.environ.setdefault("FLASK_SECRET_KEY", "test-secret-key")
os.environ.setdefault(
    "FLASK_SQLALCHEMY_DATABASE_URI",
    "postgresql+psycopg://db_user:db_password@localhost:5432/db_database",
)


@pytest.fixture(scope="module")
def client():
    from app import create_app

    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_app_starts_and_serves_login_page(client):
    response = client.get("/login/")
    assert response.status_code == 200
