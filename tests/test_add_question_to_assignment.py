import os
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

os.environ.setdefault("FLASK_SECRET_KEY", "test-secret-key")
os.environ.setdefault(
    "FLASK_SQLALCHEMY_DATABASE_URI",
    "postgresql+psycopg://db_user:db_password@localhost:5432/db_database",
)


def test_adding_already_assigned_question_does_not_duplicate():
    """Regression: re-adding an assigned question raised a UniqueViolation."""
    from flask import Flask

    app = Flask(__name__)
    app.config.from_object("config")
    with app.app_context():
        from app.views.forms import AddQuestionToAssignmentFormView

    question = object()
    assignment = SimpleNamespace(assigned_questions=[question], created_by=None)

    view = AddQuestionToAssignmentFormView.__new__(AddQuestionToAssignmentFormView)
    view.assignment_model = MagicMock(get=MagicMock(return_value=assignment))
    view.question_model = MagicMock(get=MagicMock(return_value=question))
    form = SimpleNamespace(
        assignment_id=SimpleNamespace(raw_data=["1468"]),
        question_id=SimpleNamespace(data="1119"),
    )

    with app.test_request_context(), patch(
        "app.views.forms.g", SimpleNamespace(user=object())
    ):
        view.form_post(form)

    assert assignment.assigned_questions == [question]
