from flask import url_for, request, g
from markupsafe import Markup
from sqlalchemy import func

from app import db
from app.models.general import Question, Topic, QuestionUserState


def link_formatter(external_id):
    url = url_for(f'ExtIdToForm.ext_id_to_form', ext_id=external_id)
    return Markup(f'<a href="{url}">{external_id}</a>')


# TODO: should be in jinja and imported!
def state_to_emoji_markup(state):
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


def get_question(type):
    request_id = request.args.get('ext_id')

    if request_id:
        result = db.session.query(Question).filter_by(
            external_id=request_id, type=type).first()
    else:
        active_topic_ids = get_active_topics()
        filter_arg = Question.topic_id.in_(active_topic_ids)
        result = db.session.query(Question).order_by(
            func.random()).filter(filter_arg).filter_by(type=type).first()

    return result


def get_question_count(type):
    active_topic_ids = get_active_topics()
    filter_arg = Question.topic_id.in_(active_topic_ids)
    count = db.session.query(Question).order_by(
        func.random()).filter(filter_arg).filter_by(type=type).count()
    return count


def get_active_topics():
    topic_ids = [topic.id for topic in g.user.active_topics]

    # If no topic IDs set for this user
    if not topic_ids:
        # Set all topic IDs
        results = db.session.query(Topic).all()
        topic_ids = [result.id for result in results]

    return topic_ids


def safe_math_eval(string):
    allowed_chars = "0123456789+-*(). /"
    if string == '':
        return ''

    for char in string:
        if char not in allowed_chars:
            return ''
    return eval(string)
