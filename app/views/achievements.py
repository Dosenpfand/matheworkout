import datetime
from typing import Optional
from flask import g
from sqlalchemy import Time, cast

from app import db
from app.models.achievements import names
from app.models.general import AssocUserQuestion


def process_achievement() -> Optional[str]:
    users_achievements = [achievement.name for achievement in g.user.achievements]
    correct_question_count = g.user.correct_questions()

    if not names.BEGINNER in users_achievements and correct_question_count >= 1:
        return names.BEGINNER

    if not names.INTERMEDIATE in users_achievements and correct_question_count >= 10:
        return names.INTERMEDIATE

    if not names.PRO in users_achievements and correct_question_count >= 100:
        return names.PRO

    if not names.BAD_LUCK in users_achievements:
        answers = (
            g.user.answered_questions.oder_by(AssocUserQuestion.created_on.desc())
            .limit(5)
            .all()
        )

        if all(not answer.is_answer_correct for answer in answers):
            return names.BAD_LUCK

    # TODO: board, brain

    if not names.THIRD in users_achievements:
        for learning_group in g.user.learning_groups:
            if learning_group.position(g.user) <= 3:
                return names.THIRD

    if not names.FIRST in users_achievements:
        for learning_group in g.user.learning_groups:
            if learning_group.position(g.user) == 1:
                return names.FIRST

    if not names.NIGHT_OWL in users_achievements:
        start_time = datetime.time(22, 0, 0)
        end_time = datetime.time(4, 0, 0)
        now = datetime.datetime.now().time()

        if now > start_time or now < end_time:
            answers_count = g.user.answered_questions.filter(
                (cast(AssocUserQuestion.created_on, Time) > start_time)
                | (cast(AssocUserQuestion.created_on, Time) < end_time)
            ).count()

            if answers_count >= 10:
                return names.NIGHT_OWL

    # TODO: nth-root, infinity-rat, see-no-evil

    if not names.SPEED:
        one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
        answers_count = g.user.answered_questions.filter(
            (AssocUserQuestion.created_on > one_day_ago)
            & (AssocUserQuestion.is_answer_correct == True)
        ).count()

        if answers_count >= 50:
            return names.SPEED

    if not names.MATH:
        one_year_ago = datetime.datetime.now() - datetime.timedelta(days=365)
        if g.user.created_on < one_year_ago:
            return names.MATH
