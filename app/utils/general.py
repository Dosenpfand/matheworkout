import logging
import re

from flask import url_for, g
from markupsafe import Markup
from sqlalchemy import func

from app import db
from app.models.general import Question, Topic, QuestionUserState, Assignment, Category


def link_formatter_question(q_id, filters=None):
    assignment_id = None
    category_id = None
    external_id = db.session.query(Question).filter_by(id=q_id).first().external_id
    if filters:
        assignment_id = filters.get_filter_value('assignments')
        category_id = filters.get_filter_value('category')

    url = url_for(f'IdToForm.id_to_form', q_id=q_id, assignment_id=assignment_id, category_id=category_id)
    return Markup(f'<a class="btn btn-sm btn-primary" href="{url}">{external_id}</a>')


def link_formatter_assignment(assignmend_id):
    name = db.session.query(Assignment).filter_by(id=assignmend_id).first().name
    url = url_for('AssignmentModelStudentView.show', pk=assignmend_id)
    return Markup(f'<a class="btn btn-sm btn-primary" href="{url}">{name}</a>')


def link_formatter_category(category_id):
    name = db.session.query(Category).filter_by(id=category_id).first().name
    url = url_for('CategoryModelStudentView.show', pk=category_id)
    return Markup(f'<a class="btn btn-sm btn-primary" href="{url}">{name}</a>')


def link_formatter_topic(topic_id):
    name = db.session.query(Topic).filter_by(id=topic_id).first().name
    url = url_for('TopicModelStudentView.show', pk=topic_id)
    return Markup(f'<a class="btn btn-sm btn-primary" href="{url}">{name}</a>')


def link_formatter_topic_abbr(topic, filters=None):
    topic_name = topic.name
    # TODO: common function
    regex = r"^[a-zA-z]{1,4}\s*\d{1,4}(\.\d{1,4})?"
    match = re.match(regex, topic_name)

    if match:
        topic_short_name = match.group()
    elif len(topic_name) < 6:
        topic_short_name = topic_name
    else:
        topic_short_name = topic_name[0:6]

    return Markup(f'<abbr title="{topic_name}">{topic_short_name}</abbr>')


# TODO: should be in jinja and imported!
def state_to_emoji_markup(state, filters=None):
    del filters
    if state is QuestionUserState.solved_success:
        emoji = 'bi-emoji-sunglasses'
        label = 'label-success'
        title = 'Richtig gelöst'
    elif state is QuestionUserState.tried_failed:
        emoji = 'bi-emoji-frown'
        label = 'label-danger'
        title = 'Falsch gelöst'
    else:
        emoji = 'bi-emoji-neutral'
        label = 'label-warning'
        title = 'Kein Versuch'
    return Markup(f'<span class="label {label}" title="{title}"><i class="bi {emoji}"></i></span>')


def get_question(question_type, q_id):
    return db.session.query(Question).filter_by(id=q_id, type=question_type).first()


def safe_math_eval(string):
    string = string.replace(",", ".")
    string = string.replace('%', '*0.01')
    allowed_chars = "0123456789+-*(). /"
    if string == '':
        return ''

    for char in string:
        if char not in allowed_chars:
            return ''
    return eval(string)


def commit_safely(db_session):
    try:
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        logging.warning(e, exc_info=True)
