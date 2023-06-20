import ast
from collections import defaultdict
import logging
from math import pi, exp, log, log10, sin, cos, tan, asin, acos, atan
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime

import simpleeval
from flask import url_for
from flask_mail import Mail, Message
from markupsafe import Markup

from app import db
from app.models.general import (
    Question,
    Topic,
    QuestionUserState,
    Assignment,
    Category,
    LearningGroup,
)


def link_formatter_question(q_id, filters=None):
    assignment_id = None
    category_id = None
    topic_id = None
    external_id = db.session.query(Question).filter_by(id=q_id).first().external_id
    if filters:
        assignment_filter = filters.get_filter_value("assignments")
        assignment_id = (
            assignment_filter[0]
            if isinstance(assignment_filter, list)
            else assignment_filter
        )
        category_filter = filters.get_filter_value("category")
        category_id = (
            category_filter[0] if isinstance(category_filter, list) else category_filter
        )
        topic_filter = filters.get_filter_value("topic")
        topic_id = topic_filter[0] if isinstance(topic_filter, list) else topic_filter

    url = url_for(
        f"IdToForm.id_to_form",
        q_id=q_id,
        assignment_id=assignment_id,
        category_id=category_id,
        topic_id=topic_id,
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
    if len(name) > 150:
        name = name[:147] + "..."
    url = url_for("TopicModelStudentView.show", pk=topic_id)
    return Markup(
        f'<a class="btn btn-sm btn-primary btn-table" style="min-width: 30%" href="{url}">{name}</a>'
    )


# noinspection PyUnusedLocal
def link_formatter_topic_abbr(topic, filters=None):
    topic_name = topic.name
    topic_short_name = topic.get_short_name()

    return Markup(f'<abbr title="{topic_name}">{topic_short_name}</abbr>')


def link_formatter_learning_group(learning_group_id):
    name = db.session.query(LearningGroup).filter_by(id=learning_group_id).first().name
    url = url_for("LearningGroupModelView.show", pk=learning_group_id)

    return Markup(
        f'<a class="btn btn-sm btn-primary btn-table" style="min-width: 30%" href="{url}">{name}</a>'
    )


def link_formatter_learning_group_admin(learning_group_id):
    name = db.session.query(LearningGroup).filter_by(id=learning_group_id).first().name
    url = url_for("LearningGroupModelAdminView.show", pk=learning_group_id)

    return Markup(
        f'<a class="btn btn-sm btn-primary btn-table" style="min-width: 30%" href="{url}">{name}</a>'
    )


def link_formatter_assignment_admin(assignment_id):
    name = db.session.query(Assignment).filter_by(id=assignment_id).first().name
    url = url_for("AssignmentModelTeacherView.show", pk=assignment_id)
    return Markup(
        f'<a class="btn btn-sm btn-primary btn-table" style="min-width: 30%" href="{url}">{name}</a>'
    )


def date_formatter_de(dtime: "datetime") -> str:
    return dtime.strftime("%d.%m.%Y")


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
    s = simpleeval.SimpleEval(names={"pi": pi, "π": pi, "e": exp(1)})
    s.operators.pop(ast.Pow)
    s.operators[ast.BitXor] = simpleeval.safe_power
    s.functions.update(
        dict(
            ln=log,
            log=log10,
            sin=sin,
            cos=cos,
            tan=tan,
            arcsin=asin,
            arccos=acos,
            arctan=atan,
        )
    )

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


def groupby_unsorted(seq, key=lambda x: x):
    indexes = defaultdict(list)
    for i, elem in enumerate(seq):
        indexes[key(elem)].append(i)
    for k, idxs in indexes.items():
        yield k, (seq[i] for i in idxs)
