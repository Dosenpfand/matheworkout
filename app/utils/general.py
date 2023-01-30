import ast
import logging
from math import pi

from flask import url_for
from flask_mail import Mail, Message
from markupsafe import Markup
import simpleeval

from app import db
from app.models.general import Question, Topic, QuestionUserState, Assignment, Category


def link_formatter_question(q_id, filters=None):
    assignment_id = None
    category_id = None
    external_id = db.session.query(Question).filter_by(id=q_id).first().external_id
    if filters:
        assignment_id = filters.get_filter_value("assignments")
        category_id = filters.get_filter_value("category")

    url = url_for(
        f"IdToForm.id_to_form",
        q_id=q_id,
        assignment_id=assignment_id,
        category_id=category_id,
    )
    return Markup(
        f'<a class="btn btn-sm btn-primary btn-table" style="min-width: 30%" href="{url}">{external_id}</a>'
    )


def link_formatter_assignment(assignment_id):
    name = db.session.query(Assignment).filter_by(id=assignment_id).first().name
    url = url_for("AssignmentModelStudentView.show", pk=assignment_id)
    return Markup(
        f'<a class="btn btn-sm btn-primary btn-table" href="{url}">{name}</a>'
    )


def link_formatter_category(category_id):
    name = db.session.query(Category).filter_by(id=category_id).first().name
    url = url_for("CategoryModelStudentView.show", pk=category_id)
    return Markup(
        f'<a class="btn btn-sm btn-primary btn-table" style="min-width: 15em" href="{url}">{name}</a>'
    )


def link_formatter_topic(topic_id):
    name = db.session.query(Topic).filter_by(id=topic_id).first().name
    url = url_for("TopicModelStudentView.show", pk=topic_id)
    return Markup(
        f'<a class="btn btn-sm btn-primary btn-table" style="min-width: 30%" href="{url}">{name}</a>'
    )


# noinspection PyUnusedLocal
def link_formatter_topic_abbr(topic, filters=None):
    topic_name = topic.name
    topic_short_name = topic.get_short_name()

    return Markup(f'<abbr title="{topic_name}">{topic_short_name}</abbr>')


# TODO: should be in jinja and imported!
# noinspection PyUnusedLocal
def state_to_emoji_markup(state, filters=None):
    del filters
    if state is QuestionUserState.solved_success:
        emoji = "bi-emoji-sunglasses"
        label = "label-success"
        title = "Richtig gelöst"
    elif state is QuestionUserState.tried_failed:
        emoji = "bi-emoji-frown"
        label = "label-danger"
        title = "Falsch gelöst"
    else:
        emoji = "bi-emoji-neutral"
        label = "label-warning"
        title = "Kein Versuch"
    return Markup(
        f'<span class="label {label}" title="{title}"><i class="bi {emoji}"></i></span>'
    )


def safe_math_eval(string):
    s = simpleeval.SimpleEval(names={"pi": pi, "π": pi})
    s.operators.pop(ast.Pow)
    string = string.replace(",", ".")
    string = string.replace("%", "*0.01")
    string = string.replace(" ", "")
    string = string.lower()
    if string == "":
        return ""

    try:
        evald = s.eval(string)
    except:
        evald = ""
    return evald


def commit_safely(db_session):
    try:
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        logging.warning(e, exc_info=True)


def send_email(app, subject, html, recipient):
    mail = Mail(app)
    msg = Message()
    msg.subject = subject
    msg.html = html
    msg.recipients = [recipient]
    try:
        mail.send(msg)
    except Exception as e:
        log_instance = logging.getLogger(__name__)
        log_instance.error("Send email exception: {0}".format(str(e)))
        return False
    return True
