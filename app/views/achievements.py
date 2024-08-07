import datetime
from typing import Optional

from flask import g
from sqlalchemy import Time, cast

from app import db
from app.models.achievements import names
from app.models.general import Achievement, AssocUserQuestion, Question, QuestionType


def check_for_new_achievement() -> Optional[Achievement]:
    achievement_name = check_for_new_achievement_name()
    if achievement_name:
        achievement = (
            db.session.query(Achievement).filter_by(name=achievement_name).one()
        )
        return achievement


def check_for_new_achievement_name() -> Optional[str]:
    users_achievements = [achievement.name for achievement in g.user.achievements]
    correct_question_count = g.user.correct_questions()

    if names.HIBERNATION not in users_achievements:
        answers = (
            g.user.answered_questions.order_by(None)
            .order_by(AssocUserQuestion.created_on.desc())
            .limit(2)
            .all()
        )
        if len(answers) == 2:
            minimum_ago = datetime.datetime.now() - datetime.timedelta(days=90)
            if answers[1].created_on <= minimum_ago:
                return names.HIBERNATION

    if names.BEGINNER not in users_achievements and correct_question_count >= 1:
        return names.BEGINNER

    if names.INTERMEDIATE not in users_achievements and correct_question_count >= 10:
        return names.INTERMEDIATE

    if names.PRO not in users_achievements and correct_question_count >= 100:
        return names.PRO

    if names.STAR not in users_achievements:
        if correct_question_count > 500:
            if g.user.correct_percentage_int() >= 90:
                return names.STAR

    if names.BAD_LUCK not in users_achievements:
        answers = (
            g.user.answered_questions.order_by(None)
            .order_by(AssocUserQuestion.created_on.desc())
            .limit(5)
            .all()
        )

        if (len(answers) == 5) and all(
            not answer.is_answer_correct for answer in answers
        ):
            return names.BAD_LUCK

    if names.BOARD not in users_achievements:
        last_answer = (
            g.user.answered_questions.order_by(None)
            .order_by(AssocUserQuestion.created_on.desc())
            .first()
        )
        category_id = last_answer.question.category_id

        if last_answer.is_answer_correct:
            count_answer_correct = (
                g.user.answered_questions.filter_by(is_answer_correct=True)
                .order_by(None)
                .order_by(AssocUserQuestion.question_id)
                .distinct(AssocUserQuestion.question_id)
                .join(AssocUserQuestion.question)
                .filter(Question.category_id == category_id)
                .count()
            )

            count_questions = db.session.query(Question).filter_by(
                category_id=category_id
            )

            if count_answer_correct == count_questions:
                return names.BOARD

    if names.BRAIN not in users_achievements:
        correct_question_count = (
            g.user.answered_questions.filter_by(is_answer_correct=True)
            .order_by(None)
            .order_by(AssocUserQuestion.question_id)
            .distinct(AssocUserQuestion.question_id)
            .count()
        )
        question_count = db.session.query(Question).count()

        if correct_question_count == question_count:
            return names.BRAIN

    if names.THIRD not in users_achievements:
        for learning_group in g.user.learning_groups:
            if learning_group.position(g.user) <= 3:
                return names.THIRD

    if names.FIRST not in users_achievements:
        for learning_group in g.user.learning_groups:
            if learning_group.position(g.user) == 1:
                return names.FIRST

    if names.NIGHT_OWL not in users_achievements:
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

    if names.INFINITY_RAT not in users_achievements:
        last_answer = (
            g.user.answered_questions.order_by(None)
            .order_by(AssocUserQuestion.created_on.desc())
            .first()
        )

        if last_answer.is_answer_correct:
            count_answered = g.user.answered_questions.filter(
                (AssocUserQuestion.question_id == last_answer.question_id)
                & (AssocUserQuestion.is_answer_correct == True)  # noqa: E712
            ).count()

            if count_answered >= 10:
                return names.INFINITY_RAT

    if names.SEE_NO_EVIL not in users_achievements:
        last_answers = (
            g.user.answered_questions.order_by(None)
            .order_by(AssocUserQuestion.created_on.desc())
            .limit(5)
            .all()
        )

        is_overestimated = all(
            [
                (answer.question.type == QuestionType.self_assessed)
                and (answer.is_answer_correct)
                for answer in last_answers
            ]
        )

        if is_overestimated:
            return names.SEE_NO_EVIL

    if names.NTH_ROOT not in users_achievements:
        last_answer = (
            g.user.answered_questions.order_by(None)
            .order_by(AssocUserQuestion.created_on.desc())
            .first()
        )

        if last_answer.is_answer_correct:
            is_first_correct = (
                db.session.query(AssocUserQuestion)
                .filter(
                    (AssocUserQuestion.is_answer_correct == True)  # noqa: E712
                    & (AssocUserQuestion.question_id == last_answer.question_id)
                )
                .count()
                == 1
            )

            if is_first_correct:
                return names.NTH_ROOT

    if names.SPEED not in users_achievements:
        one_day_ago = datetime.datetime.now() - datetime.timedelta(days=1)
        answers_count = g.user.answered_questions.filter(
            (AssocUserQuestion.created_on > one_day_ago)
            & (AssocUserQuestion.is_answer_correct == True)  # noqa: E712
        ).count()

        if answers_count >= 50:
            return names.SPEED

    if names.MATH not in users_achievements:
        one_year_ago = datetime.datetime.now() - datetime.timedelta(days=365)
        if g.user.created_on < one_year_ago:
            return names.MATH
