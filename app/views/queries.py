from flask import g

from app.app_factory import db
from app.models.general import Assignment


def assignment_query():
    return db.session.query(Assignment).filter_by(created_by=g.user)
